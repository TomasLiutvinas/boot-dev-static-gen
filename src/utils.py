from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode, TextType, BlockType
from functools import reduce
import re


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": ""})


def split_nodes_image(old_nodes):
    res = list()
    for node in old_nodes:
        matches = extract_markdown_images(node.text)
        if len(matches) == 0:
            if node.text == "":
                continue
            res.append(node)
            continue

        match = matches[0]
        delimiter = f"![{match[0]}]({match[1]})"
        parts = node.text.split(delimiter)
        if len(parts) > 1:
            before = TextNode(parts[0], node.text_type)
            item = TextNode(match[0], TextType.IMAGE, match[1])
            after = TextNode(parts[1], node.text_type)
            res = res + split_nodes_image([before]) + [item] + split_nodes_image([after])
    return res


def split_nodes_link(old_nodes):
    res = list()
    for node in old_nodes:
        matches = extract_markdown_links(node.text)
        if len(matches) == 0:
            if node.text == "":
                continue
            res.append(node)
            continue

        match = matches[0]
        delimiter = f"[{match[0]}]({match[1]})"
        parts = node.text.split(delimiter)
        if len(parts) > 1:
            before = TextNode(parts[0], node.text_type)
            item = TextNode(match[0], TextType.LINK, match[1])
            after = TextNode(parts[1], node.text_type)
            res = res + split_nodes_link([before]) + [item] + split_nodes_link([after])
    return res


def split_nodes_delimiter(old_nodes, delimiter):
    def get_type(delimiter):
        match delimiter:
            case '`':
                return TextType.CODE
            case '_':
                return TextType.ITALIC
            case '**':
                return TextType.BOLD
            case _:
                return TextType.TEXT

    res = list()
    if type(old_nodes) == str:
        old_nodes = [TextNode(old_nodes, TextType.TEXT)]

    for node in old_nodes:
        parts = node.text.split(delimiter)
        if len(parts) > 2:
            before = TextNode(parts[0], node.text_type)
            item = TextNode(parts[1], get_type(delimiter))
            after = list(map(lambda x: TextNode(x.replace('\n', ' '), node.text_type), parts[2:]))
            res += split_nodes_delimiter([before, item] + after, delimiter)
        else:
            if len(parts) > 0 and parts[0] != "":
                res.append(node)

    return res

# this is wrong
# text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
def text_to_textnodes(text):
    delimiters = ['`', '_', '**', '\n']
    updated_nodes = text
    for pisau in delimiters:
        updated_nodes = split_nodes_delimiter(updated_nodes, pisau)
    updated_nodes = split_nodes_image(updated_nodes)
    updated_nodes = split_nodes_link(updated_nodes)
    return updated_nodes


def markdown_to_blocks(markdown):
    res = list(map(lambda x: x.strip(), markdown.split('\n\n')))
    return list(filter(lambda x: x != "", res))


# Headings start with 1-6 # characters, followed by a space and then the heading text.
# Code blocks must start with 3 backticks and end with 3 backticks.
# Every line in a quote block must start with a > character.
# Every line in an unordered list block must start with a - character, followed by a space.
# Every line in an ordered list block must start with a number followed by a . character and a space. The number must start at 1 and increment by 1 for each line.
# If none of the above conditions are met, the block is a normal paragraph.
def block_to_block_type(block_md):
    def get_head():
        parts = block_md.split()
        if parts[0].strip("#") == "":
            return len(parts[0]) < 7
        return False

    def get_code():
        return len(list(filter(lambda x: x == '`', block_md[:3]))) == 3 and len(list(filter(lambda x: x == '`', block_md[-3:]))) == 3

    def get_quote():
        return len(list(filter(lambda x: len(x) > 0 and x[0] != '>', block_md.split('\n')))) == 0

    def get_unordered_l():
        return len(list(filter(lambda x: len(x) > 2 and x[0] != '-' and x[1] != ' ', block_md.split('\n')))) == 0

    def get_ordered_l():
        count = 1
        parts = block_md.split('\n')
        for part in parts:
            if len(part) < 3:
                return False
            if part[0] != str(count) or part[1] != '.' or part[2] != ' ':
                return False
            count = count + 1

        return True

    if len(block_md) < 1:
        return BlockType.PARAGRAPH

    if get_head():
        return BlockType.HEADING
    if get_code():
        return BlockType.CODE
    if get_quote():
        return BlockType.QUOTE
    if get_unordered_l():
        return BlockType.UNORDERED_LIST
    if get_ordered_l():
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def code_block_strip(md):
    md = md.strip('\n')
    md = md[3:-3]
    return md.lstrip('\n')

# md = """
# This is **bolded** paragraph
# text in a p
# tag here
#
# This is another paragraph with _italic_ text and `code` here
#
# """
def md_to_paragraphs(md):
    paragraphs = md.split('\n\n')
    if len(paragraphs) > 1:
        res = []
        for paragraph in paragraphs:
            if len(paragraph) < 1 or not paragraph:
                continue
            res.append(ParentNode("p", list(map(lambda x: text_node_to_html_node(x),text_to_textnodes(paragraph)))))
        return ParentNode("div", res)
    return ParentNode("div", [ParentNode("p", list(map(lambda x: text_node_to_html_node(x),text_to_textnodes(md))))])


def markdown_to_html_node(md):
    match block_to_block_type(md.strip('\n')):
        case BlockType.HEADING:
            return LeafNode("h1",text_to_textnodes(md))
        case BlockType.CODE:
            code_node = LeafNode("code", code_block_strip(md))
            pre_node = ParentNode("pre", [code_node])
            div_node = ParentNode("div", [pre_node])
            return div_node
        case BlockType.QUOTE:
            return ParentNode("quote", text_to_textnodes(md))
        case BlockType.UNORDERED_LIST:
            return ParentNode("ul", text_to_textnodes(md))
        case BlockType.ORDERED_LIST:
            return ParentNode("ol", text_to_textnodes(md))
        case BlockType.PARAGRAPH:
            return md_to_paragraphs(md.strip('\n'))
