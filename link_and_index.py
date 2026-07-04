#!/usr/bin/env python3
"""
Three tasks in one pass:
1. Add 30 new pages to sitemap.xml
2. Update Google Indexing workflow with new URLs
3. Internal linking: inject cluster sections into existing pages
"""

import os, re

BASE = os.path.dirname(os.path.abspath(__file__))

# ── 1. NEW PAGE SLUGS ─────────────────────────────────────────────────────────
NEW_PAGES = [
    "what-is-exclusive-lead-generation",
    "angi-alternatives",
    "ranklocall-vs-angi",
    "ranklocall-vs-homeadvisor",
    "ranklocall-vs-thumbtack",
    "homeadvisor-alternatives",
    "google-local-services-ads-for-contractors",
    "google-lsa-vs-pay-per-call",
    "google-lsa-cost-per-lead-roofing",
    "speed-to-lead-for-contractors",
    "how-to-close-more-roofing-estimates",
    "lead-follow-up-sequence-for-contractors",
    "contractor-lead-generation-guide",
    "roofing-leads-texas",
    "roofing-leads-florida",
    "roofing-leads-georgia",
    "insurance-roofing-leads",
    "tree-service-leads",
    "solar-roofing-leads",
    "irrigation-leads",
    "hardscaping-leads",
    "mosquito-control-leads",
    "bee-removal-leads",
    "roofing-leads-in-winter",
    "what-is-cost-per-lead",
    "contractor-lead-generation-glossary",
    "contractor-marketing-metrics-guide",
    "appointment-setting-cost",
    "how-to-scale-a-roofing-company",
    "ai-appointment-setting-for-contractors",
]

# ── 2. UPDATE SITEMAP ─────────────────────────────────────────────────────────
sitemap_path = os.path.join(BASE, "sitemap.xml")
with open(sitemap_path, encoding="utf-8") as f:
    sitemap = f.read()

new_entries = ""
added = 0
for slug in NEW_PAGES:
    if f"/{slug}/" not in sitemap:
        new_entries += f"""
  <url>
    <loc>https://ranklocall.com/{slug}/</loc>
    <lastmod>2026-07-05</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
"""
        added += 1

if added:
    sitemap = sitemap.replace("</urlset>", new_entries + "\n</urlset>")
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(sitemap)
    print(f"Sitemap updated — {added} new URLs added")
else:
    print("Sitemap already up to date")

# ── 3. UPDATE GOOGLE INDEXING WORKFLOW ───────────────────────────────────────
workflow_path = os.path.join(BASE, ".github", "workflows", "google-indexing.yml")
with open(workflow_path, encoding="utf-8") as f:
    workflow = f.read()

# Build the chunk to append — just the new URL strings to add before "]}')"
new_url_chunk = ""
for slug in NEW_PAGES:
    url = f"https://ranklocall.com/{slug}/"
    if url not in workflow:
        new_url_chunk += f', "{url}"'

if new_url_chunk:
    # Both the IndexNow and Bing calls end with: "https://ranklocall.com/wood-fence-leads/"]}')
    # We replace that anchor in both occurrences
    anchor = '"https://ranklocall.com/wood-fence-leads/"]}\')'
    replacement = f'"https://ranklocall.com/wood-fence-leads/"{new_url_chunk}]}}\')'
    new_workflow = workflow.replace(anchor, replacement)
    if new_workflow == workflow:
        print("WARNING: Could not find anchor in workflow file — check format")
    else:
        with open(workflow_path, "w", encoding="utf-8") as f:
            f.write(new_workflow)
        count = workflow.count(anchor)
        print(f"Workflow updated — {len(NEW_PAGES)} new URLs added to {count} IndexNow call(s)")
else:
    print("Workflow already up to date")

# ── 4. INTERNAL LINKING ───────────────────────────────────────────────────────
LINK_STYLE = 'style="display:block;padding:.55rem .9rem;background:rgba(0,170,255,0.07);border:1px solid rgba(0,170,255,0.18);border-radius:8px;color:#aac4e0;text-decoration:none;font-size:.88rem;transition:background .2s"'

def make_cluster_section(heading, links):
    items = "\n".join(
        f'<a href="{href}" {LINK_STYLE}>{label}</a>'
        for href, label in links
    )
    return (
        f'\n<section style="margin:2.5rem 0 1rem">\n'
        f'<h2 style="font-size:1.1rem;color:#fff;margin:0 0 1rem">{heading}</h2>\n'
        f'<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:.6rem">\n'
        f'{items}\n'
        f'</div>\n'
        f'</section>\n'
    )

# The "More Home Service Verticals" section — we inject our new section just before it
INSERT_BEFORE = '<section style="margin:3rem 0 1rem">\n<h2 style="font-size:1.15rem;color:#fff;margin:0 0 1rem">More Home Service Verticals</h2>'

def inject_section(folder, heading, links):
    page_path = os.path.join(BASE, folder, "index.html")
    if not os.path.exists(page_path):
        print(f"  MISSING: {page_path}")
        return False
    with open(page_path, encoding="utf-8") as f:
        html = f.read()
    if INSERT_BEFORE not in html:
        print(f"  SKIP (no insert point): {folder}/")
        return False
    # Idempotency check — if the first link already in the file, skip
    first_href = links[0][0]
    if first_href in html:
        print(f"  SKIP (already linked): {folder}/")
        return False
    section_html = make_cluster_section(heading, links)
    html = html.replace(INSERT_BEFORE, section_html + INSERT_BEFORE)
    with open(page_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  Updated: {folder}/")
    return True

# ── 5. INJECTION MAP ──────────────────────────────────────────────────────────
INJECTIONS = [
    ("roofing-leads", "Roofing Leads by State & Type", [
        ("/roofing-leads-texas/", "Roofing Leads — Texas"),
        ("/roofing-leads-florida/", "Roofing Leads — Florida"),
        ("/roofing-leads-georgia/", "Roofing Leads — Georgia"),
        ("/insurance-roofing-leads/", "Insurance Roofing Leads"),
        ("/roofing-leads-in-winter/", "Roofing Leads in Winter"),
        ("/how-to-close-more-roofing-estimates/", "How to Close More Roofing Estimates"),
        ("/how-to-scale-a-roofing-company/", "How to Scale a Roofing Company"),
        ("/google-lsa-cost-per-lead-roofing/", "Google LSA Cost Per Lead — Roofing"),
    ]),
    ("contractor-leads", "Contractor Lead Generation Resources", [
        ("/contractor-lead-generation-guide/", "Full Lead Generation Guide"),
        ("/contractor-marketing-metrics-guide/", "7 Metrics Every Contractor Must Track"),
        ("/what-is-exclusive-lead-generation/", "What Is Exclusive Lead Generation?"),
        ("/what-is-cost-per-lead/", "What Is Cost Per Lead?"),
        ("/contractor-lead-generation-glossary/", "Lead Generation Glossary"),
        ("/how-to-scale-a-roofing-company/", "How to Scale a Roofing Company"),
    ]),
    ("appointment-setting", "Appointment Setting Resources", [
        ("/appointment-setting-cost/", "How Much Does Appointment Setting Cost?"),
        ("/ai-appointment-setting-for-contractors/", "AI Appointment Setting"),
        ("/speed-to-lead-for-contractors/", "Speed-to-Lead for Contractors"),
        ("/lead-follow-up-sequence-for-contractors/", "Lead Follow-Up Sequence"),
        ("/how-to-close-more-roofing-estimates/", "How to Close More Estimates"),
    ]),
    ("pay-per-call", "Pay-Per-Call vs Other Lead Models", [
        ("/google-lsa-vs-pay-per-call/", "Google LSA vs Pay-Per-Call"),
        ("/google-local-services-ads-for-contractors/", "Google LSA for Contractors"),
        ("/what-is-cost-per-lead/", "What Is Cost Per Lead?"),
        ("/what-is-exclusive-lead-generation/", "What Is Exclusive Lead Generation?"),
        ("/contractor-marketing-metrics-guide/", "7 Metrics Every Contractor Must Track"),
    ]),
    ("pay-per-call-leads", "Related Lead Generation Topics", [
        ("/google-lsa-vs-pay-per-call/", "Google LSA vs Pay-Per-Call"),
        ("/google-local-services-ads-for-contractors/", "Google LSA for Contractors"),
        ("/what-is-cost-per-lead/", "What Is Cost Per Lead?"),
        ("/contractor-lead-generation-guide/", "Contractor Lead Gen Guide"),
    ]),
    ("home-service-leads", "Lead Generation Guides", [
        ("/contractor-lead-generation-guide/", "Contractor Lead Generation Guide"),
        ("/what-is-exclusive-lead-generation/", "What Is Exclusive Lead Generation?"),
        ("/contractor-marketing-metrics-guide/", "7 Metrics Every Contractor Must Track"),
        ("/what-is-cost-per-lead/", "What Is Cost Per Lead?"),
    ]),
    ("pest-control-leads", "Pest Control Sub-Vertical Leads", [
        ("/mosquito-control-leads/", "Mosquito Control Leads"),
        ("/bee-removal-leads/", "Bee Removal Leads"),
    ]),
    ("best-lead-generation-companies-for-contractors", "Angi & HomeAdvisor Alternatives", [
        ("/angi-alternatives/", "Best Angi Alternatives"),
        ("/homeadvisor-alternatives/", "Best HomeAdvisor Alternatives"),
        ("/ranklocall-vs-angi/", "RankLocal vs Angi"),
        ("/ranklocall-vs-homeadvisor/", "RankLocal vs HomeAdvisor"),
        ("/ranklocall-vs-thumbtack/", "RankLocal vs Thumbtack"),
    ]),
    ("roofing-lead-generation", "Roofing Lead Generation by State & Type", [
        ("/roofing-leads-texas/", "Roofing Leads — Texas"),
        ("/roofing-leads-florida/", "Roofing Leads — Florida"),
        ("/roofing-leads-georgia/", "Roofing Leads — Georgia"),
        ("/insurance-roofing-leads/", "Insurance Roofing Leads"),
        ("/solar-roofing-leads/", "Solar Roofing Leads"),
    ]),
    ("roofing-cost-per-lead-benchmarks", "Related Cost & Metrics Guides", [
        ("/google-lsa-cost-per-lead-roofing/", "Google LSA Cost Per Lead — Roofing"),
        ("/what-is-cost-per-lead/", "What Is Cost Per Lead?"),
        ("/contractor-marketing-metrics-guide/", "7 Metrics Every Contractor Must Track"),
    ]),
    ("buy-roofing-leads", "Marketplace Alternatives", [
        ("/angi-alternatives/", "Best Angi Alternatives"),
        ("/homeadvisor-alternatives/", "Best HomeAdvisor Alternatives"),
        ("/what-is-exclusive-lead-generation/", "What Is Exclusive Lead Generation?"),
    ]),
    ("exclusive-vs-shared-leads", "Learn More About Exclusive Leads", [
        ("/what-is-exclusive-lead-generation/", "What Is Exclusive Lead Generation?"),
        ("/what-is-cost-per-lead/", "What Is Cost Per Lead?"),
        ("/angi-alternatives/", "Best Angi Alternatives for Contractors"),
    ]),
    ("how-to-grow-a-roofing-business", "Roofing Growth Resources", [
        ("/how-to-scale-a-roofing-company/", "How to Scale a Roofing Company"),
        ("/how-to-close-more-roofing-estimates/", "How to Close More Estimates"),
        ("/lead-follow-up-sequence-for-contractors/", "Lead Follow-Up Sequence"),
        ("/speed-to-lead-for-contractors/", "Speed-to-Lead for Contractors"),
    ]),
    ("how-to-get-roofing-customers", "Roofing Sales & Lead Resources", [
        ("/speed-to-lead-for-contractors/", "Speed-to-Lead for Contractors"),
        ("/how-to-close-more-roofing-estimates/", "How to Close More Roofing Estimates"),
        ("/lead-follow-up-sequence-for-contractors/", "Lead Follow-Up Sequence"),
        ("/roofing-leads-texas/", "Roofing Leads — Texas"),
        ("/roofing-leads-florida/", "Roofing Leads — Florida"),
    ]),
    ("lead-generation-for-contractors", "Lead Generation Deep Dives", [
        ("/contractor-lead-generation-guide/", "Full Contractor Lead Generation Guide"),
        ("/google-local-services-ads-for-contractors/", "Google LSA for Contractors"),
        ("/google-lsa-vs-pay-per-call/", "Google LSA vs Pay-Per-Call"),
        ("/what-is-exclusive-lead-generation/", "What Is Exclusive Lead Generation?"),
        ("/appointment-setting-cost/", "How Much Does Appointment Setting Cost?"),
    ]),
    ("roofing-leads-cost", "Related Cost Benchmarks", [
        ("/google-lsa-cost-per-lead-roofing/", "Google LSA Cost Per Lead — Roofing"),
        ("/what-is-cost-per-lead/", "What Is Cost Per Lead?"),
        ("/insurance-roofing-leads/", "Insurance Roofing Leads"),
    ]),
    ("how-to-choose-a-lead-generation-company", "Provider Comparisons", [
        ("/angi-alternatives/", "Best Angi Alternatives"),
        ("/homeadvisor-alternatives/", "Best HomeAdvisor Alternatives"),
        ("/ranklocall-vs-angi/", "RankLocal vs Angi"),
        ("/ranklocall-vs-homeadvisor/", "RankLocal vs HomeAdvisor"),
    ]),
]

# ── 6. RUN INJECTIONS ─────────────────────────────────────────────────────────
print("\nInjecting internal links...")
total_updated = 0
for folder, heading, links in INJECTIONS:
    if inject_section(folder, heading, links):
        total_updated += 1

print(f"\nDone — {total_updated} pages updated with internal links")
print("Next: git add -A && git commit && git push")
