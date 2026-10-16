# -*- coding: utf-8 -*-
import io, os, json, re
from collections import Counter, defaultdict

# 0. find unresolved old-style prefixes
import weekly_seo_batch as W
queue = json.load(io.open(W.QUEUE_PATH, encoding='utf-8'))

def is_stub(slug):
    try:
        return 'http-equiv="refresh"' in io.open(os.path.join(W.BASE, slug, 'index.html'), encoding='utf-8').read(400)
    except Exception:
        return True

old_live = [t for t in queue if t.get('type') == 'city-leads'
            and not re.search(r'-[a-z]{2}$', t['slug'])
            and os.path.isdir(os.path.join(W.BASE, t['slug']))
            and not is_stub(t['slug'])]
prefixes = Counter()
for t in old_live:
    m = re.match(r'(.+-leads)-', t['slug'])
    if m:
        prefixes[m.group(1)] += 1
print('live old-style prefixes:', dict(prefixes))

# 1. patch _same_city_trade_links with the extra prefixes
P = 'weekly_seo_batch.py'
s = io.open(P, encoding='utf-8').read()
old = '''                     ("Tree Service", "tree-service-leads"), ("Insulation", "insulation-leads"),
                     ("Locksmith", "locksmith-leads")]:'''
extra = ''
done = set(['roofing-leads','hvac-leads','plumbing-leads','pest-control-leads','landscaping-leads',
            'fencing-leads','garage-door-leads','mca-leads','electrical-leads','painting-leads',
            'window-replacement-leads','siding-leads','gutters-leads','pressure-washing-leads',
            'tree-service-leads','insulation-leads','locksmith-leads'])
for pref in sorted(prefixes):
    if pref in done:
        continue
    label = pref[:-6].replace('-', ' ').title()
    extra += '\n                     ("' + label + '", "' + pref + '"),'
new = '''                     ("Tree Service", "tree-service-leads"), ("Insulation", "insulation-leads"),
                     ("Locksmith", "locksmith-leads"),''' + extra.rstrip(',') + ']:'
assert old in s
s = s.replace(old, new, 1)
# raise cap so legacy trades fit
s = s.replace('def _same_city_trade_links(city, state, exclude_prefix, n=8):',
              'def _same_city_trade_links(city, state, exclude_prefix, n=14):', 1)
io.open(P, 'w', encoding='utf-8').write(s)
import importlib, py_compile
py_compile.compile(P, doraise=True)
importlib.reload(W)
print('prefixes patched')

# 2. regen new-style pages for legacy metros
legacy = set((t.get('city'), t.get('state')) for t in old_live)
makers = {'city-leads': W.make_city_page, 'mca-city': W.make_mca_city_page,
          'combined-city': W.make_combined_city_page}
regen = 0
for t in queue:
    ty = t.get('type')
    if ty not in makers or (t.get('city'), t.get('state')) not in legacy:
        continue
    slug = t['slug']
    if ty == 'city-leads' and not re.search(r'-[a-z]{2}$', slug):
        continue
    d = os.path.join(W.BASE, slug)
    if not os.path.isdir(d):
        continue
    p = makers[ty](t)
    io.open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(W.render_service(p))
    regen += 1
print('regenerated:', regen)

# 3. final audit (stubs excluded)
geo = [t for t in queue if t.get('type') in ('city-leads', 'mca-city', 'combined-city', 'mca-state', 'hs-state')]
inbound = defaultdict(int)
href_re = re.compile(r"href='/([a-z0-9-]+)/'")
stubs = set()
for t in geo:
    p = os.path.join(W.BASE, t['slug'], 'index.html')
    try:
        txt = io.open(p, encoding='utf-8').read()
    except Exception:
        continue
    if 'http-equiv="refresh"' in txt[:400]:
        stubs.add(t['slug']); continue
    for m in set(href_re.findall(txt)):
        if m != t['slug']:
            inbound[m] += 1
for hub in ['business-loan-leads', 'mca-leads', 'merchant-cash-advance-leads',
            'home-service-leads', 'contractor-leads', 'pay-per-call']:
    p = os.path.join(W.BASE, hub, 'index.html')
    if os.path.exists(p):
        for m in set(href_re.findall(io.open(p, encoding='utf-8').read())):
            inbound[m] += 1
by = defaultdict(lambda: [0, 0]); orph = []
for t in geo:
    if t['slug'] in stubs or not os.path.isdir(os.path.join(W.BASE, t['slug'])):
        continue
    by[t['type']][1] += 1
    if inbound.get(t['slug'], 0) > 0:
        by[t['type']][0] += 1
    else:
        orph.append(t['slug'])
print('stubs excluded:', len(stubs))
for ty, (l, tot) in sorted(by.items()):
    print(ty, ':', l, '/', tot, '| orphans:', tot - l)
print('orphans left:', len(orph), orph[:10])
