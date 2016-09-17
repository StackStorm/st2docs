#!/usr/bin/env python2
"""Parse stackstorm docs for KB articles. Output articles to YAML file.
"""
import re
import os
import yaml
import pypandoc

ST2DOCS_PATH = "./kb"
RST_PATH = "./docs/source/kb.rst"

RST_HEADER = """Knowledge Base
==============

This collection of knowledge base articles can also be found at
https://stackstorm.reamaze.com/


"""


def get_files():
    """Get document files and prepare to parse.
    """
    doc_files = []
    for (dirpath, _, files_in_dir) in os.walk(ST2DOCS_PATH):
        for files in files_in_dir:
            doc_files.append(dirpath + '/' + files)
    return doc_files


def get_kb_data(doc_files):
    """Iterate over files and get KB data from them.
    """
    kb_data = []
    for doc_file in doc_files:
        print "Getting contents for %s" % doc_file
        contents = get_contents(doc_file)
        kb_data.append(contents)

    return kb_data


def get_contents(path):
    """Open file and get its contents. Return contents.
    """
    with open(path, "r") as doc_file:
        return yaml.load(doc_file.read())


def convert_to_rst(article):
    """Take article dict and parse to rst. Append parsed data to kb.rst
    """
    body = re.sub(r'(#+)(\s+)', r'\1####\2', article['body'])
    convert_string = "### %s\n %s" % (article['title'], body)
    print convert_string
    return pypandoc.convert_text(convert_string, 'rst', 'md')


def write_rst(kb_data):
    """Write RST file to disk.
    """
    with open(RST_PATH, "w+") as rst_file:
        rst_file.write(RST_HEADER)

    with open(RST_PATH, "a") as rst_file:
        for article in kb_data:
            print "Writing rst for %s" % article['title']
            rst_contents = convert_to_rst(article)
            rst_file.write(rst_contents+"\n\n")


def install_pandoc():
    """Install pandoc to the local system for use.
    """
    pypandoc.pandoc_download.download_pandoc()


def main():
    """Main entry point
    """
    install_pandoc()
    files = get_files()
    kb_data = get_kb_data(files)
    write_rst(kb_data)


if __name__ == "__main__":
    main()
