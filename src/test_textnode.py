import unittest

from textnode import TextNode, TextType
from utils import split_nodes_delimiter


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
        node = TextNode("Text `asd` xxx", TextType.NORMAL)
        node2 = TextNode("Text `www` www", TextType.BOLD)
        nodes = [node, node2]
        result_nodes = split_nodes_delimiter(nodes, '`',TextType.CODE)
        test_nodes = [
            TextNode("Text ", TextType.NORMAL),
            TextNode("asd", TextType.CODE),
            TextNode(" xxx", TextType.NORMAL),
            TextNode("Text ", TextType.BOLD),
            TextNode("www", TextType.CODE),
            TextNode(" www", TextType.BOLD)
        ]
        self.assertEqual(test_nodes,result_nodes)

    def test_split_bold(self):
        node = TextNode("Text **asd** xxx _ite_", TextType.NORMAL)
        node2 = TextNode("Text `www` www", TextType.BOLD)
        nodes = [node, node2]
        result_nodes = split_nodes_delimiter(nodes, '`',TextType.CODE)
        result_nodes = split_nodes_delimiter(result_nodes, '_',TextType.ITALIC)
        result_nodes = split_nodes_delimiter(result_nodes, '**',TextType.BOLD)
        test_nodes = [
            TextNode("Text ", TextType.NORMAL),
            TextNode("asd", TextType.BOLD),
            TextNode(" xxx ", TextType.NORMAL),
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

if __name__ == "__main__":
    unittest.main()
