from enum import Enum


# Normal text
# **Bold text**
# _Italic text_
# `Code text`
# Links, in this format: [anchor text](url)
# Images, in this format: ![alt text](url)
class TextType(Enum):
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "links"
    IMAGE = "image"
    TEXT = "text"


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
