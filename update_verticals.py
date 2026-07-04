"""
Add /contractor-leads/ hub link to all 5 vertical lead pages.
- Inserts highlighted hub card into "More Home Service Verticals" section
- Inserts highlighted hub link into footer "Explore All Verticals" section
"""

files = [
    r'C:\Users\19522\Documents\ranklocal-deploy-push\roofing-leads\index.html',
    r'C:\Users\19522\Documents\ranklocal-deploy-push\fence-leads\index.html',
    r'C:\Users\19522\Documents\ranklocal-deploy-push\landscaping-leads\index.html',
    r'C:\Users\19522\Documents\ranklocal-deploy-push\pest-control-leads\index.html',
    r'C:\Users\19522\Documents\ranklocal-deploy-push\garage-door-repair-leads\index.html',
]

# Highlighted hub card for "More Home Service Verticals" grid
hub_card = '<a href="/contractor-leads/" style="display:block;padding:.55rem .9rem;background:rgba(0,170,255,0.15);border:1px solid rgba(0,170,255,0.35);border-radius:8px;color:#00AAFF;text-decoration:none;font-size:.88rem;font-weight:600;transition:background .2s">← All Contractor Leads</a>\n'

# Highlighted hub link for footer "Explore All Verticals"
hub_footer = '<a href="/contractor-leads/" style="color:#00AAFF;text-decoration:none;font-size:.88rem;font-weight:600">All Contractor Leads</a>\n'

# Unique markers
# The "More Home Service Verticals" grid uses minmax(190px,...) gap:.6rem
section_marker = 'gap:.6rem">\n'
# The footer "Explore All Verticals" heading
footer_marker = 'text-transform:uppercase">Explore All Verticals</strong>\n'

updated = 0
for path in files:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Add hub card to More Home Service Verticals section (only if not already there)
    if section_marker in content and '/contractor-leads/' not in content.split(section_marker)[1][:200]:
        content = content.replace(section_marker, section_marker + hub_card, 1)

    # Add hub link to footer Explore All Verticals (only if not already there)
    if footer_marker in content and hub_footer not in content:
        content = content.replace(footer_marker, footer_marker + hub_footer, 1)

    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        updated += 1
        print(f"Updated: {path}")
    else:
        print(f"No changes: {path}")

print(f"\nTotal updated: {updated}/5")
