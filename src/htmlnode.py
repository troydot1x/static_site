class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is None:
            return ""
        return "".join([f' {key}="{value}"' for key, value in self.props.items()])
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, attributes=None):
        super().__init__(tag, value, None, attributes)
        self.attributes = attributes
    
    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return self.value
        
        attr_str = ""
        if self.attributes:
            for key, value in self.attributes.items():
                attr_str += f' {key}="{value}"'

        return f"<{self.tag}{attr_str}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("invalid HTML: no tag")
        if self.children is None:
            raise ValueError("invalid HTML: no children")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
    