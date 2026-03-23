"""
add_import_cards.py — Insert Import Supply Chain context cards into dashboard/index.html.
One card per sector, inserted after the Government Programmes grid.
"""

import re

PATH = "dashboard/index.html"

def import_card(sector_color, content_rows, risk_level, risk_color):
    rows_html = "\n        ".join(
        f'<div class="context-row"><div class="context-label">{label}</div><div class="context-value">{val}</div></div>'
        for label, val in content_rows
    )
    risk_badge = f'<span style="background:{risk_color};color:#fff;font-family:var(--mono);font-size:8px;letter-spacing:0.1em;text-transform:uppercase;padding:2px 8px;margin-left:6px;">{risk_level}</span>'
    return f'''    <div class="context-grid" style="margin-top:18px;">
      <div class="context-card" style="border-top-color:{sector_color};grid-column:1/-1;">
        <h4>↔ Import Supply Chain{risk_badge}</h4>
        {rows_html}
      </div>
    </div>'''


CARDS = {
    "CanExport SME — Critical Minerals Stream</div></div>\n        </div>\n      </div>\n    </div>": import_card(
        "#1a6b42",
        [
            ("What CA imports", "Canadian manufacturers import processed battery materials (lithium hydroxide, cobalt sulphate), rare earth compounds, and semiconductor-grade metals — primarily for EV, battery, and electronics production."),
            ("Top source countries", "China (dominant — ~80% of processed critical minerals globally), South Korea (battery cells), Japan (specialty alloys and rare earths)."),
            ("Current risk", "China export restrictions on gallium, germanium, and graphite (2023–2024) directly affect Canadian downstream manufacturers. China controls ~60% of global rare earth processing — a structural dependency with no near-term domestic substitute."),
        ],
        "ELEVATED", "#b83030"
    ),
    "TCS Clean Energy Sector Desks</div></div>\n        </div>\n      </div>\n    </div>": import_card(
        "#c8640a",
        [
            ("What CA imports", "Canadian businesses import solar panels (residential and utility-scale), wind turbine components, EV batteries and cells, and power electronics for grid infrastructure."),
            ("Top source countries", "China (80%+ of solar panels globally), Denmark and Germany (wind components), China and South Korea (EV batteries)."),
            ("Current risk", "US tariffs on Chinese clean energy goods create supply chain rerouting pressure — some Chinese product flows to Canada via third countries, raising quality and origin verification concerns. IRA incentives may redirect Canadian-bound clean energy equipment to US market."),
        ],
        "MODERATE–HIGH", "#c8640a"
    ),
    "CME Export Growth Program</div></div>\n        </div>\n      </div>\n    </div>": import_card(
        "#2a5090",
        [
            ("What CA imports", "Canadian manufacturers import steel (structural and specialty grades), aluminum ingot and sheet, precision machined components, and industrial electronics for production lines."),
            ("Top source countries", "United States (largest — steel and aluminum), South Korea and China (steel), Germany and Japan (precision components, machinery), Taiwan (semiconductors for embedded systems)."),
            ("Current risk", "US Section 232 tariffs create steel and aluminum pricing volatility for Canadian manufacturers sourcing cross-border. Taiwan semiconductor supply concentration is a watch-level risk for manufacturers with embedded electronics in their products."),
        ],
        "MODERATE", "#e07b20"
    ),
    "DND MINDS Programme</div></div>\n        </div>\n      </div>\n    </div>": import_card(
        "#6a20b0",
        [
            ("What CA imports", "Canadian aerospace primes and Tier-1 suppliers import specialized titanium and nickel alloys, avionics systems, engine components (CFM, Pratt &amp; Whitney modules), and composite materials."),
            ("Top source countries", "United States (largest — avionics, engines, materials), United Kingdom (aerostructures, systems), France (engines, Airbus supply chain components)."),
            ("Current risk", "ITAR restrictions affect access to US-sourced components — Canadian companies must maintain proper DSP-5 authorizations. NATO supply chain prioritization for defence production may affect Canadian commercial aerospace importers competing for the same components."),
        ],
        "WATCH", "#8860c0"
    ),
    "footnote\">Sources: Agriculture": import_card(
        "#b07800",
        [
            ("What CA imports", "Canadian food processors import fruit and vegetables (year-round supply from US and Mexico), seafood (Chile, Norway, Ecuador), specialty ingredients, food processing equipment, and packaging materials."),
            ("Top source countries", "United States and Mexico (fresh produce under CUSMA), Chile and Norway (salmon, seafood), Germany and Italy (food processing equipment), China (packaging and food service equipment)."),
            ("Current risk", "CUSMA rules of origin and phytosanitary requirements affect cross-border food supply chains. Climate events in California, Mexico, and South America create price and availability volatility for Canadian processors dependent on consistent ingredient supply."),
        ],
        "MODERATE", "#b07800"
    ),
    "TCS Technology Sector Desks</div></div>\n        </div>\n      </div>\n    </div>": import_card(
        "#0a6080",
        [
            ("What CA imports", "Canadian tech companies import semiconductors (logic chips, memory, FPGAs), server hardware and networking equipment, and cloud infrastructure (AWS, Azure, GCP — all US-headquartered)."),
            ("Top source countries", "Taiwan (critical — TSMC produces ~90% of advanced logic chips globally), United States (hyperscaler cloud, hardware OEMs), China (legacy semiconductors, IT hardware)."),
            ("Current risk", "Taiwan Strait geopolitical tension is the single highest supply chain risk for the Canadian tech sector. US export controls on advanced AI chips (H100, A100) affect Canadian AI companies seeking compute access. Cloud infrastructure concentration in US providers creates regulatory and resilience dependencies."),
        ],
        "ELEVATED", "#b83030"
    ),
}

with open(PATH, encoding="utf-8") as f:
    content = f.read()

original = content
for anchor, card_html in CARDS.items():
    if anchor.startswith("footnote"):
        # Special case: insert before the footnote div
        target = '  <div class="footnote">Sources: Agriculture'
        if card_html not in content and target in content:
            content = content.replace(target, card_html + "\n" + target, 1)
            print(f"  ✅ agri_food: import card inserted before footnote")
    else:
        # anchor ends with the last prog-item closing, insert the card right after
        suffix = "\n      </div>\n    </div>"
        full_anchor = anchor + suffix
        if full_anchor in content and card_html not in content:
            content = content.replace(full_anchor, anchor + suffix + "\n" + card_html, 1)
            sector = "unknown"
            if "Critical Minerals" in anchor: sector = "critical_minerals"
            elif "Clean Energy" in anchor: sector = "energy_cleantech"
            elif "CME Export" in anchor: sector = "advanced_manufacturing"
            elif "MINDS" in anchor: sector = "aerospace_defence"
            elif "TCS Technology" in anchor: sector = "technology_digital"
            print(f"  ✅ {sector}: import card inserted")
        else:
            if card_html in content:
                print(f"  ℹ️  card already present — skipping")
            else:
                print(f"  ⚠️  anchor not matched — manual insertion needed")
                print(f"     anchor: {anchor[:80]}")

if content != original:
    with open(PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print("\nFile updated.")
else:
    print("\nNo changes made.")
