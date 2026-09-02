"""
InkPort - Convert canonical JSON articles into Markdown files.

This is the "Convert to HTML/Markdown" step from InkPort's core
workflow: Article URL -> Extract -> Canonical JSON -> Convert -> Export.
"""

import json
import os
import re


def slugify(title):
    """Turn a title into a safe filename, e.g. 'Am i still in august?'
    becomes 'am-i-still-in-august'. It is using python's regular expressions.""" 
    slug = title.lower()
    slug = re.sub(r"[^a-z 0-9\s-]", "", slug)  # remove punctuation
    slug = re.sub(r"\s+", "-", slug.strip())  # spaces become dashes
    return slug


def article_to_markdown(article):
    """Turn one canonical article dictionary into a Markdown string."""
    lines = []

    # Title as a top-level Markdown heading
    lines.append(f"# {article['title']}")
    lines.append("")

    # A small metadata block, common in Markdown for blogs/articles
    author = article.get("author", "unknown")
    published = article.get("published", "unknown")
    lines.append(f"*By {author} — {published}*")
    lines.append("")

    tags = article.get("tags", [])
    if tags:
        tag_line = ", ".join(f"`{tag}`" for tag in tags)
        lines.append(f"**Tags:** {tag_line}")
        lines.append("")

    # The article body. Paragraphs in "text" are separated by \n\n,
    # which is also exactly how Markdown separates paragraphs -
    # so no real conversion is needed here, just pass it through.
    lines.append(article.get("text", ""))

    return "\n".join(lines)


def main():
    with open("medium_articles.json", "r", encoding="utf-8") as f:
        articles = json.load(f)

    # Make a folder to hold all the converted Markdown files.
    output_dir = "markdown_output"
    os.makedirs(output_dir, exist_ok=True) # This creates a folder if it doesn't exist.

    for article in articles:
        markdown = article_to_markdown(article)
        filename = slugify(article["title"]) + ".md"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(markdown)

        print(f"Saved: {filepath}")

    print(f"\nConverted {len(articles)} articles to Markdown in '{output_dir}/'")


if __name__ == "__main__":
    main()