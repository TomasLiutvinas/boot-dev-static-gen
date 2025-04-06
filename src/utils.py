from htmlnode import HTMLNode
from leafnode import LeafNode
from textnode import TextNode, TextType
import re
from functools import reduce

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)",text)

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)",text)

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.CODE:
            return HTMLNode("code",text_node.text)
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text,{"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "",{"src":text_node.url, "alt":""})

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
            after = TextNode(parts[1],node.text_type)
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
            after = TextNode(parts[1],node.text_type)
            res = res + split_nodes_link([before]) + [item] + split_nodes_link([after])
    return res



def split_nodes_delimiter(old_nodes, delimiter):
    # print("CALLED WITH NODES:", old_nodes)
    # print("CALLED WITH DELIMITERO:", delimiter)
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
    for node in old_nodes:
        parts = node.text.split(delimiter)
        if len(parts) > 2:
            before = TextNode(parts[0], node.text_type)
            item = TextNode(parts[1], get_type(delimiter))
            after = list(map(lambda x: TextNode(x,node.text_type),parts[2:]))
            res += split_nodes_delimiter([before,item] + after, delimiter)
        else:
            if len(parts) > 0 and parts[0] != "":
                res.append(node)
    return res

def text_to_textnodes(text):
    delimiters = ['`','_','**']
    updated_nodes = list(text)
    for pisau in delimiters:
        updated_nodes = split_nodes_delimiter(updated_nodes,pisau)
    updated_nodes = split_nodes_image(updated_nodes)
    updated_nodes = split_nodes_link(updated_nodes)
    return updated_nodes

def markdown_to_blocks(markdown):
    res = list(map(lambda x: x.strip(),markdown.split('\n\n')))
    return list(filter(lambda x: x != "",res))


