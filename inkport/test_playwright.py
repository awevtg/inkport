"""
InkPort - Test script: trying Playwright (a real browser) against Medium.

This uses an actual, invisible Chromium browser instead of a bare HTTP
request, so it can run JavaScript and looks much more like a real visitor.
"""

from playwright.sync_api import sync_playwright

URL = "https://medium.com/@se_emdtobego_od/every-book-has-a-time-in-your-life-22182fcc3d4d?sharedUserId=se_emdtobego_od"


def main():
    with sync_playwright() as p:
        # Launch an invisible ("headless") Chromium browser.
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print(f"Visiting: {URL}")
        response = page.goto(URL)

        print(f"\nStatus code: {response.status}")

        if response.status == 200:
            print("Success! Got the page.")
            # .content() gets the FULL rendered HTML, after JavaScript
            # has run - unlike a bare requests.get(), which only sees
            # the initial empty shell.
            html = page.content()
            print(f"Page length: {len(html)} characters")

            # Try to grab the title.
            title = page.title()
            print(f"Page title: {title}")
        else:
            print(f"Still blocked. Status: {response.status}")

        browser.close()


if __name__ == "__main__":
    main()
