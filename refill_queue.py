import json, shutil, collections

PATH = r'C:\Users\19522\Documents\ranklocal-deploy-push\topic_queue.json'
shutil.copy(PATH, PATH.replace('.json', '.backup.json'))

data = json.load(open(PATH, encoding='utf-8'))
existing_slugs = {x['slug'] for x in data}

STATES = ['Alabama','Alaska','Arizona','Arkansas','California','Colorado',
 'Connecticut','Delaware','Florida','Georgia','Hawaii','Idaho','Illinois',
 'Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland',
 'Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana',
 'Nebraska','Nevada','New Hampshire','New Jersey','New Mexico','New York',
 'North Carolina','North Dakota','Ohio','Oklahoma','Oregon','Pennsylvania',
 'Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah',
 'Vermont','Virginia','Washington','West Virginia','Wisconsin','Wyoming']

def state_slug(s):
    return s.lower().replace(' ', '-')

STATE_TYPES = ['service','buy-calls','exclusive-leads','pay-per-call',
               'appointment-setting','contractor-leads','phone-leads']

# Build slug templates from existing entries: (type, trade) -> template with {st}
templates = {}
for x in data:
    t = x['type']
    if t not in STATE_TYPES:
        continue
    key = (t, x['trade'])
    if key in templates:
        continue
    ss = state_slug(x['state'])
    slug = x['slug']
    if slug.endswith('-' + ss):
        templates[key] = slug[: -len(ss)] + '{st}'

new_entries = []
for (t, trade), tmpl in sorted(templates.items()):
    for st in STATES:
        slug = tmpl.format(st=state_slug(st))
        if slug in existing_slugs:
            continue
        existing_slugs.add(slug)
        new_entries.append({'slug': slug, 'type': t, 'trade': trade,
                            'state': st, 'status': 'pending'})

data.extend(new_entries)
with open(PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print('Added', len(new_entries), 'pending topics. Queue total:', len(data))
print('By type:', dict(collections.Counter(x['type'] for x in new_entries)))
print('New states covered:', sorted(set(x['state'] for x in new_entries)))
print('Sample slugs:', [x['slug'] for x in new_entries[:5]])
