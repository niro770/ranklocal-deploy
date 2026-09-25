import json, collections
d = json.load(open(r'C:\Users\19522\Documents\ranklocal-deploy-push\topic_queue.json', encoding='utf-8'))
print('status counts', collections.Counter(x['status'] for x in d))
by_type = collections.Counter(x['type'] for x in d)
print('by type', by_type)
seen = set()
for x in d:
    if x['type'] not in seen:
        seen.add(x['type'])
        print(x)
