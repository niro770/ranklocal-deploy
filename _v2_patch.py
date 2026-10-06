import json
REPO = r"C:\Users\19522\Documents\ranklocal-deploy-push"
pre = ["how-to-answer-contractor-leads", "speed-to-lead-for-contractors", "lead-follow-up-sequence-for-contractors",
       "angi-alternatives", "homeadvisor-alternatives", "google-lsa-vs-pay-per-call", "ai-appointment-setting-for-contractors"]
json.dump(pre, open(REPO + r"\_v2_pre_existing.json", "w"))
p = REPO + r"\build_v2_pages.py"
s = open(p, encoding="utf-8").read()
old = "pre_existing = {s for s in all_slugs if exists_live(s)}"
new = ("_pf = os.path.join(REPO, '_v2_pre_existing.json')\n"
       "pre_existing = set(json.load(open(_pf))) if os.path.exists(_pf) else {s for s in all_slugs if exists_live(s)}")
assert old in s
open(p, "w", encoding="utf-8").write(s.replace(old, new))
q = REPO + r"\_v2_qa.py"
t = open(q, encoding="utf-8").read()
t = t.replace('i, j = t.index("<main"), t.index("</main>")', 'i = max(t.find("<main"), 0); j = t.find("</main>"); j = j if j > 0 else len(t)')
open(q, "w", encoding="utf-8").write(t)
print("ok")
