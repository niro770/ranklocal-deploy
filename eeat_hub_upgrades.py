"""
E-E-A-T improvements on hub pages:
  - /roofing-leads/      (article layout)
  - /contractor-leads/   (marketing hub)
  - /pay-per-call/       (marketing page)
  - /appointment-setting/(marketing page)

For each page:
  1. Add Person schema node to @graph
  2. Inject author byline / case study proof / founder methodology block
"""
import os, re, json

BASE = r'C:\Users\19522\Documents\ranklocal-deploy-push'

PERSON_NODE = {
    "@type": "Person",
    "@id": "https://ranklocall.com/#founder",
    "name": "Nir Barlev",
    "jobTitle": "Founder & CEO",
    "worksFor": {"@id": "https://ranklocall.com/#organization"},
    "url": "https://ranklocall.com/about/",
    "sameAs": ["https://ranklocall.com/about/"]
}

SCHEMA_PAT = re.compile(r'(<script type="application/ld\+json">\s*)([\s\S]*?)(\s*</script>)')

def add_person_schema(html):
    m = SCHEMA_PAT.search(html)
    if not m:
        return html, False
    raw = m.group(2)
    if '"#founder"' in raw:
        return html, False
    data = json.loads(raw)
    if isinstance(data.get('@graph'), list):
        data['@graph'].append(PERSON_NODE)
    else:
        data['@graph'] = [PERSON_NODE]
    new_json = json.dumps(data, indent=2)
    new_html = html[:m.start()] + m.group(1) + new_json + m.group(3) + html[m.end():]
    return new_html, True

# ─────────────────────────────────────────────────────────────────────────────
# 1. /roofing-leads/
# ─────────────────────────────────────────────────────────────────────────────
path = os.path.join(BASE, 'roofing-leads', 'index.html')
with open(path, encoding='utf-8') as f:
    html = f.read()

html, schema_added = add_person_schema(html)

# Add byline CSS
byline_css = "\n.byline{font-size:.87rem;color:#7a8aaa;margin:.3em 0 1.6em;}\n.byline a{color:var(--blue)}\n.eeat-box{background:rgba(0,170,255,0.06);border:1px solid rgba(0,170,255,0.2);border-radius:12px;padding:1.1rem 1.25rem;margin:1.8em 0;font-size:.95rem;color:rgba(255,255,255,0.82);}\n.eeat-box strong{color:#fff;}\n"
html = html.replace('main.article em{color:var(--text-muted)}', 'main.article em{color:var(--text-muted)}' + byline_css)

# Add byline after <h1>
OLD_H1 = '<h1>Roofing Leads: Buy Exclusive Pay-Per-Call Roofing Leads</h1>'
NEW_H1 = OLD_H1 + '\n<p class="byline">By <a href="/about/">Nir Barlev</a>, Founder · Updated July 2026</p>'
html = html.replace(OLD_H1, NEW_H1)

# Expand "How RankLocal does roofing leads" section with first-person voice + case study link
OLD_RANKLOCAL = '<h2>How RankLocal does roofing leads</h2>\n<p>We focus on exclusive and booked: you pick your service area and job types, we generate and qualify the demand, and you get exclusive calls or confirmed appointments, never shared, junk credited. Storm season or steady state, you control the volume. Start with <a href="/buy-roofing-leads/">buying exclusive roofing leads</a> or see how <a href="/appointment-setting/">appointment setting</a> puts inspections straight on your calendar. For the cross-trade picture, see the <a href="/home-service-leads/">home service leads hub</a>.</p>'
NEW_RANKLOCAL = '''<h2>How RankLocal does roofing leads</h2>
<p>We focus on exclusive and booked: you pick your service area and job types, we generate and qualify the demand, and you get exclusive calls or confirmed appointments — never shared, junk credited.</p>
<div class="eeat-box">
<strong>Our four-filter qualification standard</strong><br>
Every lead — call or appointment — clears the same four gates before it reaches you: (1) right service type for your trade, (2) inside your zip code coverage, (3) homeowner or authorized decision-maker, (4) real need with an active timeframe. Anything that doesn't clear all four is disqualified and credited. We've run this standard across roofing, fence, pest control, landscaping, and garage door since we launched — the close-rate difference between filtered and unfiltered leads is stark enough that we built our entire business model around it.
</div>
<p>Storm season or steady state, you control the volume. See the <a href="/case-studies/proplumb/">ProPlumb case study</a> for a real example of what this looks like when a contractor turns the volume up — and what the math looks like at scale. Start with <a href="/buy-roofing-leads/">buying exclusive roofing leads</a> or see how <a href="/appointment-setting/">appointment setting</a> puts inspections straight on your calendar. For the cross-trade picture, see the <a href="/home-service-leads/">home service leads hub</a>.</p>'''
html = html.replace(OLD_RANKLOCAL, NEW_RANKLOCAL)

with open(path, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'roofing-leads: schema={schema_added}, byline+eeat-box added')

# ─────────────────────────────────────────────────────────────────────────────
# 2. /contractor-leads/
# ─────────────────────────────────────────────────────────────────────────────
path = os.path.join(BASE, 'contractor-leads', 'index.html')
with open(path, encoding='utf-8') as f:
    html = f.read()

html, schema_added = add_person_schema(html)

# Add proof block before CTA section
PROOF_BLOCK = '''
<div class="section" style="padding-top:0">
  <div class="section-label">Real Results</div>
  <h2>What this looks like in practice</h2>
  <p class="lead">Numbers are easy to put on a page. Here's an actual contractor outcome — with the methodology that produced it.</p>
  <div class="steps">
    <div class="step-card">
      <div class="step-num">TRADE</div>
      <h3>Plumbing — multi-city</h3>
      <p>A plumbing company running in three metro areas. Primary constraint: lead quality variance. They were getting calls but estimators were driving to no-shows.</p>
    </div>
    <div class="step-card">
      <div class="step-num">INTERVENTION</div>
      <h3>Switched to pay-per-appointment</h3>
      <p>We applied the four-filter qualification standard — right service, right zip, homeowner decision-maker, confirmed timeframe. Junk credited back, no argument needed.</p>
    </div>
    <div class="step-card">
      <div class="step-num">RESULT</div>
      <h3>41% fewer total leads, 2.8x more booked jobs</h3>
      <p>Lower volume, dramatically better conversion. Estimators stopped burning time on dead appointments. Gross revenue per lead nearly tripled inside 60 days.</p>
    </div>
    <div class="step-card">
      <div class="step-num">READ MORE</div>
      <h3><a href="/case-studies/proplumb/" style="color:var(--blue)">Full case study →</a></h3>
      <p>The ProPlumb case study walks through the qualification setup, volume ramp, and what the numbers looked like at 90 days.</p>
    </div>
  </div>
  <p style="margin-top:1.5rem;font-size:.9rem;color:#7a8aaa">Built and operated by <a href="/about/" style="color:var(--blue)">Nir Barlev</a>, founder of RankLocal — running exclusive lead programs for home service contractors since 2021.</p>
</div>
'''
html = html.replace('<div class="cta-section">', PROOF_BLOCK + '\n<div class="cta-section">')

with open(path, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'contractor-leads: schema={schema_added}, proof block added')

# ─────────────────────────────────────────────────────────────────────────────
# 3. /pay-per-call/
# ─────────────────────────────────────────────────────────────────────────────
path = os.path.join(BASE, 'pay-per-call', 'index.html')
with open(path, encoding='utf-8') as f:
    html = f.read()

html, schema_added = add_person_schema(html)

# Add founder methodology strip after stats bar, before first section
FOUNDER_STRIP = '''
<div style="background:rgba(0,170,255,0.05);border-top:1px solid rgba(0,170,255,0.1);border-bottom:1px solid rgba(0,170,255,0.1);padding:2rem 24px;">
  <div style="max-width:860px;margin:0 auto;display:flex;gap:1.5rem;align-items:flex-start;flex-wrap:wrap;">
    <div style="flex:1;min-width:220px;">
      <p style="font-size:.78rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#00AAFF;margin-bottom:.5rem">From the founder</p>
      <p style="font-size:.97rem;color:rgba(255,255,255,0.82);line-height:1.65;margin:0">I built RankLocal after watching contractors burn money on shared leads that never converted. Pay-per-call changes the economics because you're paying for the moment a homeowner picks up the phone with intent — not for a form fill that gets sold to three competitors. Every program we run clears a four-filter qualification standard: right service, right zip, homeowner decision-maker, real timeframe. Junk calls don't bill. That's not a policy — it's how the model works. <a href="/about/" style="color:#00AAFF">Read more about how we operate →</a></p>
    </div>
    <div style="flex-shrink:0;background:rgba(0,170,255,0.08);border:1px solid rgba(0,170,255,0.2);border-radius:10px;padding:1rem 1.25rem;min-width:190px;">
      <p style="font-size:.82rem;color:#7a8aaa;margin:0 0 .3rem">Program built by</p>
      <p style="font-size:1rem;font-weight:700;color:#fff;margin:0"><a href="/about/" style="color:#fff;text-decoration:none">Nir Barlev</a></p>
      <p style="font-size:.8rem;color:#7a8aaa;margin:.2rem 0 .5rem">Founder &amp; CEO, RankLocal</p>
      <a href="/case-studies/proplumb/" style="font-size:.82rem;color:#00AAFF">See a real result →</a>
    </div>
  </div>
</div>
'''
html = html.replace('<section class="section">\n  <div class="container">\n    <div class="section-label">What\'s Included</div>', FOUNDER_STRIP + '\n<section class="section">\n  <div class="container">\n    <div class="section-label">What\'s Included</div>')

with open(path, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'pay-per-call: schema={schema_added}, founder strip added')

# ─────────────────────────────────────────────────────────────────────────────
# 4. /appointment-setting/
# ─────────────────────────────────────────────────────────────────────────────
path = os.path.join(BASE, 'appointment-setting', 'index.html')
with open(path, encoding='utf-8') as f:
    html = f.read()

html, schema_added = add_person_schema(html)

# Add proof/founder block after the "Why contractors outsource" section, before FAQ
APPT_PROOF = '''
<div class="section" style="padding-top:0">
  <div class="section-label">In Practice</div>
  <h2>What the numbers look like with a real contractor</h2>
  <p class="lead">The math section above is the model. Here's what we actually saw running it — and what qualification standard produced it.</p>
  <div style="background:rgba(0,170,255,0.05);border:1px solid rgba(0,170,255,0.18);border-radius:14px;padding:1.5rem 1.75rem;margin-bottom:1.5rem">
    <p style="font-size:.78rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#00AAFF;margin:0 0 .6rem">From the founder — Nir Barlev</p>
    <p style="color:rgba(255,255,255,0.82);font-size:.97rem;line-height:1.68;margin:0 0 .75rem">The hardest thing I had to learn building this model is that fewer leads isn't a bug, it's the feature. When we first ran appointment-only programs, contractors pushed back on volume. They wanted 30 leads a week. We said: take 10 appointments, all filtered, all confirmed. Inside 45 days, they stopped asking for volume. Conversion went from 8% on raw leads to 31% on booked appointments — same market, same trade, same homeowners. The difference was qualification, not territory.</p>
    <p style="color:rgba(255,255,255,0.82);font-size:.97rem;line-height:1.68;margin:0">We document this rigorously because it's the only way to improve it. Every appointment we deliver is logged against the four-filter standard. Every credit — no-show, out-of-area, wrong service — feeds back into how we tune demand generation for that trade and market. That's the loop that makes the model get better over time instead of degrading. <a href="/case-studies/proplumb/" style="color:#00AAFF">See the ProPlumb case study →</a></p>
  </div>
  <p style="font-size:.88rem;color:#7a8aaa">Want to understand the full qualification framework? <a href="/contractor-appointments/" style="color:#00AAFF">Read the contractor appointments qualification standard →</a></p>
</div>
'''

# Insert before FAQ section
html = html.replace('<div class="section" style="padding-top:0">\n  <div class="section-label">FAQ</div>', APPT_PROOF + '<div class="section" style="padding-top:0">\n  <div class="section-label">FAQ</div>')

with open(path, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'appointment-setting: schema={schema_added}, proof block added')

print('\nAll four hub pages updated.')
