import os, re, json, sys
sys.stdout.reconfigure(encoding="utf-8")
REPO = r"C:\Users\19522\Documents\ranklocal-deploy-push"
rep = json.load(open(os.path.join(REPO, "_v2_build_report.json")))
bad = 0
def exists(h):
    h = h.split("#")[0].split("?")[0]
    if not h.startswith("/"): return True
    if h == "/": return True
    return os.path.exists(os.path.join(REPO, h.strip("/"), "index.html")) or os.path.exists(os.path.join(REPO, h.strip("/")))
for s in rep["built"] + rep["touched"]:
    t = open(os.path.join(REPO, s, "index.html"), encoding="utf-8").read()
    i = max(t.find("<main"), 0); j = t.find("</main>"); j = j if j > 0 else len(t)
    m = t[i:j]
    probs = []
    if t.count("<h1") != 1: probs.append("h1=%d" % t.count("<h1"))
    for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
        try: json.loads(blk)
        except Exception as e: probs.append("jsonld")
    if re.search(r"\*\*|^#{1,4} |\]\(/", m, re.M): probs.append("raw-markdown")
    for h in re.findall(r'href="([^"]+)"', m):
        if not exists(h): probs.append("dead:" + h)
    if "\u2014" in m: probs.append("emdash")
    if probs and s in rep["built"]:
        print(s, probs); bad += 1
    elif probs: print("(touched)", s, probs[:5])
print("checked", len(rep["built"]), "built;", "problem pages:", bad)
c = open(os.path.join(REPO, "break-even-close-rate-calculator", "index.html"), encoding="utf-8").read()
print("calculator has form/script:", "<form" in c, "<script>" in c or "<script" in c[c.index("<main"):])
for s in ["pay-per-call", "contractor-leads", "appointment-setting"]:
    t = open(os.path.join(REPO, s, "index.html"), encoding="utf-8").read()
    print(s, "has </main>:", "</main>" in t, "len", len(t), "guides:", "v2-guides" in t)
