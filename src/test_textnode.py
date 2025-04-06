import unittest

from textnode import BlockType, TextNode, TextType
from utils import block_to_block_type, split_nodes_delimiter, text_node_to_html_node, extract_markdown_images, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks


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
        result_nodes = split_nodes_delimiter(nodes, '`')
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
        result_nodes = split_nodes_delimiter(nodes, '`')
        result_nodes = split_nodes_delimiter(result_nodes, '_')
        result_nodes = split_nodes_delimiter(result_nodes, '**')
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

    def test_full_thing(self):
        node = TextNode(
            "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)",
            TextType.TEXT,
        )
        new_nodes = text_to_textnodes([node])
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )

    def test_markdown_to_blocks(self):
        # well this is fucking stupid
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    # PARAGRAPH = "paragraph"
    # HEADING = "heading"
    # CODE = "code"
    # QUOTE = "quote"
    # UNORDERED_LIST= "unordered_list"
    # ORDERED_LIST= "ordered_list"

    def test_paragraph(self):
        md = "anything really"
        block = block_to_block_type(md)
        self.assertEqual(block,BlockType.PARAGRAPH)

    def test_head(self):
        md = "# Hed1"
        block = block_to_block_type(md)
        self.assertEqual(block,BlockType.HEADING)

    def test_code(self):
        md = "```wowowo```"
        block = block_to_block_type(md)
        self.assertEqual(block,BlockType.CODE)

    def test_quote(self):
        md = "> something"
        block = block_to_block_type(md)
        self.assertEqual(block,BlockType.QUOTE)

    def test_unordered(self):
        md = "- something\n- something also"
        block = block_to_block_type(md)
        self.assertEqual(block,BlockType.UNORDERED_LIST)

    def test_ordered(self):
        md = "1. something\n2. something also"
        block = block_to_block_type(md)
        self.assertEqual(block,BlockType.ORDERED_LIST)

if __name__ == "__main__":
    unittest.main()
