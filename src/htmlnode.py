from functools import reduce

class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props:dict = {}):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def props_to_html(self):
        return reduce(lambda x,y: f"{x} {y[0]}='{y[1]}'",self.props.items(),"")
