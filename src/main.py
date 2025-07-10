from os import path
import os
from textnode import TextNode, TextType
import shutil


def main():
    delete_public()
    copy_thing("static", "public")
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node)


def delete_public():
    shutil.rmtree("public")
    os.mkdir("public")

def copy_thing(source_dir, target_dir):
    stuff = os.listdir(source_dir)
    for item in stuff:
        existing_item_path = f"{source_dir}/{item}"
        target_item_path = f"{target_dir}/{item}"
        if os.path.isdir(existing_item_path):
            if not os.path.exists(target_item_path):
                os.mkdir(target_item_path)
            copy_thing(existing_item_path, target_item_path)
        else:
            shutil.copy(existing_item_path, target_item_path)

main()
