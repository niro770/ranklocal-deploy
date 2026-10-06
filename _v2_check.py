import os, json, re, sys
sys.stdout.reconfigure(encoding="utf-8")
os.chdir(r"C:\Users\19522\Documents\ranklocal-deploy-push")
m = json.load(open(r"C:\Users\19522\Documents\Claude\Projects\Presentation for finance leads\v2-drafts\map.json"))
sl = []
for c in m.values():
    sl += [c["hub"]] + [s[0] for s in c["spokes"]]
print("slugs", len(sl))
print("existing of 72:", [s for s in sl if os.path.exists(s.strip("/") + "/index.html")])
allow = ["/pay-per-call/", "/contractor-leads/", "/appointment-setting/", "/apply/", "/what-is-a-billable-call/", "/tcpa-lead-compliance/", "/exclusive-vs-shared-leads/", "/what-is-exclusive-lead-generation/", "/how-does-pay-per-call-work/", "/roofing-leads/", "/fence-leads/", "/landscaping-leads/", "/pest-control-leads/", "/garage-door-repair-leads/"]
print("missing allowed:", [a for a in allow if not os.path.exists(a.strip("/") + "/index.html")])
p = open("what-is-a-billable-call/index.html", encoding="utf-8").read() if os.path.exists("what-is-a-billable-call/index.html") else ""
print(len(p))
print(p[:500])
i = p.find("<main")
print(p[i:i + 600])
