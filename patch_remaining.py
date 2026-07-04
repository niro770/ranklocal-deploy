#!/usr/bin/env python3
"""Patch the 5 remaining pages that were skipped due to different HTML structure."""
import os

BASE = os.path.dirname(os.path.abspath(__file__))

LINK_STYLE = 'style="display:block;padding:.55rem .9rem;background:rgba(0,170,255,0.07);border:1px solid rgba(0,170,255,0.18);border-radius:8px;color:#aac4e0;text-decoration:none;font-size:.88rem;transition:background .2s"'

def make_section(heading, links):
    items = "\n".join(f'<a href="{h}" {LINK_STYLE}>{l}</a>' for h, l in links)
    return (
        f'\n<section style="margin:2.5rem 0 1rem">\n'
        f'<h2 style="font-size:1.1rem;color:#fff;margin:0 0 1rem">{heading}</h2>\n'
        f'<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:.6rem">\n'
        f'{items}\n</div>\n</section>\n'
    )

def patch(path, marker, heading, links):
    with open(path, encoding="utf-8") as f:
        html = f.read()
    first_href = links[0][0]
    if first_href in html:
        print(f"  SKIP (already done): {path}")
        return
    if marker not in html:
        print(f"  SKIP (no marker '{marker[:40]}...'): {path}")
        return
    section = make_section(heading, links)
    html = html.replace(marker, section + marker, 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  Updated: {path}")

# ── Blog pages — use same marker as gen_pages output ─────────────────────────
BLOG_MARKER = '<section style="margin:3rem 0 1rem">\n<h2 style="font-size:1.15rem;color:#fff;margin:0 0 1rem">More Home Service Verticals</h2>'

patch(
    os.path.join(BASE, "blog", "how-to-grow-a-roofing-business", "index.html"),
    BLOG_MARKER,
    "Roofing Growth Resources",
    [
        ("/how-to-scale-a-roofing-company/", "How to Scale a Roofing Company"),
        ("/how-to-close-more-roofing-estimates/", "How to Close More Estimates"),
        ("/lead-follow-up-sequence-for-contractors/", "Lead Follow-Up Sequence"),
        ("/speed-to-lead-for-contractors/", "Speed-to-Lead for Contractors"),
    ]
)

patch(
    os.path.join(BASE, "blog", "how-to-get-roofing-customers", "index.html"),
    BLOG_MARKER,
    "Roofing Sales & Lead Resources",
    [
        ("/speed-to-lead-for-contractors/", "Speed-to-Lead for Contractors"),
        ("/how-to-close-more-roofing-estimates/", "How to Close More Roofing Estimates"),
        ("/lead-follow-up-sequence-for-contractors/", "Lead Follow-Up Sequence"),
        ("/roofing-leads-texas/", "Roofing Leads — Texas"),
        ("/roofing-leads-florida/", "Roofing Leads — Florida"),
    ]
)

# ── contractor-leads and appointment-setting — use cta-section marker ─────────
CTA_MARKER = '<div class="cta-section">'

patch(
    os.path.join(BASE, "contractor-leads", "index.html"),
    CTA_MARKER,
    "Contractor Lead Generation Resources",
    [
        ("/contractor-lead-generation-guide/", "Full Lead Generation Guide"),
        ("/contractor-marketing-metrics-guide/", "7 Metrics Every Contractor Must Track"),
        ("/what-is-exclusive-lead-generation/", "What Is Exclusive Lead Generation?"),
        ("/what-is-cost-per-lead/", "What Is Cost Per Lead?"),
        ("/contractor-lead-generation-glossary/", "Lead Generation Glossary"),
        ("/how-to-scale-a-roofing-company/", "How to Scale a Roofing Company"),
    ]
)

patch(
    os.path.join(BASE, "appointment-setting", "index.html"),
    CTA_MARKER,
    "Appointment Setting Resources",
    [
        ("/appointment-setting-cost/", "How Much Does Appointment Setting Cost?"),
        ("/ai-appointment-setting-for-contractors/", "AI Appointment Setting"),
        ("/speed-to-lead-for-contractors/", "Speed-to-Lead for Contractors"),
        ("/lead-follow-up-sequence-for-contractors/", "Lead Follow-Up Sequence"),
        ("/how-to-close-more-roofing-estimates/", "How to Close More Estimates"),
    ]
)

# ── pay-per-call — use container+cta-section marker ──────────────────────────
PPC_MARKER = '<div class="container">\n  <div class="cta-section">'

patch(
    os.path.join(BASE, "pay-per-call", "index.html"),
    PPC_MARKER,
    "Pay-Per-Call vs Other Lead Models",
    [
        ("/google-lsa-vs-pay-per-call/", "Google LSA vs Pay-Per-Call"),
        ("/google-local-services-ads-for-contractors/", "Google LSA for Contractors"),
        ("/what-is-cost-per-lead/", "What Is Cost Per Lead?"),
        ("/what-is-exclusive-lead-generation/", "What Is Exclusive Lead Generation?"),
        ("/contractor-marketing-metrics-guide/", "7 Metrics Every Contractor Must Track"),
    ]
)

print("\nPatch complete.")
