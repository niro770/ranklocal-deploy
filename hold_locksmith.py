import json
p = r"C:\Users\19522\Documents\ranklocal-deploy-push\topic_queue.json"
d = json.load(open(p, encoding="utf-8"))
n = 0
for x in d:
    if x["trade"] == "Locksmith" and x["status"] == "pending":
        x["status"] = "hold"
        n += 1
json.dump(d, open(p, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("held", n, "pending", sum(1 for x in d if x["status"] == "pending"))
