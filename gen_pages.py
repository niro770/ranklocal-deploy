import os, re

BASE = r"C:\Users\19522\Documents\ranklocal-deploy-push"

CSS = """<style>*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
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
main.article em{color:var(--text-muted)}</style>"""

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

CROSS = """<section style="margin:3rem 0 1rem">
<h2 style="font-size:1.15rem;color:#fff;margin:0 0 1rem">More Home Service Verticals</h2>
<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:.6rem">
<a href="/contractor-leads/" style="display:block;padding:.55rem .9rem;background:rgba(0,170,255,0.15);border:1px solid rgba(0,170,255,0.35);border-radius:8px;color:#00AAFF;text-decoration:none;font-size:.88rem;font-weight:600">&larr; All Contractor Leads</a>
<a href="/roofing-leads/" style="display:block;padding:.55rem .9rem;background:rgba(0,170,255,0.07);border:1px solid rgba(0,170,255,0.18);border-radius:8px;color:#aac4e0;text-decoration:none;font-size:.88rem">Roofing Leads</a>
<a href="/fence-leads/" style="display:block;padding:.55rem .9rem;background:rgba(0,170,255,0.07);border:1px solid rgba(0,170,255,0.18);border-radius:8px;color:#aac4e0;text-decoration:none;font-size:.88rem">Fence Leads</a>
<a href="/pest-control-leads/" style="display:block;padding:.55rem .9rem;background:rgba(0,170,255,0.07);border:1px solid rgba(0,170,255,0.18);border-radius:8px;color:#aac4e0;text-decoration:none;font-size:.88rem">Pest Control Leads</a>
<a href="/landscaping-leads/" style="display:block;padding:.55rem .9rem;background:rgba(0,170,255,0.07);border:1px solid rgba(0,170,255,0.18);border-radius:8px;color:#aac4e0;text-decoration:none;font-size:.88rem">Landscaping Leads</a>
<a href="/appointment-setting/" style="display:block;padding:.55rem .9rem;background:rgba(0,170,255,0.07);border:1px solid rgba(0,170,255,0.18);border-radius:8px;color:#aac4e0;text-decoration:none;font-size:.88rem">Appointment Setting</a>
<a href="/pay-per-call-leads/" style="display:block;padding:.55rem .9rem;background:rgba(0,170,255,0.07);border:1px solid rgba(0,170,255,0.18);border-radius:8px;color:#aac4e0;text-decoration:none;font-size:.88rem">Pay-Per-Call Leads</a>
</div>
</section>"""

FOOTER = """<footer style="background:#060c1a;border-top:1px solid rgba(0,170,255,0.12);padding:2.5rem 1.5rem;margin-top:3rem">
<div style="max-width:1100px;margin:0 auto">
<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:.4rem .75rem;margin-bottom:1.75rem">
<strong style="color:#00AAFF;grid-column:1/-1;display:block;margin-bottom:.5rem;font-size:.85rem;letter-spacing:.08em;text-transform:uppercase">Explore All Verticals</strong>
<a href="/contractor-leads/" style="color:#00AAFF;text-decoration:none;font-size:.88rem;font-weight:600">All Contractor Leads</a>
<a href="/roofing-leads/" style="color:#aac4e0;text-decoration:none;font-size:.88rem">Roofing Leads</a>
<a href="/fence-leads/" style="color:#aac4e0;text-decoration:none;font-size:.88rem">Fence Leads</a>
<a href="/pest-control-leads/" style="color:#aac4e0;text-decoration:none;font-size:.88rem">Pest Control Leads</a>
<a href="/landscaping-leads/" style="color:#aac4e0;text-decoration:none;font-size:.88rem">Landscaping Leads</a>
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


def make_page(slug, title, meta, h1, bc, body):
    schema = f"""<script type="application/ld+json">
{{"@context":"https://schema.org","@graph":[
{{"@type":"Organization","@id":"https://ranklocall.com/#organization","name":"RankLocal","url":"https://ranklocall.com/"}},
{{"@type":"WebPage","@id":"https://ranklocall.com/{slug}/#webpage","url":"https://ranklocall.com/{slug}/","name":"{title}","description":"{meta}","isPartOf":{{"@id":"https://ranklocall.com/#website"}}}},
{{"@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"https://ranklocall.com/"}},{{"@type":"ListItem","position":2,"name":"{bc}","item":"https://ranklocall.com/{slug}/"}}]}}
]}}</script>"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<base href="/">
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{meta}">
<link rel="canonical" href="https://ranklocall.com/{slug}/">
<meta name="robots" content="index,follow">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{meta}">
<meta property="og:type" content="article">
<meta property="og:url" content="https://ranklocall.com/{slug}/">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
{schema}
{CSS}
</head>
<body>
{NAV}
<main class="article">
<h1>{h1}</h1>
{body}
{CROSS}
</main>
{FOOTER}
</body>
</html>"""

PAGES = []

# PAGE 1
PAGES.append(("what-is-exclusive-lead-generation",
"What Is Exclusive Lead Generation? | RankLocal",
"Exclusive lead generation explained: one lead, one contractor, no competition. Learn why exclusive leads close at 30% vs 5% for shared and cost less per job.",
"What Is Exclusive Lead Generation? (And Why Shared Leads Kill Your Close Rate)",
"Exclusive Lead Generation",
"""<p>An exclusive lead is a prospect delivered to exactly one contractor. Nobody else gets the phone number, no one else gets the address, no one races you to the callback. That sounds simple. In practice it is the single biggest variable in whether a lead generation program makes money or burns it.</p>
<p>Shared leads are the opposite: a homeowner fills out a form on Angi, HomeAdvisor, or any aggregator marketplace, and that form gets sold to three, four, sometimes five contractors simultaneously. The homeowner didn't ask to be called by a committee. They filled out one form. They get six calls in twelve minutes and pick up for whoever sounds least pushy. That's the game you're playing when you buy shared.</p>
<h2>The math that makes exclusive worth the premium</h2>
<p>Run it side by side. Buy 100 shared roofing leads at $25 each — that's $2,500. Close rate on shared leads averages around 5% because you're one of five roofers chasing the same person. You book 5 jobs.</p>
<p>Now buy 40 exclusive calls at $50 each — same $2,000. Close rate on exclusive climbs to 25-35% because the homeowner talked to you and only you. You book 10-14 jobs. Less spend, more than double the work. The shared lead wasn't the cheap option. It was the most expensive thing on the menu.</p>
<table>
<tr><th>Model</th><th>Unit cost</th><th>Close rate</th><th>Cost per job</th></tr>
<tr><td>Shared form fill</td><td>$25</td><td>~5%</td><td>$500</td></tr>
<tr><td>Exclusive call</td><td>$40</td><td>~25%</td><td>$160</td></tr>
<tr><td>Booked appointment</td><td>$120</td><td>~60%</td><td>$200</td></tr>
</table>
<p>The cost per <em>job</em> is what matters, never the cost per <em>lead</em>. Shared looks cheap on the sticker and destroys margin on the scoreboard.</p>
<h2>Why exclusivity raises close rates so dramatically</h2>
<p>It is not magic. It is psychology and logistics. A homeowner who calls one contractor is in buying mode. They have not yet been annoyed by four other calls, talked into three estimates, or confused by competing quotes. They want to fix the roof (or the fence, or the pest problem). You answer. You schedule. You go.</p>
<p>A homeowner who filled out a shared form is in sorting mode. They are now evaluating five contractors against each other on price, speed, and persistence. The best sales team wins, not the best contractor. Exclusivity removes that game entirely.</p>
<h2>The three exclusive lead types</h2>
<p>Not all exclusive leads are built the same. <strong>Exclusive calls</strong> are live inbound phone calls routed only to your number. The homeowner is on the line; your office needs to pick up and close for the inspection. <strong>Exclusive form fills</strong> are digitally gated to prevent resale, but they still require outbound follow-up. <strong>Booked appointments</strong> are the gold tier: the lead is called, qualified, and scheduled on your calendar before you ever see it. You skip to the estimate.</p>
<p>For most home service contractors, exclusive calls or booked appointments are the fastest path to ROI because they skip the form-to-call friction entirely. <a href="/appointment-setting/">Appointment setting</a> is how you get the booked version at scale without building an inside sales team.</p>
<h2>What "exclusive" actually means in the contract</h2>
<p>The word gets abused. Always confirm in writing: the lead is not resold under any circumstance, junk leads are credited, and you can verify exclusivity with call tracking. Any provider who hedges on those three points is running a shared model with exclusive pricing. The details that matter: is exclusivity locked at time of delivery, or does it expire after a window? Are there territories, or is exclusivity just per-call? Read the actual agreement.</p>
<p>RankLocal's model is exclusive at the infrastructure level: your campaigns generate your calls, meaning no other contractor is ever in the pool for your leads. That is structurally different from a shared marketplace that "pre-sells" to one buyer. <a href="/contractor-leads/">See how exclusive contractor leads work</a>, or <a href="/pay-per-call/">explore the pay-per-call model</a> that underlies it.</p>
<h2>Frequently asked questions</h2>
<p><strong>What is the difference between exclusive and semi-exclusive leads?</strong><br>
Semi-exclusive typically means the lead is sold to two to three buyers instead of five or six. The footrace still exists; it is just smaller. True exclusive means one contractor, confirmed in the contract.</p>
<p><strong>Why do shared leads have such low close rates?</strong><br>
By the time you call, the homeowner has already spoken with one or two competitors, is annoyed by the volume of calls, or has already booked someone else. You get the leftovers of a first-mover market.</p>
<p><strong>Is pay-per-call always exclusive?</strong><br>
It should be by definition, since a call rings one phone. Verify that the campaign is not a shared call queue or that calls are not being routed to multiple contractors in rotation. Dedicated campaigns per contractor are the gold standard.</p>
<hr>
<p><em>Ready to stop competing for shared leads? <a href="/contractor-leads/">Get exclusive contractor leads through RankLocal</a> or see how <a href="/appointment-setting/">appointment setting</a> books jobs straight onto your calendar.</em></p>"""))

# PAGE 2
PAGES.append(("angi-alternatives",
"Best Angi Alternatives for Contractors (Exclusive Leads That Actually Close)",
"Angi alternatives for home service contractors: platforms that send exclusive leads instead of shared form fills. Compare pay-per-call, appointment setting, and more.",
"Best Angi Alternatives for Contractors (That Send Exclusive Leads)",
"Angi Alternatives",
"""<p>Angi (formerly Angie's List) sells your lead to multiple contractors at once. You pay, five other roofers pay, and whoever calls back fastest and cheapest wins the job. That is the fundamental problem with marketplace lead models, and it is why so many contractors are actively looking for Angi alternatives.</p>
<p>This page covers the real alternatives: how each model works, what it costs, and what close rates to expect. If you are frustrated with shared marketplace leads, the options below are structurally different, not just a different marketplace.</p>
<h2>Why contractors leave Angi</h2>
<p>The complaints are consistent: high cost per lead that does not translate to jobs, homeowners who have already booked someone else by the time you call, leads sold to too many competitors, and customer service that credits less than it should. The underlying cause is the shared-lead model. Angi's revenue depends on selling each lead multiple times. That incentive is directly opposed to yours.</p>
<p>The other issue is intent timing. Angi captures homeowners who are "researching" as readily as those who are ready to buy. You pay the same price for both. Exclusive sources that filter for intent — live phone calls, pre-screened appointments — deliver a smaller volume at higher unit cost but dramatically better close rates.</p>
<h2>Angi alternatives compared</h2>
<table>
<tr><th>Alternative</th><th>Model</th><th>Lead type</th><th>Close rate (approx)</th></tr>
<tr><td><strong>RankLocal</strong></td><td>Pay-per-call / Appointment setting</td><td>Exclusive call or booked appt</td><td>25–60%</td></tr>
<tr><td>Google LSA</td><td>Pay-per-lead (Google Guaranteed)</td><td>Exclusive call</td><td>20–35%</td></tr>
<tr><td>Thumbtack</td><td>Pay-to-bid</td><td>Shared lead</td><td>5–15%</td></tr>
<tr><td>HomeAdvisor/Angi</td><td>Subscription + pay-per-lead</td><td>Shared form fill</td><td>3–8%</td></tr>
<tr><td>Houzz</td><td>Advertising + leads</td><td>Shared lead</td><td>5–12%</td></tr>
<tr><td>Facebook Ads (DIY)</td><td>Ad spend</td><td>Exclusive form fill</td><td>5–15%</td></tr>
</table>
<h2>Pay-per-call: the structural alternative</h2>
<p>Pay-per-call is the cleanest break from the shared-lead model. Instead of a form fill sold multiple times, you receive a live inbound phone call from a homeowner who dialed a number your campaign owns. No one else gets that call. The homeowner is in active buying mode. Your close rate climbs to 25-40% on a cold call and higher on a pre-screened one.</p>
<p>The unit cost is higher than a shared Angi lead, but the cost per booked job is dramatically lower. Most contractors who switch from Angi to exclusive pay-per-call report paying less per closed job within 60 days, even though the per-lead number went up. <a href="/pay-per-call/">Read how pay-per-call works</a> and see the math.</p>
<h2>Appointment setting: the highest-conversion alternative</h2>
<p>If your team is not fast at calling back leads, appointment setting is the right alternative. An <a href="/appointment-setting/">appointment setting service</a> calls the prospect, qualifies them (right job type, your service area, ready timeline), and books a confirmed time on your calendar. You show up to an estimate, not a cold call. Close rates for booked, pre-screened appointments run 50–70% because the only people on your calendar are people who want the work done.</p>
<h2>Google Local Services Ads</h2>
<p>Google LSA is a legitimate Angi alternative for contractors who want to own their Google presence. You pay per verified lead, the Google Guaranteed badge builds trust, and calls come directly to your business. The limitations: setup takes weeks, Google controls lead quality and crediting, and your budget is pooled with local competitors. For a full comparison, see <a href="/google-lsa-vs-pay-per-call/">Google LSA vs pay-per-call</a>.</p>
<h2>Which alternative is right for you</h2>
<p>If your office answers quickly and your team closes well on live calls: pay-per-call exclusive leads. If phone coverage is the bottleneck: appointment setting. If you want Google-backed trust signals and are willing to wait for setup: Google LSA. What you want to avoid is any marketplace that resells your lead to competitors — that includes Angi, HomeAdvisor, Thumbtack, and Houzz in their default configurations.</p>
<p>See the full <a href="/contractor-leads/">exclusive contractor leads hub</a> to compare by vertical, or <a href="/ranklocall-vs-angi/">read the head-to-head RankLocal vs Angi comparison</a>.</p>
<h2>Frequently asked questions</h2>
<p><strong>Is there a better alternative to Angi for roofing contractors?</strong><br>
Yes. Exclusive pay-per-call and appointment setting both deliver higher close rates than Angi's shared form fills. For roofing specifically, where job values are high, the premium per-lead cost of exclusive is almost always recovered in fewer lost jobs.</p>
<p><strong>Can I use multiple alternatives at the same time?</strong><br>
Absolutely. Many contractors run pay-per-call for volume, appointment setting for pre-screened estimates, and Google LSA for brand visibility simultaneously. The key is tracking cost per job across each channel, not just cost per lead.</p>
<p><strong>Does leaving Angi affect my reviews?</strong><br>
Your Angi reviews stay on the platform whether you are actively paying or not. Leaving the lead program does not delete your profile or reviews.</p>
<hr>
<p><em>Done with shared leads? <a href="/contractor-leads/">Get exclusive contractor leads from RankLocal</a> and see the cost-per-job difference in 30 days.</em></p>"""))

# PAGE 3
PAGES.append(("ranklocall-vs-angi",
"RankLocAll vs Angi: Exclusive Pay-Per-Call vs Shared Lead Marketplace | 2026",
"RankLocAll vs Angi Leads: exclusive pay-per-call calls and booked appointments vs shared form fills sold to 4 contractors. See cost-per-job comparison.",
"RankLocAll vs Angi: Why Exclusive Beats the Marketplace",
"RankLocAll vs Angi",
"""<p>Angi and RankLocal both send you leads from homeowners who want work done. Everything else about the two models is different. This page is the honest side-by-side: how each works, what it costs per job, and who each is right for.</p>
<h2>How each model works</h2>
<p><strong>Angi (formerly Angie's List)</strong> is a marketplace. Homeowners search or fill out a form, and Angi sells that contact to multiple contractors — typically three to five. You pay a per-lead fee or monthly subscription. You compete with four other contractors to get the callback first. Close rates on shared marketplace leads average 3–8%.</p>
<p><strong>RankLocal</strong> runs exclusive pay-per-call and appointment setting. Your campaign generates inbound calls that ring only your number. No other contractor is in the pool. You pay per call or per booked appointment, and because there is no competition, your close rate runs 25–60% depending on whether you received a live call or a pre-screened appointment.</p>
<h2>Head-to-head comparison</h2>
<table>
<tr><th>Factor</th><th>Angi</th><th>RankLocal</th></tr>
<tr><td>Lead exclusivity</td><td>Shared (3–5 contractors)</td><td>Exclusive (yours only)</td></tr>
<tr><td>Lead type</td><td>Form fill</td><td>Live call or booked appt</td></tr>
<tr><td>Typical close rate</td><td>3–8%</td><td>25–60%</td></tr>
<tr><td>Cost per lead</td><td>$15–$80</td><td>$35–$150</td></tr>
<tr><td>Cost per booked job</td><td>$300–$800+</td><td>$100–$250</td></tr>
<tr><td>Subscription required</td><td>Yes (often)</td><td>No</td></tr>
<tr><td>Homeowner intent</td><td>Mixed (browsing + buying)</td><td>High (active inquiry)</td></tr>
<tr><td>Competition per lead</td><td>3–5 contractors</td><td>0</td></tr>
</table>
<h2>The cost per job math</h2>
<p>The comparison that matters is not cost per lead — it is cost per job won. Take a roofing example: you buy 50 Angi leads at $40 each ($2,000). Close 5% and you win 2.5 jobs. That is $800 per job. You buy 25 exclusive calls at $50 each ($1,250). Close 28% and you win 7 jobs. That is $178 per job. Less spend, nearly 3x the output.</p>
<p>That gap closes a bit in lower-ticket verticals and widens in higher-ticket ones. In roofing, garage doors, and pest control contracts, the math almost always favors exclusive at any reasonable unit cost premium.</p>
<h2>Where Angi has an advantage</h2>
<p>Angi has a larger brand footprint and homeowners actively search for contractors there. If your business has no online presence and you are starting from zero, Angi provides immediate access to homeowners. It also has a review system that builds long-term trust. The problem is not that Angi has no value — it is that the per-job cost is high and the shared model creates a race you often lose.</p>
<h2>Where RankLocal has the edge</h2>
<p>Exclusive lead delivery means you are the only contractor the homeowner is talking to. Higher close rates mean lower cost per job. No monthly subscription means you pay for performance, not access. And the appointment setting option means you can offload the inbound-to-scheduled conversion entirely. <a href="/appointment-setting/">See how appointment setting works</a>.</p>
<h2>Which should you use</h2>
<p>If you are evaluating a switch: track your current Angi cost per closed job over the last 90 days. Then compare it to the exclusive call cost per job scenarios above with your actual close rate. Most contractors find the math favors exclusivity at unit costs up to three times higher than their current shared lead cost. If you have a fast-answering front office, start with <a href="/pay-per-call/">exclusive pay-per-call</a>. If phone coverage is an issue, start with <a href="/appointment-setting/">appointment setting</a>.</p>
<h2>Frequently asked questions</h2>
<p><strong>Can I run both Angi and RankLocal at the same time?</strong><br>
Yes. Some contractors use Angi for market coverage while testing exclusive pay-per-call to compare per-job cost. Once the comparison is clear, most shift budget toward exclusive.</p>
<p><strong>Does RankLocal work for the same verticals as Angi?</strong><br>
RankLocal covers roofing, fencing, landscaping, pest control, garage door repair, and more. See the <a href="/contractor-leads/">contractor leads hub</a> for all verticals.</p>
<p><strong>How quickly does RankLocal deliver calls?</strong><br>
Campaigns typically go live within a few days. Most contractors receive their first calls within the first week. Volume scales with budget and service area.</p>
<hr>
<p><em>Compare cost per job with your own numbers. <a href="/#contact">Talk to RankLocal</a> about exclusive pay-per-call for your vertical.</em></p>"""))

# PAGE 4
PAGES.append(("ranklocall-vs-homeadvisor",
"RankLocAll vs HomeAdvisor: Exclusive Leads vs Shared Marketplace | 2026",
"RankLocAll vs HomeAdvisor comparison: exclusive pay-per-call leads vs HomeAdvisor shared form fills. See cost per job, close rates, and which wins for home service contractors.",
"RankLocAll vs HomeAdvisor: Exclusive Leads vs the Shared Marketplace",
"RankLocAll vs HomeAdvisor",
"""<p>HomeAdvisor (now part of the Angi family) pioneered the pay-per-lead marketplace model for home service contractors. It also perfected selling the same lead to four competitors simultaneously. This page breaks down how the two models compare and which delivers better cost per job for the five most common home service trades.</p>
<h2>The fundamental difference</h2>
<p>HomeAdvisor aggregates homeowner demand and monetizes it by selling each inquiry multiple times. Your $40 lead was also sold to three other contractors. The homeowner gets called by all four within minutes. Whoever calls fastest, sounds most professional, and quotes lowest tends to win — not necessarily the best contractor.</p>
<p>RankLocal's pay-per-call model inverts this. Your campaign generates exclusive inbound demand. The homeowner calls a number your campaign controls and your number only. No other contractor is in the picture. Close rates reflect that structural difference: 3–8% for shared form fills vs 25–40% for exclusive live calls.</p>
<h2>HomeAdvisor's specific problems</h2>
<p>Beyond the shared model, HomeAdvisor has faced consistent contractor complaints: leads delivered outside your service area, fake or low-intent form fills that still charge you, difficult credit processes, and mandatory subscription fees on top of per-lead costs. The FTC settlement in 2022 confirmed some of these practices were systematic. Contractors are not imagining the problem.</p>
<h2>Head-to-head comparison</h2>
<table>
<tr><th>Factor</th><th>HomeAdvisor</th><th>RankLocal</th></tr>
<tr><td>Exclusivity</td><td>Shared (up to 4 contractors)</td><td>Exclusive</td></tr>
<tr><td>Lead format</td><td>Form fill</td><td>Live call or booked appointment</td></tr>
<tr><td>Close rate (typical)</td><td>4–8%</td><td>25–55%</td></tr>
<tr><td>Lead cost range</td><td>$15–$100</td><td>$35–$150</td></tr>
<tr><td>Cost per won job</td><td>$300–$1,000+</td><td>$100–$300</td></tr>
<tr><td>Monthly subscription</td><td>Yes ($300+/mo)</td><td>No</td></tr>
<tr><td>Junk lead credits</td><td>Inconsistent</td><td>Included</td></tr>
</table>
<h2>The math for roofing vs fencing</h2>
<p>In roofing, where a replacement job runs $10,000–$20,000, the higher per-call cost of exclusive is insignificant relative to the job value. Paying $75 per exclusive call vs $25 per shared lead looks like a 3x premium until you realize the exclusive delivers a job and the shared delivers a race. In fencing, where jobs average $3,000–$6,000, the math still holds but the spread is tighter. Track your own cost-per-job numbers over 90 days and compare the actual close rate on each source.</p>
<h2>When HomeAdvisor makes sense</h2>
<p>HomeAdvisor can be useful for brand discovery — homeowners do search there, and maintaining a profile with reviews builds long-term credibility even if you stop buying leads. If you are just starting out with zero marketing and need any incoming leads to test your sales process, a low-budget HomeAdvisor trial gives you volume quickly. The issue is staying on it once you have alternatives to compare against.</p>
<h2>Transitioning away from HomeAdvisor</h2>
<p>The transition is straightforward: run both for 60 days, track cost per job on each line, and shift budget to whichever wins. Most contractors who try exclusive pay-per-call alongside HomeAdvisor shift 80-100% of their budget within 90 days. <a href="/homeadvisor-alternatives/">See more HomeAdvisor alternatives</a> or <a href="/contractor-leads/">start with exclusive contractor leads</a>.</p>
<h2>Frequently asked questions</h2>
<p><strong>Can I keep my HomeAdvisor reviews while switching providers?</strong><br>
Yes. Your HomeAdvisor/Angi reviews stay on the platform permanently. You can stop buying leads while keeping the review asset.</p>
<p><strong>Does HomeAdvisor charge a cancellation fee?</strong><br>
Contracts vary. Read the fine print on annual subscriptions. Month-to-month plans have more flexibility.</p>
<p><strong>What homeAdvisor verticals does RankLocal replace?</strong><br>
Roofing, fencing, landscaping, pest control, garage door, and several others. See the <a href="/contractor-leads/">vertical list</a> for coverage.</p>
<hr>
<p><em>Track your HomeAdvisor cost per job, then <a href="/#contact">compare it to exclusive pay-per-call</a>. Most contractors are surprised which number wins.</em></p>"""))

# PAGE 5
PAGES.append(("ranklocall-vs-thumbtack",
"RankLocAll vs Thumbtack: Exclusive Leads vs Bidding on Jobs | 2026",
"RankLocAll vs Thumbtack for contractors: exclusive pay-per-call calls vs Thumbtack's bidding model. Which gets better close rates and cost per job?",
"RankLocAll vs Thumbtack: Exclusive Pay-Per-Call vs Bidding for Jobs",
"RankLocAll vs Thumbtack",
"""<p>Thumbtack's model requires you to bid on job requests from homeowners. You pay to send a quote, compete with multiple other contractors, and the homeowner picks whoever they like. If they ghost you after you paid to respond, the credit is gone. RankLocal's model is the opposite: you receive an inbound call from a homeowner who is already calling you specifically.</p>
<h2>How Thumbtack works</h2>
<p>Homeowners post a job or answer a few questions about what they need. Thumbtack notifies relevant contractors. You see the opportunity and decide whether to spend credits to contact the homeowner. If multiple contractors respond (common), the homeowner reviews messages and picks one or ignores all. You pay whether they respond or not in some configurations.</p>
<p>The result is a time-intensive model that requires active monitoring, crafting messages, and competing against other contractors' pitches. For trade contractors who are busy on job sites, this is the wrong workflow.</p>
<h2>Head-to-head comparison</h2>
<table>
<tr><th>Factor</th><th>Thumbtack</th><th>RankLocal</th></tr>
<tr><td>Lead initiation</td><td>Contractor bids outbound</td><td>Homeowner calls inbound</td></tr>
<tr><td>Exclusivity</td><td>Shared (multiple bidders)</td><td>Exclusive</td></tr>
<tr><td>Time required</td><td>High (monitoring + bidding)</td><td>Low (answer the phone)</td></tr>
<tr><td>Close rate</td><td>5–15%</td><td>25–55%</td></tr>
<tr><td>Lead intent level</td><td>Mixed</td><td>High (active inbound call)</td></tr>
<tr><td>Job type coverage</td><td>Broad (all home services)</td><td>Focus verticals</td></tr>
</table>
<h2>The inbound vs outbound intent gap</h2>
<p>The biggest structural difference: Thumbtack leads require you to reach out. RankLocal leads are homeowners who reached out to you. That intent gap is enormous. A homeowner who saw your Thumbtack listing and posted a generic job is at a different buying stage than a homeowner who picked up the phone, dialed a number, and is actively talking to you. Inbound calls close at 3–5x the rate of bidding-model outbound contacts.</p>
<h2>When Thumbtack makes sense</h2>
<p>Thumbtack works better for service categories where the customer needs to evaluate multiple options (photography, event planning, specialized home improvements). For high-frequency home service trades like roofing, pest control, and garage door repair, the bidding model is too slow and too competitive to be efficient. Homeowners with a broken spring on their garage door are not posting a job and waiting for quotes.</p>
<h2>The real cost comparison</h2>
<p>Calculate your actual cost per job on Thumbtack including all credits spent, not just credits that converted. Many contractors find the effective cost per job is $300-$600+ once wasted credits are included. For that same spend in exclusive calls, most verticals yield 2-4x more jobs. <a href="/pay-per-call/">See how exclusive pay-per-call pricing compares</a>.</p>
<hr>
<p><em>Stop bidding on jobs. <a href="/contractor-leads/">Get exclusive inbound calls from contractors who are already calling you</a>.</em></p>"""))

# PAGE 6
PAGES.append(("homeadvisor-alternatives",
"HomeAdvisor Alternatives for Contractors: 7 Better Ways to Get Exclusive Leads",
"The best HomeAdvisor alternatives for home service contractors in 2026. From exclusive pay-per-call to Google LSA, find lead sources that actually close.",
"HomeAdvisor Alternatives: 7 Better Ways to Get Exclusive Contractor Leads",
"HomeAdvisor Alternatives",
"""<p>HomeAdvisor sells your lead to three or four competitors. You already know this. This page is about what you can switch to, in order of how well each alternative works for the most common home service trades.</p>
<h2>1. Exclusive pay-per-call (best overall replacement)</h2>
<p>Pay-per-call delivers live inbound phone calls from homeowners who are actively seeking your service. The call rings only your number. No other contractor receives it. Close rates average 25-40% compared to 4-8% for HomeAdvisor's shared form fills. Cost per job is typically 40-60% lower even though the cost per lead is higher. <a href="/pay-per-call/">Learn how pay-per-call works</a>.</p>
<h2>2. Appointment setting (best for busy offices)</h2>
<p>If your team cannot answer calls consistently, appointment setting removes the problem. The service calls prospects, qualifies them, and delivers confirmed calendar appointments. You show up to pre-screened estimates. Close rates hit 50-70%. <a href="/appointment-setting/">See appointment setting services</a>.</p>
<h2>3. Google Local Services Ads</h2>
<p>Google LSA is a pay-per-lead program directly from Google. The Google Guaranteed badge builds trust, and leads are calls made directly to your business. Setup is slower than pay-per-call and requires background checks and license verification, but the brand association with Google is valuable. <a href="/google-local-services-ads-for-contractors/">Full Google LSA guide for contractors</a>.</p>
<h2>4. Google Ads (pay-per-click)</h2>
<p>Running your own Google Ads gives you exclusive inbound leads but requires campaign management expertise, ongoing optimization, and significant testing budget. Works well for contractors with marketing staff or agencies. Higher control, higher effort than managed services.</p>
<h2>5. Facebook and Instagram Ads</h2>
<p>Social ads reach homeowners earlier in the buying cycle. Effective for seasonal services (HVAC maintenance, storm prep) and areas with younger homeowner demographics. Lower cost per lead than Google, lower intent, longer follow-up cycle. Works best with appointment setting on the back end.</p>
<h2>6. Nextdoor (for neighborhood density)</h2>
<p>Nextdoor advertising reaches specific neighborhoods where your crews work, which is useful for referral-style geographic expansion. Lower volume but high local trust. Best used as a supplement, not a replacement for volume lead sources.</p>
<h2>7. SEO and Google Business Profile (long game)</h2>
<p>Building your organic presence takes 6-12 months but produces the lowest long-term cost per lead. Your Google Business Profile reviews, local search rankings, and website content generate inbound calls without per-lead cost once established. Combine with exclusive pay-per-call while the organic pipeline builds. <a href="/buying-roofing-leads-vs-seo/">Compare buying leads vs building SEO</a>.</p>
<h2>How to evaluate any HomeAdvisor alternative</h2>
<p>The only metric that matters is cost per booked job over 90 days. Not cost per lead — cost per job. Set up call tracking across every source, track which jobs close and at what revenue, and calculate your true acquisition cost. Any lead source that cannot prove its cost per job after 90 days is not a serious marketing channel for a growing contractor.</p>
<hr>
<p><em>Ready to try exclusive? <a href="/contractor-leads/">Start with RankLocal exclusive leads</a> or <a href="/ranklocall-vs-homeadvisor/">compare RankLocal vs HomeAdvisor directly</a>.</em></p>"""))

# PAGE 7
PAGES.append(("google-local-services-ads-for-contractors",
"Google Local Services Ads for Contractors: Complete 2026 Guide",
"Everything home service contractors need to know about Google Local Services Ads (LSA): setup, costs, Google Guaranteed badge, and how to maximize ROI in 2026.",
"Google Local Services Ads for Contractors: Complete 2026 Guide",
"Google LSA for Contractors",
"""<p>Google Local Services Ads put your business at the very top of Google search results for local queries like &ldquo;roofer near me&rdquo; or &ldquo;pest control [city].&rdquo; You only pay when a homeowner calls or messages directly through the ad. The Google Guaranteed or Google Screened badge tells homeowners Google has verified your license and background. This page covers everything you need to know to run LSA profitably as a contractor.</p>
<h2>What are Google Local Services Ads?</h2>
<p>LSAs are a pay-per-lead ad format that appears above standard Google Ads in local search results. They show your business name, rating, number of reviews, and hours. When a homeowner calls from the ad or sends a message, you pay for that lead. If the lead is for a service you do not offer or is outside your area, you can dispute it and potentially receive a credit.</p>
<p>The Google Guaranteed badge requires passing Google's verification process: license check, insurance verification, and background checks on owners and employees. Google Screened applies to knowledge-based professionals. Most home service trades qualify for Google Guaranteed.</p>
<h2>How to set up Google LSA for your contracting business</h2>
<p>Setup happens at ads.google.com/local-services-ads. The process: select your trade and service area, pass the verification steps, set your weekly budget, and wait for approval. Expect 2-4 weeks for the full verification process. You will need proof of general liability insurance, business license, and to pass a background check.</p>
<p>Once live, Google assigns a ranking within the local pack based on your proximity to the searcher, review count and rating, your responsiveness, and your budget. Higher budgets do not guarantee top placement — Google optimizes for homeowner experience, so review quality matters significantly.</p>
<h2>Google LSA costs for home service contractors</h2>
<table>
<tr><th>Trade</th><th>Typical cost per lead</th><th>Notes</th></tr>
<tr><td>Roofing</td><td>$25–$85</td><td>Higher in storm season, competitive markets</td></tr>
<tr><td>Pest control</td><td>$20–$60</td><td>Seasonal spikes in summer</td></tr>
<tr><td>Fence installation</td><td>$20–$55</td><td>Moderate competition</td></tr>
<tr><td>Landscaping</td><td>$15–$45</td><td>Varies by service type</td></tr>
<tr><td>Garage door</td><td>$20–$65</td><td>Emergency calls are higher value</td></tr>
</table>
<p>Leads are technically exclusive per your account but note that other contractors running LSA in the same area will appear in the same results. Homeowners can and do call multiple contractors from the pack. The exclusivity is at the billing level, not the impression level. <a href="/google-lsa-vs-pay-per-call/">See how this compares to true exclusive pay-per-call</a>.</p>
<h2>Getting the most from Google LSA</h2>
<p>Response time is the most critical performance factor. Google tracks whether you answer LSA calls and responds to messages. Low response rates hurt your ranking and can suspend your account. Build a dedicated response protocol: answer immediately, log the call, and follow up within 5 minutes on missed calls. Reviews drive ranking, so build a systematic review request process. Aim for 50+ reviews before expecting consistent placement.</p>
<p>Dispute leads aggressively. Google credits are available for calls outside your service area, wrong service category, spam, or excessively short calls. Most contractors under-dispute. Review your call log weekly and submit disputes for anything that does not meet the threshold.</p>
<h2>Google LSA limitations</h2>
<p>Setup is slow, Google controls budgeting and ranking algorithms you cannot fully override, and credit disputes are unpredictable. During high-demand periods (storm season, spring landscaping rush), budgets can exhaust quickly. For contractors who want immediate volume and price certainty, managed <a href="/pay-per-call/">pay-per-call campaigns</a> provide more control. For brand credibility and Google ecosystem integration, LSA is hard to beat.</p>
<h2>Frequently asked questions</h2>
<p><strong>How long does Google LSA verification take?</strong><br>
Typically 2–4 weeks. License and insurance checks are fast; background checks take the most time. Prepare documents before starting to avoid delays.</p>
<p><strong>Do I need a minimum review count to run LSA?</strong><br>
No minimum, but zero reviews significantly hurt your ranking. Build at least 10 reviews before launching for competitive results.</p>
<p><strong>Can I run Google LSA and pay-per-call at the same time?</strong><br>
Yes, and many contractors do. LSA captures Google-native searches; pay-per-call adds dedicated demand volume. Compare cost per job across both channels at 90 days.</p>
<hr>
<p><em>Complement your LSA with <a href="/pay-per-call/">exclusive pay-per-call leads</a> for more volume and price certainty. Or <a href="/google-lsa-vs-pay-per-call/">compare both models head-to-head</a>.</em></p>"""))

# PAGE 8
PAGES.append(("google-lsa-vs-pay-per-call",
"Google LSA vs Pay-Per-Call for Contractors: Which Gets Better Leads? | 2026",
"Google LSA vs pay-per-call for home service contractors: compare cost per lead, exclusivity, close rates, setup time, and which works better in 2026.",
"Google LSA vs Pay-Per-Call: Which Gets Home Service Contractors Better Leads?",
"Google LSA vs Pay-Per-Call",
"""<p>Google Local Services Ads and exclusive pay-per-call are the two most effective ways to get inbound phone calls from homeowners who want your service right now. They work differently, cost differently, and suit different contractor profiles. This page is the direct comparison.</p>
<h2>How each model generates leads</h2>
<p><strong>Google LSA</strong> places your business in Google's local ad unit at the top of search results. When a homeowner searches &ldquo;roofer near me&rdquo; or &ldquo;pest control [city],&rdquo; your listing appears. They see your reviews, call directly, and Google charges you for the lead. You are appearing alongside two or three other LSA advertisers in the same results.</p>
<p><strong>Exclusive pay-per-call</strong> runs campaigns across multiple channels (Google, Facebook, display, local sites) that route calls through a dedicated phone number controlled by your campaign. When someone calls that number, the call goes to you and only you. No other contractor receives it under any circumstance.</p>
<h2>Side-by-side comparison</h2>
<table>
<tr><th>Factor</th><th>Google LSA</th><th>Exclusive Pay-Per-Call</th></tr>
<tr><td>Exclusivity</td><td>Billing-level only (homeowners see multiple LSA ads)</td><td>True exclusive (one contractor per call)</td></tr>
<tr><td>Setup time</td><td>2–4 weeks (verification)</td><td>Days</td></tr>
<tr><td>Control over spend</td><td>Weekly budget cap; Google controls distribution</td><td>You set volume and budget</td></tr>
<tr><td>Lead cost range</td><td>$25–$85 (varies by vertical)</td><td>$35–$120 (varies by vertical)</td></tr>
<tr><td>Call quality</td><td>Good (Google search intent)</td><td>Excellent (dedicated campaign intent)</td></tr>
<tr><td>Close rate (typical)</td><td>20–35%</td><td>25–45%</td></tr>
<tr><td>Review dependency</td><td>High (reviews drive ranking)</td><td>Low</td></tr>
<tr><td>Google Guaranteed badge</td><td>Yes</td><td>No</td></tr>
<tr><td>Credit disputes</td><td>Available but inconsistent</td><td>Included</td></tr>
</table>
<h2>When Google LSA wins</h2>
<p>LSA wins when trust signals matter most. The Google Guaranteed badge reduces homeowner friction significantly — some homeowners will only call a Google-verified contractor. If you have strong reviews (50+), are in a mid-sized market without heavy LSA saturation, and can wait 3-4 weeks for setup, LSA is a cost-effective channel with good intent quality.</p>
<h2>When pay-per-call wins</h2>
<p>Pay-per-call wins when you need volume now, want price certainty, or are in a market where LSA competition is intense. Because you set your per-call budget and the campaigns are dedicated to your number, you have more predictable costs and faster ramp. In storm markets, where LSA costs spike dramatically during high demand, managed pay-per-call often provides price stability.</p>
<h2>The exclusivity gap matters most at scale</h2>
<p>At low volumes (5–10 leads/week), LSA and pay-per-call perform similarly. At high volumes (30+ leads/week), the billing-level exclusivity gap in LSA compounds. More homeowners seeing multiple LSA advertisers means more price-shopping, more multi-calling, and lower close rates. True exclusive pay-per-call maintains its close rate advantage at higher volume.</p>
<h2>The hybrid approach</h2>
<p>Most successful contractors run both. LSA for brand credibility, Google ecosystem integration, and review building. Pay-per-call for volume certainty, price stability, and markets where they need more calls than LSA can deliver. Track cost per job on each channel separately and allocate budget to the winner.</p>
<p>See the full guide on <a href="/google-local-services-ads-for-contractors/">Google LSA setup for contractors</a> and <a href="/pay-per-call/">how exclusive pay-per-call works</a>.</p>
<hr>
<p><em>Need volume now while your LSA gets verified? <a href="/contractor-leads/">Start with exclusive pay-per-call</a> — calls in days, not weeks.</em></p>"""))

# PAGE 9
PAGES.append(("google-lsa-cost-per-lead-roofing",
"Google LSA Cost Per Lead for Roofing: 2026 Benchmarks + Comparison",
"Google LSA cost per lead for roofing contractors in 2026: real benchmarks by market, season, and comparison to exclusive pay-per-call cost per job.",
"Google LSA Cost Per Lead for Roofing: 2026 Benchmarks + How Pay-Per-Call Compares",
"Google LSA Cost Per Lead Roofing",
"""<p>Google Local Services Ads cost per lead for roofing varies more than any other trade category. Storm season, market competition, and account health all move the number significantly. This page tracks real 2026 benchmarks and shows how LSA cost per lead translates to cost per job compared to exclusive pay-per-call.</p>
<h2>2026 Google LSA roofing cost per lead benchmarks</h2>
<table>
<tr><th>Market type</th><th>Off-peak CPL</th><th>Storm season CPL</th><th>High-competition market CPL</th></tr>
<tr><td>Small market (&lt;500k pop)</td><td>$25–$45</td><td>$55–$120</td><td>$40–$75</td></tr>
<tr><td>Mid-size market</td><td>$35–$60</td><td>$75–$150</td><td>$55–$100</td></tr>
<tr><td>Major metro</td><td>$55–$85</td><td>$100–$200+</td><td>$75–$150</td></tr>
</table>
<p>Storm season spikes are the most important factor to understand. When a hail storm or hurricane hits a market, every roofing contractor in the area increases their LSA budget simultaneously. Google's auction-based model responds by raising prices. In Dallas after a major hailstorm, LSA roofing CPL has reached $200+ for several weeks. Contractors who rely solely on LSA for storm volume are routinely priced out during the highest-demand periods.</p>
<h2>CPL is the wrong metric — use cost per job</h2>
<p>A $60 LSA lead and a $60 exclusive call have completely different economics. The LSA lead is one of several ads the homeowner saw; they may have also called your competitor. The exclusive call is just you. Typical close rate on an LSA roofing lead: 15–25%. Typical close rate on an exclusive call: 28–40%.</p>
<table>
<tr><th>Source</th><th>Cost per lead</th><th>Close rate</th><th>Cost per job</th></tr>
<tr><td>Google LSA (mid-market)</td><td>$55</td><td>20%</td><td>$275</td></tr>
<tr><td>Google LSA (storm peak)</td><td>$130</td><td>18%</td><td>$722</td></tr>
<tr><td>Exclusive pay-per-call</td><td>$65</td><td>32%</td><td>$203</td></tr>
<tr><td>Booked appointment</td><td>$140</td><td>58%</td><td>$241</td></tr>
</table>
<h2>How to reduce your LSA cost per lead</h2>
<p>Review count is the highest-leverage lever. More reviews, higher rating, and regular new reviews improve your ranking and lower your effective CPL because you win more impressions at the same budget. Response time is the second lever — Google tracks how quickly you answer LSA calls and penalizes slow responders with lower ranking. Answer every call immediately or have a professional answering service cover the gaps.</p>
<p>Dispute actively. Many contractors let unchargeable leads (out-of-area, wrong service, too short) slip by without disputing. Even recovering 10% of disputed leads reduces effective CPL significantly over a year.</p>
<h2>When to supplement LSA with pay-per-call</h2>
<p>If your LSA cost per job exceeds $300 consistently, or spikes above $500 during peak season, adding exclusive pay-per-call gives you price stability. Managed campaigns use fixed-cost-per-call pricing that does not spike during storm season because the traffic source is diversified. <a href="/pay-per-call-roofing/">See pay-per-call for roofing</a> for specific pricing.</p>
<hr>
<p><em>LSA costs too high in your market? <a href="/roofing-leads/">Compare exclusive roofing lead options</a> or <a href="/#contact">talk to RankLocal about your cost per job targets</a>.</em></p>"""))

# PAGE 10
PAGES.append(("speed-to-lead-for-contractors",
"Speed to Lead for Contractors: Why the First 5 Minutes Determine Your ROI",
"Speed to lead for contractors: research shows 5x close rate drop after 5 minutes. Learn how fast response and appointment setting solve the lead response problem.",
"Speed to Lead for Contractors: Why the First 5 Minutes Make or Break Your ROI",
"Speed to Lead",
"""<p>There is a study contractors should print and hang in every office: responding to a lead within 5 minutes makes you 100 times more likely to contact that prospect than responding after 30 minutes. In the first hour, every minute of delay reduces your odds dramatically. By the time your evening callback gets through, you are chasing someone who already booked the contractor who answered at 2pm.</p>
<h2>The speed-to-lead statistics that change how you think about your pipeline</h2>
<p>Research from MIT and InsideSales.com consistently shows the same pattern. Leads contacted within 5 minutes convert at 5x the rate of leads contacted at 10 minutes. After one hour, conversion rate drops by 80%. After 24 hours, you are cold-calling someone who has almost certainly already hired someone else or at minimum is far less interested than they were when they filled out the form.</p>
<p>For home service contractors, this is existential. Most jobs — roofing, pest control, fence installation, garage door repair — are not purely price-driven. They are urgency-driven. A homeowner with a roof leak is not comparison shopping. They are calling whoever answers. The contractor who answers immediately gets the job. The contractor who calls back at 6pm gets voicemail.</p>
<h2>Why most contractor offices fail at speed-to-lead</h2>
<p>The owner is on a roof. The office manager is handling invoices. The one person who might answer the phone is on another call. This is not a people problem — it is a systems problem. Most contractor businesses are built around delivering work, not answering phones. The result is leads that cost real money going cold because no one was available at the right moment.</p>
<p>Shared lead sources make this worse because you are competing against three or four other contractors simultaneously. The one who answers first wins. In an exclusive model, speed still matters but the pressure is lower because no one else is racing you. You still want to answer immediately, but a 15-minute callback on an exclusive lead is recoverable. The same 15-minute callback on a shared lead is often too late.</p>
<h2>How to improve speed-to-lead without hiring</h2>
<p>Three practical systems: First, route all leads directly to a mobile number that is always answered, not a landline that rings in the office. If the owner is the primary closer, route leads to the owner's cell. If volume grows past one person's capacity, build a rotation. Second, set up immediate text-back automation for missed calls. A homeowner who gets a text within 30 seconds of an unanswered call — &ldquo;Just missed you, calling right back in 2 minutes&rdquo; — stays warm far longer than one who gets silence. Third, use call scoring to prioritize callbacks: high-intent keywords, longer call duration, specific job types.</p>
<h2>The appointment setting solution</h2>
<p>If speed-to-lead is structurally unsolvable at your business — you are on job sites, your office coverage is inconsistent, you work alone — <a href="/appointment-setting/">appointment setting</a> removes the problem entirely. An appointment setting service answers within seconds, qualifies the lead, and books a time on your calendar before you ever see the inquiry. You show up to the appointment, not the call. Speed is handled by a team whose entire job is answering the phone.</p>
<p>This is the reason appointment setting has become the fastest-growing segment in contractor lead generation. The value is not just the appointment — it is the 5-minute response guarantee that most contractor offices cannot deliver on their own. See how <a href="/appointment-setting/">appointment setting works</a> and what it costs.</p>
<h2>Measuring your current speed-to-lead</h2>
<p>If you use call tracking (you should), run a report on average time to first response. If you are above 15 minutes consistently, you are losing a significant percentage of your inbound leads before anyone speaks to them. If you cannot get below 15 minutes with current staffing, appointment setting pays for itself in recovered leads alone.</p>
<h2>Frequently asked questions</h2>
<p><strong>Does speed-to-lead matter as much for exclusive leads as shared?</strong><br>
Less critical because there is no competitor race, but still very important. A homeowner who gets an immediate answer is still far more likely to book than one who waits an hour. Aim for under 10 minutes even on exclusive leads.</p>
<p><strong>What is a good average speed-to-lead for a contractor?</strong><br>
Under 5 minutes is excellent. 5–15 minutes is good. 15–60 minutes costs you jobs. Over 60 minutes requires a systems fix immediately.</p>
<p><strong>Does appointment setting work for emergency services like garage door repair?</strong><br>
Yes — appointment setting services operate extended hours specifically because emergency home service calls happen outside business hours. A same-day or next-morning appointment slot is appropriate for most emergency services.</p>
<hr>
<p><em>If speed-to-lead is your bottleneck, <a href="/appointment-setting/">appointment setting</a> is the fastest fix. If you answer quickly and want more exclusive calls, <a href="/contractor-leads/">start here</a>.</em></p>"""))

# PAGE 11
PAGES.append(("how-to-close-more-roofing-estimates",
"How to Close More Roofing Estimates: Scripts, Timing, and Objection Handling",
"Close more roofing estimates with proven scripts, same-day follow-up sequences, and objection handling for price, timing, and insurance claims.",
"How to Close More Roofing Estimates: Scripts, Timing, and Objection Handling",
"Close More Roofing Estimates",
"""<p>Roofing is a high-stakes, high-emotion purchase. A homeowner spending $12,000 on a roof they did not plan to buy this year is not comparing shingles — they are deciding whether they trust you. The contractors who close 40-60% of their estimates are not just cheaper or faster. They have a repeatable process for building trust fast and moving the homeowner to a decision before doubt sets in.</p>
<h2>The timeline that wins roofing estimates</h2>
<p>Same-day follow-up is the most reliable closer in roofing. When you finish the estimate, do not leave without a verbal commitment to next steps. If the homeowner says &ldquo;let me think about it,&rdquo; your response should be: &ldquo;Absolutely — I'll send the written proposal in the next hour and follow up tomorrow morning. What time works?&rdquo; Establishing a specific follow-up time creates accountability on both sides.</p>
<p>Follow up at the times you promised. If you said morning, call at 9am. Homeowners evaluate contractors by how well they follow through even before the work starts. A contractor who calls when they said they would has already demonstrated reliability. A contractor who calls three days later when &ldquo;I said morning&rdquo; has already failed a trust test.</p>
<h2>Closing scripts for common roofing objections</h2>
<p><strong>Objection: &ldquo;I need to get more quotes.&rdquo;</strong><br>
Response: &ldquo;That makes total sense. While you do that, a few things I'd recommend asking every contractor: ask to see their license and insurance in writing, ask for references on jobs in this zip code from the last 90 days, and ask what happens if they find additional damage once the tear-off starts. Those three questions will tell you a lot. I'm happy to answer all of them for you right now.&rdquo;</p>
<p><strong>Objection: &ldquo;Your price is too high.&rdquo;</strong><br>
Response: &ldquo;I hear you — it's a significant investment. Can I ask what you were expecting? I want to make sure we're comparing the same scope. Some contractors quote the minimum to get the job and add costs once they're on the roof. Our price includes [specific items]. Would it help if I walked you through exactly what you're getting?&rdquo;</p>
<p><strong>Objection: &ldquo;I need to talk to my spouse.&rdquo;</strong><br>
Response: &ldquo;Of course. Would it be easier if I set up a quick 10-minute call with both of you? That way I can answer any questions directly rather than playing phone tag. When are you both usually available?&rdquo;</p>
<p><strong>Objection: &ldquo;I want to wait and see if insurance covers it first.&rdquo;</strong><br>
Response: &ldquo;Smart move. Typically the adjuster comes out within 5-7 days. I can actually be there when the adjuster arrives to make sure nothing gets missed on the damage assessment — contractors who are present at adjuster meetings recover significantly more on claims. Want me to be there?&rdquo;</p>
<h2>The three-day follow-up sequence</h2>
<p>Day 1 (same day): Text with written proposal attached. &ldquo;Great meeting you today. Proposal attached — let me know if you have any questions.&rdquo; Day 2 (morning): Phone call. Reference specific detail from the estimate visit to show you remember them. Day 3 (if no response): Final text. &ldquo;Just want to make sure you received everything. Happy to answer any questions or adjust the scope to better fit your budget.&rdquo; After day 3, move to monthly check-in. Do not abandon — roofing decisions sometimes take 2-3 weeks for insurance-related jobs.</p>
<h2>What the top 10% of roofers do differently</h2>
<p>Top closers show up on time, present a written proposal during or immediately after the estimate visit, address objections before the homeowner raises them (&ldquo;you're probably wondering about the price vs. the other quotes you'll get&rdquo;), and make the next step specific and confirmed, not vague. They also stay in contact through the insurance adjuster process and treat the estimate as the beginning of the relationship, not a transaction to win or lose.</p>
<p>For the top of the funnel — getting more estimates in the first place — see <a href="/roofing-leads/">exclusive roofing leads</a> and <a href="/appointment-setting/roofing/">roofing appointment setting</a>.</p>
<hr>
<p><em>More estimates on the calendar: <a href="/appointment-setting/roofing/">roofing appointment setting</a> books pre-screened inspections straight to your calendar.</em></p>"""))

# PAGE 12
PAGES.append(("lead-follow-up-sequence-for-contractors",
"Lead Follow-Up Sequence for Contractors: Close 40% More Jobs",
"The exact lead follow-up sequence home service contractors should use: day-by-day timing, call scripts, text templates, and how to keep warm leads from going cold.",
"The Lead Follow-Up Sequence That Closes 40% More Contractor Jobs",
"Lead Follow-Up Sequence",
"""<p>Most contractor leads do not close because the follow-up stops too early. Research consistently shows that 80% of sales require at least five follow-up attempts, but most contractors give up after one or two. The homeowner is not lost — they are still warm, still interested, and still going to hire someone. That someone is whoever stays in front of them long enough.</p>
<h2>The 14-day follow-up sequence</h2>
<p><strong>Day 0 (lead received):</strong> Call within 5 minutes. If voicemail, leave a concise message with your name, the service they inquired about, and a specific callback number. Send a text immediately after: &ldquo;Hi [name], this is [your name] from [company]. Just called about your [service] request. Call or text me at [number] anytime.&rdquo;</p>
<p><strong>Day 1:</strong> Second call, different time of day. Morning and afternoon. If still no answer, send a text: &ldquo;Still happy to help with [service]. When is a good time to connect?&rdquo;</p>
<p><strong>Day 3:</strong> Call plus value-add text. &ldquo;Hi [name], following up on the [service] quote. I wanted to mention — [relevant tip or local info, e.g., 'with the weather this week, roof repairs go faster with dry days']. Let me know if you'd like to get the estimate scheduled.&rdquo;</p>
<p><strong>Day 7:</strong> Email or text with a soft offer: &ldquo;Still available this week if you want to get [service] taken care of before [season/weather/event]. No pressure — just want to make it easy.&rdquo;</p>
<p><strong>Day 14:</strong> Final active follow-up. Keep it simple and leave the door open. &ldquo;Just checking in one last time. I'll stop reaching out unless you want me to, but I'm here whenever the timing is right.&rdquo; Then move to monthly check-ins.</p>
<h2>Monthly check-in cadence (weeks 4+)</h2>
<p>For homeowners who did not close in 14 days, monthly touches keep you top of mind for when they are ready. One text or email per month is not annoying — it is what separates contractors who get referrals from contractors who get forgotten. A simple &ldquo;Checking in — any [service] needs this month?&rdquo; is sufficient. Personalize when you can: reference the original inquiry, their address, or a local event.</p>
<h2>What to track</h2>
<p>Use a simple spreadsheet or CRM to log every lead with: date received, follow-up dates, outcome notes. The most valuable metric to track is contact rate (how many leads you actually reached) and conversion rate by follow-up attempt number. Most contractors find that attempt 3-5 converts at nearly the same rate as attempt 1-2, confirming that stopping at two attempts is burning half the pipeline.</p>
<h2>Tools that automate the sequence</h2>
<p>CRMs like Jobber, ServiceTitan, and HouseCall Pro have built-in follow-up automation. Simple setups: Podium or Birdeye for text automation, Mailchimp for monthly email check-ins. If you want zero technology: a weekly review of your lead log with a commitment to call anyone from the prior week who has not been reached three times.</p>
<p>If your team cannot execute a consistent follow-up sequence because of bandwidth, <a href="/appointment-setting/">appointment setting</a> handles the first-contact problem at the point of lead delivery. The homeowner is already scheduled before you see the lead.</p>
<hr>
<p><em>Get more leads into your follow-up sequence: <a href="/contractor-leads/">exclusive contractor leads</a> mean no one else is running a competing sequence on the same prospect.</em></p>"""))

# PAGE 13
PAGES.append(("contractor-lead-generation-guide",
"Contractor Lead Generation Guide 2026: Every Model, Cost, and ROI Breakdown",
"Complete contractor lead generation guide for 2026: pay-per-call, appointment setting, Google LSA, Angi, SEO, and Facebook Ads — costs, close rates, and ROI for each.",
"Contractor Lead Generation Guide 2026: Every Model, Cost, and ROI Breakdown",
"Contractor Lead Generation Guide",
"""<p>There is no single best lead generation model for every contractor. The best model depends on your trade, your close rate, how fast your office answers calls, and how much risk you can absorb while you wait for SEO to build. This guide covers every model available in 2026, what each costs, and what return to expect.</p>
<h2>The five lead generation models available to contractors</h2>
<p><strong>1. Exclusive pay-per-call.</strong> You receive live inbound phone calls from homeowners who are actively seeking your service. The call goes exclusively to your number. No other contractor is in the pool. Cost per call: $35–$120 depending on vertical and market. Close rate: 25–45%. Cost per job: $100–$300. Best for: contractors with responsive offices who close well on live calls.</p>
<p><strong>2. Appointment setting.</strong> A team calls leads, qualifies them, and books confirmed appointments on your calendar. You skip the call-to-estimate conversion. Cost per appointment: $100–$200. Close rate: 50–70%. Cost per job: $150–$350. Best for: busy contractors who cannot handle inbound calls consistently, or those who want zero follow-up required.</p>
<p><strong>3. Google Local Services Ads (LSA).</strong> Your business appears at the top of Google search for local queries. Google Guaranteed badge. Pay per lead. Cost per lead: $25–$100. Close rate: 15–30% (homeowner may have called multiple LSA advertisers). Cost per job: $150–$500. Best for: established businesses with strong reviews and fast call response.</p>
<p><strong>4. Shared marketplace leads (Angi, HomeAdvisor, Thumbtack).</strong> Leads sold to multiple contractors simultaneously. Cost per lead: $15–$80. Close rate: 3–8%. Cost per job: $300–$1,000+. Best for: price-testing markets and building review platforms — not for primary lead volume in competitive trades.</p>
<p><strong>5. Organic (SEO + Google Business Profile).</strong> Build search rankings and a strong GBP presence to generate inbound calls at zero per-lead cost. Time to results: 6–18 months. Cost: agency or time investment upfront, then near-zero per call. Close rate: 35–60% (highest intent of all sources). Best for: long-term cost reduction; not a substitute for immediate volume.</p>
<h2>Cost per job comparison across all models</h2>
<table>
<tr><th>Model</th><th>Avg cost/lead</th><th>Close rate</th><th>Cost per job</th><th>Speed to first job</th></tr>
<tr><td>Exclusive call</td><td>$60</td><td>32%</td><td>$188</td><td>Days</td></tr>
<tr><td>Booked appointment</td><td>$140</td><td>60%</td><td>$233</td><td>Days</td></tr>
<tr><td>Google LSA</td><td>$55</td><td>22%</td><td>$250</td><td>Weeks</td></tr>
<tr><td>Shared marketplace</td><td>$30</td><td>6%</td><td>$500</td><td>Days</td></tr>
<tr><td>Organic / SEO</td><td>$0/call (after buildup)</td><td>50%</td><td>$0–$30 long-term</td><td>6–18 months</td></tr>
</table>
<h2>How to choose based on your situation</h2>
<p>New contractor, no pipeline: Start with exclusive pay-per-call or appointment setting for immediate volume while building reviews and Google Business Profile in parallel. Established contractor, slow season: Layer appointment setting on top of existing LSA to fill calendar gaps. Growing from 5 to 20 jobs/week: Exclusive pay-per-call scales linearly — set your volume target and increase budget. Reducing long-term cost: Invest in SEO now; it takes a year but produces the cheapest leads over a 3-5 year horizon.</p>
<h2>The metrics that matter</h2>
<p>Track these three numbers across every lead source: cost per lead, close rate per source, and cost per booked job. Do not aggregate — break it down per channel. Most contractors find two or three sources that work well and one or two that waste budget. Cutting the underperformers and doubling down on the winners is how you scale without increasing total spend.</p>
<p>For vertical-specific guides: <a href="/roofing-leads/">roofing leads</a>, <a href="/fence-leads/">fence leads</a>, <a href="/landscaping-leads/">landscaping leads</a>, <a href="/pest-control-leads/">pest control leads</a>, <a href="/garage-door-repair-leads/">garage door leads</a>. For the exclusive model that powers the top two options: <a href="/pay-per-call/">pay-per-call</a> and <a href="/appointment-setting/">appointment setting</a>.</p>"""))

# PAGE 14
PAGES.append(("roofing-leads-texas",
"Roofing Leads in Texas: Exclusive Pay-Per-Call for TX Contractors | 2026",
"Exclusive roofing leads in Texas — Dallas, Houston, San Antonio, Austin, and beyond. Hail season, storm damage, and year-round roofing demand. Pay per call only.",
"Roofing Leads in Texas: Exclusive Pay-Per-Call for TX Contractors",
"Roofing Leads Texas",
"""<p>Texas is the highest-volume roofing market in the United States. Hail season in the DFW metroplex alone generates more roofing demand than most entire states. Storm damage from spring hail, hurricane remnants on the Gulf Coast, and a year-round replacement cycle driven by extreme heat and temperature swings make Texas the most important state for any roofing contractor looking to scale.</p>
<h2>Texas roofing market by region</h2>
<p><strong>Dallas-Fort Worth:</strong> The nation's largest hail market. DFW sits in Hail Alley — the band from Texas through Colorado that sees the highest frequency of large hail events in North America. A single major hailstorm can generate 5,000-10,000+ insurance roofing claims in one evening. Contractors from across the country mobilize for DFW hail events. Exclusive leads are critical here because storm-chasing competition is extreme during events.</p>
<p><strong>Houston:</strong> Gulf Coast hurricane and tropical storm exposure combined with one of the country's fastest-growing metro populations. High demand year-round with storm spikes. Insurance claims are common. Lead costs run higher during and after named storms.</p>
<p><strong>San Antonio:</strong> Hail exposure plus rapid suburban expansion. Growing market with less saturation than DFW. Good ground for contractors building steady volume rather than chasing storm peaks.</p>
<p><strong>Austin:</strong> Fast-growing metro with high housing values and homeowners willing to invest in premium roofing materials. Less hail exposure than DFW but strong steady-state replacement demand. Ice storm events (like the 2021 winter storm) generate surge demand.</p>
<h2>Texas roofing lead costs</h2>
<table>
<tr><th>Region</th><th>Standard season CPL</th><th>Post-storm CPL</th></tr>
<tr><td>DFW</td><td>$45–$75</td><td>$100–$200+</td></tr>
<tr><td>Houston</td><td>$40–$70</td><td>$80–$160</td></tr>
<tr><td>San Antonio</td><td>$35–$60</td><td>$70–$130</td></tr>
<tr><td>Austin</td><td>$40–$65</td><td>$75–$140</td></tr>
</table>
<h2>How exclusive leads perform differently in Texas storm markets</h2>
<p>During hail events, shared lead platforms flood with contractors. HomeAdvisor and Angi leads in DFW after a storm can go to 6+ contractors within minutes. Homeowners stop answering because they have been called six times. Your response rate on shared leads plummets exactly when volume is highest.</p>
<p>Exclusive pay-per-call campaigns dedicated to your number maintain their performance regardless of storm volume. You pay more per call in peak season, but you are talking to homeowners who are reaching out to you specifically, not everyone. Close rates stay at 25-35% even during peak competitive periods.</p>
<h2>Getting started with Texas roofing leads</h2>
<p>RankLocal's Texas roofing campaigns cover all major metros and can be set up by city, zip code, or county. Service area and job type filters ensure you receive calls for work you want — replacements, repairs, storm damage, or specific materials. <a href="/roofing-leads/">See all exclusive roofing lead options</a> or <a href="/appointment-setting/roofing/">get pre-screened roofing appointments</a> booked directly on your calendar.</p>
<hr>
<p><em>Texas roofers: get exclusive calls for your market. <a href="/#contact">Talk to RankLocal about Dallas, Houston, San Antonio, or Austin campaigns</a>.</em></p>"""))

# PAGE 15
PAGES.append(("roofing-leads-florida",
"Roofing Leads in Florida: Exclusive Leads for FL Roofers | 2026",
"Exclusive roofing leads in Florida — Miami, Tampa, Orlando, Jacksonville. Hurricane season, wind damage, and year-round roofing demand for FL contractors.",
"Roofing Leads in Florida: Exclusive Leads for FL Roofers",
"Roofing Leads Florida",
"""<p>Florida is the most storm-exposed roofing market in the country and one of the highest-demand states for year-round roofing work. Hurricane season runs June through November, but the combination of UV degradation, high humidity, and frequent rain means Florida roofs age faster than most of the country. Florida roofers face both the opportunity of a huge market and the challenge of intense competition, especially after named storms.</p>
<h2>Florida roofing demand by region</h2>
<p><strong>Miami-Dade and Broward:</strong> The country's most strict building code market after Hurricane Andrew (1992). Roof replacements require code-compliant systems that command premium prices. Post-hurricane demand after Ian, Idalia, and subsequent storms drove massive backlogs. High homeowner values mean close rates are good; high competition means exclusive sourcing is critical.</p>
<p><strong>Tampa Bay:</strong> Hit hard by Hurricane Milton in 2024. Active insurance claims market with strong demand for both repair and full replacement. Growing population driving steady new construction and replacement demand alongside storm work.</p>
<p><strong>Orlando and Central Florida:</strong> Away from the immediate coast but still exposed to storm damage and tropical storm remnants. Steady year-round demand driven by one of the country's fastest-growing housing markets.</p>
<p><strong>Jacksonville:</strong> Less storm exposure than the coast but significant roofing market with a large military and suburban population. Strong steady-state replacement demand.</p>
<h2>Florida roofing lead costs</h2>
<table>
<tr><th>Region</th><th>Standard season</th><th>Hurricane season peak</th></tr>
<tr><td>Miami/Broward</td><td>$50–$90</td><td>$120–$250+</td></tr>
<tr><td>Tampa Bay</td><td>$45–$75</td><td>$100–$200</td></tr>
<tr><td>Orlando</td><td>$40–$65</td><td>$80–$150</td></tr>
<tr><td>Jacksonville</td><td>$35–$60</td><td>$65–$120</td></tr>
</table>
<h2>Insurance claims and the Florida roofing market</h2>
<p>Florida is the most litigated homeowners insurance market in the country. This has had a complex effect on roofing: many carriers have pulled out of the state, premiums have surged, and homeowners are often navigating complex claims processes. Contractors who understand insurance adjuster meetings, can assist with supplement documentation, and work well with public adjusters win significantly more jobs. Position your estimate process around claims expertise, not just roof price.</p>
<p>For exclusive roofing leads that target Florida markets regardless of season, see <a href="/roofing-leads/">the full roofing leads program</a>. For appointments pre-screened for insurance claims leads specifically, <a href="/appointment-setting/roofing/">roofing appointment setting</a> can filter by job type.</p>
<hr>
<p><em>Florida roofers: exclusive calls in your market. <a href="/#contact">Contact RankLocal about Miami, Tampa, Orlando, or Jacksonville campaigns</a>.</em></p>"""))

# PAGE 16
PAGES.append(("roofing-leads-georgia",
"Roofing Leads in Georgia: Exclusive Leads for GA Roofers | 2026",
"Exclusive roofing leads in Georgia — Atlanta, Savannah, Augusta, Macon. Storm damage, year-round replacements, and fast-growing suburban markets for GA contractors.",
"Roofing Leads in Georgia: Exclusive Leads for GA Roofers",
"Roofing Leads Georgia",
"""<p>Georgia's roofing market has grown significantly with Atlanta's population boom and the state's exposure to severe thunderstorms, occasional tornadoes, and ice events in the north. Atlanta's northern suburbs — Marietta, Alpharetta, Roswell, Kennesaw — represent some of the highest-density roofing demand in the Southeast, driven by aging housing stock from the 1980s and 1990s boom alongside active storm damage claims.</p>
<h2>Georgia roofing market breakdown</h2>
<p><strong>Metro Atlanta:</strong> The fastest-growing major metro in the Southeast means constant new construction demand alongside a large replacement market. Northern suburbs see the most hail exposure. The I-20 corridor in DeKalb and Rockdale counties generates consistent storm damage work after spring storm seasons.</p>
<p><strong>Savannah and coastal Georgia:</strong> Hurricane exposure similar to Florida's northern counties. Post-storm surge demand after major systems. Growing Lowcountry market with significant real estate investment activity.</p>
<p><strong>Augusta and Macon:</strong> Steady mid-size market demand with less seasonal variation than coastal regions. Strong demand for basic repair and full replacement from older housing stock.</p>
<h2>Georgia roofing lead costs</h2>
<table>
<tr><th>Region</th><th>Cost per call</th><th>Storm spike</th></tr>
<tr><td>Metro Atlanta</td><td>$40–$70</td><td>$85–$150</td></tr>
<tr><td>Savannah</td><td>$35–$60</td><td>$70–$130</td></tr>
<tr><td>Augusta/Macon</td><td>$30–$55</td><td>$60–$110</td></tr>
</table>
<h2>Storm season in Georgia</h2>
<p>Georgia's storm season peaks in spring (March through May) with severe thunderstorm activity across the northern half of the state. Atlanta sits in a zone that sees frequent hail-producing storms. Unlike Texas where a single storm can cover an entire metro, Georgia storms are often isolated cells that affect specific neighborhoods — which means geographic targeting by zip code is important for maximizing lead relevance.</p>
<p><a href="/roofing-leads/">Get exclusive Georgia roofing leads</a> with zip code targeting for your service area, or <a href="/appointment-setting/roofing/">book pre-screened estimates</a> for your Georgia market.</p>
<hr>
<p><em>Georgia roofers: <a href="/#contact">set up your exclusive campaign for Atlanta, Savannah, or wherever you work</a>.</em></p>"""))

# PAGE 17
PAGES.append(("insurance-roofing-leads",
"Insurance Roofing Leads: Exclusive Storm Damage Claims Leads for Roofers",
"Insurance roofing leads for storm damage contractors: exclusive calls and appointments for homeowners with active insurance claims. How to close insurance jobs faster.",
"Insurance Roofing Leads: Exclusive Storm Damage Claims Leads for Roofers",
"Insurance Roofing Leads",
"""<p>Insurance roofing leads are a separate buying cycle from standard roofing leads. The homeowner is not shopping price — they are navigating a process. Their insurance company will pay most or all of the cost. Their primary concern is whether you know how to work with their carrier, whether you can be there for the adjuster meeting, and whether you will handle the paperwork. The contractor who understands this wins at a completely different rate than the contractor trying to compete on price.</p>
<h2>What makes insurance roofing leads different</h2>
<p>Standard roofing leads: homeowner is self-funding, comparing prices, deciding whether to do the work at all. Insurance roofing leads: homeowner has damage, is filing a claim, and is specifically looking for a contractor experienced with the insurance process. The job is effectively pre-sold. The question is whether they choose you or your competitor.</p>
<p>Close rates on insurance roofing leads that are properly positioned run 35-55%, significantly above the 25-30% average for standard replacement calls. The trade-off is a longer sales cycle — the typical insurance roofing job takes 30-90 days from initial contact to final payment as the claim processes.</p>
<h2>How to win insurance roofing leads</h2>
<p>The four statements that win insurance roofing leads: (1) &ldquo;We'll be there for your adjuster meeting to make sure nothing gets missed on the claim.&rdquo; (2) &ldquo;We work directly with your insurance company — you won't have to handle the paperwork.&rdquo; (3) &ldquo;We have experience with [their carrier's name].&rdquo; (4) &ldquo;We supplement claims when adjusters miss items, which means you get what you're entitled to.&rdquo;</p>
<p>Adjuster meeting presence is the highest-leverage tactic. Contractors who attend adjuster meetings recover significantly more on claims than those who do not. When you are at the meeting, you document additional damage, ensure the scope is complete, and build a relationship with the homeowner that makes you the obvious choice once the check arrives.</p>
<h2>Storm damage lead generation timing</h2>
<p>The first 48-72 hours after a storm are the highest-conversion window for insurance leads. Homeowners are freshly aware of damage, neighbors are talking, adjusters are being scheduled. Being in front of them in this window through exclusive pay-per-call means you arrive before the insurance company has reset their expectations on contractor choice.</p>
<p>After the initial window, a second surge occurs when claim checks arrive — typically 3-6 weeks post-storm. A pipeline of leads from the initial storm event that you stayed in front of during the claims process converts strongly in this second wave.</p>
<p>For exclusive insurance roofing leads by market, see <a href="/roofing-leads/">the roofing leads program</a>. For storm-specific sub-verticals, see <a href="/storm-damage-roofing-leads/">storm damage roofing leads</a>.</p>
<hr>
<p><em>Specialize in insurance work? <a href="/#contact">Talk to RankLocal about campaign targeting for storm damage and insurance claims leads in your market.</a></em></p>"""))

# PAGE 18
PAGES.append(("tree-service-leads",
"Tree Service Leads: Exclusive Pay-Per-Call for Arborists and Tree Removal Companies",
"Exclusive tree service leads for arborists and tree removal companies. Pay-per-call and appointment setting for emergency removal, storm damage, and scheduled trimming.",
"Tree Service Leads: Exclusive Pay-Per-Call for Arborists and Tree Removal Companies",
"Tree Service Leads",
"""<p>Tree service leads split into two very different markets: emergency removal (a tree fell, there is danger, it needs to come down today) and scheduled work (trimming, health assessment, stump removal, preventive removal before storm season). Emergency tree removal leads have the highest conversion rate in home services — a homeowner with a tree on their house is not shopping. They are calling whoever answers first and can come today.</p>
<h2>Emergency tree removal leads</h2>
<p>Emergency tree leads are triggered by storms, high winds, diseased trees failing suddenly, and trees encroaching on structures. These calls are urgent and high-value. The typical emergency tree removal job runs $800-$3,000+ depending on tree size and access. Close rate on exclusive emergency calls is often 50-70% because there is essentially no price shopping — the homeowner needs it done now.</p>
<p>Response time is the most critical variable. Emergency tree calls that go unanswered for 15 minutes will be answered by the next contractor in the homeowner's search results. Exclusive pay-per-call matters especially here because shared marketplace leads on emergency jobs go to five companies simultaneously, and whoever answers first gets the job regardless of any other factor.</p>
<h2>Scheduled tree service leads</h2>
<p>Seasonal trimming, tree health assessments, stump grinding, and preventive removal generate consistent year-round demand with spring and fall peaks. These homeowners have more patience than emergency callers but still want to book quickly. Close rate on exclusive calls: 25-40%. Job value: $400-$2,000+ depending on scope.</p>
<p>Appointment setting works particularly well for scheduled tree services. A homeowner who called to discuss trimming or stump removal and was booked for an on-site estimate is much further down the sales funnel than a form fill. <a href="/appointment-setting/">See how appointment setting works for tree service companies</a>.</p>
<h2>Geographic patterns in tree service demand</h2>
<p>Storm-prone markets (Southeast, Gulf Coast, Midwest tornado belt) generate the highest emergency volume. Pacific Northwest and Northeast markets have high arborist demand for hazardous tree assessment and health management. The Mountain West generates significant fire-risk tree removal work. RankLocal's tree service campaigns can be targeted by job type and geographic market.</p>
<h2>Tree service lead costs</h2>
<table>
<tr><th>Lead type</th><th>Cost per call</th><th>Typical close rate</th><th>Cost per job</th></tr>
<tr><td>Emergency removal (exclusive)</td><td>$45–$80</td><td>55%</td><td>$100–$150</td></tr>
<tr><td>Scheduled trimming (exclusive)</td><td>$35–$60</td><td>30%</td><td>$120–$200</td></tr>
<tr><td>Booked appointment</td><td>$100–$150</td><td>60%</td><td>$167–$250</td></tr>
</table>
<p>For tree service companies with fast emergency response, exclusive pay-per-call is the highest-ROI model. For companies with more scheduled work and inconsistent call coverage, appointment setting removes the response speed bottleneck. See the full <a href="/contractor-leads/">contractor leads hub</a> or <a href="/#contact">talk to RankLocal about your tree service market</a>.</p>
<hr>
<p><em>Exclusive tree service calls in your market: <a href="/#contact">set up your campaign with RankLocal</a>.</em></p>"""))

# PAGE 19
PAGES.append(("solar-roofing-leads",
"Solar Roofing Leads: Exclusive Pay-Per-Call for Solar + Roofing Contractors",
"Exclusive solar roofing leads for contractors who combine roof replacement with solar installation. Pay-per-call campaigns for the high-LTV solar+roofing market.",
"Solar Roofing Leads: Exclusive Pay-Per-Call for Solar + Roofing Contractors",
"Solar Roofing Leads",
"""<p>Solar roofing is the highest-LTV job type available to roofing contractors. A combined roof replacement and solar installation runs $25,000–$60,000+. The homeowner is not shopping for the cheapest contractor — they are looking for someone they trust to do a complex job correctly. Exclusive leads matter more here because a homeowner with a $40,000 job in mind is going to do some research before committing, and whoever contacts them first and builds the most trust wins.</p>
<h2>The solar roofing opportunity</h2>
<p>Utility rate inflation, federal and state solar tax incentives, and homeowners who want to address both an aging roof and rising energy costs simultaneously have created a strong pipeline for contractors who offer the combined service. Roofing contractors with solar installation capability (or solar subcontractor relationships) can access this market. Pure solar installers who add roofing capability are entering from the other direction.</p>
<p>The close cycle is longer than standard roofing — 2-6 weeks from first contact to signed contract is normal. This means follow-up sequence matters: a homeowner who expressed interest in solar+roofing but did not close immediately should remain in your pipeline for months, not days.</p>
<h2>Solar roofing lead costs and conversion</h2>
<table>
<tr><th>Lead type</th><th>Cost per call</th><th>Close rate</th><th>Avg job value</th></tr>
<tr><td>Exclusive solar roofing call</td><td>$75–$140</td><td>15–25%</td><td>$30,000–$50,000</td></tr>
<tr><td>Booked solar+roof appointment</td><td>$200–$350</td><td>40–55%</td><td>$30,000–$50,000</td></tr>
</table>
<p>Even at a 15% close rate, a $120 exclusive call with a $35,000 average job produces a cost per job of $800 and an LTV that justifies significant per-lead cost. Solar roofing is a case where the math on appointment setting is also very strong — at $300 per booked appointment with a 45% close rate, your cost per job is $667 on a $35,000 average.</p>
<h2>Markets with highest solar roofing demand</h2>
<p>California, Texas, Florida, Arizona, Colorado, and New Jersey lead in solar adoption. Federal ITC (Investment Tax Credit) availability drives national demand, but state-level incentives, net metering policies, and utility rate levels vary significantly by state and affect close rates. California and Arizona have the most established markets; Texas is rapidly expanding.</p>
<p>See <a href="/roofing-leads/">exclusive roofing leads</a> and <a href="/appointment-setting/roofing/">roofing appointment setting</a> for program details, or <a href="/#contact">ask RankLocal about solar+roofing campaign targeting in your market</a>.</p>"""))

# PAGE 20
PAGES.append(("irrigation-leads",
"Irrigation Leads: Exclusive Pay-Per-Call for Irrigation and Sprinkler Contractors",
"Exclusive irrigation leads for sprinkler and irrigation contractors. Pay-per-call and appointment setting for new installs, repairs, and spring startups.",
"Irrigation Leads: Exclusive Pay-Per-Call for Irrigation and Sprinkler Contractors",
"Irrigation Leads",
"""<p>Irrigation leads fall into three categories with distinct seasonality and buying patterns: new system installations, repair and maintenance calls, and spring startup and fall winterization service. Each has different conversion economics and each benefits from exclusive lead delivery for different reasons.</p>
<h2>New irrigation system installs</h2>
<p>New install leads are the highest-value irrigation jobs, running $3,000–$15,000+ depending on property size and system complexity. These homeowners are in planning mode — they may have researched for weeks before calling. Close cycle is 1–3 weeks. Close rate on exclusive calls: 25–35%. The homeowner is often getting two or three estimates but is not in emergency mode, so your sales process matters more than raw speed.</p>
<h2>Repair and emergency calls</h2>
<p>Sprinkler repair calls — broken heads, controller failures, pipe leaks, zone issues — are urgent, lower ticket ($150–$800), and highly speed-sensitive. The homeowner whose sprinkler system failed the week before summer wants it fixed this week. Exclusive calls on repair leads convert at 45–60% because there is urgency and no time for extended comparison shopping. These are the highest-ROI irrigation calls on a cost-per-job basis.</p>
<h2>Spring startup and fall winterization</h2>
<p>Seasonal service calls are the most geographic and weather-dependent irrigation leads. In freeze-climate markets (Colorado, Minnesota, Midwest), fall blowouts and spring startups drive enormous volume in compressed 4–6 week windows. Exclusive pay-per-call in these markets during the window is extremely efficient because homeowners are actively seeking services simultaneously and exclusivity prevents the race.</p>
<h2>Irrigation lead costs</h2>
<table>
<tr><th>Service type</th><th>Cost per call</th><th>Close rate</th><th>Avg job value</th></tr>
<tr><td>New install</td><td>$50–$90</td><td>28%</td><td>$5,000+</td></tr>
<tr><td>Repair/emergency</td><td>$35–$65</td><td>50%</td><td>$300</td></tr>
<tr><td>Seasonal service</td><td>$25–$45</td><td>55%</td><td>$150</td></tr>
</table>
<p>Irrigation companies often benefit from combining exclusive call campaigns for repair/emergency volume (highest conversion) with appointment setting for new install estimates (highest value). <a href="/landscaping-leads/">See landscaping leads</a> for broader context or <a href="/#contact">contact RankLocal about irrigation campaigns in your market</a>.</p>"""))

# PAGE 21
PAGES.append(("hardscaping-leads",
"Hardscaping Leads: Exclusive Leads for Patio, Retaining Wall, and Outdoor Living Contractors",
"Exclusive hardscaping leads for contractors installing patios, retaining walls, driveways, and outdoor living spaces. Pay-per-call and appointment setting.",
"Hardscaping Leads: Exclusive Pay-Per-Call for Outdoor Living Contractors",
"Hardscaping Leads",
"""<p>Hardscaping is one of the highest-ticket landscaping services — patios, retaining walls, driveways, walkways, and outdoor living spaces run from $5,000 for a small patio to $80,000+ for a full outdoor kitchen and entertainment space. These are discretionary, high-consideration purchases where the homeowner spends weeks or months planning before the first contractor call. Exclusive leads matter enormously here because the homeowner is evaluating you, not just taking the first callback.</p>
<h2>The hardscaping sales cycle</h2>
<p>The typical hardscaping close cycle runs 2–6 weeks. Homeowners often gather 2-3 estimates, review portfolios, check references, and discuss the project with their spouse or partner. This is a relationship-driven sale where the estimate visit matters as much as the price. Contractors who bring design sketches, material samples, and references to the first meeting close at significantly higher rates than those who quote only from description.</p>
<p>Because the sales cycle is longer, appointment setting — where the prospect is pre-screened and already expecting your visit — outperforms cold inbound calls for hardscaping. The conversion on a booked hardscaping estimate runs 40–60% versus 20–30% on a live call, because the homeowner has already been qualified and committed to a time before you arrive.</p>
<h2>Hardscaping lead costs and economics</h2>
<table>
<tr><th>Lead type</th><th>Cost per lead</th><th>Close rate</th><th>Avg job value</th></tr>
<tr><td>Exclusive call</td><td>$60–$100</td><td>22%</td><td>$12,000</td></tr>
<tr><td>Booked appointment</td><td>$150–$250</td><td>50%</td><td>$12,000</td></tr>
</table>
<p>At $12,000 average job value, even a $200 booked appointment at 50% close rate gives you a $400 cost per job on a $12,000 project — exceptional ROI. This is the vertical where appointment setting delivers its clearest math advantage over cold calls.</p>
<h2>Seasonal patterns</h2>
<p>Hardscaping demand peaks in spring (homeowners planning for summer entertaining) and again in late summer (planning fall installs before ground freezes). In warm-climate markets (Southeast, Southwest), demand is year-round. Northern markets compress demand into April–October.</p>
<p>See <a href="/landscaping-leads/">landscaping leads</a> for the broader outdoor services market, or <a href="/appointment-setting/">appointment setting</a> for the highest-conversion hardscaping lead model.</p>"""))

# PAGE 22
PAGES.append(("mosquito-control-leads",
"Mosquito Control Leads: Exclusive Pay-Per-Call for Mosquito Treatment Companies",
"Exclusive mosquito control leads for pest companies and mosquito treatment specialists. Pay-per-call and appointment setting for recurring treatment plans.",
"Mosquito Control Leads: Exclusive Pay-Per-Call for Mosquito Treatment Companies",
"Mosquito Control Leads",
"""<p>Mosquito control is one of the fastest-growing pest control segments in the United States. Demand spikes from April through October in most markets, with year-round activity in the Deep South. The business model is particularly attractive because mosquito treatment converts to recurring service plans at high rates — a homeowner who signs up for monthly barrier spray treatments generates annual revenue of $400–$800 from one acquisition.</p>
<h2>Mosquito control lead types</h2>
<p><strong>One-time event treatment:</strong> Homeowners with outdoor events — weddings, parties, graduation celebrations — who want mosquito-free yards for a single day. High urgency, moderate job value ($150–$300), and occasional conversion to recurring plan. Fast response is critical here.</p>
<p><strong>Seasonal recurring plans:</strong> The primary revenue driver. Homeowners who want consistent yard protection through the season sign monthly or bimonthly service agreements. LTV is $400–$1,200 per year. This is the lead that justifies the highest acquisition cost.</p>
<p><strong>Tick and mosquito combo:</strong> Increasingly popular as tick-borne illness awareness grows. Bundle pricing. Higher value per plan. Growing demand in Northeastern and Midwestern markets particularly.</p>
<h2>Why exclusivity matters specifically for mosquito control</h2>
<p>Mosquito control leads bought from shared platforms like Angi land simultaneously with multiple competitors. Most homeowners who request quotes will go with whoever calls first and sounds professional. At $500 annual LTV, losing a potential customer to a competitor because they answered first costs you $500 per year indefinitely. The math on exclusive leads is particularly strong when recurring service revenue is in the calculation.</p>
<h2>Mosquito control lead costs</h2>
<table>
<tr><th>Lead type</th><th>Cost per call</th><th>Close rate</th><th>Annual LTV</th></tr>
<tr><td>Exclusive call (recurring)</td><td>$40–$70</td><td>35%</td><td>$600</td></tr>
<tr><td>Booked appointment</td><td>$90–$140</td><td>60%</td><td>$600</td></tr>
</table>
<p>See <a href="/pest-control-leads/">pest control leads</a> for the full pest management vertical, or <a href="/#contact">contact RankLocal about mosquito control campaigns in your market</a>.</p>"""))

# PAGE 23
PAGES.append(("bee-removal-leads",
"Bee Removal Leads: Exclusive Pay-Per-Call for Beekeepers and Pest Control Companies",
"Exclusive bee removal leads for pest control and beekeeping companies. Pay-per-call for emergency hive removal, swarm capture, and structural removal.",
"Bee Removal Leads: Exclusive Pay-Per-Call for Bee Removal Specialists",
"Bee Removal Leads",
"""<p>Bee removal leads are highly urgent and highly exclusive by nature. A homeowner with an active beehive in their wall, a swarm in their tree, or bees entering their attic is not comparison shopping. They are calling whoever answers and sounds competent. This is one of the highest-conversion lead types available to pest control and beekeeping companies — exclusive calls on bee removal convert at 45–65%.</p>
<h2>Types of bee removal leads</h2>
<p><strong>Emergency swarm removal:</strong> Bees are swarming, visible in yard or on structure. High urgency but lower risk — swarms are usually docile. Job value: $150–$400. Very fast response required.</p>
<p><strong>Established hive removal:</strong> Bees have built a hive inside a structure (wall void, attic, chimney). Higher complexity, often requires opening the structure. Job value: $400–$1,500+. Homeowner is motivated by property damage and health concern.</p>
<p><strong>Beekeeping and live removal:</strong> Conservation-minded homeowners who specifically want bees relocated rather than exterminated. Often work with beekeepers rather than pest companies. Emerging niche market.</p>
<h2>Seasonality</h2>
<p>Bee removal demand peaks in spring and early summer (swarm season) and again in early fall (hive consolidation). The Southeast and Southwest see longer seasons. In most US markets, peak bee removal volume runs April through August.</p>
<h2>Bee removal lead costs</h2>
<table>
<tr><th>Lead type</th><th>Cost per call</th><th>Close rate</th><th>Avg job value</th></tr>
<tr><td>Exclusive emergency call</td><td>$35–$65</td><td>55%</td><td>$350</td></tr>
<tr><td>Booked appointment</td><td>$80–$120</td><td>70%</td><td>$600</td></tr>
</table>
<p>See <a href="/pest-control-leads/">pest control leads</a> for the full pest management vertical, or <a href="/#contact">ask RankLocal about bee removal campaigns in your market</a>.</p>"""))

# PAGE 24
PAGES.append(("roofing-leads-in-winter",
"How to Get Roofing Leads in Winter: Keeping the Pipeline Full Year-Round",
"Roofing leads in winter: strategies for roofers to maintain pipeline during slow season. Lead gen tactics, marketing angles, and how to close jobs even when demand drops.",
"How to Get Roofing Leads in Winter: Keeping the Pipeline Full Year-Round",
"Roofing Leads in Winter",
"""<p>Winter is roofing's weakest season in most of the country. Homeowners are not thinking about roof replacements in January. Storm season is over. Cold weather limits install days in northern markets. And yet the roofers who come out of winter strong are the ones who treated slow season as a strategic advantage, not a gap to wait out.</p>
<h2>Why winter roofing leads are actually a buying opportunity</h2>
<p>Competition collapses in winter. Roofing companies pull back marketing spend, reduce their lead buying, and shift crews to essential repairs. Google LSA auctions are cheaper. Pay-per-call volumes are lower but cost per call drops with them. The homeowner who does call in December or January is dealing with a real problem — a failing roof they noticed during the first cold snap — and they are not surrounded by five other roofers calling them back.</p>
<p>The close rate on winter roofing leads often exceeds spring and summer rates precisely because competition is thinner. A homeowner who decides to replace their roof in February is talking to fewer contractors and more motivated to commit before another season passes.</p>
<h2>Winter roofing lead strategies</h2>
<p><strong>Target late-storm follow-up leads.</strong> Fall hail and wind damage creates a pool of homeowners who were meaning to address roofing damage but put it off. December and January are when they get serious before insurance claim deadlines close. These are some of the warmest winter leads available.</p>
<p><strong>Focus on energy efficiency messaging.</strong> Winter is when homeowners feel heat loss through poor insulation and aging roofing systems. &ldquo;Is your old roof costing you money on heating bills this winter?&rdquo; is a legitimately relevant angle in December and January in cold climates.</p>
<p><strong>Book spring installations now.</strong> Many homeowners know they need a new roof by spring. Presenting a &ldquo;secure your spring slot now before schedule fills up&rdquo; offer closes jobs in winter that you will install in March and April. Deposit collected, job committed.</p>
<p><strong>Reduce cost-per-call with winter pricing.</strong> If you are using pay-per-call, winter is the most cost-effective time to buy. Competitors reduce spend; your budget goes further. The leads you close in January are at lower acquisition cost than the same leads in April.</p>
<h2>Geographic differences in winter demand</h2>
<p>In the South (Texas, Florida, Georgia, Carolinas), winter roofing season barely slows. Temperature rarely prevents installs. Marketing in these markets year-round without a winter pullback is the right call. In the Midwest and Northeast, February and March represent genuine install limitations but not demand limitations — homeowners are still making decisions and signing contracts even if installation waits for weather.</p>
<p>For roofing leads year-round including slower months, see <a href="/roofing-leads/">exclusive roofing leads</a>. For appointment setting that keeps your calendar full across all seasons, see <a href="/appointment-setting/roofing/">roofing appointment setting</a>.</p>
<hr>
<p><em>Don't let slow season mean no pipeline. <a href="/#contact">Talk to RankLocal about year-round roofing lead strategies for your market</a>.</em></p>"""))

# PAGE 25
PAGES.append(("what-is-cost-per-lead",
"What Is Cost Per Lead? (And Why CPL Alone Misleads Contractors)",
"What is cost per lead (CPL)? Definition, calculation, and why the real metric contractors should track is cost per job, not cost per lead. With roofing and fence examples.",
"What Is Cost Per Lead? (And Why CPL Alone Misleads Contractors)",
"What Is Cost Per Lead",
"""<p>Cost per lead (CPL) is the amount you pay to acquire one potential customer inquiry. Simple formula: total marketing spend divided by total leads received. If you spend $1,000 on lead generation and receive 20 leads, your CPL is $50. But CPL alone tells you almost nothing useful about whether your lead generation is working.</p>
<h2>How to calculate cost per lead</h2>
<p>The basic calculation: CPL = Total marketing spend ÷ Total leads received. If you are tracking multiple channels, calculate CPL separately per channel. A Google Ads CPL of $40 and an Angi CPL of $25 look different until you factor in what happens to those leads after they arrive.</p>
<h2>Why CPL is the wrong primary metric</h2>
<p>A $25 lead that converts at 5% costs you $500 per job. A $60 lead that converts at 30% costs you $200 per job. The $25 lead is cheaper. The $200 job is what actually matters. When contractors optimize for CPL instead of cost per job, they end up over-investing in cheap sources that do not close (Angi, HomeAdvisor) and under-investing in premium sources that do (exclusive pay-per-call, appointment setting).</p>
<p>This is the most common lead generation mistake in home services: buying cheaper leads that produce worse jobs and believing you are being financially responsible.</p>
<h2>The metric that replaces CPL: cost per booked job</h2>
<p>Cost per booked job = Total spend on source ÷ Number of jobs closed from that source. Track this separately for every lead source over 90 days. Most contractors who run this analysis discover their most expensive CPL source has the best cost per job, and their cheapest CPL source has the worst.</p>
<table>
<tr><th>Source</th><th>CPL</th><th>Close rate</th><th>Cost per job</th></tr>
<tr><td>Shared marketplace</td><td>$25</td><td>5%</td><td>$500</td></tr>
<tr><td>Exclusive call</td><td>$55</td><td>30%</td><td>$183</td></tr>
<tr><td>Booked appointment</td><td>$140</td><td>58%</td><td>$241</td></tr>
</table>
<h2>What affects close rate by lead source</h2>
<p>Exclusivity is the biggest factor: shared leads close at 3–8%, exclusive calls at 20–40%, booked appointments at 50–70%. Lead intent is the second factor: homeowners who called versus homeowners who filled out a form close at meaningfully different rates. Third is lead qualification — was the homeowner screened for your service area, job type, and timing before the lead was delivered to you.</p>
<p>For a model built entirely around cost per job rather than CPL, see <a href="/pay-per-call/">exclusive pay-per-call</a> and <a href="/what-is-exclusive-lead-generation/">what exclusive lead generation is</a>.</p>
<hr>
<p><em>Track your real cost per job. <a href="/#contact">Talk to RankLocal about what exclusive leads cost per job in your vertical and market</a>.</em></p>"""))

# PAGE 26
PAGES.append(("contractor-lead-generation-glossary",
"Contractor Lead Generation Glossary: 25 Terms Every Home Service Business Should Know",
"Complete contractor lead generation glossary: exclusive leads, CPL, cost per job, pay-per-call, appointment setting, TCPA, billable call, and 20 more key terms defined.",
"Contractor Lead Generation Glossary: 25 Terms Every Home Service Business Should Know",
"Lead Generation Glossary",
"""<p>Lead generation has its own vocabulary. Understanding these terms helps you evaluate lead sources, read contracts accurately, and avoid common mistakes when comparing providers.</p>
<h2>Core terms</h2>
<p><strong>Lead:</strong> A homeowner who has expressed interest in a home service by submitting a form, calling a number, or clicking a call-to-action. A lead is potential, not guaranteed work.</p>
<p><strong>Exclusive lead:</strong> A lead delivered to one contractor only. No other contractor receives the same inquiry. The defining characteristic is structural — the lead cannot be resold. See <a href="/what-is-exclusive-lead-generation/">exclusive lead generation explained</a>.</p>
<p><strong>Shared lead:</strong> A lead sold to multiple contractors simultaneously, typically 3–5. The homeowner gets called by everyone who purchased the lead. Close rates are low (3–8%) because of competition.</p>
<p><strong>Pay-per-call:</strong> A lead generation model where you pay for each inbound phone call from a homeowner, not for form fills or impressions. Calls are typically exclusive and carry higher intent than form-based leads. See <a href="/pay-per-call/">pay-per-call explained</a>.</p>
<p><strong>Appointment setting:</strong> A managed service that calls leads, qualifies them, and schedules confirmed appointments directly on your calendar. You receive ready-to-estimate prospects rather than raw leads. See <a href="/appointment-setting/">appointment setting explained</a>.</p>
<p><strong>Cost per lead (CPL):</strong> Total marketing spend divided by total leads received. Important but not the primary metric for evaluating lead quality. See <a href="/what-is-cost-per-lead/">why CPL misleads contractors</a>.</p>
<p><strong>Cost per job:</strong> Total marketing spend divided by number of jobs won. The correct primary metric for evaluating any lead generation source.</p>
<p><strong>Close rate:</strong> The percentage of leads that convert to a closed job. Shared leads: 3–8%. Exclusive calls: 20–40%. Booked appointments: 50–70%.</p>
<p><strong>Billable call:</strong> A call that meets the criteria for charging under your pay-per-call agreement. Usually requires a minimum duration (60–90 seconds) and correct service category. Non-billable calls (wrong number, too short, out of area) should not be charged. See <a href="/what-is-a-billable-call/">what is a billable call</a>.</p>
<p><strong>Lead quality:</strong> A subjective but important measure of how likely a lead is to become a job. High-quality leads: right service area, correct job type, homeowner not renter, immediate need. Low-quality leads: wrong area, vague request, outside your service category.</p>
<h2>Technical terms</h2>
<p><strong>Call tracking:</strong> Phone numbers used to attribute calls to specific marketing sources. If someone calls a number from a specific campaign, you know which campaign generated that call. Essential for measuring ROI per channel.</p>
<p><strong>Junk lead:</strong> A lead that does not meet your service criteria — wrong area, wrong service type, wrong homeowner type, or fraudulent. Most lead providers offer credits for confirmed junk leads.</p>
<p><strong>Lead credit:</strong> A refund or billing adjustment for a lead that does not meet agreed quality standards. Policies vary significantly by provider. Get the credit policy in writing before signing.</p>
<p><strong>Speed-to-lead:</strong> The time between a lead being delivered and your first contact attempt. Research shows leads contacted within 5 minutes convert at 5x the rate of leads contacted at 10 minutes. See <a href="/speed-to-lead-for-contractors/">speed-to-lead for contractors</a>.</p>
<p><strong>TCPA:</strong> Telephone Consumer Protection Act. Federal law governing consent requirements for calling consumers. Lead providers should obtain proper consent. Verify compliance with any lead source you use. See <a href="/tcpa-lead-compliance/">TCPA lead compliance</a>.</p>
<h2>Model-specific terms</h2>
<p><strong>Google Guaranteed:</strong> The badge earned by contractors who pass Google's verification process for Local Services Ads. Homeowners see the badge as a trust signal.</p>
<p><strong>LSA (Local Services Ads):</strong> Google's pay-per-lead ad product for local service providers. Appears above standard search ads. See <a href="/google-local-services-ads-for-contractors/">Google LSA for contractors</a>.</p>
<p><strong>Form fill:</strong> A lead generated when a homeowner submits an online form. Lower intent than a phone call. Almost always shared across multiple contractors in marketplace models.</p>
<p><strong>Inbound vs. outbound:</strong> Inbound leads are homeowners who reached out to you (called your number, filled out your form). Outbound leads require you to initiate contact. Inbound closes at significantly higher rates.</p>
<p><strong>Service area targeting:</strong> Restricting lead delivery to specific zip codes, cities, or counties where you operate. Critical for exclusive leads — receiving calls outside your area wastes budget and hurts close rate.</p>
<p><strong>Vertical:</strong> A specific trade or service category (roofing, fencing, pest control, etc.). Lead providers often price and deliver by vertical because competition and demand vary significantly by trade.</p>"""))

# PAGE 27
PAGES.append(("contractor-marketing-metrics-guide",
"The 7 Lead Generation Metrics Every Contractor Must Track in 2026",
"Stop measuring the wrong things. Learn the 7 lead generation metrics every contractor must track: cost per lead, cost per job, close rate, speed-to-lead, LTV, CAC, and appointment rate.",
"The 7 Lead Generation Metrics Every Contractor Must Track",
"Contractor Marketing Metrics Guide",
"""<p>Most contractors track the wrong numbers. They obsess over cost per lead — a metric that tells you nothing about whether a lead source is profitable — while ignoring the numbers that actually determine whether a marketing channel works.</p>
<p>Here are the seven metrics that matter.</p>
<h2>1. Cost per job won (not cost per lead)</h2>
<p>The single most important metric in contractor marketing. It answers: for every dollar I spend on this lead source, how many dollars do I win in revenue?</p>
<p>Formula: <strong>Total spend ÷ Jobs won = Cost per job</strong></p>
<p>Example: You spend $1,200 on a lead source in March. You win 4 jobs. Cost per job = $300.</p>
<p>Is $300 a good cost per job? It depends on your average job value. A roofing company averaging $8,000/job would find $300 excellent. A gutter cleaning company averaging $400/job would find it unsustainable.</p>
<p>Target: Cost per job should be 3–8% of average job value for most home service trades.</p>
<h2>2. Close rate by lead source</h2>
<p>Formula: <strong>Jobs won ÷ Leads received × 100 = Close rate %</strong></p>
<p>Track this separately for each lead source. A 15% close rate from one source and a 4% close rate from another tells you which source sends higher-intent prospects.</p>
<p>Benchmarks by lead type: Exclusive pay-per-call: 20–40%. Shared marketplace leads: 3–8%. Appointment setting: 50–70%. Referrals: 60–80%.</p>
<h2>3. Speed-to-lead</h2>
<p>The time between a lead being delivered and your first contact attempt. This is the metric most contractors ignore, and it's one of the highest-leverage levers you have.</p>
<p>Research benchmark: Leads contacted within 5 minutes convert at 5x the rate of leads contacted at 10 minutes. See <a href="/speed-to-lead-for-contractors/">the full speed-to-lead guide</a>.</p>
<p>Track this by logging call timestamps and comparing to lead delivery timestamps. If your average speed-to-lead is over 30 minutes, fix this before spending more on leads.</p>
<h2>4. Cost per lead (secondary metric)</h2>
<p>CPL matters — but only in context of your close rate. A $25 lead with a 3% close rate costs you $833 per job. A $90 lead with a 30% close rate costs you $300 per job. See <a href="/what-is-cost-per-lead/">the full CPL breakdown</a>.</p>
<p>Use CPL for budgeting and channel comparison. Never use it as your primary quality metric.</p>
<h2>5. Appointment set rate</h2>
<p>Formula: <strong>Appointments scheduled ÷ Leads received × 100 = Appointment rate %</strong></p>
<p>This metric reveals contact and qualification efficiency. If you receive 100 leads and set 30 appointments, your appointment rate is 30%.</p>
<p>Benchmark: 25–45% for self-managed follow-up. 65–80% with professional <a href="/appointment-setting/">appointment setting</a>.</p>
<h2>6. Customer acquisition cost (CAC)</h2>
<p>Total all marketing spend — not just lead generation — and divide by new customers won. This is your real cost to acquire a customer and the number to compare against LTV.</p>
<p>Formula: <strong>Total marketing spend ÷ New customers = CAC</strong></p>
<h2>7. Customer lifetime value (LTV)</h2>
<p>Especially important for trades with repeat business: HVAC, pest control, lawn care, mosquito control. A one-time roofing job has LTV equal to the job value. A recurring pest control plan at $150/month has LTV of $1,800/year.</p>
<p>The LTV:CAC ratio tells you how profitable your marketing is over the customer relationship. Target: LTV:CAC of 3:1 or higher.</p>
<h2>How to track these metrics</h2>
<p>A spreadsheet works. Create columns for: lead source, leads received, appointments set, estimates run, jobs won, total revenue, total spend. Update weekly. Calculate the ratios above.</p>
<p>Most contractors who do this for the first time discover they've been over-investing in low-quality lead sources while under-investing in their best performers.</p>"""))

# PAGE 28
PAGES.append(("appointment-setting-cost",
"How Much Does Appointment Setting Cost for Contractors? 2026 Pricing Guide",
"Contractor appointment setting cost breakdown: per-appointment pricing ($45-$150), monthly retainer models, and how to calculate true ROI. Compare DIY vs managed appointment setting.",
"How Much Does Appointment Setting Cost for Contractors? 2026 Pricing Guide",
"Appointment Setting Cost",
"""<p>Appointment setting for contractors is priced in several ways depending on the provider model. Understanding how each works helps you evaluate whether the cost makes sense for your business.</p>
<h2>Pricing models</h2>
<h3>Per-appointment pricing</h3>
<p>You pay a flat fee for each confirmed appointment delivered to your calendar. No appointment, no charge. This model aligns incentives well — the provider only gets paid when they deliver value.</p>
<p>Typical range: $45–$150 per confirmed appointment, depending on trade, market, and qualification criteria.</p>
<p>What's included: a lead contacts your business (or is generated via advertising), an agent calls and qualifies them against your criteria (service area, job type, homeowner status, budget), and schedules a confirmed time slot directly on your calendar. You receive a notification with the homeowner's details.</p>
<h3>Monthly retainer model</h3>
<p>A flat monthly fee covering a set number of appointments or an agreed lead volume. Predictable cost but less direct alignment between payment and performance.</p>
<p>Typical range: $1,500–$5,000/month depending on volume and trade.</p>
<h3>Percentage of revenue</h3>
<p>Some providers charge based on revenue from jobs won through the service. Less common in the contractor space but found in some franchise and enterprise models.</p>
<h2>The real question: does it cost less than your alternatives?</h2>
<p>The right way to evaluate appointment setting cost is to compare cost per job — not cost per appointment or cost per lead.</p>
<p><strong>Example comparison:</strong></p>
<table>
<tr><th>Model</th><th>Cost</th><th>Close rate</th><th>Cost per job</th></tr>
<tr><td>Shared marketplace leads</td><td>$30/lead</td><td>5%</td><td>$600</td></tr>
<tr><td>Google LSA</td><td>$80/lead</td><td>20%</td><td>$400</td></tr>
<tr><td>Appointment setting</td><td>$100/appt</td><td>55%</td><td>$182</td></tr>
</table>
<p>In this example, appointment setting has the highest per-appointment cost but the lowest cost per job — because the close rate on a scheduled, qualified appointment is 10x higher than a shared lead.</p>
<h2>What determines appointment setting cost</h2>
<p><strong>Trade:</strong> Emergency trades (tree removal, garage door) command higher prices because of urgency and LTV. Routine service trades are priced lower.</p>
<p><strong>Market competition:</strong> High-competition markets (South Florida, major metros) cost more per appointment than smaller markets.</p>
<p><strong>Qualification depth:</strong> More stringent criteria (homeowner only, minimum job value, specific service type) reduces volume but improves quality, typically at higher per-appointment cost.</p>
<p><strong>Call timing:</strong> Speed to first contact significantly affects set rates. Providers with 24/7 coverage or near-instant callbacks deliver higher appointment set rates and justify higher per-appointment pricing.</p>
<h2>DIY appointment setting: the real cost</h2>
<p>If you're calling your own leads, your cost isn't zero — it's your time or a staff member's time. A dedicated appointment setter earns $18–$28/hour. At 20 hours/week, that's $1,440–$2,240/month plus benefits and training.</p>
<p>In-house appointment setters typically set appointments at 25–35% of leads. A professional outsourced team with trained scripts, CRM tools, and multi-touch follow-up typically achieves 65–75%.</p>
<p>See <a href="/appointment-setting/">how RankLocal's appointment setting works</a> for contractor-specific details.</p>"""))

# PAGE 29
PAGES.append(("how-to-scale-a-roofing-company",
"How to Scale a Roofing Company from 5 to 20 Jobs Per Week",
"Practical guide to scaling a roofing company: lead systems, crew capacity, estimating workflow, admin processes, and the lead generation infrastructure to support 20+ jobs per week.",
"How to Scale a Roofing Company from 5 to 20 Jobs Per Week",
"How to Scale a Roofing Company",
"""<p>Going from 5 to 20 jobs per week isn't just about getting more leads — it's about building the infrastructure to handle them. Most roofing companies that try to grow fast either run out of leads or out of capacity, and both problems follow the same pattern: one side of the business moves faster than the other.</p>
<p>Here's how to scale both sides at the same time.</p>
<h2>Phase 1: Fix your lead pipeline before hiring</h2>
<p>At 5 jobs/week, your lead generation is probably inconsistent. Some weeks are great, some weeks the phone doesn't ring. Before you add crew capacity, you need predictable lead flow.</p>
<p><strong>What predictable looks like:</strong> You know, within 20%, how many leads you'll receive next week. You have at least two reliable sources. Your cost per job is measurable and consistent.</p>
<p>Roofing companies at this scale typically use one of these to stabilize lead flow: Google Local Services Ads (reliable but competitive — see <a href="/google-local-services-ads-for-contractors/">the LSA guide</a>), exclusive pay-per-call (higher quality, predictable volume), or a combination of both.</p>
<p>Fix this first. Do not hire crew to fill capacity you don't have leads to support.</p>
<h2>Phase 2: Build your estimating capacity</h2>
<p>At 5 jobs/week, you're probably estimating yourself. At 20 jobs/week, that's 20+ estimates — which can mean 30+ homeowner conversations and 60+ follow-up calls. You physically cannot do this alone.</p>
<p><strong>Options:</strong></p>
<p>Hire a dedicated estimator. A good roofing estimator earns $60,000–$90,000/year. At 20 jobs/week averaging $8,000/job, your weekly revenue is $160,000+. An estimator is 1% of revenue.</p>
<p>Use an appointment setting service to pre-qualify and schedule estimates. This frees your time for the highest-value estimates while filtering out tire-kickers. See <a href="/appointment-setting/">contractor appointment setting</a>.</p>
<h2>Phase 3: Standardize your close process</h2>
<p>At 5 jobs/week, your close process is probably in your head. At 20 jobs/week with a separate estimator running appointments, the close process needs to be written down and repeatable.</p>
<p>Document: how you handle the estimate visit, how you present pricing, what you say when they ask for a lower number, how you follow up if they don't decide on-site, and what the timeline and process looks like. See <a href="/how-to-close-more-roofing-estimates/">closing more roofing estimates</a>.</p>
<h2>Phase 4: Build production capacity systematically</h2>
<p><strong>At 5 jobs/week:</strong> Likely 1–2 crews. At 20 jobs/week you need 4–6 crews depending on job size and complexity.</p>
<p>Add one crew at a time, not all at once. Each new crew requires: trained foreman who can run jobs independently, material procurement processes that scale, quality control checkpoints, and warranty documentation.</p>
<p>The constraint usually isn't finding workers — it's finding foremen you can trust to run a job without you on-site.</p>
<h2>Phase 5: Admin and back-office infrastructure</h2>
<p>At 20 jobs/week, you're invoicing $160k+ per week. You need: someone handling permits and insurance certificates, someone doing job costing and invoicing, someone handling customer communication (scheduling, status updates, follow-up reviews), and a project management system so nothing falls through.</p>
<h2>The lead generation system for 20 jobs/week</h2>
<p>To sustain 20 jobs/week with a 40% close rate on estimates, you need approximately 50 estimates/week. To generate 50 estimates with a 65% appointment-to-estimate show rate, you need 77 booked appointments/week. To book 77 appointments, you need a reliable inbound lead volume of 100–150 qualified calls per week.</p>
<p>That volume requires a combination of sources working simultaneously. Contractors at this level typically run: Google LSA in their primary markets, exclusive pay-per-call for overflow and geographic expansion, and referral programs to maintain 15–25% of volume from existing customer networks.</p>
<p>See <a href="/roofing-leads/">RankLocal's roofing lead generation</a> for exclusive inbound call volume at scale.</p>"""))

# PAGE 30
PAGES.append(("ai-appointment-setting-for-contractors",
"AI Appointment Setting for Contractors: How Automated Booking Is Changing Lead Gen",
"How AI appointment setting works for contractors: automated follow-up, qualification, and calendar booking. Compare AI vs human appointment setting and what the right model looks like in 2026.",
"AI Appointment Setting for Contractors: How Automated Booking Is Changing Lead Gen in 2026",
"AI Appointment Setting for Contractors",
"""<p>AI appointment setting is one of the most discussed trends in contractor lead generation right now — and also one of the most misunderstood. Here's what it actually is, where it outperforms human agents, and where it doesn't.</p>
<h2>What AI appointment setting means in practice</h2>
<p>AI appointment setting refers to automated systems — typically using large language models or rule-based conversation flows — that contact leads, qualify them through conversation, and schedule confirmed appointments without a human agent on the call.</p>
<p>These systems can operate 24/7, respond to new leads within seconds, and handle unlimited volume simultaneously. They don't get tired, don't forget to follow up on day 7, and don't have bad days.</p>
<h2>Where AI outperforms human appointment setters</h2>
<p><strong>Speed to first contact:</strong> An AI system can respond to a new lead within 30 seconds, 24 hours a day, 7 days a week. The best human-staffed teams respond within 5 minutes during business hours. Speed-to-lead research shows each minute of delay reduces conversion — AI closes that gap completely. See <a href="/speed-to-lead-for-contractors/">speed-to-lead for contractors</a>.</p>
<p><strong>Follow-up consistency:</strong> Most contractors give up after 1–2 contact attempts. AI systems execute the full <a href="/lead-follow-up-sequence-for-contractors/">multi-touch follow-up sequence</a> — day 0, day 1, day 3, day 7, day 14 — without fail, for every lead, every time.</p>
<p><strong>Scale:</strong> A human appointment setter handles 40–60 conversations per day. AI handles 400–4,000 simultaneously.</p>
<h2>Where AI still falls short</h2>
<p><strong>Complex objection handling:</strong> A homeowner who says "my neighbor's roofer said he could do it for $3,000 less" requires nuanced response. Current AI systems can handle scripted objections but struggle with novel, emotionally complex situations.</p>
<p><strong>Trust-building on high-ticket jobs:</strong> A $15,000 roof replacement involves significant trust. Many homeowners, particularly older demographics, are more comfortable scheduling with a human who demonstrates expertise and answers questions naturally.</p>
<p><strong>Compliance risk:</strong> AI outbound calling is governed by TCPA and related regulations. Improper consent handling by automated systems creates liability. Human agents with proper training and consent documentation carry lower compliance risk. See <a href="/tcpa-lead-compliance/">TCPA lead compliance for contractors</a>.</p>
<h2>The hybrid model: AI + human</h2>
<p>The most effective approach in 2026 uses AI for speed and consistency — instant first contact, automated multi-touch sequences, calendar integration — while routing complex conversations and high-ticket jobs to human agents.</p>
<p>In this model, AI handles: immediate lead response (within 60 seconds), initial qualification (service area, homeowner status, job type), scheduling when the homeowner is ready to book. Human agents handle: homeowners who ask detailed questions, high-value jobs over threshold, leads who express hesitation about the service or company.</p>
<h2>What to ask any AI appointment setting provider</h2>
<p>If you're evaluating an AI-driven appointment setting solution, ask these questions: How is consent obtained and documented for outbound AI calls? What happens when the AI can't resolve an objection — is there human escalation? What is the average appointment set rate and how is it measured? How is quality controlled — do you review recordings or transcripts? What are the TCPA compliance protocols?</p>
<p>See how <a href="/appointment-setting/">RankLocal's appointment setting</a> handles qualification and scheduling for home service contractors.</p>"""))

# ============================================================
# EXECUTION LOOP
# ============================================================
import os

BASE = os.path.dirname(os.path.abspath(__file__))

for (slug, title, meta, h1, bc, body) in PAGES:
    path = os.path.join(BASE, slug)
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, "index.html"), "w", encoding="utf-8") as f:
        f.write(make_page(slug, title, meta, h1, bc, body))
    print(f"Written: {slug}")

print(f"Done! {len(PAGES)} pages generated.")
