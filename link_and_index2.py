"""
Update sitemap.xml and google-indexing.yml with the 25 new batch-2 pages.
"""
import os, re
from datetime import date

BASE = r'C:\Users\19522\Documents\ranklocal-deploy-push'
SITE = 'https://ranklocall.com'
TODAY = date.today().isoformat()

NEW_SLUGS = [
    'hvac-leads',
    'ac-repair-leads',
    'heating-leads',
    'plumbing-leads',
    'emergency-plumbing-leads',
    'water-heater-leads',
    'fence-leads-texas',
    'fence-leads-florida',
    'fence-leads-arizona',
    'fence-leads-california',
    'garage-door-spring-repair-leads',
    'garage-door-opener-leads',
    'garage-door-replacement-leads',
    'outdoor-lighting-leads',
    'roofing-leads-ohio',
    'roofing-leads-illinois',
    'roofing-leads-colorado',
    'roofing-leads-north-carolina',
    'roofing-leads-arizona',
    'painting-leads',
    'window-replacement-leads',
    'siding-leads',
    'gutter-leads',
    'pressure-washing-leads',
    'electrical-leads',
]

# ── 1. sitemap.xml ──────────────────────────────────────────────────────────
sitemap_path = os.path.join(BASE, 'sitemap.xml')
with open(sitemap_path, encoding='utf-8') as f:
    sitemap = f.read()

new_entries = []
for slug in NEW_SLUGS:
    url = f'{SITE}/{slug}/'
    if url in sitemap:
        print(f'  sitemap SKIP (exists): {url}')
        continue
    new_entries.append(
        f'  <url>\n'
        f'    <loc>{url}</loc>\n'
        f'    <lastmod>{TODAY}</lastmod>\n'
        f'    <changefreq>monthly</changefreq>\n'
        f'    <priority>0.8</priority>\n'
        f'  </url>'
    )

if new_entries:
    insert_before = '</urlset>'
    sitemap = sitemap.replace(insert_before, '\n'.join(new_entries) + '\n' + insert_before)
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(sitemap)
    print(f'sitemap.xml: added {len(new_entries)} URLs')
else:
    print('sitemap.xml: nothing to add')

# ── 2. google-indexing.yml ──────────────────────────────────────────────────
yml_path = os.path.join(BASE, '.github', 'workflows', 'google-indexing.yml')
with open(yml_path, encoding='utf-8') as f:
    yml = f.read()

yml_new = []
for slug in NEW_SLUGS:
    url = f'{SITE}/{slug}/'
    if url in yml:
        print(f'  yml SKIP (exists): {url}')
        continue
    yml_new.append(f'          - "{url}"')

if yml_new:
    insert_marker = '          # END_URLS'
    if insert_marker not in yml:
        # Fall back: append before last closing bracket area
        # Find the last URL entry line and insert after
        lines = yml.splitlines()
        # Find last occurrence of a URL line
        last_url_idx = -1
        for i, line in enumerate(lines):
            if line.strip().startswith('- "https://ranklocall.com/'):
                last_url_idx = i
        if last_url_idx >= 0:
            lines = lines[:last_url_idx+1] + yml_new + lines[last_url_idx+1:]
            yml = '\n'.join(lines) + '\n'
        else:
            print('ERROR: could not find insertion point in yml')
            exit(1)
    else:
        yml = yml.replace(insert_marker, '\n'.join(yml_new) + '\n' + insert_marker)
    with open(yml_path, 'w', encoding='utf-8') as f:
        f.write(yml)
    print(f'google-indexing.yml: added {len(yml_new)} URLs')
else:
    print('google-indexing.yml: nothing to add')

print('\nDone. Now run: git add -A && git commit -m "batch2: 25 new pages" && git push')
