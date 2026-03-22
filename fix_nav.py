"""
fix_nav.py — Apply consistent nav fixes to all HTML files in the website repo.

Fixes applied:
1. nav-dropdown-menu: top:calc(100% + 8px) → top:100%  (removes gap between trigger and menu)
2. nav-dropdown-menu: ensure padding-top:14px is present (bridges the hover gap inside the menu)
3. nav-dropdown-menu a: add font-size and font-family !important to prevent inheritance
4. .nav-inner (and .site-nav-inner): ensure justify-content:space-between is present
5. nav-dropdown-btn:hover: add explicit font-size/font-family to prevent glitch

Skips: reports/ directory, .git/, non-HTML files.
"""

import os
import re
import glob

WEBSITE_DIR = os.path.dirname(os.path.abspath(__file__))

# Collect all HTML files, skip reports/ and .git/
html_files = []
for root, dirs, files in os.walk(WEBSITE_DIR):
    # Skip unwanted dirs
    dirs[:] = [d for d in dirs if d not in ('.git', 'reports', '__pycache__')]
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))

html_files.sort()

changes = {}  # path -> list of change descriptions

def fix_file(path):
    with open(path, encoding='utf-8') as f:
        original = f.read()

    content = original
    file_changes = []

    # ── Fix 1: top:calc(100% + 8px) → top:100% ──────────────────────────────
    # Handles both compressed and spaced versions
    new_content = re.sub(
        r'(\.nav-dropdown-menu\{[^}]*)top:\s*calc\(100%\s*\+\s*8px\)',
        lambda m: m.group(0).replace(m.group(0).split('top:')[1].split(';')[0],
                                      'calc(100% + 8px)', 1).replace(
            'top:calc(100% + 8px)', 'top:100%').replace(
            'top: calc(100% + 8px)', 'top:100%'),
        content
    )
    # Simpler, direct replace for both variants
    for old, new in [
        ('top:calc(100% + 8px)', 'top:100%'),
        ('top: calc(100% + 8px)', 'top:100%'),
    ]:
        if old in content:
            content = content.replace(old, new)
            file_changes.append(f'  dropdown gap: {old!r} → top:100%')

    # ── Fix 2: ensure nav-dropdown-menu has padding-top:14px ─────────────────
    # Match the compressed single-line form most pages use
    def fix_dropdown_menu_padding(m):
        block = m.group(0)
        if 'padding-top:' in block or 'padding-top :' in block:
            # Already has explicit padding-top; don't touch it
            return block
        # Replace padding:6px 0 → padding:14px 0 6px (top 14px, sides 0, bottom 6px)
        # or add padding-top if padding is set differently
        if 'padding:6px 0' in block:
            new_block = block.replace('padding:6px 0', 'padding:14px 0 6px')
            file_changes.append('  dropdown menu: padding:6px 0 → padding:14px 0 6px')
            return new_block
        elif re.search(r'padding:\d', block):
            # Some other padding — just inject padding-top after opening brace
            new_block = block.replace('{', '{padding-top:14px;', 1)
            file_changes.append('  dropdown menu: injected padding-top:14px')
            return new_block
        else:
            new_block = block.replace('{', '{padding-top:14px;', 1)
            file_changes.append('  dropdown menu: injected padding-top:14px (no prior padding)')
            return new_block

    content = re.sub(
        r'\.nav-dropdown-menu\{[^}]+\}',
        fix_dropdown_menu_padding,
        content
    )

    # ── Fix 3: nav-dropdown-menu a — add !important to font props ─────────────
    # Target: .nav-dropdown-menu a{...font-family:...; font-size:...;...}
    def fix_dropdown_a(m):
        block = m.group(0)
        if '!important' in block:
            return block  # already fixed
        new_block = block
        # font-size:9px → font-size:9px !important
        new_block = re.sub(r'font-size:(\S+?)([;}])', r'font-size:\1 !important\2', new_block)
        # font-family:'DM Mono',monospace → font-family:'DM Mono',monospace !important
        new_block = re.sub(r"font-family:('DM Mono',monospace)([;}])", r"font-family:\1 !important\2", new_block)
        if new_block != block:
            file_changes.append("  dropdown menu a: added !important to font-size and font-family")
        return new_block

    content = re.sub(
        r'\.nav-dropdown-menu a\{[^}]+\}',
        fix_dropdown_a,
        content
    )

    # Also fix .nav-dropdown-menu a:hover to lock font size
    def fix_dropdown_a_hover(m):
        block = m.group(0)
        if 'font-size' in block:
            return block  # already has font-size
        # Add font-size:9px !important and font-family before closing }
        new_block = block[:-1] + ";font-size:9px !important;font-family:'DM Mono',monospace !important}"
        file_changes.append("  dropdown menu a:hover: added explicit font-size + font-family")
        return new_block

    content = re.sub(
        r'\.nav-dropdown-menu a:hover\{[^}]+\}',
        fix_dropdown_a_hover,
        content
    )

    # ── Fix 4: .nav-inner — ensure display:flex + justify-content:space-between
    # Only applies to files that have .nav-inner in HTML but no corresponding CSS rule
    has_nav_inner_html = 'class="nav-inner"' in content or "class='nav-inner'" in content
    has_nav_inner_css  = bool(re.search(r'\.nav-inner\s*\{', content))

    if has_nav_inner_html and not has_nav_inner_css:
        # Insert .nav-inner CSS after the .nav-hamburger block or after nav { } block
        # Find the nav CSS block to inject after it
        # Look for the nav closing brace pattern
        insert_after = re.search(r'(\.nav-hamburger\s*span[^}]+\})', content)
        if not insert_after:
            insert_after = re.search(r'(\.nav-cta-mobile[^}]+\})', content)
        if insert_after:
            nav_inner_css = '\n  .nav-inner { max-width:1200px; margin:0 auto; height:100%; display:flex; justify-content:space-between; align-items:center; }'
            pos = insert_after.end()
            content = content[:pos] + nav_inner_css + content[pos:]
            file_changes.append("  .nav-inner: injected flex + justify-content:space-between CSS")
        else:
            # Fallback: inject before </style>
            content = content.replace(
                '</style>',
                '  .nav-inner { max-width:1200px; margin:0 auto; height:100%; display:flex; justify-content:space-between; align-items:center; }\n</style>',
                1
            )
            file_changes.append("  .nav-inner: injected flex + justify-content:space-between CSS (before </style>)")

    # Also check .site-nav-inner — should already be fine but verify
    if 'class="site-nav-inner"' in content or "class='site-nav-inner'" in content:
        site_inner_match = re.search(r'\.site-nav-inner\s*\{([^}]+)\}', content)
        if site_inner_match and 'justify-content' not in site_inner_match.group(1):
            content = content[:site_inner_match.start(1)] + \
                      site_inner_match.group(1).rstrip() + ' justify-content:space-between;' + \
                      content[site_inner_match.end(1):]
            file_changes.append("  .site-nav-inner: added justify-content:space-between")

    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return file_changes
    return []


print(f"Scanning {len(html_files)} HTML files...\n")
total_changed = 0

for path in html_files:
    rel = os.path.relpath(path, WEBSITE_DIR)
    file_changes = fix_file(path)
    if file_changes:
        total_changed += 1
        print(f"✅  {rel}")
        for c in file_changes:
            print(c)
        print()

print(f"{'─'*60}")
print(f"Done — {total_changed} file(s) modified, {len(html_files) - total_changed} already correct.")
