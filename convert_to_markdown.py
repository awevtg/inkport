"""
InkPort - Convert canonical JSON articles into Markdown files.

This is the "Convert to HTML/Markdown" step from InkPort's core
workflow: Article URL -> Extract -> Canonical JSON -> Convert -> Export.
"""

import json
import os
import re
import mistune



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
        # Images, if there are any, using Markdown's image syntax:
    # ![alt text](image-url)
    images = article.get("images", [])
    if images and "![" not in article.get("text", ""):
        lines.append("")
        lines.append("## Images")
        lines.append("")
        for i, image_url in enumerate(images, start=1):
            lines.append(f"![Image {i}]({image_url})")
            lines.append("")

    return "\n".join(lines)

def article_to_html(article):
    markdown_text = article_to_markdown(article)
    body = mistune.html(markdown_text)

    title = article.get("title", "InkPort Article")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <style>
        body {{
            max-width: 800px;
            margin: 40px auto;
            padding: 0 20px;
            font-family: system-ui, sans-serif;
            line-height: 1.7;
            color: #222;
        }}

        img {{
            max-width: 100%;
            height: auto;
        }}

        h1, h2, h3 {{
            line-height: 1.3;
        }}

        code {{
            background: #f3f3f3;
            padding: 2px 5px;
            border-radius: 4px;
        }}
    </style>
</head>
<body>
{body}
</body>
</html>"""

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
    