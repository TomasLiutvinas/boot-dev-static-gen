import unittest

from htmlnode import HTMLNode


class TestHtmlNode(unittest.TestCase):

    def test_repr(self):
        node = HTMLNode("a", "https://tomsen.dev", {}, {"href": "https://tomsen.dev"})
        expected = "HTMLNode(a, https://tomsen.dev, {}, {'href': 'https://tomsen.dev'})"
        self.assertEqual(expected, str(node))

    def test_to_html_simple(self):
        node = HTMLNode("a", "https://tomsen.dev", {}, {"href": "https://tomsen.dev"})
        res = node.props_to_html()
        expected = " href='https://tomsen.dev'"
        self.assertEqual(expected, res)

    def test_to_html_double(self):
        node = HTMLNode("a", "https://tomsen.dev", {}, {"href": "https://tomsen.dev", "_target": "blank"})
        res = node.props_to_html()
        expected = " href='https://tomsen.dev' _target='blank'"
        self.assertEqual(expected, res)


if __name__ == "__main__":
    unittest.main()
