"""
InkPort - Step 1: Extract an article's title and text from a URL.

This is the very first building block of InkPort. It doesn't do anything
fancy yet - just proves we can pull readable content out of a webpage.
"""
# added a json import on the file to use it later for saving the extracted data.

import json 
import requests
from bs4 import BeautifulSoup

# Medium or Substack article links to test it on real content.
URL = "https://en.wikipedia.org/wiki/Ludwig_Wittgenstein"


def fetch_html(url):
    """Download the raw HTML of a page."""
 # medium blocked me when i used a user agent,so i switched to wikipedia for testing.
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # crash loudly if failed
    return response.text


def extract_title(soup):
    """Pull the article title out of the parsed HTML."""
    if soup.title:
        return soup.title.get_text(strip=True)
    return "(no title found)"


def extract_text(soup):
    """Pull the main body text out of the parsed HTML."""
    # This is a rough first pass - real Medium/Substack pages need
    # smarter targeting later, but this proves the concept.
    paragraphs = soup.find_all("p")
    text = "\n\n".join(p.get_text(" ", strip=True) for p in paragraphs)
    return text

def extract_headings(soup):
    headings = soup.find_all(["h1", "h2", "h3", "h4"])
    return [heading.get_text(" ", strip=True) for heading in headings]

def extract_images(soup):
    images =soup.find_all("img") 
    return [img.get("src") for img in images if img.get("src")]

def extract_links(soup):
    links =soup.find_all("a")
    return [a.get("href") for a in links if a.get("href")]


def main():
    print(f"Fetching: {URL}")
    html = fetch_html(URL)

    soup = BeautifulSoup(html, "html.parser")

    title = extract_title(soup)
    text = extract_text(soup)
    headings = extract_headings(soup)
    images = extract_images(soup)
    links =extract_links(soup)


    print("\n--- TITLE ---")
    print(title)

    print("\n--- TEXT ---")
    print(text[:1000])  # just show the first 1000 characters for now
    print("\n...(truncated)" if len(text) > 1000 else "")
    print(headings[:10]) 
    print("\n--- IMAGES ---") 
    print(images[:5]) # just show 5 images for now
    print("\n--- LINKS ---")
    print(links[:10]) #just show 10 links for now


    article = {
        "url": URL,
        "title": title,
        "text": text,
        "headings": headings,
        "images": images,
        "links": links,
    }

    with open ("article.json", "w", encoding ="utf-8") as f:
        json.dump(article, f, ensure_ascii= False)

        print("\nSaved to article.json")


if __name__ == "__main__":
    main()


