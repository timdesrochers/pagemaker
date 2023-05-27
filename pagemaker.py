"""
A script to generate an HTML file from content and metadata files.
"""

import argparse
import json
import urllib.parse
from datetime import datetime
import markdown
from tidylib import tidy_document


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate an HTML file from content and metadata files.")
    parser.add_argument("-i", "--content", required=True,
                        help="Path to the content file (plain text or markdown).")
    parser.add_argument("-m", "--metafile", required=True,
                        help="Path to the metadata file (JSON).")
    parser.add_argument(
        "-o", "--output", help="Path to the output HTML file (optional).")
    return parser.parse_args()


def choose_option(options, prompt):
    """Interactively choose an option from a list."""
    print(prompt)
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")
    choice = int(input("Enter the number of your choice: "))
    return options[choice - 1]


def main():
    """Main function."""
    args = parse_args()

    # Read content file
    with open(args.content, "r", encoding="utf-8") as content_file:
        content_md = content_file.read()

    # Read metadata file
    with open(args.metafile, "r", encoding="utf-8") as meta_file:
        meta = json.load(meta_file)

    # Parse markdown to HTML
    md = markdown.Markdown()
    content_html = md.convert(content_md)

    # Choose headline and summary
    headline = choose_option(meta["headlines"], "Choose a headline:")
    summary = choose_option(meta["summaries"], "Choose a summary:")

    # Set output file name
    if args.output:
        output_file = args.output
        if not output_file.endswith(".html"):
            output_file += ".html"
    else:
        output_file = f"{urllib.parse.quote(headline)}.html"

    # Create the HTML file
    html_content = (
        '<!DOCTYPE html>'
        f'<html lang="en">'
        f'<head>'
        f'<title>{headline}</title>'
        f'<meta charset="utf-8">'
        f'<meta name="viewport" content="width=device-width, initial-scale=1">'
        f'<meta name="description" content="{summary}">'
        f'<link rel="stylesheet" href="style.css">'
        f'</head>'
        f'<body>'
        f'<div id="content.header">'
        f"<h1>{headline}</h1>"
        f"<h3>{summary}</h3>"
        f"<p>Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>"
        "</div>"
        f'<div id="content.content">{content_html}</div>'
        '<div id="content.footer">'
        "<ul>"
        + "".join(f"<li>{topic}</li>" for topic in meta["related_topics"])
        + "</ul>"
        "<ul>"
        + "".join(f"<li>{keyword}</li>" for keyword in meta["keywords"])
        + "</ul>"
        "</div>"
        "</body>"
        "</html>"
    )

    # Tidy the HTML
    tidy_html, _ = tidy_document(
        html_content, options={"indent": 1, "wrap": 80})

    with open(output_file, "w", encoding="utf-8") as output_html_file:
        output_html_file.write(tidy_html)

    print(f"Generated HTML file: {output_file}")


if __name__ == "__main__":
    main()
