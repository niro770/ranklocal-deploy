import json, shutil, collections, sys
sys.stdout.reconfigure(encoding="utf-8")
import weekly_seo_batch as w

PATH = w.QUEUE_PATH
shutil.copy(PATH, PATH.replace(".json", ".backup2.json"))
data = json.load(open(PATH, encoding="utf-8"))
existing = {x["slug"] for x in data}
NEW = "Locksmith"
assert NEW in w.TRADE_DATA

# slug templates from Roofing entries of each type
tmpl = {}
for x in data:
    if x["trade"] == "Roofing" and x["type"] not in tmpl:
        tmpl[x["type"]] = x
new = []
for t, ex in tmpl.items():
    if t == "city-leads":
        cities = sorted({y["city"]: y["state"] for y in data if y["type"] == "city-leads"}.items())
        for c, st in cities:
            slug = ex["slug"].replace("roofing", "locksmith").replace(c.lower().replace(" ", "-"), "{c}") if False else None
        # derive: roofing-leads-<city>
        for c, st in cities:
            slug = "locksmith-leads-" + c.lower().replace(" ", "-")
            if slug not in existing:
                existing.add(slug)
                new.append({"slug": slug, "type": t, "trade": NEW, "city": c, "state": st, "status": "pending"})
    else:
        sts = sorted({y["state"] for y in data if y["type"] == t})
        base = ex["slug"][: -len(ex["state"].lower().replace(" ", "-"))]
        for s in sts:
            slug = base.replace("roofing", "locksmith") + s.lower().replace(" ", "-")
            if slug not in existing:
                existing.add(slug)
                new.append({"slug": slug, "type": t, "trade": NEW, "state": s, "status": "pending"})

# smoke-test the generators on one of each type before saving
makers = {"service": w.make_service_page, "buy-calls": w.make_buy_calls_page,
          "exclusive-leads": w.make_exclusive_leads_page, "pay-per-call": w.make_pay_per_call_page,
          "appointment-setting": w.make_appointment_setting_page,
          "contractor-leads": w.make_contractor_leads_page, "phone-leads": w.make_phone_leads_page,
          "city-leads": w.make_city_page}
seen = set()
for n in new:
    if n["type"] in seen:
        continue
    seen.add(n["type"])
    html = w.render_service(makers[n["type"]](n))
    assert len(html) > 3000, n
    print("OK render", n["type"], n["slug"], len(html))

data.extend(new)
json.dump(data, open(PATH, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("Added", len(new), dict(collections.Counter(n["type"] for n in new)))
print("Pending now:", sum(1 for x in data if x["status"] == "pending"))
print([n["slug"] for n in new[:8]])
