import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, ParentNode, LeafNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        # Test equality with URL property
        node = TextNode("Click here", TextType.LINK, "https://example.com")
        node2 = TextNode("Click here", TextType.LINK, "https://example.com")
        self.assertEqual(node, node2)

    def test_not_eq_different_text(self):
        # Test inequality with different text content
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is different text", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_type(self):
        # Test inequality with different text types
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_url(self):
        # Test inequality with different URLs
        node = TextNode("Click here", TextType.LINK, "https://example.com")
        node2 = TextNode("Click here", TextType.LINK, "https://different.com")
        self.assertNotEqual(node, node2)

    def test_eq_none_url(self):
        # Test equality when URL is None (default value)
        node = TextNode("Plain text", TextType.TEXT)
        node2 = TextNode("Plain text", TextType.TEXT)
        self.assertEqual(node, node2)

class TestHTMLNode(unittest.TestCase):
        def test_props_to_html_none_props(self):
            # Test when props is None
            node = HTMLNode(props=None)
            self.assertEqual(node.props_to_html(), "")

        def test_props_to_html_empty_props(self):
            # Test when props is an empty dictionary
            node = HTMLNode(props={})
            self.assertEqual(node.props_to_html(), "")

        def test_props_to_html_with_props(self):
            # Test with actual properties
            node = HTMLNode(props={"href": "https://google.com", "target": "_blank"})
            expected = ' href="https://google.com" target="_blank"'
            self.assertEqual(node.props_to_html(), expected)

        def test_repr_empty_node(self):
            # Test string representation of empty node
            node = HTMLNode()
            self.assertEqual(repr(node), "HTMLNode(None, None, None, None)")

        def test_repr_full_node(self):
            # Test string representation of node with all attributes
            node = HTMLNode(
                "div",
                "Hello",
                [HTMLNode("p", "World")],
                {"class": "greeting"}
            )
            expected = 'HTMLNode(div, Hello, [HTMLNode(p, World, None, None)], {\'class\': \'greeting\'})'
            self.assertEqual(repr(node), expected)

        def test_initialization(self):
            # Test that initialization properly sets all attributes
            tag = "div"
            value = "content"
            children = [HTMLNode("p", "child")]
            props = {"class": "test"}

            node = HTMLNode(tag, value, children, props)

            self.assertEqual(node.tag, tag)
            self.assertEqual(node.value, value)
            self.assertEqual(node.children, children)
            self.assertEqual(node.props, props)
        
        def test_leaf_to_html_p(self):
            node = LeafNode("p", "Hello, world!")
            self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

        def test_leaf_to_html_a(self):
            node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
            self.assertEqual(
                node.to_html(),
                '<a href="https://www.google.com">Click me!</a>',
            )

        def test_leaf_to_html_no_tag(self):
            node = LeafNode(None, "Hello, world!")
            self.assertEqual(node.to_html(), "Hello, world!")

        def test_to_html_with_children(self):
            child_node = LeafNode("span", "child")
            parent_node = ParentNode("div", [child_node])
            self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

        def test_to_html_with_grandchildren(self):
            grandchild_node = LeafNode("b", "grandchild")
            child_node = ParentNode("span", [grandchild_node])
            parent_node = ParentNode("div", [child_node])
            self.assertEqual(
                parent_node.to_html(),
                "<div><span><b>grandchild</b></span></div>",
            )

        def test_to_html_many_children(self):
            node = ParentNode(
                "p",
                [
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                    LeafNode("i", "italic text"),
                    LeafNode(None, "Normal text"),
                ],
            )
            self.assertEqual(
                node.to_html(),
                "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
            )

        def test_headings(self):
            node = ParentNode(
            "h2",
                [
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                    LeafNode("i", "italic text"),
                    LeafNode(None, "Normal text"),
                ],
            )
            self.assertEqual(
                node.to_html(),
                "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
            )

class TestTextNodeToHTMLNode(unittest.TestCase):
        def test_text(self):
            node = TextNode("This is a text node", TextType.TEXT)
            html_node = text_node_to_html_node(node)
            self.assertEqual(html_node.tag, None)
            self.assertEqual(html_node.value, "This is a text node")
        
        def test_image(self):
            node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
            html_node = text_node_to_html_node(node)
            self.assertEqual(html_node.tag, "img")
            self.assertEqual(html_node.value, "")
            self.assertEqual(
                html_node.props,
                {"src": "https://www.boot.dev", "alt": "This is an image"},
            )

        def test_bold(self):
            node = TextNode("This is bold", TextType.BOLD)
            html_node = text_node_to_html_node(node)
            self.assertEqual(html_node.tag, "b")
            self.assertEqual(html_node.value, "This is bold")


if __name__ == "__main__":
    unittest.main()