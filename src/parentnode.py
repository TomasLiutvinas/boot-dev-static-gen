from functools import reduce
from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props: dict = {}):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Tag missing")

        if self.children == None or len(self.children) < 1:
            raise ValueError("The cheeeldreen are missing")

        return reduce(lambda x,y: f"<{self.tag}{self.props_to_html()}>{x}{y.to_html()}</{self.tag}>",self.children,"")
