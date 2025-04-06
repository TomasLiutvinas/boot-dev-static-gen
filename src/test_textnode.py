import unittest

from textnode import TextNode, TextType
from utils import split_nodes_delimiter, text_node_to_html_node, extract_markdown_images, split_nodes_image, split_nodes_link


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_equal_full(self):
        node = TextNode("Text", TextType.BOLD, "https://theamazingtom.com")
        node2 = TextNode("Text", TextType.BOLD, "https://theamazingtom.com")
        self.assertEqual(node, node2)

    def test_not_equal_italic_full(self):
        node = TextNode("Text", TextType.BOLD, "https://theamazingtom.com")
        node2 = TextNode("Text", TextType.ITALIC, "https://theamazingtom.com")
        self.assertNotEqual(node, node2)
        
    def test_not_equal_site_full(self):
        node = TextNode("Text", TextType.BOLD, "https://theamazingtom.com")
        node2 = TextNode("Text", TextType.BOLD, "https://tomsen.dev")
        self.assertNotEqual(node, node2)

    def test_split_code(self):
        node = TextNode("Text `asd` xxx", TextType.TEXT)
        node2 = TextNode("Text `www` www", TextType.BOLD)
        nodes = [node, node2]
        result_nodes = split_nodes_delimiter(nodes, '`',TextType.CODE)
        test_nodes = [
            TextNode("Text ", TextType.TEXT),
            TextNode("asd", TextType.CODE),
            TextNode(" xxx", TextType.TEXT),
            TextNode("Text ", TextType.BOLD),
            TextNode("www", TextType.CODE),
            TextNode(" www", TextType.BOLD)
        ]
        self.assertEqual(test_nodes,result_nodes)

    def test_split_bold(self):
        node = TextNode("Text **asd** xxx _ite_", TextType.TEXT)
        node2 = TextNode("Text `www` www", TextType.BOLD)
        nodes = [node, node2]
        result_nodes = split_nodes_delimiter(nodes, '`',TextType.CODE)
        result_nodes = split_nodes_delimiter(result_nodes, '_',TextType.ITALIC)
        result_nodes = split_nodes_delimiter(result_nodes, '**',TextType.BOLD)
        test_nodes = [
            TextNode("Text ", TextType.TEXT),
            TextNode("asd", TextType.BOLD),
            TextNode(" xxx ", TextType.TEXT),
            TextNode("ite", TextType.ITALIC),
            TextNode("Text ", TextType.BOLD),
            TextNode("www", TextType.CODE),
            TextNode(" www", TextType.BOLD)
        ]
        self.assertEqual(test_nodes,result_nodes)

    def test_none(self):
        node = TextNode(None, None, None)
        node2 = TextNode(None, None, None)
        self.assertEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [link2](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

if __name__ == "__main__":
    unittest.main()
