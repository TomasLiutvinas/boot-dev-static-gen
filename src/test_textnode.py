import unittest

from textnode import TextNode, TextType


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

    def test_none(self):
        node = TextNode(None, None, None)
        node2 = TextNode(None, None, None)
        self.assertEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
