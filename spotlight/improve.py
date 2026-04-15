#!/usr/bin/env python3
"""
5-Improvement script for spotlight/index.html
"""
import re, os, textwrap

SPOTLIGHT = '/Users/nikkoyetman/Documents/canadiantradeintel/spotlight/index.html'

with open(SPOTLIGHT, 'r', encoding='utf-8') as f:
    html = f.read()

# ──────────────────────────────────────────────────────────────────────────────
# IMPROVEMENT 1: Issue pills on article-footer + CSS
# ──────────────────────────────────────────────────────────────────────────────

# Map tile-prefix → issue number
def issue_pill_for_tile(tile_id):
    prefix = tile_id.split('-')[0]
    if prefix in ('002', '007'):
        num = '002'
    else:
        num = '001'
    return (
        f'<a href="/reports/" class="issue-pill" '
        f'style="font-family:\'DM Mono\',monospace;font-size:7px;letter-spacing:0.1em;'
        f'text-transform:uppercase;color:#8B1A1A;border:1px solid #8B1A1A;padding:2px 7px;'
        f'text-decoration:none;white-space:nowrap;" '
        f'target="_self">Featured in Issue #{num} \u2192</a>'
    )

# Find each unique article-footer per tile and replace it
# Strategy: for each tile, find its article-card block and replace the article-footer inside it
def add_issue_pill_to_footer(html, tile_id):
    pill = issue_pill_for_tile(tile_id)
    # Pattern: inside data-tile="TILE_ID" card div, find article-footer
    # The footer is: <div class="article-footer">\n          <span class="article-date">...</span>\n          <span class="article-toggle">+</span>
    # We do a targeted replace: find the card's footer and inject pill
    # Because cards are duplicated (same tile_id repeated), use replace_all logic

    # Match the footer within a card that has data-tile="tile_id"
    # We'll find all occurrences of this exact footer pattern and add pill after date span
    # Since footers may differ by date, do a pattern search

    # Find all article-footer blocks inside article-cards for this tile
    # Use regex to find footer without pill already there
    pattern = (
        r'(data-tile="' + re.escape(tile_id) + r'"[^>]*>.*?'
        r'<div class="article-footer">\s*'
        r'<span class="article-date">[^<]*</span>)\s*'
        r'(<span class="article-toggle">\+</span>\s*</div>)'
    )
    replacement = r'\1\n          ' + pill + r'\n          \2'
    new_html = re.sub(pattern, replacement, html, flags=re.DOTALL)
    return new_html

# Get all unique tile IDs
tile_ids = re.findall(r'data-tile="([^"]+)"', html)
unique_tiles = list(dict.fromkeys(tile_ids))

print(f"Found {len(unique_tiles)} unique tile IDs")

for tile_id in unique_tiles:
    html = add_issue_pill_to_footer(html, tile_id)

# Add CSS before closing </style>
css_addition = """  .issue-pill { display: inline-block; }
  .issue-pill:hover { background: #8B1A1A; color: #fff !important; }
"""
html = html.replace('</style>', css_addition + '</style>', 1)

print("Improvement 1 done: Issue pills added")

# ──────────────────────────────────────────────────────────────────────────────
# IMPROVEMENT 2: Share button slug URLs
# ──────────────────────────────────────────────────────────────────────────────

SLUGS = {
    '002-1': 'finkl-steel-sorel-april-2026',
    '002-2': 'ivanhoe-mines-april-2026',
    '002-3': 'denarius-metals-corp-april-2026',
    '002-4': 'montage-resources-april-2026',
    '002-5': 'canola-council-of-canada-april-2026',
    '002-6': 'appdirect-april-2026',
    '002-7': 'ph7-april-2026',
    '002-8': 'poet-technologies-april-2026',
    '007-1': 'rbc-canadian-growth-fund-april-2026',
    '007-2': 'nano-one-materials-corp-april-2026',
    '007-3': 'adf-group-april-2026',
    '007-4': 'nanuk-gear-protection-april-2026',
    '007-5': 'rock-tech-lithium-april-2026',
    '007-6': 'innovair-solutions-april-2026',
    '007-7': 'unknown-april-2026',
    '006-1': 'vizsla-silver-corp-april-2026',
    '006-2': 'green-bay-copper-gold-april-2026',
    '005-1': 'vizsla-silver-corp-april-2026b',
    '005-2': 'green-bay-copper-gold-april-2026b',
    '004-1': 'vizsla-silver-corp-april-2026c',
    '004-2': 'green-bay-copper-gold-april-2026c',
    '003-1': 'vizsla-silver-corp-april-2026d',
    '003-2': 'green-bay-copper-gold-april-2026d',
    # 001-series use existing slugs where they exist, else generate
    '001-01': 'defense-metals-corp-march-2026',
    '001-02': 'nouveau-monde-graphite-march-2026',
    '001-03': 'boart-longyear-march-2026',
    '001-04': 'port-of-saint-john-march-2026',
    '001-05': 'top-aces-march-2026',
    '001-06': 'patriot-battery-metals-mar-2026',
    '001-07': 'nutrien-indonesia-mar-2026',
    '001-08': 'cae-uk-mod-mar-2026',
    '001-09': 'vital-metals-src-mar-2026',
    '001-10': 'govtech-japan-mar-2026',
    '001-11': 'thyssenkrupp-hamilton-mar-2026',
    '001-12': 'cameco-march-2026',
    '001-13': 'richardson-international-march-2026',
    '001-14': 'standardaero-march-2026',
}

BASE = 'https://canadiantradeintel.ca/spotlight'

def update_share_urls(html, tile_id, slug):
    """Update LinkedIn and X share URLs in a drawer."""
    drawer_id = f'drawer-{tile_id}'
    # Find the drawer block
    # Replace the generic spotlight URL with slug URL within each drawer occurrence
    old_li = f'href="https://www.linkedin.com/sharing/share-offsite/?url={BASE}"'
    new_li = f'href="https://www.linkedin.com/sharing/share-offsite/?url={BASE}/{slug}/"'
    old_x  = f'href="https://twitter.com/intent/tweet?url={BASE}"'
    new_x  = f'href="https://twitter.com/intent/tweet?url={BASE}/{slug}/"'
    # Replace within drawer blocks for this tile
    # Find all drawer-TILE_ID blocks and replace URLs inside them
    def replace_in_drawer(m):
        block = m.group(0)
        block = block.replace(old_li, new_li)
        block = block.replace(old_x, new_x)
        return block
    pattern = r'(<div class="article-drawer" id="' + re.escape(drawer_id) + r'".*?</div>\s*</div>\s*</div>)'
    new_html = re.sub(pattern, replace_in_drawer, html, flags=re.DOTALL)
    return new_html

for tile_id, slug in SLUGS.items():
    html = update_share_urls(html, tile_id, slug)

print("Improvement 2 done: Share URLs updated")

# ──────────────────────────────────────────────────────────────────────────────
# IMPROVEMENT 3 & 5: Related intelligence blocks + RBC fix
# ──────────────────────────────────────────────────────────────────────────────

RELATED_INTEL = {
    '002-1': {
        'sentence': 'Finkl Steel\'s entry into TKMS defence supply chains reflects the broader NATO industrial rearmament trend tracked in our Advanced Manufacturing report.',
        'links': [
            ('<a href="/reports/advanced-manufacturing/" style="font-family:\'DM Mono\',monospace;font-size:8px;letter-spacing:0.08em;text-transform:uppercase;color:#8B1A1A;border:1px solid #8B1A1A;padding:4px 10px;text-decoration:none;">Read Advanced Manufacturing Report \u2192</a>', None),
            (None, '<a href="/countries/germany/" style="font-family:\'DM Mono\',monospace;font-size:8px;letter-spacing:0.08em;text-transform:uppercase;color:#8B1A1A;border:1px solid #8B1A1A;padding:4px 10px;text-decoration:none;">Country Dossier: Germany \u2192</a>'),
        ],
    },
    '002-2': {
        'sentence': 'Ivanhoe Mines\' Hormuz warning connects to our Critical Minerals report\'s analysis of supply chain chokepoint exposure for Canadian copper producers.',
        'links': [
            ('<a href="/reports/critical-minerals/" style="font-family:\'DM Mono\',monospace;font-size:8px;letter-spacing:0.08em;text-transform:uppercase;color:#8B1A1A;border:1px solid #8B1A1A;padding:4px 10px;text-decoration:none;">Read Critical Minerals Report \u2192</a>', None),
        ],
    },
    '002-3': {
        'sentence': 'Denarius Metals\' Iberian acquisition reflects the European base metals consolidation wave detailed in our Critical Minerals report.',
        'links': [
            ('<a href="/reports/critical-minerals/" style="font-family:\'DM Mono\',monospace;font-size:8px;letter-spacing:0.08em;text-transform:uppercase;color:#8B1A1A;border:1px solid #8B1A1A;padding:4px 10px;text-decoration:none;">Read Critical Minerals Report \u2192</a>', None),
            (None, '<a href="/countries/spain/" style="font-family:\'DM Mono\',monospace;font-size:8px;letter-spacing:0.08em;text-transform:uppercase;color:#8B1A1A;border:1px solid #8B1A1A;padding:4px 10px;text-decoration:none;">Country Dossier: Spain \u2192</a>'),
        ],
    },
    '002-4': {
        'sentence': 'Montage Resources\' West Africa expansion aligns with the frontier exploration strategies reviewed in our Critical Minerals report.',
        'links': [
            ('<a href="/reports/critical-minerals/" style="font-family:\'DM Mono\',monospace;font-size:8px;letter-spacing:0.08em;text-transform:uppercase;color:#8B1A1A;border:1px solid #8B1A1A;padding:4px 10px;text-decoration:none;">Read Critical Minerals Report \u2192</a>', None),
        ],
    },
    '002-5': {
        'sentence': 'The canola tariff relief from China is analysed in depth — including its durability and implications for other agri-exporters — in our Agri-food report.',
        'links': [
            ('<a href="/reports/agri-food/" style="font-family:\'DM Mono\',monospace;font-size:8px;letter-spacing:0.08em;text-transform:uppercase;color:#8B1A1A;border:1px solid #8B1A1A;padding:4px 10px;text-decoration:none;">Read Agri-food Report \u2192</a>', None),
            (None, '<a href="/countries/china/" style="font-family:\'DM Mono\',monospace;font-size:8px;letter-spacing:0.08em;text-transform:uppercase;color:#8B1A1A;border:1px solid #8B1A1A;padding:4px 10px;text-decoration:none;">Country Dossier: China \u2192</a>'),
        ],
    },
    '002-6': {
        'sentence': 'AppDirect\'s M&A velocity in Canadian SaaS is contextualised within the North American tech consolidation trends in our Technology & Digital report.',
        'links': [
            ('<a href="/reports/technology-digital/" style="font-family:\'DM Mono\',monospace;font-size:8px;letter-spacing:0.08em;text-transform:uppercase;color:#8B1A1A;border:1px solid #8B1A1A;padding:4px 10px;text-decoration:none;">Read Technology Report \u2192</a>', None),
        ],
    },
    '002-7': {
        'sentence': 'pH7\'s Series B raise sits within the broader Canadian cleantech-minerals funding landscape tracked in our Critical Minerals report.',
        'links': [
            ('<a href="/reports/critical-minerals/" style="font-family:\'DM Mono\',monospace;font-size:8px;letter-spacing:0.08em;text-transform:uppercase;color:#8B1A1A;border:1px solid #8B1A1A;padding:4px 10px;text-decoration:none;">Read Critical Minerals Report \u2192</a>', None),
        ],
    },
    '002-8': {
        'sentence': 'POET Technologies\' PFIC redomiciliation is part of a larger structural challenge for Canadian tech companies with US listings, covered in our Technology report.',
        'links': [
            ('<a href="/reports/technology-digital/" style="font-family:\'DM Mono\',monospace;font-size:8px;letter-spacing:0.08em;text-transform:uppercase;color:#8B1A1A;border:1px solid #8B1A1A;padding:4px 10px;text-decoration:none;">Read Technology Report \u2192</a>', None),
        ],
    },
    '007-1': {
        'sentence': 'RBC\'s $1B Canadian growth fund is a cross-sector capital story — our full reports cover how defence, infrastructure, and critical minerals sectors stand to benefit.',
        'links': [
            ('<a href="/reports/" style="font-family:\'DM Mono\',monospace;font-size:8px;letter-spacing:0.08em;text-transform:uppercase;color:#8B1A1A;border:1px solid #8B1A1A;padding:4px 10px;text-decoration:none;">Browse All Reports \u2192</a>', None),
        ],
    },
    '007-2': {
        'sentence': 'Federal battery investment in Nano One, EcoPro, and NanoXplore connects to the Canadian EV supply chain strategy detailed in our Critical Minerals report.',
        'links': [
            ('<a href="/reports/critical-minerals/" style="font-family:\'DM Mono\',monospace;font-size:8px;letter-spacing:0.08em;text-transform:uppercase;color:#8B1A1A;border:1px solid #8B1A1A;padding:4px 10px;text-decoration:none;">Read Critical Minerals Report \u2192</a>', None),
        ],
    },
    '007-3': {
        'sentence': 'ADF Group\'s US infrastructure wins are tracked alongside the broader Canadian advanced manufacturing export picture in our Advanced Manufacturing report.',
        'links': [
            ('<a href="/reports/advanced-manufacturing/" style="font-family:\'DM Mono\',monospace;font-size:8px;letter-spacing:0.08em;text-transform:uppercase;color:#8B1A1A;border:1px solid #8B1A1A;padding:4px 10px;text-decoration:none;">Read Advanced Manufacturing Report \u2192</a>', None),
            (None, '<a href="/countries/united-states/" style="font-family:\'DM Mono\',monospace;font-size:8px;letter-spacing:0.08em;text-transform:uppercase;color:#8B1A1A;border:1px solid #8B1A1A;padding:4px 10px;text-decoration:none;">Country Dossier: United States \u2192</a>'),
        ],
    },
    '007-4': {
        'sentence': 'NANUK\'s US acquisition reflects the FDI-into-Canada manufacturing trend explored in our Advanced Manufacturing report.',
        'links': [
            ('<a href="/reports/advanced-manufacturing/" style="font-family:\'DM Mono\',monospace;font-size:8px;letter-spacing:0.08em;text-transform:uppercase;color:#8B1A1A;border:1px solid #8B1A1A;padding:4px 10px;text-decoration:none;">Read Advanced Manufacturing Report \u2192</a>', None),
        ],
    },
    '007-5': {
        'sentence': 'Rock Tech Lithium\'s $200M European anchor deal is a flagship case study in the Canada-EU critical minerals partnership documented in our Critical Minerals report.',
        'links': [
            ('<a href="/reports/critical-minerals/" style="font-family:\'DM Mono\',monospace;font-size:8px;letter-spacing:0.08em;text-transform:uppercase;color:#8B1A1A;border:1px solid #8B1A1A;padding:4px 10px;text-decoration:none;">Read Critical Minerals Report \u2192</a>', None),
        ],
    },
    '007-6': {
        'sentence': 'Innovair Solutions\' CDPQ-backed multi-country manufacturing model is part of the advanced manufacturing export landscape in our report.',
        'links': [
            ('<a href="/reports/advanced-manufacturing/" style="font-family:\'DM Mono\',monospace;font-size:8px;letter-spacing:0.08em;text-transform:uppercase;color:#8B1A1A;border:1px solid #8B1A1A;padding:4px 10px;text-decoration:none;">Read Advanced Manufacturing Report \u2192</a>', None),
        ],
    },
    '007-7': {
        'sentence': 'Canadian bus manufacturers winning US transit contracts is a recurring theme in our Advanced Manufacturing report\'s North American market access section.',
        'links': [
            ('<a href="/reports/advanced-manufacturing/" style="font-family:\'DM Mono\',monospace;font-size:8px;letter-spacing:0.08em;text-transform:uppercase;color:#8B1A1A;border:1px solid #8B1A1A;padding:4px 10px;text-decoration:none;">Read Advanced Manufacturing Report \u2192</a>', None),
        ],
    },
    '006-1': {
        'sentence': 'Vizsla Silver\'s Mexico security crisis underscores the operational risk dimension of Canadian mining in Latin America, covered in our Critical Minerals report.',
        'links': [
            ('<a href="/reports/critical-minerals/" style="font-family:\'DM Mono\',monospace;font-size:8px;letter-spacing:0.08em;text-transform:uppercase;color:#8B1A1A;border:1px solid #8B1A1A;padding:4px 10px;text-decoration:none;">Read Critical Minerals Report \u2192</a>', None),
            (None, '<a href="/countries/mexico/" style="font-family:\'DM Mono\',monospace;font-size:8px;letter-spacing:0.08em;text-transform:uppercase;color:#8B1A1A;border:1px solid #8B1A1A;padding:4px 10px;text-decoration:none;">Country Dossier: Mexico \u2192</a>'),
        ],
    },
    '006-2': {
        'sentence': 'Green Bay\'s high-grade copper-gold drilling results connect to the Quebec critical minerals development pipeline tracked in our Critical Minerals report.',
        'links': [
            ('<a href="/reports/critical-minerals/" style="font-family:\'DM Mono\',monospace;font-size:8px;letter-spacing:0.08em;text-transform:uppercase;color:#8B1A1A;border:1px solid #8B1A1A;padding:4px 10px;text-decoration:none;">Read Critical Minerals Report \u2192</a>', None),
        ],
    },
    '005-1': {
        'sentence': 'Vizsla Silver\'s Mexico security crisis underscores the operational risk dimension of Canadian mining in Latin America, covered in our Critical Minerals report.',
        'links': [
            ('<a href="/reports/critical-minerals/" style="font-family:\'DM Mono\',monospace;font-size:8px;letter-spacing:0.08em;text-transform:uppercase;color:#8B1A1A;border:1px solid #8B1A1A;padding:4px 10px;text-decoration:none;">Read Critical Minerals Report \u2192</a>', None),
            (None, '<a href="/countries/mexico/" style="font-family:\'DM Mono\',monospace;font-size:8px;letter-spacing:0.08em;text-transform:uppercase;color:#8B1A1A;border:1px solid #8B1A1A;padding:4px 10px;text-decoration:none;">Country Dossier: Mexico \u2192</a>'),
        ],
    },
    '005-2': {
        'sentence': 'Green Bay\'s high-grade copper-gold drilling results connect to the Quebec critical minerals development pipeline tracked in our Critical Minerals report.',
        'links': [
            ('<a href="/reports/critical-minerals/" style="font-family:\'DM Mono\',monospace;font-size:8px;letter-spacing:0.08em;text-transform:uppercase;color:#8B1A1A;border:1px solid #8B1A1A;padding:4px 10px;text-decoration:none;">Read Critical Minerals Report \u2192</a>', None),
        ],
    },
    '004-1': {
        'sentence': 'Vizsla Silver\'s Mexico security crisis underscores the operational risk dimension of Canadian mining in Latin America, covered in our Critical Minerals report.',
        'links': [
            ('<a href="/reports/critical-minerals/" style="font-family:\'DM Mono\',monospace;font-size:8px;letter-spacing:0.08em;text-transform:uppercase;color:#8B1A1A;border:1px solid #8B1A1A;padding:4px 10px;text-decoration:none;">Read Critical Minerals Report \u2192</a>', None),
            (None, '<a href="/countries/mexico/" style="font-family:\'DM Mono\',monospace;font-size:8px;letter-spacing:0.08em;text-transform:uppercase;color:#8B1A1A;border:1px solid #8B1A1A;padding:4px 10px;text-decoration:none;">Country Dossier: Mexico \u2192</a>'),
        ],
    },
    '004-2': {
        'sentence': 'Green Bay\'s high-grade copper-gold drilling results connect to the Quebec critical minerals development pipeline tracked in our Critical Minerals report.',
        'links': [
            ('<a href="/reports/critical-minerals/" style="font-family:\'DM Mono\',monospace;font-size:8px;letter-spacing:0.08em;text-transform:uppercase;color:#8B1A1A;border:1px solid #8B1A1A;padding:4px 10px;text-decoration:none;">Read Critical Minerals Report \u2192</a>', None),
        ],
    },
    '003-1': {
        'sentence': 'Vizsla Silver\'s Mexico security crisis underscores the operational risk dimension of Canadian mining in Latin America, covered in our Critical Minerals report.',
        'links': [
            ('<a href="/reports/critical-minerals/" style="font-family:\'DM Mono\',monospace;font-size:8px;letter-spacing:0.08em;text-transform:uppercase;color:#8B1A1A;border:1px solid #8B1A1A;padding:4px 10px;text-decoration:none;">Read Critical Minerals Report \u2192</a>', None),
            (None, '<a href="/countries/mexico/" style="font-family:\'DM Mono\',monospace;font-size:8px;letter-spacing:0.08em;text-transform:uppercase;color:#8B1A1A;border:1px solid #8B1A1A;padding:4px 10px;text-decoration:none;">Country Dossier: Mexico \u2192</a>'),
        ],
    },
    '003-2': {
        'sentence': 'Green Bay\'s high-grade copper-gold drilling results connect to the Quebec critical minerals development pipeline tracked in our Critical Minerals report.',
        'links': [
            ('<a href="/reports/critical-minerals/" style="font-family:\'DM Mono\',monospace;font-size:8px;letter-spacing:0.08em;text-transform:uppercase;color:#8B1A1A;border:1px solid #8B1A1A;padding:4px 10px;text-decoration:none;">Read Critical Minerals Report \u2192</a>', None),
        ],
    },
    '001-01': {
        'sentence': 'Defense Metals\' rare earth play connects to Canada\'s critical minerals diversification strategy detailed in our Critical Minerals report.',
        'links': [
            ('<a href="/reports/critical-minerals/" style="font-family:\'DM Mono\',monospace;font-size:8px;letter-spacing:0.08em;text-transform:uppercase;color:#8B1A1A;border:1px solid #8B1A1A;padding:4px 10px;text-decoration:none;">Read Critical Minerals Report \u2192</a>', None),
            (None, '<a href="/countries/china/" style="font-family:\'DM Mono\',monospace;font-size:8px;letter-spacing:0.08em;text-transform:uppercase;color:#8B1A1A;border:1px solid #8B1A1A;padding:4px 10px;text-decoration:none;">Country Dossier: China \u2192</a>'),
        ],
    },
    '001-02': {
        'sentence': 'Nouveau Monde Graphite\'s EDC/CIB financing reflects the Canadian battery supply chain investment patterns tracked in our Critical Minerals report.',
        'links': [
            ('<a href="/reports/critical-minerals/" style="font-family:\'DM Mono\',monospace;font-size:8px;letter-spacing:0.08em;text-transform:uppercase;color:#8B1A1A;border:1px solid #8B1A1A;padding:4px 10px;text-decoration:none;">Read Critical Minerals Report \u2192</a>', None),
        ],
    },
    '001-03': {
        'sentence': 'Boart Longyear\'s job relocation to China illustrates supply chain migration risks in mining equipment, tracked in our Critical Minerals report.',
        'links': [
            ('<a href="/reports/critical-minerals/" style="font-family:\'DM Mono\',monospace;font-size:8px;letter-spacing:0.08em;text-transform:uppercase;color:#8B1A1A;border:1px solid #8B1A1A;padding:4px 10px;text-decoration:none;">Read Critical Minerals Report \u2192</a>', None),
        ],
    },
    '001-04': {
        'sentence': 'Port of Saint John\'s tariff-driven boom is part of the trade corridor reshaping story covered across our sector reports.',
        'links': [
            ('<a href="/reports/" style="font-family:\'DM Mono\',monospace;font-size:8px;letter-spacing:0.08em;text-transform:uppercase;color:#8B1A1A;border:1px solid #8B1A1A;padding:4px 10px;text-decoration:none;">Browse All Reports \u2192</a>', None),
        ],
    },
    '001-05': {
        'sentence': 'Top Aces\' Argentine F-16 training contract is part of the Latin America defence market opportunity explored in our Aerospace & Defence report.',
        'links': [
            ('<a href="/reports/aerospace-defence/" style="font-family:\'DM Mono\',monospace;font-size:8px;letter-spacing:0.08em;text-transform:uppercase;color:#8B1A1A;border:1px solid #8B1A1A;padding:4px 10px;text-decoration:none;">Read Aerospace & Defence Report \u2192</a>', None),
        ],
    },
    '001-06': {
        'sentence': 'Patriot Battery Metals\' Japanese trading house financing is a case study in the Indo-Pacific lithium strategy covered in our Critical Minerals report.',
        'links': [
            ('<a href="/reports/critical-minerals/" style="font-family:\'DM Mono\',monospace;font-size:8px;letter-spacing:0.08em;text-transform:uppercase;color:#8B1A1A;border:1px solid #8B1A1A;padding:4px 10px;text-decoration:none;">Read Critical Minerals Report \u2192</a>', None),
            (None, '<a href="/countries/japan/" style="font-family:\'DM Mono\',monospace;font-size:8px;letter-spacing:0.08em;text-transform:uppercase;color:#8B1A1A;border:1px solid #8B1A1A;padding:4px 10px;text-decoration:none;">Country Dossier: Japan \u2192</a>'),
        ],
    },
    '001-07': {
        'sentence': 'Nutrien\'s Indonesia potash deal is examined alongside EDC\'s Indo-Pacific financing strategy in our Agri-food report.',
        'links': [
            ('<a href="/reports/agri-food/" style="font-family:\'DM Mono\',monospace;font-size:8px;letter-spacing:0.08em;text-transform:uppercase;color:#8B1A1A;border:1px solid #8B1A1A;padding:4px 10px;text-decoration:none;">Read Agri-food Report \u2192</a>', None),
        ],
    },
    '001-08': {
        'sentence': 'CAE\'s UK MoD contract is part of the Five Eyes defence market access story in our Aerospace & Defence report.',
        'links': [
            ('<a href="/reports/aerospace-defence/" style="font-family:\'DM Mono\',monospace;font-size:8px;letter-spacing:0.08em;text-transform:uppercase;color:#8B1A1A;border:1px solid #8B1A1A;padding:4px 10px;text-decoration:none;">Read Aerospace & Defence Report \u2192</a>', None),
        ],
    },
    '001-09': {
        'sentence': 'Vital Metals\' SRC offtake creates Canada\'s first end-to-end rare earth pathway — a supply chain milestone explored in our Critical Minerals report.',
        'links': [
            ('<a href="/reports/critical-minerals/" style="font-family:\'DM Mono\',monospace;font-size:8px;letter-spacing:0.08em;text-transform:uppercase;color:#8B1A1A;border:1px solid #8B1A1A;padding:4px 10px;text-decoration:none;">Read Critical Minerals Report \u2192</a>', None),
        ],
    },
    '001-10': {
        'sentence': 'Ottawa GovTech firms\' Japan Digital Agency shortlisting is a CPTPP access case study covered in our Technology & Digital report.',
        'links': [
            ('<a href="/reports/technology-digital/" style="font-family:\'DM Mono\',monospace;font-size:8px;letter-spacing:0.08em;text-transform:uppercase;color:#8B1A1A;border:1px solid #8B1A1A;padding:4px 10px;text-decoration:none;">Read Technology Report \u2192</a>', None),
            (None, '<a href="/countries/japan/" style="font-family:\'DM Mono\',monospace;font-size:8px;letter-spacing:0.08em;text-transform:uppercase;color:#8B1A1A;border:1px solid #8B1A1A;padding:4px 10px;text-decoration:none;">Country Dossier: Japan \u2192</a>'),
        ],
    },
    '001-11': {
        'sentence': 'Thyssenkrupp\'s Hamilton acquisition and its Canadian supply chain opportunities are covered in our Advanced Manufacturing report.',
        'links': [
            ('<a href="/reports/advanced-manufacturing/" style="font-family:\'DM Mono\',monospace;font-size:8px;letter-spacing:0.08em;text-transform:uppercase;color:#8B1A1A;border:1px solid #8B1A1A;padding:4px 10px;text-decoration:none;">Read Advanced Manufacturing Report \u2192</a>', None),
        ],
    },
    '001-12': {
        'sentence': 'Cameco\'s Kazakhstan supply disruption play is a case study in critical minerals market timing, detailed in our Critical Minerals report.',
        'links': [
            ('<a href="/reports/critical-minerals/" style="font-family:\'DM Mono\',monospace;font-size:8px;letter-spacing:0.08em;text-transform:uppercase;color:#8B1A1A;border:1px solid #8B1A1A;padding:4px 10px;text-decoration:none;">Read Critical Minerals Report \u2192</a>', None),
        ],
    },
    '001-13': {
        'sentence': 'Richardson International\'s EU canola pivot under CETA is the diversification playbook explored in our Agri-food report.',
        'links': [
            ('<a href="/reports/agri-food/" style="font-family:\'DM Mono\',monospace;font-size:8px;letter-spacing:0.08em;text-transform:uppercase;color:#8B1A1A;border:1px solid #8B1A1A;padding:4px 10px;text-decoration:none;">Read Agri-food Report \u2192</a>', None),
        ],
    },
    '001-14': {
        'sentence': 'StandardAero\'s USAF C-130 MRO win illustrates NORAD adjacency as a market entry tool, explored in our Aerospace & Defence report.',
        'links': [
            ('<a href="/reports/aerospace-defence/" style="font-family:\'DM Mono\',monospace;font-size:8px;letter-spacing:0.08em;text-transform:uppercase;color:#8B1A1A;border:1px solid #8B1A1A;padding:4px 10px;text-decoration:none;">Read Aerospace & Defence Report \u2192</a>', None),
        ],
    },
}

def build_related_block(tile_id):
    info = RELATED_INTEL.get(tile_id)
    if not info:
        return ''
    links_html = ''
    for primary, secondary in info['links']:
        if primary:
            links_html += '\n    ' + primary
        if secondary:
            links_html += '\n    ' + secondary
    return f'''<div style="background:var(--color-background-secondary,#f8f6f2);border-top:1px solid var(--rule);padding:14px 18px;margin-top:16px;margin-left:-22px;margin-right:-22px;">
  <div style="font-family:\'DM Mono\',monospace;font-size:7px;letter-spacing:0.14em;text-transform:uppercase;color:var(--ink-light);margin-bottom:8px;">Related intelligence</div>
  <div style="font-size:11px;color:var(--ink-mid);margin-bottom:10px;">{info['sentence']}</div>
  <div style="display:flex;gap:8px;flex-wrap:wrap;">{links_html}
  </div>
</div>'''

def inject_related_intel(html, tile_id):
    """Add related intel block before drawer-share, remove old sector report link."""
    drawer_id = f'drawer-{tile_id}'
    related_block = build_related_block(tile_id)
    if not related_block:
        return html

    def process_drawer(m):
        block = m.group(0)
        # Remove the old sector report link (but not the original story link)
        # Pattern: <a href="/reports/full_report_*.html" class="drawer-link"...>Read the ... report →</a>
        block = re.sub(
            r'\s*<a href="/reports/full_report_[^"]*\.html" class="drawer-link"[^>]*>Read the [^<]*report[^<]*</a>',
            '',
            block
        )
        # Also handle the RBC special case (007-1): remove cross-sector report link
        block = re.sub(
            r'\s*<a href="/reports/full_report_critical_minerals_2026-04-09\.html" class="drawer-link"[^>]*>Read the Cross-sector report[^<]*</a>',
            '',
            block
        )
        # Insert related block before <div class="drawer-share">
        block = block.replace(
            '<div class="drawer-share">',
            related_block + '\n              <div class="drawer-share">',
            1
        )
        return block

    pattern = r'<div class="article-drawer" id="' + re.escape(drawer_id) + r'".*?(?=<div class="article-(?:card|drawer)"|</div>\s*</div>\s*(?:<!--|\Z))'
    new_html = re.sub(pattern, process_drawer, html, flags=re.DOTALL)
    return new_html

for tile_id in unique_tiles:
    html = inject_related_intel(html, tile_id)

print("Improvement 3 & 5 done: Related intelligence blocks added, old report links removed")

# ──────────────────────────────────────────────────────────────────────────────
# Write the modified index.html
# ──────────────────────────────────────────────────────────────────────────────
with open(SPOTLIGHT, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Written: {SPOTLIGHT}")

# ──────────────────────────────────────────────────────────────────────────────
# IMPROVEMENT 4: Individual slug pages
# ──────────────────────────────────────────────────────────────────────────────

NAV_HTML = '''<nav id="main-nav"></nav>'''
SCRIPT_TAG = '<script src="/nav.js"></script>'

FOOTER_HTML = '''<footer>
  <div class="footer-grid">
    <div class="footer-col-brand">
      <div class="footer-brand-name">Canadian Trade Intel</div>
      <div class="footer-brand-tagline">Weekly trade intelligence for Canadian businesses.<br>Six sectors. Every Tuesday.</div>
      <a href="/pricing" class="footer-plans-btn">See Plans \u2192</a>
    </div>
    <div>
      <div class="footer-col-title">Intelligence</div>
      <div class="footer-links">
        <a href="/reports">Weekly Reports</a>
        <a href="/spotlight">Spotlight</a>
        <a href="/dashboard">Dashboard</a>
        <a href="/terminal/">FDI Monitor</a>
      </div>
    </div>
    <div>
      <div class="footer-col-title">Tools</div>
      <div class="footer-links">
        <a href="/terminal">Live Data Terminal</a>
        <a href="/procurement">Procurement Hub</a>
        <a href="/tariffs">Tariff Reference</a>
      </div>
    </div>
    <div>
      <div class="footer-col-title">Resources</div>
      <div class="footer-links">
        <a href="/guides">Practical Guides</a>
        <a href="/map">Canadian Business Map</a>
        <a href="/methodology">Methodology</a>
      </div>
    </div>
    <div>
      <div class="footer-col-title">Company</div>
      <div class="footer-links">
        <a href="/about">About</a>
        <a href="/pricing">Pricing</a>
        <a href="mailto:hello@canadiantradeintel.ca">Contact</a>
      </div>
    </div>
  </div>
  <div class="footer-bottom">
    <span class="footer-copy">\u00a9 2026 Canadian Trade Intelligence Inc. \u00b7 Federally incorporated \u00b7 Not legal or investment advice</span>
  </div>
</footer>'''

# Re-read the now-modified HTML to extract drawer content for slug pages
with open(SPOTLIGHT, 'r', encoding='utf-8') as f:
    modified_html = f.read()

# Extract the CSS block from the main page (between <style> and </style>)
css_match = re.search(r'<style>(.*?)</style>', modified_html, re.DOTALL)
PAGE_CSS = css_match.group(1) if css_match else ''

def extract_tile_data(html, tile_id):
    """Extract content for a tile from the HTML."""
    drawer_id = f'drawer-{tile_id}'

    # Get company name from aside
    company_m = re.search(
        r'id="' + re.escape(drawer_id) + r'".*?<div class="drawer-aside-company">([^<]+)</div>',
        html, re.DOTALL
    )
    company = company_m.group(1).strip() if company_m else tile_id

    # Get h2 headline
    h2_m = re.search(
        r'id="' + re.escape(drawer_id) + r'".*?<h2>([^<]+)</h2>',
        html, re.DOTALL
    )
    headline = h2_m.group(1).strip() if h2_m else ''

    # Get drawer-body
    body_m = re.search(
        r'id="' + re.escape(drawer_id) + r'".*?<div class="drawer-body">(.*?)</div>\s*<div class="drawer-actions"',
        html, re.DOTALL
    )
    body_html = body_m.group(1).strip() if body_m else ''

    # Get sector label
    sector_m = re.search(
        r'id="' + re.escape(drawer_id) + r'".*?<span class="drawer-sector-label"[^>]*>([^<]+)</span>',
        html, re.DOTALL
    )
    sector_label = sector_m.group(1).strip() if sector_m else ''

    # Get sector dot color
    sector_dot_m = re.search(
        r'id="' + re.escape(drawer_id) + r'".*?<span class="drawer-sector-dot" style="([^"]+)"',
        html, re.DOTALL
    )
    sector_dot_style = sector_dot_m.group(1) if sector_dot_m else 'background:var(--minerals)'

    # Get original story URL
    orig_m = re.search(
        r'id="' + re.escape(drawer_id) + r'".*?<a href="(https?://[^"]+)" target="_blank" rel="noopener" class="drawer-link"',
        html, re.DOTALL
    )
    orig_url = orig_m.group(1) if orig_m else ''

    # Get date from card
    date_m = re.search(
        r'data-tile="' + re.escape(tile_id) + r'".*?<span class="article-date">([^<]+)</span>',
        html, re.DOTALL
    )
    date_str = date_m.group(1).strip() if date_m else 'Apr 2026'

    # Get sector from card data-sector attribute
    sector_attr_m = re.search(
        r'data-tile="' + re.escape(tile_id) + r'"[^>]*data-sector="([^"]+)"',
        html
    )
    if not sector_attr_m:
        sector_attr_m = re.search(
            r'data-sector="([^"]+)"[^>]*data-tile="' + re.escape(tile_id) + r'"',
            html
        )
    sector_attr = sector_attr_m.group(1) if sector_attr_m else 'minerals'

    # Get aside rows
    aside_m = re.search(
        r'id="' + re.escape(drawer_id) + r'".*?<div class="drawer-aside">(.*?)</div>\s*</div>\s*</div>',
        html, re.DOTALL
    )
    aside_html = aside_m.group(1).strip() if aside_m else ''

    # Extract Why It Matters text for meta description
    why_m = re.search(
        r'Why It Matters</p><p>([^<]+)',
        body_html
    )
    why_text = why_m.group(1) if why_m else company + ' — ' + headline
    meta_desc = why_text[:160].strip()
    if len(why_text) > 160:
        meta_desc = meta_desc.rstrip() + '...'

    return {
        'company': company,
        'headline': headline,
        'body_html': body_html,
        'sector_label': sector_label,
        'sector_dot_style': sector_dot_style,
        'sector_attr': sector_attr,
        'orig_url': orig_url,
        'date_str': date_str,
        'aside_html': aside_html,
        'meta_desc': meta_desc,
    }

def build_related_block_standalone(tile_id):
    """Build related intelligence block HTML for standalone page."""
    return build_related_block(tile_id)

def generate_slug_page(tile_id, slug, data):
    """Generate a complete standalone HTML page for a tile."""
    company = data['company']
    headline = data['headline']
    meta_desc = data['meta_desc']
    sector_label = data['sector_label']
    sector_dot_style = data['sector_dot_style']
    body_html = data['body_html']
    orig_url = data['orig_url']
    aside_html = data['aside_html']
    date_str = data['date_str']

    related_block = build_related_block_standalone(tile_id)

    orig_link = ''
    if orig_url:
        orig_link = f'<a href="{orig_url}" target="_blank" rel="noopener" class="drawer-link" style="color:var(--ink-mid);">Read original story \u2192</a>'

    canonical = f'https://canadiantradeintel.ca/spotlight/{slug}/'

    issue_prefix = tile_id.split('-')[0]
    if issue_prefix in ('002', '007'):
        issue_num = '002'
        issue_date = 'April 14, 2026'
    else:
        issue_num = '001'
        issue_date = 'March 2026'

    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{company} \u2014 {headline} | Canadian Trade Intel Spotlight</title>
<meta name="description" content="{meta_desc}">
<meta property="og:title" content="{company} \u2014 {headline}">
<meta property="og:description" content="{meta_desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Canadian Trade Intel">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{company} | Canadian Trade Intel Spotlight">
<meta name="twitter:description" content="{meta_desc}">
<link rel="canonical" href="{canonical}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,600;1,700&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
{PAGE_CSS}
  /* Slug page specific */
  .slug-breadcrumb {{ font-family: 'DM Mono', monospace; font-size: 9px; letter-spacing: 0.12em; text-transform: uppercase; color: var(--ink-light); padding: 14px 0; }}
  .slug-breadcrumb a {{ color: var(--ink-light); text-decoration: none; }}
  .slug-breadcrumb a:hover {{ color: var(--brand); }}
  .slug-back {{ display: inline-block; font-family: 'DM Mono', monospace; font-size: 9px; letter-spacing: 0.12em; text-transform: uppercase; color: var(--ink-light); text-decoration: none; margin-bottom: 20px; }}
  .slug-back:hover {{ color: var(--brand); }}
  .slug-body {{ max-width: 1140px; margin: 0 auto; padding: 32px 40px 80px; }}
  .slug-content {{ display: grid; grid-template-columns: 1fr 280px; gap: 0; background: #fff; border: 1px solid var(--rule); }}
  .slug-main {{ padding: 32px; border-right: 1px solid var(--rule); }}
  .slug-aside {{ padding: 24px; background: #fafaf8; }}
  @media (max-width: 900px) {{
    .slug-content {{ grid-template-columns: 1fr; }}
    .slug-aside {{ border-top: 1px solid var(--rule); }}
    .slug-body {{ padding: 24px 16px 60px; }}
  }}
</style>
{SCRIPT_TAG}
</head>
<body>

{NAV_HTML}

<!-- PAGE HEADER -->
<header class="page-header" style="padding:32px 40px 28px;">
  <div class="page-header-inner" style="align-items:flex-start;">
    <div>
      <div class="page-eyebrow">\U0001f1e8\U0001f1e6 Canadian Spotlight \u00b7 Issue #{issue_num} \u00b7 {issue_date}</div>
      <h1 style="font-size:clamp(22px,3vw,36px);">{company}</h1>
      <p class="page-header-desc" style="margin-top:8px;">{headline}</p>
    </div>
  </div>
</header>

<main class="slug-body">

  <!-- Breadcrumb -->
  <nav class="slug-breadcrumb" aria-label="Breadcrumb">
    <a href="/spotlight/">Canadian Spotlight</a> &rsaquo; {company}
  </nav>

  <a href="/spotlight/" class="slug-back">\u2190 All stories</a>

  <div class="slug-content">
    <div class="slug-main">
      <div class="drawer-eyebrow" style="margin-bottom:14px;">
        <span class="drawer-sector-dot" style="{sector_dot_style}"></span>
        <span class="drawer-sector-label" style="color:var(--ink-mid);">{sector_label}</span>
        <span style="font-family:\'DM Mono\',monospace;font-size:7px;color:var(--ink-light);letter-spacing:0.1em;">{date_str}</span>
      </div>
      <h2 class="drawer-content" style="font-family:\'Cormorant Garamond\',serif;font-size:26px;font-weight:600;font-style:italic;color:var(--ink);line-height:1.3;margin-bottom:18px;padding:0;">{headline}</h2>
      <div class="drawer-body">
        {body_html}
      </div>
      <div class="drawer-actions" style="padding-top:18px;border-top:1px solid var(--rule);margin-top:20px;display:flex;gap:12px;flex-wrap:wrap;align-items:center;">
        {orig_link}
        {related_block}
        <div class="drawer-share" style="margin-left:auto;">
          <span class="drawer-share-label">Share</span>
          <a href="https://www.linkedin.com/sharing/share-offsite/?url={canonical}" target="_blank" rel="noopener">LinkedIn</a>
          <a href="https://twitter.com/intent/tweet?url={canonical}" target="_blank" rel="noopener">X</a>
        </div>
      </div>
    </div>
    <div class="slug-aside">
      {aside_html}
      <div style="margin-top:16px;padding-top:12px;border-top:1px solid var(--rule);">
        <a href="/spotlight/" style="font-family:\'DM Mono\',monospace;font-size:8px;letter-spacing:0.12em;text-transform:uppercase;color:var(--brand);text-decoration:none;">\u2190 Back to all stories</a>
      </div>
    </div>
  </div>

</main>

{FOOTER_HTML}

</body>
</html>'''
    return page

SLUG_BASE = '/Users/nikkoyetman/Documents/canadiantradeintel/spotlight'

generated = []
for tile_id, slug in SLUGS.items():
    data = extract_tile_data(modified_html, tile_id)
    page_html = generate_slug_page(tile_id, slug, data)

    slug_dir = os.path.join(SLUG_BASE, slug)
    os.makedirs(slug_dir, exist_ok=True)
    slug_file = os.path.join(slug_dir, 'index.html')
    with open(slug_file, 'w', encoding='utf-8') as f:
        f.write(page_html)
    generated.append(slug)
    print(f"Generated: {slug_file}")

print(f"\nTotal slug pages generated: {len(generated)}")
print("All improvements complete.")
