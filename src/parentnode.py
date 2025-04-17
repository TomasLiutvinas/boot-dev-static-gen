from functools import reduce
from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props: dict = {}):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag missing")

        if self.children is None or len(self.children) < 1:
            raise ValueError("The cheeeldreen are missing")

        something = reduce(lambda x, y: f"{x}{y.to_html()}", self.children, "")
        return f"<{self.tag}{self.props_to_html()}>{something}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
