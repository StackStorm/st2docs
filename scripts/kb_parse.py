#!/usr/bin/env python2
"""Parse stackstorm docs for KB articles. Output articles to YAML file.
"""
import os
import json
import re

ST2DOCS_PATH = "../docs/source"
KB_DATA_PATH = "./kbdata.yml"


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
        contents = get_contents(doc_file)
        kb_articles = parse(contents)
        if len(kb_articles) > 0:
            kb_data += kb_articles

    return kb_data


def get_contents(path):
    """Open file and get its contents. Return contents.
    """
    with open(path, "r") as doc_file:
        return doc_file.read()


def parse(contents):
    """Parse input text and pull out KB data. Push parsed data into dict and
    return that dict.
    """
    parsed_articles = []
    kb_articles = re.findall(
        r"\.\.\sbegin-kb\n(?:.*\n)*\.\.\send-kb",
        contents
    )
    for article in kb_articles:
        parsed_article = {}

        article_split = article.split("\n")

        parsed_article['metadata'] = get_metadata(article_split[1])
        parsed_article['tile'] = get_title(article)
        parsed_article['body'] = get_body(article)

        parsed_articles.append(parsed_article)

    return parsed_articles


def get_metadata(metadata_line):
    """Extract metadata from KB Article metadata line.
    """
    return json.loads(metadata_line[3:])


def get_title(article):
    """Extract title from article.
    """
    clean_body = re.findall(
        r"\.\.\sbegin-kb\n.*\n+((?:.*\n)*)\n+\.\.\send-kb",
        article
    )[0]
    title = re.findall(
        r"(.*)\n\^+\n",
        clean_body
    )[0]
    return title


def get_body(article):
    """Extract body from article.
    """
    clean_body = re.findall(
        r"\.\.\sbegin-kb\n.*\n+((?:.*\n)*)\n+\.\.\send-kb",
        article
    )[0]
    title = re.search(
        r"(.*)\n\^+\n",
        clean_body
    )
    body = clean_body[title.end():]
    return body


def write_data(kb_data):
    """Take dict and write it to disk.
    """
    with open(KB_DATA_PATH, "w+") as kb_data_file:
        kb_data_file.write(json.dumps(kb_data))


def main():
    """Main entry point
    """
    files = get_files()
    kb_data = get_kb_data(files)

    # Printing articles for testing.
    print kb_data
    # write_data(kb_data)

if __name__ == "__main__":
    main()
