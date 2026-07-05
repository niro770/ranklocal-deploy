import os, json, textwrap

BASE = r'C:\Users\19522\Documents\ranklocal-deploy-push'
DATE = '2026-07-05'
ORG  = 'https://ranklocall.com/#organization'
PERSON = 'https://ranklocall.com/about/#person'

CSS = """*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:'Inter',system-ui,-apple-system,sans-serif;background:#0a0f1e;color:#fff;line-height:1.65}
a{text-decoration:none;color:inherit}
:root{--blue:#00AAFF;--blue2:#0044BB;--bg-1:#0d1a35;--border:rgba(255,255,255,0.07);--border-blue:rgba(0,170,255,0.2);--text-muted:#7a7a9a;--radius:14px}
nav{position:fixed;top:0;left:0;right:0;z-index:100;padding:0 28px;height:68px;display:flex;align-items:center;justify-content:space-between;background:rgba(7,7,10,0.97);border-bottom:1px solid var(--border)}
.nav-logo{display:flex;align-items:center;gap:10px;font-weight:800;font-size:18px}
.logo-icon{width:32px;height:32px;background:linear-gradient(135deg,#00AAFF,#0044BB);border-radius:8px;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:14px}
.logo-text span{color:var(--blue)}
.nav-links{display:flex;gap:28px;list-style:none}
.nav-links a{font-size:14px;font-weight:500;color:rgba(255,255,255,0.7);transition:color .2s}
.nav-links a:hover{color:#fff}
.btn-primary{background:linear-gradient(135deg,#00AAFF,#0044BB);color:#fff;border:none;padding:10px 20px;border-radius:10px;font-weight:700;font-size:14px;cursor:pointer;display:inline-flex;align-items:center;gap:6px}
@media(max-width:640px){.nav-links{display:none}}
main.article{max-width:768px;margin:0 auto;padding:104px 22px 96px}
main.article h1{font-size:2.1rem;line-height:1.18;margin:0 0 .55em;font-weight:800;letter-spacing:-.01em}
main.article h2{font-size:1.42rem;margin:1.9em 0 .55em;font-weight:700;padding-top:1.15em;border-top:1px solid var(--border)}
main.article h3{font-size:1.12rem;margin:1.5em 0 .4em;font-weight:600}
main.article p,main.article li{color:rgba(255,255,255,0.82);font-size:1.02rem}
main.article a{color:var(--blue)}
main.article a:hover{text-decoration:underline}
main.article strong{color:#fff;font-weight:650}
main.article ul,main.article ol{margin:.5em 0 1.1em 1.3em}
main.article li{margin:.32em 0}
main.article table{border-collapse:collapse;width:100%;margin:1.3em 0;font-size:.95rem}
main.article th,main.article td{border:1px solid var(--border);padding:9px 12px;text-align:left}
main.article th{background:rgba(255,255,255,0.05);color:#fff}
main.article hr{border:0;border-top:1px solid var(--border);margin:2.2em 0}
main.article em{color:var(--text-muted)}"""

NAV = """<nav>
  <a href="/" class="nav-logo"><div class="logo-icon">R</div><div class="logo-text">Rank<span>Local</span></div></a>
  <ul class="nav-links">
    <li><a href="/appointment-setting/">Appointment Setting</a></li>
    <li><a href="/pay-per-call/">Pay-Per-Call</a></li>
    <li><a href="/contractor-leads/">Contractor Leads</a></li>
    <li><a href="/blog/">Blog</a></li>
  </ul>
  <a href="/#contact" class="btn-primary">&#128222; Book Free Call</a>
</nav>"""

FOOTER = """<footer style="background:#060c1a;border-top:1px solid rgba(0,170,255,0.12);padding:2.5rem 1.5rem;margin-top:3rem">
<div style="max-width:1100px;margin:0 auto">
<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:.4rem .75rem;margin-bottom:1.75rem">
<strong style="color:#00AAFF;grid-column:1/-1;display:block;margin-bottom:.5rem;font-size:.85rem;letter-spacing:.08em;text-transform:uppercase">Explore All Verticals</strong>
<a href="/contractor-leads/" style="color:#00AAFF;text-decoration:none;font-size:.88rem;font-weight:600">All Contractor Leads</a>
<a href="/roofing-leads/" style="color:#aac4e0;text-decoration:none;font-size:.88rem">Roofing Leads</a>
<a href="/fence-leads/" style="color:#aac4e0;text-decoration:none;font-size:.88rem">Fence Leads</a>
<a href="/pest-control-leads/" style="color:#aac4e0;text-decoration:none;font-size:.88rem">Pest Control Leads</a>
<a href="/landscaping-leads/" style="color:#aac4e0;text-decoration:none;font-size:.88rem">Landscaping Leads</a>
<a href="/hvac-leads/" style="color:#aac4e0;text-decoration:none;font-size:.88rem">HVAC Leads</a>
<a href="/plumbing-leads/" style="color:#aac4e0;text-decoration:none;font-size:.88rem">Plumbing Leads</a>
<a href="/appointment-setting/" style="color:#aac4e0;text-decoration:none;font-size:.88rem">Appointment Setting</a>
<a href="/pay-per-call-leads/" style="color:#aac4e0;text-decoration:none;font-size:.88rem">Pay-Per-Call Leads</a>
<a href="/home-service-leads/" style="color:#aac4e0;text-decoration:none;font-size:.88rem">Home Service Leads</a>
</div>
<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:.4rem .75rem;margin-bottom:1.75rem">
<strong style="color:#00AAFF;grid-column:1/-1;display:block;margin-bottom:.5rem;font-size:.85rem;letter-spacing:.08em;text-transform:uppercase">RankLocal Services</strong>
<a href="/" style="color:#aac4e0;text-decoration:none;font-size:.88rem">Home</a>
<a href="/pay-per-call/" style="color:#aac4e0;text-decoration:none;font-size:.88rem">Pay-Per-Call</a>
<a href="/local-seo/" style="color:#aac4e0;text-decoration:none;font-size:.88rem">Local SEO</a>
<a href="/blog/" style="color:#aac4e0;text-decoration:none;font-size:.88rem">Blog</a>
<a href="/apply/" style="color:#aac4e0;text-decoration:none;font-size:.88rem">Apply</a>
</div>
<p style="color:#556;font-size:.8rem;margin:0">&copy; 2026 RankLocal &middot; Exclusive pay-per-call leads &amp; booked appointments for US home service companies.</p>
</div>
</footer>"""

def cluster_links(links):
    """links = list of (href, label, is_primary)"""
    items = []
    for href, label, primary in links:
        if primary:
            items.append(f'<a href="{href}" style="display:block;padding:.55rem .9rem;background:rgba(0,170,255,0.15);border:1px solid rgba(0,170,255,0.35);border-radius:8px;color:#00AAFF;text-decoration:none;font-size:.88rem;font-weight:600">{label}</a>')
        else:
            items.append(f'<a href="{href}" style="display:block;padding:.55rem .9rem;background:rgba(0,170,255,0.07);border:1px solid rgba(0,170,255,0.18);border-radius:8px;color:#aac4e0;text-decoration:none;font-size:.88rem">{label}</a>')
    grid = '\n'.join(items)
    return f'<section style="margin:3rem 0 1rem">\n<h2 style="font-size:1.15rem;color:#fff;margin:0 0 1rem">More Home Service Verticals</h2>\n<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:.6rem">\n{grid}\n</div>\n</section>'

def make_schema(slug, title, desc, schema_type, svc_name=None, svc_desc=None, area=None, breadcrumb_name=None):
    url = f'https://ranklocall.com/{slug}/'
    bname = breadcrumb_name or title.split('|')[0].strip()
    graph = [
        {'@type':'Organization','@id':ORG,'name':'RankLocal','url':'https://ranklocall.com/'},
        {'@type':'WebPage','@id':f'{url}#webpage','url':url,'name':title,'description':desc,'isPartOf':{'@id':'https://ranklocall.com/#website'}},
        {'@type':'BreadcrumbList','itemListElement':[
            {'@type':'ListItem','position':1,'name':'Home','item':'https://ranklocall.com/'},
            {'@type':'ListItem','position':2,'name':bname,'item':url}
        ]}
    ]
    if schema_type == 'Service' and svc_name:
        area_obj = [{'@type':'State','name':a} for a in area] if isinstance(area,list) else {'@type':'Country','name':area}
        graph.append({'@type':'Service','@id':f'{url}#service','name':svc_name,'description':svc_desc,'provider':{'@id':ORG},'serviceType':'Lead Generation','areaServed':area_obj,'url':url})
    else:
        graph.append({'@type':'Article','@id':f'{url}#article','headline':title,'description':desc,'author':{'@id':PERSON},'publisher':{'@id':ORG},'datePublished':DATE,'dateModified':DATE,'mainEntityOfPage':{'@id':f'{url}#webpage'}})
    return json.dumps({'@context':'https://schema.org','@graph':graph},separators=(',',':'))

def build_page(slug, title, meta_desc, h1, body_html, cluster_html, schema_json):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<base href="/">
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{meta_desc}">
<link rel="canonical" href="https://ranklocall.com/{slug}/">
<meta name="robots" content="index,follow">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{meta_desc}">
<meta property="og:type" content="article">
<meta property="og:url" content="https://ranklocall.com/{slug}/">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<script type="application/ld+json">
{schema_json}</script>
<style>{CSS}</style>
</head>
<body>
{NAV}
<main class="article">
<h1>{h1}</h1>
{body_html}
{cluster_html}
</main>
{FOOTER}
</body>
</html>"""

# ─── PAGE DEFINITIONS ────────────────────────────────────────────────
PAGES = {}

# ── 1. HVAC LEADS ──────────────────────────────────────────────────
PAGES['hvac-leads'] = dict(
    title='HVAC Leads for Contractors | Exclusive Pay-Per-Call | 2026',
    meta='Exclusive HVAC leads for heating and cooling contractors. Pay per call only — no shared leads, no subscriptions. Filter by service type, zip code, and season.',
    h1='HVAC Leads: Exclusive Pay-Per-Call for Heating and Cooling Contractors',
    schema_type='Service',
    svc_name='Exclusive HVAC Leads',
    svc_desc='Exclusive pay-per-call HVAC leads for heating, cooling, and air conditioning contractors nationwide.',
    area='United States',
    body="""<p>HVAC is the most seasonal lead market in home services. Demand collapses when the weather is mild and spikes hard at the extremes — 100-degree July days in Phoenix, single-digit January nights in Chicago. That pattern makes timing and exclusivity the two variables that matter most. A shared HVAC lead in July is worth nothing if five other contractors already spoke to the homeowner. An exclusive call the day the AC fails is worth the job.</p>
<h2>What HVAC leads actually look like</h2>
<p>Most inbound HVAC leads fall into one of four categories: emergency service (AC not working, furnace won't start), scheduled replacement (unit is old and homeowner is ready), maintenance plan signups, and new construction or remodel installs. Emergency calls have the highest close rate and the shortest sales cycle — the homeowner needs help now. Replacement leads have the highest ticket but longer consideration periods. Know which type you're buying before you set a budget.</p>
<h2>HVAC lead cost by call type</h2>
<table>
<tr><th>Call Type</th><th>Cost Per Call</th><th>Typical Close Rate</th></tr>
<tr><td>Emergency AC/heat</td><td>$35–$75</td><td>40–60%</td></tr>
<tr><td>System replacement</td><td>$50–$100</td><td>20–35%</td></tr>
<tr><td>Tune-up / maintenance</td><td>$20–$40</td><td>30–50%</td></tr>
<tr><td>New installation</td><td>$60–$120</td><td>15–25%</td></tr>
</table>
<h2>Seasonality: buying leads year-round vs. surge buying</h2>
<p>Two schools of thought exist on HVAC lead buying. The surge approach: spend heavily in June–August (cooling) and November–February (heating), when homeowners are actively calling. The year-round approach: maintain consistent volume at lower cost during mild months to build a replacement pipeline that converts over 60–90 days. Most successful contractors combine both — a lower baseline year-round, with higher budgets when the phones are already ringing.</p>
<p>Exclusive pay-per-call campaigns let you adjust spend weekly rather than being locked into monthly contracts. See <a href="/appointment-setting/">appointment setting</a> if your technicians are too busy during surge months to handle raw lead volume — pre-booked appointments can be scheduled 48–72 hours out.</p>
<h2>What to filter for when buying HVAC leads</h2>
<p>Service type matters enormously. An HVAC company that specializes in commercial refrigeration does not want residential tune-up calls. A contractor focused on high-efficiency heat pump installs doesn't want window-unit repair calls. Good lead programs let you filter by service type, equipment category, and job size. Insist on that level of control before you commit budget. Vague "HVAC lead" programs with no filters produce a mix of junk you'll spend time sorting.</p>
<hr>
<p><em>Ready for exclusive HVAC calls in your service area? <a href="/#contact">Talk to RankLocal</a>.</em></p>""",
    links=[('/contractor-leads/','← All Contractor Leads',True),('/ac-repair-leads/','AC Repair Leads',False),('/heating-leads/','Heating & Furnace Leads',False),('/home-service-leads/','Home Service Leads',False),('/appointment-setting/','Appointment Setting',False),('/pay-per-call-leads/','Pay-Per-Call Leads',False)]
)

# ── 2. AC REPAIR LEADS ─────────────────────────────────────────────
PAGES['ac-repair-leads'] = dict(
    title='AC Repair Leads | Exclusive Pay-Per-Call for HVAC Contractors | 2026',
    meta='Exclusive AC repair leads — homeowners with non-working air conditioning calling your line only. Pay per call, no shared leads, filter by zip code.',
    h1='AC Repair Leads: Exclusive Calls for HVAC Contractors',
    schema_type='Service',
    svc_name='Exclusive AC Repair Leads',
    svc_desc='Exclusive pay-per-call AC repair and air conditioning service leads for HVAC contractors.',
    area='United States',
    body="""<p>An AC repair call on a 95-degree afternoon has the highest sense of urgency in residential home services. The homeowner isn't comparing prices. They want someone there today. That urgency is also why shared AC leads are almost worthless — if the homeowner called your number because they found you specifically, you're in the conversation. If a platform sold their info to four HVAC companies, the homeowner already picked up the first callback and stopped answering.</p>
<h2>AC repair lead volume by season</h2>
<p>Volume peaks in May–September in the South and Southwest, June–August in the Midwest and Northeast. The first heat wave of the year always generates a spike — units that sat all winter fail on the first genuinely hot day. Budget up in the 30 days before predicted heat peaks in your market. Weather forecasting apps and historical heat event data can guide this.</p>
<table>
<tr><th>Region</th><th>Peak Season</th><th>Cost Per Call Range</th></tr>
<tr><td>Southwest (AZ, NV, CA desert)</td><td>April–October</td><td>$45–$90</td></tr>
<tr><td>Southeast (FL, GA, TX Gulf)</td><td>March–November</td><td>$35–$75</td></tr>
<tr><td>Midwest / Northeast</td><td>June–August</td><td>$30–$65</td></tr>
</table>
<h2>AC repair vs. AC replacement calls</h2>
<p>Repair and replacement calls come in through the same pipeline but require different handling. Repair calls close faster with a lower ticket. Replacement calls close slower but carry $4,000–$12,000+ in revenue. Some contractors separate campaigns for each — replacement calls get sent to senior technicians who can close the full system, repair calls go to field techs. If you don't have that separation yet, at minimum track which call type produces the higher 90-day revenue per call and adjust your bid accordingly.</p>
<p>See the full <a href="/hvac-leads/">HVAC leads overview</a> for context on year-round lead strategy and call type filtering.</p>
<hr>
<p><em>Get exclusive AC repair calls in your zip codes. <a href="/#contact">Contact RankLocal</a>.</em></p>""",
    links=[('/hvac-leads/','← All HVAC Leads',True),('/heating-leads/','Heating & Furnace Leads',False),('/contractor-leads/','All Contractor Leads',False),('/appointment-setting/','Appointment Setting',False),('/pay-per-call-leads/','Pay-Per-Call Leads',False)]
)

# ── 3. HEATING LEADS ───────────────────────────────────────────────
PAGES['heating-leads'] = dict(
    title='Heating & Furnace Leads | Exclusive Pay-Per-Call for HVAC Contractors | 2026',
    meta='Exclusive heating and furnace repair leads for HVAC contractors. Homeowners with no heat, calling your number only. Pay per call, no shared leads.',
    h1='Heating & Furnace Leads: Exclusive Calls for HVAC Contractors',
    schema_type='Service',
    svc_name='Exclusive Heating & Furnace Leads',
    svc_desc='Exclusive pay-per-call heating, furnace repair, and boiler leads for HVAC contractors.',
    area='United States',
    body="""<p>A furnace that stops working in January is an emergency. Unlike an AC failure in summer, a heating failure can be a safety issue — pipes freeze, vulnerable occupants are at risk, and the homeowner has zero patience for callbacks. The contractor who picks up the phone and arrives quickly earns the job almost every time. Heating leads are some of the highest-intent calls in home services precisely because the stakes are that high.</p>
<h2>Heating lead types and their value</h2>
<p><strong>Emergency no-heat calls:</strong> Furnace or boiler stopped working. Highest urgency, highest close rate. Worth paying $60–$110 per exclusive call because the job is almost always yours if you show up the same day.</p>
<p><strong>Furnace replacement calls:</strong> Homeowner knows their unit is old or inefficient and wants to replace it before it fails. Longer sales cycle, higher ticket ($3,000–$8,000+). These leads benefit from booked appointments because the homeowner isn't in panic mode and will comparison shop if left unbooked.</p>
<p><strong>Heat pump installation calls:</strong> Growing fast as energy efficiency incentives push homeowners toward heat pump systems. Higher install ticket, longer consideration. Benefit from educated sales approach.</p>
<h2>Regions with the highest heating lead demand</h2>
<table>
<tr><th>Region</th><th>Peak Season</th><th>Primary Lead Type</th></tr>
<tr><td>Midwest (IL, OH, MI, MN)</td><td>October–March</td><td>Emergency + replacement</td></tr>
<tr><td>Northeast (NY, PA, MA, NJ)</td><td>November–February</td><td>Emergency + boiler</td></tr>
<tr><td>Mountain (CO, UT, ID)</td><td>October–April</td><td>Furnace + heat pump</td></tr>
<tr><td>Pacific Northwest (WA, OR)</td><td>November–March</td><td>Heat pump + forced air</td></tr>
</table>
<p>See the full <a href="/hvac-leads/">HVAC leads guide</a> for year-round strategy and how to balance heating and cooling lead budgets across seasons.</p>
<hr>
<p><em>Exclusive furnace and heating calls in your service area. <a href="/#contact">Talk to RankLocal</a>.</em></p>""",
    links=[('/hvac-leads/','← All HVAC Leads',True),('/ac-repair-leads/','AC Repair Leads',False),('/contractor-leads/','All Contractor Leads',False),('/appointment-setting/','Appointment Setting',False),('/pay-per-call-leads/','Pay-Per-Call Leads',False)]
)

# ── 4. PLUMBING LEADS ─────────────────────────────────────────────
PAGES['plumbing-leads'] = dict(
    title='Plumbing Leads for Contractors | Exclusive Pay-Per-Call | 2026',
    meta='Exclusive plumbing leads for contractors — emergency repairs, water heater replacement, and drain service. Pay per call, no shared leads.',
    h1='Plumbing Leads: Exclusive Pay-Per-Call for Plumbing Contractors',
    schema_type='Service',
    svc_name='Exclusive Plumbing Leads',
    svc_desc='Exclusive pay-per-call plumbing leads for residential and commercial plumbing contractors nationwide.',
    area='United States',
    body="""<p>Plumbing leads span the widest range of urgency in home services. A burst pipe at 2am is a five-alarm emergency. A slow drain the homeowner has lived with for a month is barely a consideration. That range matters because it produces two very different types of callers: emergency callers who need someone now and will pay whatever it takes, and consideration-stage callers who are researching prices and won't decide for a week. Good plumbing lead programs let you filter for the former.</p>
<h2>Plumbing lead types and what each is worth</h2>
<table>
<tr><th>Call Type</th><th>Cost Per Call</th><th>Average Job Value</th></tr>
<tr><td>Emergency repair (burst pipe, no water)</td><td>$45–$85</td><td>$500–$3,000+</td></tr>
<tr><td>Water heater replacement</td><td>$50–$90</td><td>$800–$2,500</td></tr>
<tr><td>Drain cleaning / sewer</td><td>$30–$60</td><td>$150–$600</td></tr>
<tr><td>Remodel / new install</td><td>$60–$110</td><td>$1,500–$8,000+</td></tr>
</table>
<h2>Exclusive calls vs. shared plumbing leads</h2>
<p>The plumbing market is crowded with lead resellers. Most of them are selling the same form fills to five or six plumbing companies simultaneously. The homeowner who filled out a "get quotes" form online is not the same as the homeowner who searched "emergency plumber near me" and called the first number they saw. Exclusive inbound calls capture the second type. Shared form fills capture the first type and then send them to your competitors too.</p>
<p>For the average residential plumbing contractor, exclusive calls close at 30–40% versus 8–12% for shared form fills. The math heavily favors exclusive even at two or three times the cost per unit.</p>
<h2>Building a plumbing lead program that holds up year-round</h2>
<p>Unlike roofing or HVAC, plumbing doesn't have sharp seasonal peaks — pipes burst in winter, but drain issues and water heater failures happen all year. The most successful plumbing contractors run consistent exclusive call campaigns year-round rather than chasing seasonal bursts, and supplement with <a href="/appointment-setting/">booked appointments</a> for water heater and remodel jobs where the homeowner needs time to decide. See <a href="/water-heater-leads/">water heater leads</a> and <a href="/emergency-plumbing-leads/">emergency plumbing leads</a> for the sub-vertical breakdowns.</p>
<hr>
<p><em>Exclusive plumbing calls in your area. <a href="/#contact">Talk to RankLocal</a>.</em></p>""",
    links=[('/contractor-leads/','← All Contractor Leads',True),('/emergency-plumbing-leads/','Emergency Plumbing Leads',False),('/water-heater-leads/','Water Heater Leads',False),('/hvac-leads/','HVAC Leads',False),('/appointment-setting/','Appointment Setting',False),('/pay-per-call-leads/','Pay-Per-Call Leads',False)]
)

# ── 5. EMERGENCY PLUMBING LEADS ────────────────────────────────────
PAGES['emergency-plumbing-leads'] = dict(
    title='Emergency Plumbing Leads | Exclusive Pay-Per-Call | 2026',
    meta='Exclusive emergency plumbing leads — burst pipes, flooding, no water. Inbound calls from homeowners who need a plumber now. Pay per call only.',
    h1='Emergency Plumbing Leads: Exclusive Inbound Calls',
    schema_type='Service',
    svc_name='Emergency Plumbing Leads',
    svc_desc='Exclusive pay-per-call emergency plumbing leads for contractors. Burst pipes, flooding, and no-water calls from homeowners needing immediate service.',
    area='United States',
    body="""<p>Emergency plumbing calls are different from every other lead type. The homeowner is not shopping. There is water on the floor, or no water at all, and they need a licensed plumber today. The contractor who answers the phone and gives a realistic ETA wins the job. No amount of marketing polish matters — what matters is pickup rate and speed to arrival.</p>
<h2>What qualifies as an emergency plumbing call</h2>
<p>True emergency calls typically involve: burst or leaking pipes causing active damage, sewer line backup causing sewage in the home, complete loss of water pressure, gas line concerns connected to plumbing, or flooding from a broken supply line or appliance connection. These are distinct from "urgent" calls (slow drain, dripping faucet) where the homeowner can wait a day or two.</p>
<p>Quality emergency plumbing lead programs screen for active damage — the homeowner should be describing a situation happening right now, not something they noticed last week. Ask any lead provider how they qualify "emergency" before you buy.</p>
<h2>Emergency vs. non-emergency plumbing: the cost difference</h2>
<table>
<tr><th>Call Type</th><th>Cost Per Call</th><th>Close Rate</th><th>Typical Job Value</th></tr>
<tr><td>Emergency (active damage)</td><td>$55–$95</td><td>45–65%</td><td>$600–$4,000</td></tr>
<tr><td>Urgent (same-day needed)</td><td>$35–$65</td><td>30–45%</td><td>$200–$1,000</td></tr>
<tr><td>Scheduled (not urgent)</td><td>$25–$50</td><td>15–25%</td><td>$150–$600</td></tr>
</table>
<p>Emergency calls justify higher cost per call because the job value and close rate are both elevated. A $85 exclusive call that closes at 55% and produces an average $1,200 job is generating $660 in revenue per call spent — well ahead of a $30 non-emergency call that closes at 20% and averages $250 ($50 in revenue per call).</p>
<p>See the full <a href="/plumbing-leads/">plumbing leads guide</a> for call type filtering and year-round lead strategy.</p>
<hr>
<p><em>Exclusive emergency plumbing calls in your market. <a href="/#contact">Talk to RankLocal</a>.</em></p>""",
    links=[('/plumbing-leads/','← All Plumbing Leads',True),('/water-heater-leads/','Water Heater Leads',False),('/contractor-leads/','All Contractor Leads',False),('/appointment-setting/','Appointment Setting',False),('/pay-per-call-leads/','Pay-Per-Call Leads',False)]
)

# ── 6. WATER HEATER LEADS ─────────────────────────────────────────
PAGES['water-heater-leads'] = dict(
    title='Water Heater Leads | Exclusive Pay-Per-Call for Plumbers | 2026',
    meta='Exclusive water heater replacement and repair leads for plumbing contractors. Tank, tankless, and heat pump water heater calls. Pay per call only.',
    h1='Water Heater Leads: Exclusive Calls for Plumbing Contractors',
    schema_type='Service',
    svc_name='Water Heater Replacement Leads',
    svc_desc='Exclusive pay-per-call water heater installation and replacement leads for plumbing contractors.',
    area='United States',
    body="""<p>Water heater replacement is one of the most predictable high-value jobs in residential plumbing. The average tank water heater lasts 8–12 years. When one fails — and it will eventually fail — the homeowner has to replace it. Unlike discretionary home improvements, a dead water heater is not optional. That makes water heater leads some of the easiest to close: the homeowner already decided they need a new unit; the only question is who installs it.</p>
<h2>Water heater lead types</h2>
<p><strong>Emergency replacement:</strong> The unit failed, there's no hot water, and the homeowner needs installation today or tomorrow. Highest urgency, highest close rate. These calls are worth $60–$100 each because the homeowner isn't shopping — they're deciding between contractors who can show up fast.</p>
<p><strong>Planned replacement:</strong> Homeowner knows the unit is aging and wants to replace it before it fails. Longer consideration period, but serious intent. These work well as <a href="/appointment-setting/">booked appointments</a> where a consultant can discuss tank vs. tankless options.</p>
<p><strong>Tankless conversion:</strong> Growing segment as homeowners upgrade from tank storage. Higher install ticket ($2,500–$5,000+). Homeowners often want multiple quotes, so speed and follow-up matter.</p>
<h2>Average water heater job values</h2>
<table>
<tr><th>Unit Type</th><th>Install Cost Range</th><th>Margin Estimate</th></tr>
<tr><td>40–50 gallon tank</td><td>$800–$1,400</td><td>40–55%</td></tr>
<tr><td>50–75 gallon tank</td><td>$1,000–$1,800</td><td>40–55%</td></tr>
<tr><td>Tankless (gas)</td><td>$2,000–$4,500</td><td>35–50%</td></tr>
<tr><td>Heat pump water heater</td><td>$2,500–$5,000</td><td>35–45%</td></tr>
</table>
<p>See the full <a href="/plumbing-leads/">plumbing leads guide</a> for how water heater calls fit into a broader plumbing lead strategy.</p>
<hr>
<p><em>Exclusive water heater calls in your zip codes. <a href="/#contact">Contact RankLocal</a>.</em></p>""",
    links=[('/plumbing-leads/','← All Plumbing Leads',True),('/emergency-plumbing-leads/','Emergency Plumbing Leads',False),('/contractor-leads/','All Contractor Leads',False),('/appointment-setting/','Appointment Setting',False),('/pay-per-call-leads/','Pay-Per-Call Leads',False)]
)

# ── 7. COMMERCIAL ROOFING LEADS ────────────────────────────────────
PAGES['commercial-roofing-leads'] = dict(
    title='Commercial Roofing Leads | Exclusive Pay-Per-Call for Contractors | 2026',
    meta='Exclusive commercial roofing leads — flat roof, TPO, EPDM, and metal roofing for commercial properties. Pay per call, no shared leads.',
    h1='Commercial Roofing Leads: Exclusive Calls for Commercial Roofers',
    schema_type='Service',
    svc_name='Commercial Roofing Leads',
    svc_desc='Exclusive pay-per-call commercial roofing leads for contractors specializing in flat roof, TPO, EPDM, and metal roofing systems.',
    area='United States',
    body="""<p>Commercial roofing is a different business than residential. The deals are larger, the sales cycles are longer, and the decision-makers are property managers and building owners rather than homeowners. A single commercial roofing job can be worth $50,000–$500,000+. The challenge is that commercial leads are harder to generate and harder to qualify — and most lead generation programs are built for residential scale.</p>
<h2>Commercial vs. residential roofing leads: what's different</h2>
<p>In residential roofing, the homeowner and the decision-maker are the same person. In commercial, you're often talking to a facility manager who needs approval from a building owner or property management company, or a property manager acting on behalf of a REIT or investment group. The qualification process is longer. An exclusive inbound call from a decision-maker who found your number and called is worth far more than a residential lead — these people have authority to approve the work.</p>
<h2>Commercial roofing lead types</h2>
<p><strong>Emergency commercial calls:</strong> Active roof leak causing interior damage. Decision-makers call fast because liability is on the clock. These have the highest urgency and often convert to immediate temporary repair plus a full replacement proposal.</p>
<p><strong>Planned replacement:</strong> Property manager knows the roof is at end of life and is getting bids. Longer sales cycle, competitive, but high ticket.</p>
<p><strong>Preventive maintenance:</strong> Growing category as property managers recognize the cost of reactive vs. preventive roof care. Recurring revenue potential.</p>
<h2>Commercial roofing lead cost benchmarks</h2>
<table>
<tr><th>Lead Type</th><th>Cost Per Call</th><th>Typical Contract Value</th></tr>
<tr><td>Emergency commercial leak</td><td>$80–$150</td><td>$5,000–$50,000+</td></tr>
<tr><td>Planned replacement (under 20,000 sq ft)</td><td>$100–$180</td><td>$20,000–$150,000</td></tr>
<tr><td>Planned replacement (large)</td><td>$150–$300</td><td>$100,000–$500,000+</td></tr>
<tr><td>Maintenance contract</td><td>$60–$120</td><td>$2,000–$15,000/year</td></tr>
</table>
<p>Commercial roofing contractors frequently combine exclusive call campaigns with <a href="/appointment-setting/">booked appointments</a> for property walkthroughs, where the appointment is set with the verified decision-maker and confirmed before the contractor's time is spent. See also the <a href="/roofing-leads/">residential roofing leads</a> hub for how commercial and residential pipelines differ.</p>
<hr>
<p><em>Exclusive commercial roofing calls for your target market. <a href="/#contact">Contact RankLocal</a>.</em></p>""",
    links=[('/roofing-leads/','← All Roofing Leads',True),('/roofing-lead-generation/','Roofing Lead Generation',False),('/appointment-setting/','Appointment Setting',False),('/contractor-leads/','All Contractor Leads',False),('/pay-per-call-leads/','Pay-Per-Call Leads',False)]
)

# ── 8-11. FENCE LEADS BY STATE ────────────────────────────────────
for state_slug, state_name, state_cities, state_notes in [
    ('fence-leads-texas','Texas','Dallas, Houston, San Antonio, Austin, and Fort Worth','Texas has one of the highest fence installation rates in the country. Suburban growth, hot summers driving backyard privacy projects, and large lot sizes make Texas a consistently strong fence market.'),
    ('fence-leads-florida','Florida','Miami, Orlando, Tampa, Jacksonville, and Fort Lauderdale','Florida fence demand is driven by year-round outdoor living, HOA requirements, pool enclosures, and hurricane preparation. Aluminum and vinyl fence dominate due to the humid climate.'),
    ('fence-leads-arizona','Arizona','Phoenix, Tucson, Scottsdale, Mesa, and Chandler','Arizona fence demand peaks in fall and spring when outdoor projects are comfortable. Block wall and vinyl fence are common in the desert Southwest, with strong suburban growth driving new install demand.'),
    ('fence-leads-california','California','Los Angeles, San Diego, Sacramento, Fresno, and the Bay Area','California fence demand comes from privacy-focused homeowners in urban and suburban markets. Wood privacy fence dominates in Northern California; vinyl and aluminum are popular in Southern California.'),
]:
    PAGES[f'fence-leads-{state_slug.split("-")[-1]}'] = dict(
        title=f'Fence Leads in {state_name}: Exclusive Pay-Per-Call | 2026',
        meta=f'Exclusive fence installation leads in {state_name} — {state_cities}. Wood, vinyl, aluminum, and chain link fence leads. Pay per call only.',
        h1=f'Fence Leads in {state_name}: Exclusive Pay-Per-Call for Fence Contractors',
        schema_type='Service',
        svc_name=f'Exclusive Fence Leads — {state_name}',
        svc_desc=f'Exclusive pay-per-call fence installation and repair leads for contractors in {state_name}.',
        area=state_name,
        body=f"""<p>{state_notes}</p>
<h2>What fence leads look like in {state_name}</h2>
<p>Inbound fence calls in {state_name} typically come from homeowners in one of three situations: they need a new fence installed for privacy, security, or code compliance; they have an existing fence that's been damaged and need it repaired or replaced; or they're building a new home and need perimeter fencing as part of the project. Each type has different urgency and conversion characteristics.</p>
<p>Privacy and security fences are the highest-ticket installs. A homeowner replacing 200 linear feet of 6-foot privacy fence in a {state_name} suburb is looking at a $4,000–$10,000 job depending on material and terrain. Pool safety fence installs — required by code in many {state_name} municipalities — are a reliable, recurring source of moderate-ticket jobs.</p>
<h2>Fence lead costs in {state_name}</h2>
<table>
<tr><th>Call Type</th><th>Cost Per Call</th><th>Typical Job Value</th></tr>
<tr><td>New privacy fence install</td><td>$35–$70</td><td>$3,000–$12,000</td></tr>
<tr><td>Fence repair</td><td>$20–$45</td><td>$300–$1,500</td></tr>
<tr><td>Pool / safety fence</td><td>$30–$60</td><td>$1,500–$5,000</td></tr>
<tr><td>Commercial fencing</td><td>$50–$100</td><td>$5,000–$40,000+</td></tr>
</table>
<p>Cities like {state_cities.split(',')[0]} and {state_cities.split(',')[1].strip()} tend to run at the higher end of cost per call due to population density and contractor competition. Smaller metro areas and rural markets in {state_name} often cost less per call with similar job values.</p>
<h2>Getting started with fence leads in {state_name}</h2>
<p>RankLocal's {state_name} fence campaigns can be targeted by city, county, or zip code, with filtering by fence type and job size. See the <a href="/fence-leads/">fence leads hub</a> for full material and job type options, or explore <a href="/contractor-leads/">all contractor lead verticals</a>.</p>
<hr>
<p><em>Exclusive fence calls in {state_name}. <a href="/#contact">Talk to RankLocal</a>.</em></p>""",
        links=[('/fence-leads/','← All Fence Leads',True),('/contractor-leads/','All Contractor Leads',False),('/roofing-leads/','Roofing Leads',False),('/appointment-setting/','Appointment Setting',False),('/pay-per-call-leads/','Pay-Per-Call Leads',False)]
    )

# ── 12-14. GARAGE DOOR SUB-VERTICALS ─────────────────────────────
PAGES['garage-door-spring-repair-leads'] = dict(
    title='Garage Door Spring Repair Leads | Exclusive Pay-Per-Call | 2026',
    meta='Exclusive garage door spring repair leads — torsion and extension spring replacements from homeowners who need same-day service. Pay per call.',
    h1='Garage Door Spring Repair Leads: Exclusive Inbound Calls',
    schema_type='Service',
    svc_name='Garage Door Spring Repair Leads',
    svc_desc='Exclusive pay-per-call garage door spring repair leads for contractors. Torsion and extension spring replacement calls.',
    area='United States',
    body="""<p>Broken garage door springs are the single most common garage door repair call, accounting for roughly 40% of all residential garage door service calls. When a torsion spring breaks, the door becomes inoperable and can't be safely lifted manually. The homeowner's car may be trapped inside. That's an urgent situation that produces exactly the kind of call you want: a homeowner who needs a contractor today and isn't shopping around.</p>
<h2>Why spring repair calls close so well</h2>
<p>Three things make garage door spring repair calls uniquely valuable for exclusive lead buying. First, the homeowner is stuck — they can't wait a week for an appointment. Second, the repair is technical and not DIY-friendly (a wound torsion spring has tremendous stored energy and is dangerous to handle without training), so the homeowner needs a professional. Third, the average spring repair ticket is $200–$450, which is high enough to be worth the trip but low enough that the homeowner doesn't spend three days getting quotes.</p>
<table>
<tr><th>Repair Type</th><th>Cost Per Call</th><th>Job Value</th><th>Close Rate</th></tr>
<tr><td>Torsion spring replacement</td><td>$30–$55</td><td>$250–$450</td><td>45–60%</td></tr>
<tr><td>Extension spring replacement</td><td>$25–$45</td><td>$175–$300</td><td>50–65%</td></tr>
<tr><td>Spring + cable combo</td><td>$35–$65</td><td>$300–$550</td><td>40–55%</td></tr>
</table>
<h2>Spring repair as an upsell opportunity</h2>
<p>Broken springs frequently expose other worn components — cables, rollers, hinges, and the opener itself. Technicians who do a thorough safety inspection alongside a spring repair consistently upsell additional work, raising average ticket to $350–$700. Build the safety inspection into your service process, not as an add-on but as a standard step. That one change materially affects revenue per call.</p>
<p>See the full <a href="/garage-door-repair-leads/">garage door leads overview</a> for all sub-vertical options.</p>
<hr>
<p><em>Exclusive garage door spring repair calls. <a href="/#contact">Talk to RankLocal</a>.</em></p>""",
    links=[('/garage-door-repair-leads/','← All Garage Door Leads',True),('/garage-door-opener-leads/','Garage Door Opener Leads',False),('/garage-door-replacement-leads/','Replacement Leads',False),('/contractor-leads/','All Contractor Leads',False),('/pay-per-call-leads/','Pay-Per-Call Leads',False)]
)

PAGES['garage-door-opener-leads'] = dict(
    title='Garage Door Opener Leads | Exclusive Pay-Per-Call | 2026',
    meta='Exclusive garage door opener installation and repair leads. Homeowners needing new openers, smart upgrades, or opener repairs. Pay per call.',
    h1='Garage Door Opener Leads: Exclusive Calls for Garage Door Contractors',
    schema_type='Service',
    svc_name='Garage Door Opener Leads',
    svc_desc='Exclusive pay-per-call garage door opener installation, repair, and smart upgrade leads.',
    area='United States',
    body="""<p>Garage door opener leads break into two clear categories: repair calls from homeowners whose existing opener stopped working, and installation calls from homeowners who want a new or upgraded opener — often triggered by a move, a security concern, or the desire for smart home integration. Both are good lead types; they just require different technician skill sets and produce different tickets.</p>
<h2>Opener repair vs. opener installation</h2>
<p><strong>Repair calls:</strong> The opener won't operate the door, responds inconsistently, or makes grinding/straining noises. These calls are often urgent — same-day or next-day. Average ticket is $150–$350 for a repair, or $300–$500 if the repair reveals the opener needs replacement. Close rate is high because the homeowner already committed to calling a professional.</p>
<p><strong>Installation calls:</strong> Homeowner wants a new opener, usually because the existing one is old, loud, or lacks smart features. This is a considered purchase — they may want to see options. Good candidates for booked appointments where a technician can demo LiftMaster, Chamberlain, or Genie systems. Average ticket is $400–$800 including hardware and labor.</p>
<h2>Smart opener demand is growing</h2>
<p>myQ-compatible and built-in WiFi openers now represent a significant portion of new opener installations. Homeowners who want smartphone control, package delivery access (Amazon Key), or integration with smart home platforms specifically ask for smart opener options. Contractors who can confidently recommend and install these systems command higher tickets and generate better reviews.</p>
<p>See the <a href="/garage-door-repair-leads/">garage door leads hub</a> for the full range of garage door lead types.</p>
<hr>
<p><em>Exclusive garage door opener calls in your market. <a href="/#contact">Contact RankLocal</a>.</em></p>""",
    links=[('/garage-door-repair-leads/','← All Garage Door Leads',True),('/garage-door-spring-repair-leads/','Spring Repair Leads',False),('/garage-door-replacement-leads/','Replacement Leads',False),('/contractor-leads/','All Contractor Leads',False),('/pay-per-call-leads/','Pay-Per-Call Leads',False)]
)

PAGES['garage-door-replacement-leads'] = dict(
    title='Garage Door Replacement Leads | Exclusive Pay-Per-Call | 2026',
    meta='Exclusive garage door replacement leads — homeowners ready to replace full door panels or entire systems. Pay per call, no shared leads.',
    h1='Garage Door Replacement Leads: Exclusive Calls for Contractors',
    schema_type='Service',
    svc_name='Garage Door Replacement Leads',
    svc_desc='Exclusive pay-per-call garage door replacement and new door installation leads for contractors.',
    area='United States',
    body="""<p>Garage door replacement leads are the highest-ticket lead type in the garage door vertical. A full garage door replacement — new panels, new hardware, new opener if needed — runs $1,200–$3,500 for a standard residential door and can exceed $5,000 for custom wood or carriage-house styles. These calls come from homeowners who've made the mental decision to replace, not just repair, and they're looking for a contractor who can show them options and quote the full job.</p>
<h2>What triggers a replacement call</h2>
<p>The most common triggers: the existing door was damaged in a vehicle collision (insurance claim involved — note this in your intake process), the door is old and showing significant wear that makes repair uneconomical, the homeowner is remodeling the home exterior and wants a new door to match, or the door is functionally obsolete (no insulation, poor security). Each trigger requires a slightly different sales approach.</p>
<h2>Replacement lead cost and ROI</h2>
<table>
<tr><th>Door Type</th><th>Cost Per Call</th><th>Average Job Value</th></tr>
<tr><td>Standard steel (single)</td><td>$45–$80</td><td>$1,200–$1,800</td></tr>
<tr><td>Standard steel (double)</td><td>$55–$95</td><td>$1,600–$2,500</td></tr>
<tr><td>Insulated / premium</td><td>$65–$110</td><td>$2,000–$3,500</td></tr>
<tr><td>Custom wood / carriage</td><td>$80–$140</td><td>$3,500–$6,000+</td></tr>
</table>
<p>Insurance-involved replacement calls close at higher rates because the homeowner has a specific budget (insurance payout) and a deadline (adjuster timeline). If your team can handle insurance documentation, targeting post-collision replacement calls in high-traffic suburban markets can be very productive.</p>
<p>For the full garage door lead landscape, see <a href="/garage-door-repair-leads/">garage door leads</a> and <a href="/contractor-leads/">all contractor verticals</a>.</p>
<hr>
<p><em>Exclusive garage door replacement calls. <a href="/#contact">Talk to RankLocal</a>.</em></p>""",
    links=[('/garage-door-repair-leads/','← All Garage Door Leads',True),('/garage-door-spring-repair-leads/','Spring Repair Leads',False),('/garage-door-opener-leads/','Opener Leads',False),('/contractor-leads/','All Contractor Leads',False),('/pay-per-call-leads/','Pay-Per-Call Leads',False)]
)

# ── 15. LAWN CARE LEADS ────────────────────────────────────────────
PAGES['lawn-care-leads'] = dict(
    title='Lawn Care Leads | Exclusive Pay-Per-Call for Lawn Service Companies | 2026',
    meta='Exclusive lawn care leads — mowing, fertilization, aeration, and lawn treatment. Recurring service and one-time job calls. Pay per call only.',
    h1='Lawn Care Leads: Exclusive Pay-Per-Call for Lawn Service Companies',
    schema_type='Service',
    svc_name='Exclusive Lawn Care Leads',
    svc_desc='Exclusive pay-per-call lawn care leads including mowing, fertilization, aeration, and lawn treatment services.',
    area='United States',
    body="""<p>Lawn care leads operate on a different economics model than most home service verticals. A single closed lawn care customer isn't worth $500 or $1,000 — they're worth $1,500–$4,000 annually on a recurring mowing and treatment contract, and often $5,000–$8,000+ over their lifetime as a customer. That changes how you should think about cost per lead. A $40 call that converts to a recurring customer paying $150/month is worth $1,800 in the first year alone.</p>
<h2>Recurring vs. one-time lawn calls</h2>
<p>The highest-value lead type for lawn care companies is the recurring contract prospect — a homeowner who wants weekly or biweekly mowing, quarterly fertilization, and seasonal treatments all on one account. These calls take longer to close (they often want a walkthrough and quote), but the lifetime value is transformational compared to one-time mowing or aeration calls.</p>
<p>One-time service calls (aeration, overseeding, spring cleanups) have their place — they're faster to close, and a good experience often converts to a recurring contract. Treat them as acquisition opportunities, not just transactions.</p>
<h2>Lawn care lead cost and volume by season</h2>
<table>
<tr><th>Lead Type</th><th>Cost Per Call</th><th>Lifetime Value (2 yr)</th></tr>
<tr><td>Recurring contract inquiry</td><td>$30–$60</td><td>$2,400–$6,000</td></tr>
<tr><td>One-time mowing</td><td>$15–$30</td><td>$50–$150</td></tr>
<tr><td>Fertilization / treatment</td><td>$25–$50</td><td>$300–$900/year</td></tr>
<tr><td>Aeration / overseeding</td><td>$25–$45</td><td>$250–$600</td></tr>
</table>
<p>Volume peaks March–May (spring startup) and September–October (fall cleanups and overseeding). See <a href="/landscaping-leads/">landscaping leads</a> for the full outdoor services picture including <a href="/hardscaping-leads/">hardscaping</a> and <a href="/irrigation-leads/">irrigation</a>.</p>
<hr>
<p><em>Exclusive lawn care calls for your service area. <a href="/#contact">Talk to RankLocal</a>.</em></p>""",
    links=[('/landscaping-leads/','← All Landscaping Leads',True),('/irrigation-leads/','Irrigation Leads',False),('/hardscaping-leads/','Hardscaping Leads',False),('/snow-removal-leads/','Snow Removal Leads',False),('/contractor-leads/','All Contractor Leads',False),('/pay-per-call-leads/','Pay-Per-Call Leads',False)]
)

# ── 16. SNOW REMOVAL LEADS ────────────────────────────────────────
PAGES['snow-removal-leads'] = dict(
    title='Snow Removal Leads | Exclusive Pay-Per-Call for Snow Contractors | 2026',
    meta='Exclusive snow removal leads — residential and commercial snow plowing and removal calls. Seasonal contracts and one-time storm calls. Pay per call.',
    h1='Snow Removal Leads: Exclusive Pay-Per-Call for Snow Contractors',
    schema_type='Service',
    svc_name='Exclusive Snow Removal Leads',
    svc_desc='Exclusive pay-per-call snow removal and plowing leads for residential and commercial contractors.',
    area='United States',
    body="""<p>Snow removal leads are among the most time-compressed in home services. When a major storm hits, a property owner or manager who doesn't have a snow contract in place has hours — not days — to find service. The contractor who answers that call captures a seasonal relationship that can be worth $1,500–$8,000 in revenue over a single winter from one commercial property.</p>
<h2>Residential vs. commercial snow removal</h2>
<p><strong>Residential snow removal</strong> calls typically come from homeowners who don't own equipment, elderly homeowners who can't safely clear their own driveways, and new homeowners in snowbelt markets who are setting up services for the first time. Average residential seasonal contract: $400–$1,200. Average per-storm call: $75–$250.</p>
<p><strong>Commercial snow removal</strong> is higher value and longer relationship. Property managers, HOAs, retailers, and office parks need reliable service and often want seasonal contracts with guaranteed response times. Average commercial seasonal contract: $2,500–$15,000 per property. Multi-property commercial accounts are worth pursuing aggressively.</p>
<h2>When to buy snow removal leads</h2>
<p>The best time to buy snow removal leads is before the first storm — September and October in the northern US, when property managers are still in planning mode. Post-storm calls have higher urgency but are one-time in nature; pre-season calls convert to seasonal contracts that pay out over multiple months. Run both, but prioritize pre-season contract acquisition.</p>
<table>
<tr><th>Market</th><th>Peak Lead Season</th><th>Contract Value Range</th></tr>
<tr><td>Midwest (IL, OH, MI, MN)</td><td>Sept–Nov</td><td>$400–$8,000</td></tr>
<tr><td>Northeast (NY, PA, MA, CT)</td><td>Oct–Dec</td><td>$500–$10,000</td></tr>
<tr><td>Mountain (CO, UT, ID, WY)</td><td>Oct–Nov</td><td>$600–$12,000</td></tr>
</table>
<p>See <a href="/landscaping-leads/">landscaping leads</a> and <a href="/lawn-care-leads/">lawn care leads</a> for how to build a full-year outdoor services pipeline that carries through winter with snow removal.</p>
<hr>
<p><em>Exclusive snow removal calls for your market. <a href="/#contact">Contact RankLocal</a>.</em></p>""",
    links=[('/landscaping-leads/','← All Landscaping Leads',True),('/lawn-care-leads/','Lawn Care Leads',False),('/hardscaping-leads/','Hardscaping Leads',False),('/contractor-leads/','All Contractor Leads',False),('/pay-per-call-leads/','Pay-Per-Call Leads',False)]
)

# ── 17. OUTDOOR LIGHTING LEADS ────────────────────────────────────
PAGES['outdoor-lighting-leads'] = dict(
    title='Outdoor Lighting Leads | Exclusive Pay-Per-Call | 2026',
    meta='Exclusive outdoor and landscape lighting leads — permanent holiday lighting, landscape path lighting, and security lighting installs. Pay per call.',
    h1='Outdoor Lighting Leads: Exclusive Pay-Per-Call for Lighting Contractors',
    schema_type='Service',
    svc_name='Outdoor Lighting Installation Leads',
    svc_desc='Exclusive pay-per-call outdoor and landscape lighting installation leads for lighting contractors.',
    area='United States',
    body="""<p>Outdoor lighting is one of the fastest-growing segments in home services, driven by permanent holiday lighting programs, landscape lighting design, and the combination of aesthetic and security value that LED lighting now delivers at accessible price points. The average outdoor lighting install job runs $1,500–$8,000 for landscape lighting and $1,000–$3,500 for permanent holiday lighting programs — making it a high-margin, recurring-revenue opportunity for the right contractor.</p>
<h2>Permanent holiday lighting vs. landscape lighting</h2>
<p><strong>Permanent holiday lighting</strong> (Jellyfish Lighting, Govee, custom LED trim systems) has exploded in demand since 2020. Homeowners install once and control color and programming by smartphone. Install tickets run $1,500–$4,000. Once installed, the relationship continues with annual service visits and potential add-ons. Very high referral rate — neighbors see the house lit up and ask who installed it.</p>
<p><strong>Landscape lighting</strong> covers path lights, uplighting for trees and architectural features, deck and patio lighting, and security motion lighting. These installs run $1,500–$8,000+ depending on scope. Landscape lighting leads respond well to <a href="/appointment-setting/">booked appointments</a> for design consultations since the scope is visual and benefits from a site visit.</p>
<h2>Why outdoor lighting leads convert well</h2>
<p>Homeowners who specifically search for outdoor lighting installation are not price shopping for a commodity service — they have a vision for their property and are looking for a professional to realize it. Close rates on exclusive lighting calls tend to run 25–40%, with higher-end jobs having lower close rates but much larger tickets. Focus your pitch on design quality and portfolio rather than lowest price.</p>
<p>See <a href="/landscaping-leads/">landscaping leads</a> for the broader outdoor services picture.</p>
<hr>
<p><em>Exclusive outdoor lighting calls in your area. <a href="/#contact">Talk to RankLocal</a>.</em></p>""",
    links=[('/landscaping-leads/','← All Landscaping Leads',True),('/lawn-care-leads/','Lawn Care Leads',False),('/hardscaping-leads/','Hardscaping Leads',False),('/contractor-leads/','All Contractor Leads',False),('/pay-per-call-leads/','Pay-Per-Call Leads',False)]
)

# ── 18-22. MORE ROOFING GEO PAGES ────────────────────────────────
for state_slug, state_name, cities, notes in [
    ('roofing-leads-ohio','Ohio','Columbus, Cleveland, Cincinnati, Akron, and Toledo','Ohio sits in the heart of the Midwest storm corridor. Spring hail events hit Columbus, Cleveland, and Cincinnati regularly, and cold winters with ice dams create a steady stream of repair calls even in the off-storm seasons.'),
    ('roofing-leads-illinois','Illinois','Chicago, Aurora, Naperville, Rockford, and Springfield','Chicago is one of the most demanding roofing markets in the country. Harsh winters, spring hail, and some of the highest housing density outside the coasts create year-round demand. The Chicago suburbs are particularly strong for replacement roofing.'),
    ('roofing-leads-colorado','Colorado','Denver, Colorado Springs, Aurora, Fort Collins, and Boulder','Colorado is a premier hail market. The Front Range from Fort Collins to Pueblo sees some of the highest hail frequency in North America. Denver alone regularly appears in the top five US cities for annual hail damage. High-value homes and strong insurance claim culture drive premium roofing demand.'),
    ('roofing-leads-north-carolina','North Carolina','Charlotte, Raleigh, Greensboro, Durham, and Winston-Salem','North Carolina combines hurricane-belt exposure on the coast with strong suburban growth inland. Charlotte and Raleigh are among the fastest-growing metro areas in the US, creating consistent new and replacement roofing demand beyond just storm events.'),
    ('roofing-leads-arizona','Arizona','Phoenix, Tucson, Mesa, Chandler, and Scottsdale','Arizona roofing demand is driven by extreme heat degrading flat and low-slope roofing systems, monsoon season damage, and one of the fastest-growing housing markets in the US. Phoenix metro is particularly strong for tile roof repairs and replacements.'),
]:
    PAGES[state_slug] = dict(
        title=f'Roofing Leads in {state_name}: Exclusive Pay-Per-Call | 2026',
        meta=f'Exclusive roofing leads in {state_name} — {cities}. Storm damage, insurance, and replacement calls. Pay per call only, no shared leads.',
        h1=f'Roofing Leads in {state_name}: Exclusive Pay-Per-Call for {state_name} Roofers',
        schema_type='Service',
        svc_name=f'Exclusive Roofing Leads — {state_name}',
        svc_desc=f'Exclusive pay-per-call roofing leads for contractors in {state_name}.',
        area=state_name,
        body=f"""<p>{notes}</p>
<h2>Roofing lead demand in {state_name}</h2>
<p>Roofing leads in {state_name} come from three primary triggers: storm damage (hail, wind, heavy rain), aging roofs reaching end of life, and new homeowners addressing deferred maintenance. The storm trigger generates the most urgent calls and the highest close rates — homeowners dealing with active damage or a fresh insurance claim are motivated to act quickly. Replacement leads convert more slowly but produce the same $8,000–$18,000 average job value.</p>
<h2>Cost per call in {state_name}</h2>
<table>
<tr><th>Market</th><th>Standard CPL</th><th>Post-Storm CPL</th></tr>
{"".join(f"<tr><td>{c.strip()}</td><td>$35–$65</td><td>$75–$150+</td></tr>" for c in cities.split(',')[:3])}
</table>
<h2>How exclusive calls outperform shared leads in {state_name}</h2>
<p>In major {state_name} markets like {cities.split(',')[0]} and {cities.split(',')[1].strip()}, shared leads are aggressively sold by Angi, HomeAdvisor, and Thumbtack simultaneously to multiple contractors. Homeowners in competitive markets are called within minutes of submitting a form and often pick the first contractor to reach them — or stop answering entirely. Exclusive calls remove that race: the homeowner called your number, and you're the only one picking up.</p>
<p>Close rates on exclusive {state_name} roofing calls run 25–35% in normal conditions and 35–50%+ during active storm events, compared to 5–8% on shared form fills in the same markets. See the full <a href="/roofing-leads/">roofing leads hub</a> for cost benchmarks and lead type comparisons.</p>
<hr>
<p><em>{state_name} roofers: exclusive calls for your service area. <a href="/#contact">Talk to RankLocal</a>.</em></p>""",
        links=[('/roofing-leads/','← All Roofing Leads',True),('/roofing-lead-generation/','Roofing Lead Generation',False),('/insurance-roofing-leads/','Insurance Roofing Leads',False),('/appointment-setting/','Appointment Setting',False),('/pay-per-call-leads/','Pay-Per-Call Leads',False)]
    )

# ── 23-30. NEW VERTICALS ─────────────────────────────────────────
PAGES['painting-leads'] = dict(
    title='House Painting Leads | Exclusive Pay-Per-Call for Painters | 2026',
    meta='Exclusive house painting leads — interior and exterior painting calls from homeowners ready to hire. Pay per call only, no shared leads.',
    h1='House Painting Leads: Exclusive Pay-Per-Call for Painting Contractors',
    schema_type='Service',
    svc_name='Exclusive House Painting Leads',
    svc_desc='Exclusive pay-per-call interior and exterior house painting leads for residential painting contractors.',
    area='United States',
    body="""<p>Painting leads split cleanly between interior and exterior work, and the two have very different seasonality and close dynamics. Exterior painting is weather-dependent — the market runs hard from April through October in most US climates. Interior painting runs year-round, with peaks around move-ins and holiday preparation. Running campaigns for both gives you volume in all seasons.</p>
<h2>Interior vs. exterior painting leads</h2>
<p><strong>Exterior painting leads</strong> tend to be higher ticket ($2,500–$6,000 for a typical home exterior) and come with more consideration — homeowners often want two or three quotes before committing. Exclusive calls help here because the homeowner who called a specific painting company is warmer than one who submitted a form to five painters simultaneously.</p>
<p><strong>Interior painting leads</strong> convert faster. A homeowner who wants two rooms painted before guests arrive in three weeks is motivated to schedule quickly. Average interior job runs $800–$2,500. Close rates on exclusive interior painting calls run 30–45% because the timeline pressure is real.</p>
<h2>Painting lead cost benchmarks</h2>
<table>
<tr><th>Service Type</th><th>Cost Per Call</th><th>Avg Job Value</th></tr>
<tr><td>Interior (1-3 rooms)</td><td>$25–$50</td><td>$800–$2,000</td></tr>
<tr><td>Interior (whole house)</td><td>$40–$75</td><td>$2,500–$6,000</td></tr>
<tr><td>Exterior (standard)</td><td>$40–$80</td><td>$2,500–$5,500</td></tr>
<tr><td>Exterior (2-story +)</td><td>$55–$95</td><td>$4,000–$8,000</td></tr>
</table>
<p>For contractors who also do deck staining, cabinet refinishing, or commercial painting, those can be layered into the same campaign with job-type filters. See <a href="/contractor-leads/">all contractor lead verticals</a>.</p>
<hr>
<p><em>Exclusive painting calls in your market. <a href="/#contact">Talk to RankLocal</a>.</em></p>""",
    links=[('/contractor-leads/','← All Contractor Leads',True),('/siding-leads/','Siding Leads',False),('/window-replacement-leads/','Window Replacement Leads',False),('/appointment-setting/','Appointment Setting',False),('/pay-per-call-leads/','Pay-Per-Call Leads',False)]
)

PAGES['window-replacement-leads'] = dict(
    title='Window Replacement Leads | Exclusive Pay-Per-Call | 2026',
    meta='Exclusive window replacement leads — homeowners ready to replace old, drafty, or damaged windows. Pay per call, no shared leads.',
    h1='Window Replacement Leads: Exclusive Calls for Window Contractors',
    schema_type='Service',
    svc_name='Window Replacement Leads',
    svc_desc='Exclusive pay-per-call window replacement and installation leads for window and door contractors.',
    area='United States',
    body="""<p>Window replacement is a considered purchase with a long decision cycle and a high ticket — the average whole-home window replacement runs $8,000–$20,000, and individual window replacements run $400–$900 each. Homeowners research extensively before calling. When they do call, they're serious. That's why close rates on exclusive window replacement calls (15–25%) can produce excellent revenue per call even at higher cost-per-call prices.</p>
<h2>What drives window replacement calls</h2>
<p>Energy costs are the most common trigger. Homeowners notice their heating and cooling bills are high and realize their old single-pane or aluminum-frame windows are a major source of loss. Energy efficiency messaging, federal tax credits for qualifying windows, and utility rebates all create urgency around window upgrades.</p>
<p>Damage is the second major driver. Broken seals (foggy glass), cracked panes, frames rotting or warping, or window damage from weather events all create immediate replacement need. These leads close faster because the damage is already visible and motivating.</p>
<h2>Window lead cost and ROI</h2>
<table>
<tr><th>Call Type</th><th>Cost Per Call</th><th>Average Job Value</th></tr>
<tr><td>Single window replacement</td><td>$30–$60</td><td>$400–$900</td></tr>
<tr><td>Multiple windows (3-8)</td><td>$50–$90</td><td>$2,500–$7,000</td></tr>
<tr><td>Whole-home replacement</td><td>$75–$130</td><td>$8,000–$20,000</td></tr>
<tr><td>Sliding door / patio door</td><td>$45–$80</td><td>$1,200–$3,500</td></tr>
</table>
<p>Window replacement leads pair well with <a href="/appointment-setting/">booked appointments</a> — the in-home consultation is a standard part of the sales process, and pre-booking the consultation removes friction and improves show rates. See <a href="/contractor-leads/">all contractor verticals</a>.</p>
<hr>
<p><em>Exclusive window replacement calls. <a href="/#contact">Talk to RankLocal</a>.</em></p>""",
    links=[('/contractor-leads/','← All Contractor Leads',True),('/siding-leads/','Siding Leads',False),('/painting-leads/','Painting Leads',False),('/appointment-setting/','Appointment Setting',False),('/pay-per-call-leads/','Pay-Per-Call Leads',False)]
)

PAGES['siding-leads'] = dict(
    title='Siding Leads | Exclusive Pay-Per-Call for Siding Contractors | 2026',
    meta='Exclusive siding replacement and installation leads — vinyl, fiber cement, and wood siding calls from homeowners ready to hire. Pay per call.',
    h1='Siding Leads: Exclusive Pay-Per-Call for Siding Contractors',
    schema_type='Service',
    svc_name='Exclusive Siding Leads',
    svc_desc='Exclusive pay-per-call siding replacement and installation leads for contractors.',
    area='United States',
    body="""<p>Siding replacement is a high-ticket, cyclical purchase that homeowners delay until they can't any longer. When they finally call, the decision to replace is already made — the only open question is who to hire and which material. That dynamic makes exclusive siding calls particularly valuable: you're not convincing anyone they need new siding, you're competing to be the contractor they choose.</p>
<h2>Siding lead types and material mix</h2>
<p><strong>Vinyl siding</strong> remains the most common replacement request by volume. Mid-range pricing ($6,000–$12,000 for a typical home) and homeowners who know exactly what they want. Fast to quote, faster to close. </p>
<p><strong>Fiber cement (James Hardie)</strong> is the premium residential choice. Higher ticket ($12,000–$22,000), buyers who have done their research and often ask specifically for Hardie products. These homeowners are less price-sensitive and more focused on finding a certified installer.</p>
<p><strong>Storm damage siding</strong> is insurance-involved and can come in waves after hail or major wind events, similar to roofing. Close rates are high because the insurance payout drives urgency.</p>
<h2>Siding lead cost benchmarks</h2>
<table>
<tr><th>Material</th><th>Cost Per Call</th><th>Average Job Value</th></tr>
<tr><td>Vinyl siding</td><td>$45–$80</td><td>$6,000–$12,000</td></tr>
<tr><td>Fiber cement</td><td>$65–$110</td><td>$12,000–$22,000</td></tr>
<tr><td>Storm damage</td><td>$55–$95</td><td>$8,000–$18,000</td></tr>
<tr><td>Wood / cedar</td><td>$60–$100</td><td>$10,000–$25,000</td></tr>
</table>
<p>Siding leads work well alongside <a href="/window-replacement-leads/">window replacement</a> leads — many homeowners replace both at the same time as part of an exterior renovation. See <a href="/contractor-leads/">all contractor verticals</a>.</p>
<hr>
<p><em>Exclusive siding calls in your area. <a href="/#contact">Contact RankLocal</a>.</em></p>""",
    links=[('/contractor-leads/','← All Contractor Leads',True),('/window-replacement-leads/','Window Replacement Leads',False),('/painting-leads/','Painting Leads',False),('/roofing-leads/','Roofing Leads',False),('/pay-per-call-leads/','Pay-Per-Call Leads',False)]
)

PAGES['gutter-leads'] = dict(
    title='Gutter Leads | Exclusive Pay-Per-Call for Gutter Contractors | 2026',
    meta='Exclusive gutter installation and repair leads — gutter guards, replacement gutters, and downspout work. Pay per call, no shared leads.',
    h1='Gutter Leads: Exclusive Pay-Per-Call for Gutter Contractors',
    schema_type='Service',
    svc_name='Exclusive Gutter Leads',
    svc_desc='Exclusive pay-per-call gutter installation, repair, and gutter guard leads for contractors.',
    area='United States',
    body="""<p>Gutter leads are a year-round business with two clear peaks: spring (post-winter damage assessment) and fall (leaf season cleanup and guard installation). The average gutter job is smaller than a roofing or siding project, but the volume is high and margins are strong — a gutter crew can complete multiple jobs per day, making cost-per-call efficiency critical.</p>
<h2>Gutter lead types</h2>
<p><strong>Gutter guard installation</strong> is the highest-ticket gutter service. LeafFilter, MasterShield, and similar products run $2,000–$6,000 for a typical home. These leads respond well to consultative selling and booked appointments. The homeowner is making a considered purchase and often gets multiple quotes.</p>
<p><strong>Gutter replacement</strong> is the core service. A full gutters-and-downspouts replacement on a standard home runs $1,200–$3,500 depending on linear footage and material (aluminum vs. copper vs. steel). These calls close faster than guard installs because the need is usually triggered by obvious failure.</p>
<p><strong>Gutter cleaning and repair</strong> are lower ticket ($150–$500) but high volume and good for customer acquisition. A homeowner who pays you $200 to clean their gutters is a strong candidate for gutter guards on the same visit.</p>
<h2>Gutter lead cost benchmarks</h2>
<table>
<tr><th>Service</th><th>Cost Per Call</th><th>Job Value</th></tr>
<tr><td>Gutter guard install</td><td>$35–$70</td><td>$2,000–$6,000</td></tr>
<tr><td>Full gutter replacement</td><td>$30–$60</td><td>$1,200–$3,500</td></tr>
<tr><td>Cleaning + inspection</td><td>$15–$30</td><td>$150–$400</td></tr>
<tr><td>Repair (sections)</td><td>$20–$40</td><td>$200–$700</td></tr>
</table>
<p>Gutter contractors often pair well with <a href="/roofing-leads/">roofing leads</a> since the same storm that damages a roof often damages gutters too. See <a href="/contractor-leads/">all contractor verticals</a>.</p>
<hr>
<p><em>Exclusive gutter calls for your area. <a href="/#contact">Talk to RankLocal</a>.</em></p>""",
    links=[('/contractor-leads/','← All Contractor Leads',True),('/roofing-leads/','Roofing Leads',False),('/siding-leads/','Siding Leads',False),('/appointment-setting/','Appointment Setting',False),('/pay-per-call-leads/','Pay-Per-Call Leads',False)]
)

PAGES['pressure-washing-leads'] = dict(
    title='Pressure Washing Leads | Exclusive Pay-Per-Call | 2026',
    meta='Exclusive pressure washing leads — driveways, house washing, deck cleaning, and commercial washing calls. Pay per call, no shared leads.',
    h1='Pressure Washing Leads: Exclusive Pay-Per-Call for Cleaning Contractors',
    schema_type='Service',
    svc_name='Pressure Washing Leads',
    svc_desc='Exclusive pay-per-call pressure washing and soft wash leads for residential and commercial cleaning contractors.',
    area='United States',
    body="""<p>Pressure washing has evolved from a commodity service into a specialized trade with clear premium tiers. Soft wash roof cleaning, house washing for sale prep, and commercial fleet washing all command very different prices and buyer types than a basic driveway cleaning. Understanding which jobs your operation handles best helps you buy the right leads rather than filtering through calls you can't convert.</p>
<h2>Pressure washing lead types and margins</h2>
<table>
<tr><th>Service</th><th>Cost Per Call</th><th>Job Value</th><th>Notes</th></tr>
<tr><td>Driveway / flatwork</td><td>$15–$30</td><td>$150–$400</td><td>High volume, low ticket</td></tr>
<tr><td>House washing</td><td>$25–$50</td><td>$300–$700</td><td>Best margins per hour</td></tr>
<tr><td>Roof soft wash</td><td>$30–$60</td><td>$400–$900</td><td>Specialty — good margins</td></tr>
<tr><td>Deck / fence cleaning</td><td>$20–$45</td><td>$200–$600</td><td>Often paired with sealing</td></tr>
<tr><td>Commercial</td><td>$40–$80</td><td>$500–$3,000+</td><td>Recurring contract potential</td></tr>
</table>
<h2>Seasonal demand and positioning</h2>
<p>Spring is peak pressure washing season — homeowners emerge from winter wanting driveways cleaned, siding washed, and decks prepped. A well-run exclusive call campaign in April–June can fill a crew's schedule three to four weeks out. Fall is the second season, driven by pre-winter house prep and post-summer algae cleanup.</p>
<p>Pre-sale house washing is a reliable niche. Real estate agents recommend pressure washing before listing almost universally. A relationship with local agents who refer clients for pre-sale cleaning can produce consistent, predictable volume outside of pure advertising.</p>
<p>See <a href="/contractor-leads/">all contractor verticals</a> for more home services lead options.</p>
<hr>
<p><em>Exclusive pressure washing calls in your market. <a href="/#contact">Talk to RankLocal</a>.</em></p>""",
    links=[('/contractor-leads/','← All Contractor Leads',True),('/painting-leads/','Painting Leads',False),('/lawn-care-leads/','Lawn Care Leads',False),('/appointment-setting/','Appointment Setting',False),('/pay-per-call-leads/','Pay-Per-Call Leads',False)]
)

PAGES['electrical-leads'] = dict(
    title='Electrical Leads | Exclusive Pay-Per-Call for Electricians | 2026',
    meta='Exclusive electrical contractor leads — panel upgrades, EV charger installation, generator installs, and electrical repair. Pay per call.',
    h1='Electrical Leads: Exclusive Pay-Per-Call for Electrical Contractors',
    schema_type='Service',
    svc_name='Exclusive Electrical Leads',
    svc_desc='Exclusive pay-per-call electrical leads for licensed electricians. Panel upgrades, EV charger, generator, and repair calls.',
    area='United States',
    body="""<p>Electrical leads span from urgent safety repairs to high-value planned upgrades. The market is being reshaped by two major demand drivers: electric vehicle adoption (EV charger installation has become one of the fastest-growing electrical services), and home electrification — the shift from gas appliances and heating to electric systems. Both trends are producing calls that electrical contractors with the right skills can capture at excellent margins.</p>
<h2>Electrical lead types and demand trends</h2>
<p><strong>Panel upgrades (100A → 200A or 400A):</strong> Required for EV charging, heat pumps, and modern load demands. Average job: $2,500–$5,000. Growing fast as older homes hit electrical limits. These are planned purchases — homeowners are motivated but not in panic mode. Booked appointments work well.</p>
<p><strong>EV charger installation (Level 2):</strong> High demand, fast-growing. Average job: $800–$2,000 including panel assessment. Homeowners who just bought an EV are highly motivated and often need work done quickly. Exclusive calls close at 35–50% because the need is immediate and clear.</p>
<p><strong>Generator installation (standby):</strong> Generac, Kohler, and whole-home standby generators run $5,000–$15,000 installed. Demand spikes after major weather events. These are high-consideration purchases.</p>
<p><strong>Emergency electrical repair:</strong> Power outages, tripped panels, burning smells, or no power to specific circuits. High urgency, call same day or next day. Close rates are high because the homeowner needs help now.</p>
<h2>Electrical lead cost benchmarks</h2>
<table>
<tr><th>Service</th><th>Cost Per Call</th><th>Avg Job Value</th></tr>
<tr><td>Panel upgrade</td><td>$60–$110</td><td>$2,500–$5,000</td></tr>
<tr><td>EV charger install</td><td>$45–$80</td><td>$800–$2,000</td></tr>
<tr><td>Generator install</td><td>$80–$140</td><td>$5,000–$15,000</td></tr>
<tr><td>Emergency repair</td><td>$45–$85</td><td>$400–$2,000</td></tr>
</table>
<p>See <a href="/contractor-leads/">all contractor verticals</a> and <a href="/hvac-leads/">HVAC leads</a> for how electrical and HVAC often come from the same homeowner during a home electrification project.</p>
<hr>
<p><em>Exclusive electrical calls in your area. <a href="/#contact">Talk to RankLocal</a>.</em></p>""",
    links=[('/contractor-leads/','← All Contractor Leads',True),('/hvac-leads/','HVAC Leads',False),('/plumbing-leads/','Plumbing Leads',False),('/appointment-setting/','Appointment Setting',False),('/pay-per-call-leads/','Pay-Per-Call Leads',False)]
)

# ── GENERATE ALL PAGES ────────────────────────────────────────────
created = 0
for slug, pd in PAGES.items():
    out_dir = os.path.join(BASE, slug)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'index.html')
    if os.path.exists(out_path):
        print(f'  SKIP (exists): {slug}')
        continue

    schema_json = make_schema(
        slug, pd['title'], pd['meta'],
        pd['schema_type'],
        svc_name=pd.get('svc_name'),
        svc_desc=pd.get('svc_desc'),
        area=pd.get('area'),
        breadcrumb_name=pd['h1'].split(':')[0]
    )
    cl_html = cluster_links(pd['links'])
    html = build_page(slug, pd['title'], pd['meta'], pd['h1'], pd['body'], cl_html, schema_json)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  CREATED: {slug} ({len(html):,} bytes)')
    created += 1

print(f'\nTotal: {created}/{len(PAGES)} pages created.')
print('Slugs:', list(PAGES.keys()))
