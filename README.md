
# InkPort

**Making your writing portable across publishing platforms.**

## The idea

If you use Spotify and switch to YouTube Music, you don't manually rebuild
every playlist song by song — there are tools that transfer your playlists
across platforms automatically.

Writers don't have that luxury. If you publish on Substack and want to also
post on Medium (or move to Ghost, or WordPress), you're stuck copy-pasting,
re-uploading images one by one, and manually fixing formatting every time.

**InkPort is that "playlist transfer" tool, but for articles.**

## How it works

```
Article URL
    ↓
Extract content (title, author, text, headings, images, links)
    ↓
Convert to a common "Article Format" (canonical JSON)
    ↓
Transform for the destination platform
    ↓
Export / Publish
```

Instead of building separate converters for every platform pair
(Substack → Medium, Medium → Ghost, Ghost → WordPress, and so on),
InkPort converts everything into one **platform-independent canonical
article format** first. Every platform only needs to know how to
import from and export to that one format — not to every other platform
directly.

```
Substack ──┐
Medium ────┤
Ghost ─────┤ → Canonical Article → Destination
WordPress ─┘
```

## Current status

🚧 Early prototype stage. So far InkPort can:
- [x] Fetch a webpage and extract title, text, headings, images, and links (`extract.py`)
- [x] Store extracted content as canonical JSON
- [x] Extract full articles + author + tags from a Medium account via its RSS feed (`extract_medium_rss.py`) — see note below
- [x] Convert canonical JSON articles into Markdown files (`convert_to_markdown.py`)
- [ ] Side-by-side preview (Substack ↔ Medium)
- [ ] Direct platform-to-platform transfer

### A note on Medium scraping

Directly scraping a single Medium article page (`extract.py` pointed at a
`medium.com` URL) gets blocked with a `403 Forbidden` error — this held
true even using realistic browser headers, and even using **Playwright**
(a real, invisible Chrome browser that runs JavaScript like a genuine
visitor). This suggests Medium's bot detection goes beyond basic
header/JS checks, likely including headless-browser fingerprinting.

**Workaround found:** Medium provides an RSS feed for every author
(`medium.com/feed/@username`), which is designed for exactly this kind
of programmatic access and isn't blocked. `extract_medium_rss.py` uses
this to pull full article content, author, publish date, and tags —
this is now the working path for getting Medium content into InkPort.

## Tech stack

- **Backend:** Python + FastAPI
- **Extraction:** BeautifulSoup, feedparser (for RSS), Playwright (tested, not currently used)
- **Frontend:** React
- **Canonical format:** JSON
- **Later additions:** PostgreSQL + OAuth (not needed for the prototype)

## About this project

This is a first-year student project, and also my first time using Git
and GitHub. I'm learning Python as I build this, so the code will be
simple and improve over time — commit history reflects that learning
process rather than a finished, polished codebase.

## Why this project

I write on both Medium and Substack myself, so this isn't a hypothetical
problem — it's one I run into as a writer moving my own work between
platforms.
