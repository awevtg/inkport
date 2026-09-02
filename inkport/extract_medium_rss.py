"""
InkPort - Extract Medium articles via RSS feed.

Unlike extract.py (which scrapes a single article page and gets
blocked by Medium. I used a wikipedia webpage instead for trials.), 
this uses Medium's official RSS feed - a
structured, intended way to get article data programmatically. This passed on the first trial,
I used playwright before to get the content page, but got blocked. Used a user agent to get the page,but still wasn't 
able to do. SO, i switched to this. And pyhton has parsing 
feedparser library to parse the feed. This is a more reliable and legitimate way to get Medium articles.
"""

import json
import feedparser
from bs4 import BeautifulSoup

# RSS feed URL pattern: medium.com/feed/@username
FEED_URL = "https://medium.com/feed/@se_emdtobego_od"


def clean_html_to_text(html):
    """Turn the article's raw HTML content into plain text."""
    soup = BeautifulSoup(html, "html.parser")
    paragraphs = soup.find_all("p")
    text = "\n\n".join(p.get_text(" ", strip=True) for p in paragraphs)
    return text


def main():
    print(f"Fetching feed: {FEED_URL}")
    feed = feedparser.parse(FEED_URL)

    print(f"\nFound {len(feed.entries)} articles.\n")

    articles = []

    for entry in feed.entries:
        # entry.content[0].value holds the full HTML article content.
        # Some entries might not have it, so we check first.
        raw_html = entry.content[0].value if "content" in entry else ""

        article = {
            "title": entry.title,
            "url": entry.link,
            "author": entry.get("author", "unknown"),
            "published": entry.get("published", "unknown"),
            "tags": [tag.term for tag in entry.get("tags", [])],
            "text": clean_html_to_text(raw_html),
        }
        articles.append(article)

        print(f"- {article['title']}")

    # Save ALL articles as one JSON file - a list of article objects.
    with open("medium_articles.json", "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)

    print(f"\nSaved {len(articles)} articles to medium_articles.json")


if __name__ == "__main__":
    main()