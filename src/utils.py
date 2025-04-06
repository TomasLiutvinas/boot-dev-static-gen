from htmlnode import HTMLNode
from leafnode import LeafNode
from textnode import TextNode, TextType

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

def split_nodes_delimiter(old_nodes, delimiter, text_type):
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
            res += split_nodes_delimiter([before,item] + after, delimiter, text_type)
        else:
            if len(parts) > 0 and parts[0] != "":
                res.append(node)
    return res
