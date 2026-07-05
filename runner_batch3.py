#!/usr/bin/env python3
"""
Batch 3 runner -- reads pages_batch3.json and generates HTML files.
"""
import os, json, re

BASE = r"C:\Users\19522\Documents\ranklocal-deploy-push"
TODAY = "July 2026"
BYLINE = 'By <a href="/about/">Nir Barlev</a>, Founder &amp; CEO &middot; Updated July 2026'

PERSON_SCHEMA = {
    "@type": "Person", "@id": "https://ranklocall.com/#founder",
    "name": "Nir Barlev", "jobTitle": "Founder & CEO",
    "worksFor": {"@id": "https://ranklocall.com/#organization"},
    "url": "https://ranklocall.com/about/",
    "sameAs": ["https://ranklocall.com/about/"]
}

def make_article_schema(p):
    faq_items = [{"@type":"Question","name":f["q"],"acceptedAnswer":{"@type":"Answer","text":f["a"]}} for f in p.get("faq",[])]
    schema = [
        {"@context":"https://schema.org","@type":"Article",
         "@id":"https://ranklocall.com/" + p["slug"] + "/#article",
         "headline":p["title"],"description":p["meta"],
         "datePublished":"2024-01-15","dateModified":"2026-07-01",
         "author":PERSON_SCHEMA,
         "publisher":{"@id":"https://ranklocall.com/#organization"},
         "mainEntityOfPage":{"@type":"WebPage","@id":"https://ranklocall.com/" + p["slug"] + "/"}},
        {"@context":"https://schema.org","@type":"BreadcrumbList",
         "itemListElement":[
             {"@type":"ListItem","position":1,"name":"Home","item":"https://ranklocall.com/"},
             {"@type":"ListItem","position":2,"name":p["h1"],"item":"https://ranklocall.com/" + p["slug"] + "/"}
         ]}
    ]
    if faq_items:
        schema.append({"@context":"https://schema.org","@type":"FAQPage","mainEntity":faq_items})
    return json.dumps(schema, indent=2)

def make_service_schema(p):
    faq_items = [{"@type":"Question","name":f["q"],"acceptedAnswer":{"@type":"Answer","text":f["a"]}} for f in p.get("faq",[])]
    schema = [
        {"@context":"https://schema.org","@type":"Service",
         "@id":"https://ranklocall.com/" + p["slug"] + "/#service",
         "name":p["h1"],"description":p["meta"],
         "provider":{"@id":"https://ranklocall.com/#organization"},
         "areaServed":{"@type":"Country","name":"United States"},
         "audience":{"@type":"Audience","audienceType":"Home service contractors"}},
        {"@context":"https://schema.org","@type":"BreadcrumbList",
         "itemListElement":[
             {"@type":"ListItem","position":1,"name":"Home","item":"https://ranklocall.com/"},
             {"@type":"ListItem","position":2,"name":p["h1"],"item":"https://ranklocall.com/" + p["slug"] + "/"}
         ]}
    ]
    if faq_items:
        schema.append({"@context":"https://schema.org","@type":"FAQPage","mainEntity":faq_items})
    return json.dumps(schema, indent=2)

def render_article(p):
    faq_html = ""
    for item in p.get("faq", []):
        faq_html += "<div class=\"faq-item\"><h3>" + item["q"] + "</h3><p>" + item["a"] + "</p></div>\n"
    links_html = "".join("<li><a href=\"" + lnk["href"] + "\">" + lnk["text"] + "</a></li>" for lnk in p.get("links",[]))
    schema = make_article_schema(p)
    return "\n".join([
        "<!DOCTYPE html>",
        "<html lang=\"en\"><head>",
        "<meta charset=\"UTF-8\">",
        "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">",
        "<title>" + p["title"] + "</title>",
        "<meta name=\"description\" content=\"" + p["meta"] + "\">",
        "<link rel=\"canonical\" href=\"https://ranklocall.com/" + p["slug"] + "/\">",
        "<link rel=\"stylesheet\" href=\"/assets/css/style.css\">",
        "<script type=\"application/ld+json\">" + schema + "</script>",
        "</head><body>",
        "<header class=\"site-header\"><div class=\"container\">",
        "<a class=\"logo\" href=\"/\">RankLocal</a>",
        "<nav><a href=\"/contractor-leads/\">Contractor Leads</a> <a href=\"/pay-per-call/\">Pay-Per-Call</a> <a href=\"/appointment-setting/\">Appointment Setting</a> <a href=\"/apply/\" class=\"btn-nav\">Apply Now</a></nav>",
        "</div></header>",
        "<main class=\"article\"><div class=\"container\">",
        "<h1>" + p["h1"] + "</h1>",
        "<p class=\"byline\">" + BYLINE + "</p>",
        p["body"],
        "<section class=\"faq-section\"><h2>Frequently Asked Questions</h2>" + faq_html + "</section>",
        "<aside class=\"related-links\"><h3>Related Resources</h3><ul>" + links_html + "</ul></aside>",
        "</div></main>",
        "<footer class=\"site-footer\"><div class=\"container\"><p>&copy; 2026 RankLocal</p></div></footer>",
        "</body></html>",
    ])

def render_service(p):
    faq_html = ""
    for item in p.get("faq", []):
        faq_html += "<div class=\"faq-item\"><h3>" + item["q"] + "</h3><p>" + item["a"] + "</p></div>\n"
    links_html = "".join("<li><a href=\"" + lnk["href"] + "\">" + lnk["text"] + "</a></li>" for lnk in p.get("links",[]))
    schema = make_service_schema(p)
    trade = p.get("trade", "contractor")
    return "\n".join([
        "<!DOCTYPE html>",
        "<html lang=\"en\"><head>",
        "<meta charset=\"UTF-8\">",
        "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">",
        "<title>" + p["title"] + "</title>",
        "<meta name=\"description\" content=\"" + p["meta"] + "\">",
        "<link rel=\"canonical\" href=\"https://ranklocall.com/" + p["slug"] + "/\">",
        "<link rel=\"stylesheet\" href=\"/assets/css/style.css\">",
        "<script type=\"application/ld+json\">" + schema + "</script>",
        "</head><body>",
        "<header class=\"site-header\"><div class=\"container\">",
        "<a class=\"logo\" href=\"/\">RankLocal</a>",
        "<nav><a href=\"/contractor-leads/\">Contractor Leads</a> <a href=\"/pay-per-call/\">Pay-Per-Call</a> <a href=\"/appointment-setting/\">Appointment Setting</a> <a href=\"/apply/\" class=\"btn-nav\">Apply Now</a></nav>",
        "</div></header>",
        "<section class=\"hero hero--inner\"><div class=\"container\">",
        "<h1>" + p["h1"] + "</h1>",
        "<p class=\"hero__sub\">" + p.get("hero_sub","") + "</p>",
        "<a href=\"/apply/\" class=\"btn btn--primary\">Apply to Join &rarr;</a>",
        "</div></section>",
        "<main><div class=\"container\">",
        p["body"],
        "<section class=\"faq-section\"><h2>Frequently Asked Questions</h2>" + faq_html + "</section>",
        "<aside class=\"related-links\"><h3>Related Resources</h3><ul>" + links_html + "</ul></aside>",
        "<div class=\"cta-block\"><h2>Ready to receive " + trade + " leads?</h2>",
        "<p>Apply now. No monthly minimums. Exclusive calls only.</p>",
        "<a href=\"/apply/\" class=\"btn btn--primary\">Apply Now &rarr;</a></div>",
        "</div></main>",
        "<footer class=\"site-footer\"><div class=\"container\"><p>&copy; 2026 RankLocal</p></div></footer>",
        "</body></html>",
    ])

def update_yml(yml_path, slugs):
    with open(yml_path, "r", encoding="utf-8") as f:
        content = f.read()
    insert_point = content.rfind("]}')")
    if insert_point == -1:
        print("YML: closing marker not found")
        return
    new_urls = ",\n".join("              \"https://ranklocall.com/" + s + "/\"" for s in slugs)
    insertion = ",\n" + new_urls + "\n"
    updated = content[:insert_point] + insertion + content[insert_point:]
    updated = re.sub(r"Submitting \d+ URLs", "Submitting 283 URLs", updated)
    with open(yml_path, "w", encoding="utf-8") as f:
        f.write(updated)
    print("YML: " + str(len(slugs)) + " URLs added")

# ---- Main ----
pages_file = os.path.join(BASE, "pages_batch3.json")
with open(pages_file, "r", encoding="utf-8") as f:
    PAGES = json.load(f)

print("Loaded " + str(len(PAGES)) + " pages")
written = []
skipped = []

for page in PAGES:
    slug = page["slug"]
    out_dir = os.path.join(BASE, slug)
    out_file = os.path.join(out_dir, "index.html")
    if os.path.exists(out_file):
        skipped.append(slug)
        continue
    os.makedirs(out_dir, exist_ok=True)
    html = render_service(page) if page.get("type") == "service" else render_article(page)
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html)
    written.append(slug)
    print("[OK] " + slug)

print("\nWritten: " + str(len(written)) + " | Skipped: " + str(len(skipped)))

sitemap_path = os.path.join(BASE, "sitemap.xml")
with open(sitemap_path, "r", encoding="utf-8") as f:
    sitemap = f.read()
new_entries = "\n".join(
    "  <url><loc>https://ranklocall.com/" + s + "/</loc><changefreq>monthly</changefreq><priority>0.7</priority></url>"
    for s in written
)
sitemap_updated = sitemap.replace("</urlset>", new_entries + "\n</urlset>")
with open(sitemap_path, "w", encoding="utf-8") as f:
    f.write(sitemap_updated)
print("Sitemap: " + str(len(written)) + " URLs added")

yml_path = os.path.join(BASE, ".github", "workflows", "google-indexing.yml")
update_yml(yml_path, written)
print("\nDone.")
