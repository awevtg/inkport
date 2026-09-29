from urllib.parse import urlparse

import feedparser
import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from convert_to_markdown import article_to_markdown, article_to_html
from extract import (
    extract_headings,
    extract_images,
    extract_links,
    extract_text,
    extract_title,
    fetch_html,
)
from extract_medium_rss import clean_html_to_text, extract_images_from_html

app = FastAPI(title="InkPort")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ConvertRequest(BaseModel):
    url: str


def extract_generic(url):
    html = fetch_html(url)
    soup = BeautifulSoup(html, "html.parser")
    return {
        "url": url,
        "title": extract_title(soup),
        "text": extract_text(soup),
        "headings": extract_headings(soup),
        "images": extract_images(soup),
        "links": extract_links(soup),
    }


def extract_medium(url):
    parts = [p for p in urlparse(url).path.split("/") if p]
    if not parts or not parts[0].startswith("@"):
        return None

    feed = feedparser.parse(f"https://medium.com/feed/{parts[0]}")
    wanted = url.split("?")[0].rstrip("/")

    for entry in feed.entries:
        if entry.link.split("?")[0].rstrip("/") == wanted:
            raw_html = entry.content[0].value if "content" in entry else ""
            return {
                "title": entry.title,
                "url": entry.link,
                "author": entry.get("author", "unknown"),
                "published": entry.get("published", "unknown"),
                "tags": [tag.term for tag in entry.get("tags", [])],
                "text": clean_html_to_text(raw_html),
                "images": extract_images_from_html(raw_html),
            }
    return None


@app.get("/")
def health():
    return {"status": "InkPort is running"}


@app.post("/convert")
def convert(req: ConvertRequest):
    url = req.url.strip()
    if not url.startswith(("http://", "https://")):
        raise HTTPException(status_code=400, detail="URL must start with http:// or https://")

    try:
        article = None
        if urlparse(url).netloc.endswith("medium.com"):
            article = extract_medium(url)
        if article is None:
            article = extract_generic(url)
    except requests.RequestException as e:
        raise HTTPException(
            status_code=502,
            detail=f"Could not fetch that page ({e}). Medium links only work for recent posts by an @author.",
        )

    return {"article": article, "markdown": article_to_markdown(article), "html": article_to_html(article)}
