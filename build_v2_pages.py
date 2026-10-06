"""Build ranklocall.com v2 topical-map pages from markdown drafts.
Usage: python build_v2_pages.py            -> build + cluster-link (no git)
Skips slugs that already exist live; holds LEGAL_HOLD pages. Idempotent."""
import os, re, json, html, sys, glob, datetime
import yaml, markdown
sys.stdout.reconfigure(encoding="utf-8")

REPO = r"C:\Users\19522\Documents\ranklocal-deploy-push"
SRC = r"C:\Users\19522\Documents\Claude\Projects\Presentation for finance leads\v2-drafts"
SITE = "https://ranklocall.com"
TODAY = datetime.date.today().isoformat()
HOLD = {"call-recording-laws-by-state-contractors", "fcc-one-to-one-consent-rule-contractors"}
MONEY_PAGES = ["pay-per-call", "contractor-leads", "appointment-setting", "what-is-a-billable-call",
               "exclusive-vs-shared-leads", "tcpa-lead-compliance", "what-is-exclusive-lead-generation"]

cmap = json.load(open(os.path.join(SRC, "map.json"), encoding="utf-8"))
all_slugs = []
cluster_of = {}
for cid, c in cmap.items():
    for s in [c["hub"]] + [x[0] for x in c["spokes"]]:
        all_slugs.append(s.strip("/"))
        cluster_of[s.strip("/")] = cid
hub_of = {cid: c["hub"].strip("/") for cid, c in cmap.items()}

def exists_live(slug):
    return os.path.exists(os.path.join(REPO, slug, "index.html"))

_pf = os.path.join(REPO, '_v2_pre_existing.json')
pre_existing = set(json.load(open(_pf))) if os.path.exists(_pf) else {s for s in all_slugs if exists_live(s)}
tmpl = open(os.path.join(REPO, "what-is-a-billable-call", "index.html"), encoding="utf-8").read()
mi = tmpl.index("<main")
mj = tmpl.index("</main>") + len("</main>")
HEAD, FOOT = tmpl[:mi], tmpl[mj:]

def load(slug):
    t = open(os.path.join(SRC, "final", slug + ".md"), encoding="utf-8").read()
    p = t.split("---", 2)
    return yaml.safe_load(p[1]), p[2].strip()

meta = {}
for s in all_slugs:
    fp = os.path.join(SRC, "final", s + ".md")
    if os.path.exists(fp):
        meta[s], _ = load(s)

to_build = [s for s in all_slugs if s in meta and s not in pre_existing and s not in HOLD]
buildset = set(to_build)
def target_ok(slug):
    return slug in buildset or (exists_live(slug) and slug not in HOLD)

def fix_links(h):
    def rep(m):
        href = m.group(1).split("#")[0]
        slug = href.strip("/")
        if href.startswith("/") and not target_ok(slug) and slug != "apply":
            return m.group(2)
        return m.group(0)
    return re.sub(r'<a href="(/[^"]*)">(.*?)</a>', rep, h, flags=re.S)

def esc(s): return html.escape(s, quote=True)

def head_for(slug, fm, hubslug):
    url = f"{SITE}/{slug}/"
    h = HEAD
    h = re.sub(r"<title>.*?</title>", lambda m: f"<title>{esc(fm['title'])}</title>", h, count=1, flags=re.S)
    h = re.sub(r'<meta name="description" content=".*?">', lambda m: f'<meta name="description" content="{esc(fm["meta_description"])}">', h, count=1)
    h = re.sub(r'<link rel="canonical" href=".*?">', lambda m: f'<link rel="canonical" href="{url}">', h, count=1)
    h = re.sub(r'<meta property="og:title" content=".*?">', lambda m: f'<meta property="og:title" content="{esc(fm["title"])}">', h, count=1)
    h = re.sub(r'<meta property="og:description" content=".*?">', lambda m: f'<meta property="og:description" content="{esc(fm["meta_description"])}">', h, count=1)
    h = re.sub(r'<meta property="og:url" content=".*?">', lambda m: f'<meta property="og:url" content="{url}">', h, count=1)
    crumbs = [("Home", SITE + "/")]
    if hubslug and hubslug != slug and hubslug in meta:
        crumbs.append((meta[hubslug]["h1"], f"{SITE}/{hubslug}/"))
    crumbs.append((fm["h1"], url))
    graph = [
        {"@type": "Organization", "@id": SITE + "/#organization", "name": "RankLocal", "url": SITE + "/",
         "description": "Exclusive pay-per-call leads, booked appointments, and qualified jobs for US home service companies.",
         "areaServed": {"@type": "Country", "name": "United States"}},
        {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "RankLocal",
         "publisher": {"@id": SITE + "/#organization"}, "inLanguage": "en-US"},
        {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": fm["title"],
         "description": fm["meta_description"], "isPartOf": {"@id": SITE + "/#website"}, "inLanguage": "en-US"},
        {"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(crumbs)]},
        {"@type": "Article", "@id": url + "#article", "headline": fm["h1"], "description": fm["meta_description"],
         "mainEntityOfPage": {"@id": url + "#webpage"}, "author": {"@id": SITE + "/#organization"},
         "publisher": {"@id": SITE + "/#organization"}, "datePublished": TODAY, "dateModified": TODAY,
         "inLanguage": "en-US"},
        {"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
            {"@type": "Question", "name": q["q"], "acceptedAnswer": {"@type": "Answer", "text": q["a"]}}
            for q in fm["faq"]]},
    ]
    ld = '<script type="application/ld+json">\n' + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2) + "\n</script>"
    h = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: ld, h, count=1, flags=re.S)
    return h

SEC = 'style="margin:3rem 0 1rem"'
H2S = 'style="font-size:1.15rem;color:#fff;margin:0 0 1rem"'
GRID = 'style="display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:.6rem"'
LNK = 'style="display:block;padding:.55rem .9rem;background:rgba(0,170,255,0.07);border:1px solid rgba(0,170,255,0.18);border-radius:8px;color:#aac4e0;text-decoration:none;font-size:.88rem"'

def link_box(title, items, marker):
    items = [(s, t) for s, t in items if target_ok(s)]
    if not items:
        return ""
    a = "".join(f'<a href="/{s}/" {LNK}>{esc(t)}</a>' for s, t in items)
    return f"<!-- {marker} --><section {SEC}><h2 {H2S}>{esc(title)}</h2><div {GRID}>{a}</div></section><!-- /{marker} -->"

def short(s):
    return meta[s]["h1"] if s in meta else s.replace("-", " ").title()

def cluster_block(slug):
    cid = cluster_of[slug]
    hub = hub_of[cid]
    sibs = [x[0].strip("/") for x in cmap[cid]["spokes"] if x[0].strip("/") != slug]
    sibs = [s for s in sibs if target_ok(s) and s not in HOLD]
    # rotate so linking is spread out across siblings
    k = all_slugs.index(slug) % max(len(sibs), 1)
    sibs = (sibs[k:] + sibs[:k])[:6]
    items = ([] if slug == hub else [(hub, short(hub))]) + [(s, short(s)) for s in sibs]
    return link_box("More in this guide", items, "v2-cluster")

def build_page(slug):
    fm, body = load(slug)
    body_html = markdown.markdown(body, extensions=["tables", "fenced_code", "sane_lists"])
    body_html = fix_links(body_html)
    body_html = re.sub(r"<p>", '<p class="answer">', body_html, count=1)
    faq = "".join(f"<h3>{esc(q['q'])}</h3><p>{esc(q['a'])}</p>" for q in fm["faq"])
    rel = [(s, short(s)) for s in fm["related"] if target_ok(s.strip("/"))]
    rel = [(s.strip("/"), t) for s, t in rel]
    related = link_box("Related resources", rel, "v2-related")
    cta = ('<section style="margin:2.5rem 0;padding:1.5rem;background:rgba(0,170,255,0.07);'
           'border:1px solid rgba(0,170,255,0.2);border-radius:12px">'
           '<p style="margin:0 0 .9rem;font-weight:600">Want exclusive inbound calls routed to your phone? You pay only for qualifying calls.</p>'
           '<a href="/apply/" class="btn-primary">Apply for a territory</a></section>')
    main = (f'<main class="article"><h1>{esc(fm["h1"])}</h1>' + body_html +
            f"<h2>Frequently asked questions</h2>{faq}" + cluster_block(slug) + related + cta + "</main>")
    page = head_for(slug, fm, hub_of[cluster_of[slug]]) + main + FOOT
    d = os.path.join(REPO, slug)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(page)

def inject(path, block, marker):
    t = open(path, encoding="utf-8").read()
    t = re.sub(rf"<!-- {marker} -->.*?<!-- /{marker} -->", "", t, flags=re.S)
    if not block:
        return False
    for anchor in ("</main>", "<footer", "</body>"):
        if anchor in t:
            t = t.replace(anchor, block + anchor, 1)
            break
    else:
        return False
    open(path, "w", encoding="utf-8").write(t)
    return True

if __name__ == "__main__":
    built = []
    for s in to_build:
        build_page(s)
        built.append(s)
    print("built", len(built))
    print("skipped existing:", sorted(pre_existing))
    print("held:", sorted(HOLD))
    # cluster links on pre-existing pages that belong to a cluster
    touched = []
    for s in sorted(pre_existing):
        if inject(os.path.join(REPO, s, "index.html"), cluster_block(s), "v2-cluster"):
            touched.append(s)
    # hub guide links on core money pages
    hubs = [(hub_of[c], short(hub_of[c])) for c in cmap]
    hubs = [(s, cmap[c]["name"]) for c, s in ((c, hub_of[c]) for c in cmap)]
    blk = link_box("Guides for contractors", hubs, "v2-guides")
    for s in MONEY_PAGES:
        p = os.path.join(REPO, s, "index.html")
        if os.path.exists(p) and inject(p, blk, "v2-guides"):
            touched.append(s)
    print("link blocks injected into:", touched)
    json.dump({"built": built, "touched": touched}, open(os.path.join(REPO, "_v2_build_report.json"), "w"))
