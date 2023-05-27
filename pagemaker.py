import argparse
import json
import os
from datetime import datetime
import markdown
import urllib.parse

def parse_args():
    parser = argparse.ArgumentParser(description="Generate an HTML file from content and metadata files.")
    parser.add_argument("-i", "--content", required=True, help="Path to the content file (plain text or markdown).")
    parser.add_argument("-m", "--metafile", required=True, help="Path to the metadata file (JSON).")
    parser.add_argument("-o", "--output", help="Path to the output HTML file (optional).")
    return parser.parse_args()

def choose_option(options, prompt):
    print(prompt)
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")
    choice = int(input("Enter the number of your choice: "))
    return options[choice - 1]

def main():
    args = parse_args()

    # Read content file
    with open(args.content, "r") as f:
        content_md = f.read()

    # Read metadata file
    with open(args.metafile, "r") as f:
        meta = json.load(f)

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
    with open(output_file, "w") as f:
        f.write(f"<html>\n<head>\n<title>{headline}</title>\n</head>\n<body>")

        # Add headline, summary, and date
        f.write('<div id="content.header">')
        f.write(f"<h1>{headline}</h1>")
        f.write(f"<h3>{summary}</h3>")
        f.write(f"<p>Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>")
        f.write("</div>")

        # Add content
        f.write('<div id="content.content">')
        f.write(content_html)
        f.write("</div>")

        # Add related topics and keywords
        f.write('<div id="content.footer">')
        f.write("<ul>")
        for topic in meta["related_topics"]:
            f.write(f"<li>{topic}</li>")
        f.write("</ul>")
        f.write("<ul>")
        for keyword in meta["keywords"]:
            f.write(f"<li>{keyword}</li>")
        f.write("</ul>")
        f.write("</div>")

        f.write("</body></html>")

    print(f"Generated HTML file: {output_file}")

if __name__ == "__main__":
    main()
