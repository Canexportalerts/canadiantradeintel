#!/usr/bin/env python3
"""
Run from ~/Documents/canadiantradeintel/
Updates nav links and sector references across all pages.
Safe — uses exact string replacement, no regex.
"""

import os

def update(path, replacements):
    if not os.path.exists(path):
        print(f"  SKIP (not found): {path}")
        return
    with open(path) as f:
        content = f.read()
    original = content
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new, 1)  # replace first occurrence only
        else:
            print(f"  WARNING — pattern not found in {path}:")
            print(f"    '{old[:60]}...'")
    if content != original:
        with open(path, 'w') as f:
            f.write(content)
        print(f"  Updated: {path}")
    else:
        print(f"  No changes: {path}")

# ─────────────────────────────────────────────
# SPOTLIGHT — add Terminal between Dashboard and Tariffs
# ─────────────────────────────────────────────
update('Spotlight/index.html', [
    (
        '<a href="https://canadiantradeintel.ca/dashboard">Dashboard</a>\n      <a href="https://canadiantradeintel.ca/tariffs">Tariffs</a>',
        '<a href="https://canadiantradeintel.ca/dashboard">Dashboard</a>\n      <a href="https://canadiantradeintel.ca/terminal">Terminal</a>\n      <a href="https://canadiantradeintel.ca/procurement">Procurement</a>\n      <a href="https://canadiantradeintel.ca/tariffs">Tariffs</a>'
    ),
])

# ─────────────────────────────────────────────
# ABOUT — add Terminal + Procurement, update sector references
# ─────────────────────────────────────────────
update('about/index.html', [
    (
        '<a href="https://canadiantradeintel.ca/tariffs">Tariffs</a>',
        '<a href="https://canadiantradeintel.ca/terminal">Terminal</a>\n      <a href="https://canadiantradeintel.ca/procurement">Procurement</a>\n      <a href="https://canadiantradeintel.ca/tariffs">Tariffs</a>'
    ),
    (
        "Canada's five most active trade sectors",
        "Canada's six most active trade sectors"
    ),
    (
        "Critical Minerals &amp; Cleantech, Agri-food &amp; Agriculture, Advanced Manufacturing, Technology &amp; Digital, and Aerospace &amp; Defence",
        "Critical Minerals &amp; Mining, Energy &amp; Cleantech, Agri-food &amp; Agriculture, Advanced Manufacturing, Technology &amp; Digital, and Aerospace &amp; Defence"
    ),
    (
        "Critical Minerals & Cleantech, Agri-food & Agriculture, Advanced Manufacturing, Technology & Digital, and Aerospace & Defence",
        "Critical Minerals & Mining, Energy & Cleantech, Agri-food & Agriculture, Advanced Manufacturing, Technology & Digital, and Aerospace & Defence"
    ),
    (
        "five sectors",
        "six sectors"
    ),
    (
        "Five sectors",
        "Six sectors"
    ),
])

# ─────────────────────────────────────────────
# TARIFFS — add Terminal + Procurement
# ─────────────────────────────────────────────
update('tariffs/index.html', [
    (
        '<a href="/tariffs" class="active">Tariffs</a>',
        '<a href="/terminal">Terminal</a>\n      <a href="/procurement">Procurement</a>\n      <a href="/tariffs" class="active">Tariffs</a>'
    ),
])

# ─────────────────────────────────────────────
# REPORTS — add Terminal + Procurement
# ─────────────────────────────────────────────
update('reports/index.html', [
    (
        '<a href="/tariffs">Tariffs</a>',
        '<a href="/terminal">Terminal</a>\n      <a href="/procurement">Procurement</a>\n      <a href="/tariffs">Tariffs</a>'
    ),
])

# ─────────────────────────────────────────────
# DASHBOARD — add Terminal + Procurement to desktop nav
# ─────────────────────────────────────────────
update('dashboard/index.html', [
    (
        '<a href="/tariffs">Tariffs</a>\n      <a href="/about">About</a>',
        '<a href="/terminal">Terminal</a>\n      <a href="/procurement">Procurement</a>\n      <a href="/tariffs">Tariffs</a>\n      <a href="/about">About</a>'
    ),
    # Mobile nav
    (
        '<a href="/tariffs" onclick="closeMobileNav()">Tariffs</a>',
        '<a href="/terminal" onclick="closeMobileNav()">Terminal</a>\n    <a href="/procurement" onclick="closeMobileNav()">Procurement</a>\n    <a href="/tariffs" onclick="closeMobileNav()">Tariffs</a>'
    ),
])

# ─────────────────────────────────────────────
# PRICING — update sector count and sector list
# ─────────────────────────────────────────────
update('pricing.html', [
    # Nav — add Terminal + Procurement
    (
        '<a href="/tariffs">Tariffs</a>',
        '<a href="/terminal">Terminal</a>\n      <a href="/procurement">Procurement</a>\n      <a href="/tariffs">Tariffs</a>'
    ),
    # Sector stat count
    (
        '>5<\n          <div class="stat-label">Sectors Covered</div>',
        '>6<\n          <div class="stat-label">Sectors Covered</div>'
    ),
    # Intelligence plan feature
    (
        'All 5 sector full reports',
        'All 6 sector full reports'
    ),
    # Add-on description sector list
    (
        'Critical Minerals, Agri-food, Advanced Manufacturing, Technology, and Aerospace &amp; Defence — each with dedicated signals',
        'Critical Minerals &amp; Mining, Energy &amp; Cleantech, Agri-food, Advanced Manufacturing, Technology &amp; Digital, and Aerospace &amp; Defence — each with dedicated signals'
    ),
    # FAQ — which sector to choose
    (
        'If you export or are considering exporting in Critical Minerals, Agri-food, Advanced Manufacturing, Technology, or Aerospace &amp; Defence',
        'If you export or are considering exporting in Critical Minerals &amp; Mining, Energy &amp; Cleantech, Agri-food, Advanced Manufacturing, Technology &amp; Digital, or Aerospace &amp; Defence'
    ),
    # Weekly email digest reference
    (
        'five-minute read that keeps you current across all five sectors',
        'five-minute read that keeps you current across all six sectors'
    ),
    # Five sectors heading
    (
        'Five sectors. Weekly delivery.',
        'Six sectors. Weekly delivery.'
    ),
])

print("\nDone. Run:")
print("  git add -A")
print("  git commit -m 'Add Terminal + Procurement to all navs, update to six sectors'")
print("  git push")
