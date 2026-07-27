#!/usr/bin/env python3
"""
CTI → Ghost Bulk Import Script
Converts existing CTI HTML files into a Ghost-compatible JSON import file.

Usage:
    cd ~/Documents/canadiantradeintel
    python3 ghost_import.py

Output:
    ghost-import.json — upload this to Ghost Admin → Settings → Labs → Import content
"""

import os
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from bs4 import BeautifulSoup

# ── Configuration ──────────────────────────────────────────────────────────────

BASE_DIR = Path.home() / "Documents" / "canadiantradeintel"

# Content folders to import and how to tag them
IMPORT_SOURCES = [
    {
        "folder": "spotlight",
        "type": "post",          # Ghost post (appears in feeds/homepage)
        "status": "published",
        "visibility": "public",
        "tags": ["Spotlight", "News"],
        "description": "Canadian Spotlight articles"
    },
    {
        "folder": "analysis",
        "type": "post",
        "status": "published",
        "visibility": "public",
        "tags": ["Canada Forward", "Analysis"],
        "description": "Canada Forward analysis pieces"
    },
    {
        "folder": "countries",
        "type": "page",          # Ghost page (static, not in feeds)
        "status": "published",
        "visibility": "public",
        "tags": ["Country Dossier"],
        "description": "Country intelligence dossiers"
    },
    {
        "folder": "guides",
        "type": "page",
        "status": "published",
        "visibility": "public",
        "tags": ["Guide", "Resources"],
        "description": "Practical guides"
    },
]

# Author to assign to all imported content
DEFAULT_AUTHOR_EMAIL = "nikko.yetman@hotmail.ca"  # Update to your Ghost admin email

# ── Helpers ────────────────────────────────────────────────────────────────────

def slugify(text: str) -> str:
    """Convert folder name to URL slug."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    return text


def extract_date_from_slug(folder_name: str) -> str:
    """
    Try to extract a publication date from folder name patterns like:
    - canada-forward-structural-outlook-2026
    - algoma-steel-2026-06
    - cae-uk-mod-mar-2026
    Falls back to current date if no date found.
    """
    # Pattern: ends in YYYY or YYYY-MM or YYYY-MM-DD
    match = re.search(r'(\d{4})-(\d{2})-(\d{2})$', folder_name)
    if match:
        return f"{match.group(1)}-{match.group(2)}-{match.group(3)}T12:00:00.000Z"

    match = re.search(r'(\d{4})-(\d{2})$', folder_name)
    if match:
        return f"{match.group(1)}-{match.group(2)}-01T12:00:00.000Z"

    match = re.search(r'(\d{4})$', folder_name)
    if match:
        return f"{match.group(1)}-01-01T12:00:00.000Z"

    # Month abbreviation patterns like -mar-2026 or -april-2026
    months = {
        'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04',
        'april': '04', 'may': '05', 'jun': '06', 'june': '06',
        'jul': '07', 'july': '07', 'aug': '08', 'sep': '09',
        'oct': '10', 'nov': '11', 'dec': '12'
    }
    for month_name, month_num in months.items():
        pattern = rf'-{month_name}-(\d{{4}})$'
        match = re.search(pattern, folder_name)
        if match:
            return f"{match.group(1)}-{month_num}-01T12:00:00.000Z"

    # Default to today
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")


def extract_content(html_path: Path) -> dict:
    """
    Extract title and body content from an HTML file.
    Returns dict with title, html, excerpt.
    """
    try:
        with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
            raw = f.read()
    except Exception as e:
        return None

    soup = BeautifulSoup(raw, 'html.parser')

    # Extract title — try multiple strategies
    title = None

    # 1. Look for <h1> in main content area
    for selector in ['main h1', 'article h1', '.report-title', '.article-title',
                     '.dossier-title', '.spotlight-title', 'h1']:
        el = soup.select_one(selector)
        if el and el.get_text(strip=True):
            title = el.get_text(strip=True)
            break

    # 2. Fall back to <title> tag
    if not title and soup.title:
        title = soup.title.get_text(strip=True)
        # Strip site name from title
        for suffix in [' — Canadian Trade Intelligence', ' | Canadian Trade Intelligence',
                       ' — CTI', ' | CTI']:
            title = title.replace(suffix, '')

    # 3. Fall back to folder name
    if not title:
        title = html_path.parent.name.replace('-', ' ').title()

    # Extract meta description as excerpt
    excerpt = ""
    meta_desc = soup.find('meta', {'name': 'description'})
    if meta_desc and meta_desc.get('content'):
        excerpt = meta_desc['content']

    # Extract main content — remove nav, header, footer, scripts, styles
    for tag in soup.find_all(['nav', 'script', 'style', 'header', 'footer',
                               'link', 'meta', 'noscript']):
        tag.decompose()

    # Also remove common nav/footer class patterns
    for selector in ['.nav', '.navigation', '.site-nav', '.site-footer',
                     '.footer', '.masthead', '#main-nav', '.breadcrumb',
                     '.proc-footer', '.site-header', '[id*="nav"]',
                     '[class*="footer"]', '[class*="cookie"]']:
        for el in soup.select(selector):
            el.decompose()

    # Find the main content container
    content_html = ""
    for selector in ['main', 'article', '.report-content', '.article-content',
                     '.dossier-content', '.spotlight-content', '.content',
                     '#content', '.page-content', 'body']:
        el = soup.select_one(selector)
        if el:
            content_html = str(el)
            break

    if not content_html:
        content_html = str(soup)

    return {
        "title": title,
        "html": content_html,
        "excerpt": excerpt
    }


def make_ghost_tag(name: str) -> dict:
    return {
        "id": f"tag-{slugify(name)}",
        "name": name,
        "slug": slugify(name),
        "description": ""
    }


def make_ghost_post(folder_name: str, html_path: Path, source_config: dict,
                    post_id: int) -> dict | None:
    """Build a Ghost post/page object from an HTML file."""
    content = extract_content(html_path)
    if not content:
        return None

    slug = slugify(folder_name)
    published_at = extract_date_from_slug(folder_name)

    # Build tag list
    tags = [{"name": t, "slug": slugify(t)} for t in source_config["tags"]]

    post = {
        "id": str(post_id),
        "title": content["title"],
        "slug": slug,
        "html": content["html"],
        "status": source_config["status"],
        "visibility": source_config["visibility"],
        "type": source_config["type"],
        "tags": tags,
        "authors": [{"email": DEFAULT_AUTHOR_EMAIL}],
        "published_at": published_at,
        "created_at": published_at,
        "updated_at": published_at,
    }

    if content["excerpt"]:
        post["custom_excerpt"] = content["excerpt"][:300]

    return post


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    print("CTI → Ghost Bulk Import Script")
    print("=" * 50)

    posts = []
    pages = []
    all_tags = set()
    post_id = 1
    errors = []

    for source in IMPORT_SOURCES:
        folder_path = BASE_DIR / source["folder"]

        if not folder_path.exists():
            print(f"⚠️  Folder not found, skipping: {folder_path}")
            continue

        # Add tags to global tag set
        for tag in source["tags"]:
            all_tags.add(tag)

        # Find all index.html files in subdirectories
        html_files = list(folder_path.glob("*/index.html"))

        if not html_files:
            # Also try direct index.html
            direct = folder_path / "index.html"
            if direct.exists():
                html_files = [direct]

        print(f"\n📁 {source['folder']} — found {len(html_files)} files ({source['description']})")

        for html_path in sorted(html_files):
            folder_name = html_path.parent.name

            # Skip certain folders that are tools/apps not content
            skip_patterns = ['_accuracy', 'api', 'archive', 'design-references',
                             'sample', 'samples', 'terminal', '.git', '.claude']
            if any(p in str(html_path) for p in skip_patterns):
                continue

            ghost_item = make_ghost_post(folder_name, html_path, source, post_id)

            if ghost_item:
                if source["type"] == "post":
                    posts.append(ghost_item)
                else:
                    pages.append(ghost_item)
                print(f"  ✓ {folder_name} → '{ghost_item['title'][:60]}'")
                post_id += 1
            else:
                errors.append(folder_name)
                print(f"  ✗ {folder_name} — could not extract content")

    # Build Ghost import format
    ghost_export = {
        "db": [{
            "meta": {
                "exported_on": int(datetime.now().timestamp() * 1000),
                "version": "5.0.0"
            },
            "data": {
                "posts": posts + pages,
                "tags": [make_ghost_tag(t) for t in sorted(all_tags)],
                "users": []
            }
        }]
    }

    # Write output file
    output_path = BASE_DIR / "ghost-import.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(ghost_export, f, ensure_ascii=False, indent=2)

    print(f"\n{'=' * 50}")
    print(f"✅ Import file written: {output_path}")
    print(f"   Posts (homepage feed): {len(posts)}")
    print(f"   Pages (static):        {len(pages)}")
    print(f"   Tags created:          {len(all_tags)}")
    if errors:
        print(f"   Errors (skipped):      {len(errors)}")
        for e in errors:
            print(f"     - {e}")
    print(f"\nNext step:")
    print(f"  Ghost Admin → Settings → Labs → Import content")
    print(f"  Upload: {output_path}")


if __name__ == "__main__":
    # Check for BeautifulSoup
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        print("Installing required dependency: beautifulsoup4")
        os.system("pip3 install beautifulsoup4")
        from bs4 import BeautifulSoup

    main()
