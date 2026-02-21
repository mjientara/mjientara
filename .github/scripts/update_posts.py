"""
Fetches the latest posts from the Substack RSS feed and updates the
BLOG-POST-LIST section in README.md.
"""

import feedparser
import re
from datetime import datetime

SUBSTACK_RSS = "https://mjientara.substack.com/feed"
README_PATH = "README.md"
MAX_POSTS = 5

START_MARKER = "<!-- BLOG-POST-LIST:START -->"
END_MARKER = "<!-- BLOG-POST-LIST:END -->"


def fetch_posts():
    feed = feedparser.parse(SUBSTACK_RSS)
    posts = []
    for entry in feed.entries[:MAX_POSTS]:
        title = entry.get("title", "Untitled")
        link = entry.get("link", "#")
        published = entry.get("published_parsed")
        if published:
            date_str = datetime(*published[:3]).strftime("%b %d, %Y")
        else:
            date_str = ""
        posts.append((title, link, date_str))
    return posts


def build_post_list(posts):
    lines = []
    for title, link, date_str in posts:
        if date_str:
            lines.append(f"- [{title}]({link}) — {date_str}")
        else:
            lines.append(f"- [{title}]({link})")
    return "\n".join(lines)


def update_readme(post_list_md):
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = re.compile(
        re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER),
        re.DOTALL,
    )
    new_block = f"{START_MARKER}\n{post_list_md}\n{END_MARKER}"

    if not pattern.search(content):
        print("Markers not found in README.md — skipping update.")
        return

    updated = pattern.sub(new_block, content)

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(updated)

    print(f"README updated with {len(post_list_md.splitlines())} posts.")


if __name__ == "__main__":
    posts = fetch_posts()
    if not posts:
        print("No posts fetched — skipping update.")
    else:
        post_list_md = build_post_list(posts)
        update_readme(post_list_md)
