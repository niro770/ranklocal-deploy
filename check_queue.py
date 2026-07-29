import json
q = json.load(open('topic_queue.json'))
pending = [t for t in q if t.get('status') == 'pending']
done = [t for t in q if t.get('status') == 'done']
print('Done:', len(done), '| Pending:', len(pending), '| Total:', len(q))
