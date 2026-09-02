"""
InkPort - Test script: trying Medium's RSS feed.

RSS is a structured XML format designed to be read by programs -
unlike scraping the regular website, this is a legitimate, intended
way to get article data, so it shouldn't get blocked. Medium provides an RSS
feed to each user, it also this extraction by application like Feedly.

"""


import requests

# RSS feed URL pattern: medium.com/feed/@username
FEED_URL = "https://medium.com/feed/@se_emdtobego_od"

print(f"Fetching feed: {FEED_URL}")
response = requests.get(FEED_URL)

print(f"\nStatus code: {response.status_code}")

if response.status_code == 200:
    print("Success! Got the feed.")
    print(f"Content length: {len(response.text)} characters")
    # Print the first 2000 characters so we can see what it looks like
    print("\n--- FIRST 2000 CHARACTERS ---")
    print(response.text[:2000])
else:
    print(f"Feed request failed. Status: {response.status_code}")