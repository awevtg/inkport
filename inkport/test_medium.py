"""
InkPort - Test script: trying to get past Medium's 403 block.

This is a throwaway test file, separate from extract.py, so we can
experiment without touching the main script.
"""

import requests

URL = "https://medium.com/@se_emdtobego_od/every-book-has-a-time-in-your-life-22182fcc3d4d?sharedUserId=se_emdtobego_od"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;q=0.9,"
        "image/webp,*/*;q=0.8"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

print(f"Trying: {URL}")
response = requests.get(URL, headers=headers)

print(f"\nStatus code: {response.status_code}")

if response.status_code == 200:
    print("Success! Got the page.")
    print(f"Page length: {len(response.text)} characters")
else:
    print(f"Still blocked. Status: {response.status_code}")
