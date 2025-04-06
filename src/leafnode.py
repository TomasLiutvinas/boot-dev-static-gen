from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props: dict = {}):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError()

        match self.tag:
            case None:
                return self.value
            case _:
                return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
