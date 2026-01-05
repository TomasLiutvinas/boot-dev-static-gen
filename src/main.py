from textnode import TextNode, TextType
from utils import copy_thing, delete_public, generate_page


def main():
    delete_public()
    copy_thing("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node)


main()
