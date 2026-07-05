"""
E-E-A-T improvements for /home-service-leads/ (article layout).
Adds: byline, Person schema, first-person founder voice in How RankLocal works,
      case study reference.
"""
import re, json

path = r'C:\Users\19522\Documents\ranklocal-deploy-push\home-service-leads\index.html'
with open(path, encoding='utf-8') as f:
    html = f.read()

# ── 1. Person schema node ───────────────────────────────────────────────────
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
m = SCHEMA_PAT.search(html)
data = json.loads(m.group(2))
if '"#founder"' not in m.group(2):
    data['@graph'].append(PERSON_NODE)
new_json = json.dumps(data, indent=2)
html = html[:m.start()] + m.group(1) + new_json + m.group(3) + html[m.end():]
print('Person schema added')

# ── 2. Byline CSS ──────────────────────────────────────────────────────────
html = html.replace(
    'main.article em{color:var(--text-muted)}',
    'main.article em{color:var(--text-muted)}\n.byline{font-size:.87rem;color:#7a8aaa;margin:.3em 0 1.6em;}\n.byline a{color:var(--blue)}'
)
print('byline CSS added')

# ── 3. Byline after H1 ─────────────────────────────────────────────────────
OLD_H1 = '<h1>Home Service &amp; Contractor Leads: Calls, Appointments, and How to Buy Them Right</h1>'
NEW_H1 = (OLD_H1 +
    '\n<p class="byline">By <a href="/about/">Nir Barlev</a>, Founder &amp; CEO · Updated July 2026</p>')
assert OLD_H1 in html, 'H1 not found!'
html = html.replace(OLD_H1, NEW_H1)
print('byline paragraph added')

# ── 4. Expand "How RankLocal works" with first-person + case study ─────────
OLD_HOW = """<h2>How RankLocal works</h2>
<p>We run the traffic, search, Local Services Ads, local SEO, for your trade and your area, then deliver the results as <strong>exclusive calls or booked appointments</strong>, never shared. You get call recordings, a dashboard, junk credited, and control over your zips, services, and budget. Calls when your phone is a strength; appointments when it's a bottleneck. You set the volume and scale it with your season.</p>
<p>Start with your trade, <a href="/roofing-leads/">roofing</a>, <a href="/pest-control-leads/">pest control</a>, or <a href="/appointment-setting/">appointment setting</a>, or learn the model in <a href="/pay-per-call-leads/">pay-per-call lead generation</a>.</p>"""

NEW_HOW = """<h2>How RankLocal works</h2>
<p>I built RankLocal because I kept watching contractors spend money on lead sources that didn't work — shared databases, aggregator resells, volume promises that quietly used form fills as the volume metric. The model I built runs its own traffic (search, Local Services Ads, local SEO) for your specific trade and area, and delivers only what cleared the four-filter standard: right service, right zip, homeowner decision-maker, real timeframe. Everything else is disqualified before it reaches you.</p>
<p>You get <strong>exclusive calls or booked appointments</strong>, never shared, with call recordings, a dashboard, junk credited, and control over your zips, services, and budget. Calls when your phone is a strength; appointments when it's a bottleneck. Volume is yours to set and scale with your season.</p>
<p>The <a href="/case-studies/proplumb/">ProPlumb case study</a> walks through what this actually looks like when a contractor turns it on — the qualification setup, the volume ramp, and the numbers at 90 days. Start with your trade — <a href="/roofing-leads/">roofing</a>, <a href="/pest-control-leads/">pest control</a>, or <a href="/appointment-setting/">appointment setting</a> — or learn the full model in <a href="/pay-per-call-leads/">pay-per-call lead generation</a>. — <em><a href="/about/">Nir Barlev, Founder</a></em></p>"""

assert OLD_HOW in html, 'How RankLocal section not found!'
html = html.replace(OLD_HOW, NEW_HOW)
print('How RankLocal section expanded with first-person + case study')

with open(path, 'w', encoding='utf-8') as f:
    f.write(html)
print('\nhome-service-leads: all E-E-A-T improvements applied.')
