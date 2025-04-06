from textnode import TextNode, TextType

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
                return TextType.NORMAL

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
