import json

path = r'C:\Users\19522\Documents\ranklocal-deploy-push\topic_queue.json'
d = json.load(open(path, encoding='utf-8'))

states = sorted(set(x['state'] for x in d))
assert len(states) == 50, len(states)

existing_slugs = set(x['slug'] for x in d)

new_trades = ["Water Damage Restoration", "Junk Removal", "Appliance Repair"]

def slugify(s):
    return s.lower().replace(' ', '-')

added = []
for trade in new_trades:
    trade_slug = slugify(trade)
    for state in states:
        state_slug = slugify(state)
        slug = f"{trade_slug}-leads-{state_slug}"
        if slug in existing_slugs:
            continue
        entry = {
            "slug": slug,
            "type": "service",
            "trade": trade,
            "state": state,
            "status": "pending",
        }
        d.append(entry)
        added.append(slug)

with open(path, 'w', encoding='utf-8') as f:
    json.dump(d, f, indent=2)
    f.write('\n')

print("Added", len(added), "new pending topics")
print("New total entries:", len(d))
print("Sample:", added[:5])
