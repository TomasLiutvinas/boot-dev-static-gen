import os
from textnode import TextNode, TextType
import shutil

from utils import markdown_to_html_node


def main():
    delete_public()
    copy_thing("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    source_file_content = open(from_path, mode="r").read()
    template_file_content = open(template_path, mode="r").read()

    title = extract_title(source_file_content)
    html_nodes = markdown_to_html_node(source_file_content)
    html_content = html_nodes.to_html()
    print("[HTML] ", "\n", html_content)
    generated_content = template_file_content.replace("{{ Title }}",title).replace("{{ Content }}", html_content)

    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(dest_path)
    with open(dest_path, mode="x+") as new_file:
        new_file.write(generated_content)


def extract_title(markdown):
    title = None
    items = markdown.splitlines()
    for item in items:
        if len(item) > 0 and item.startswith("#"):
            title = item.strip("#").strip(" ")

    if title == None:
        raise Exception("No title")

    return title


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
