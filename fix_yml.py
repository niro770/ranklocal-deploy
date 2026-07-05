"""
Append 25 new batch-2 URLs to the google-indexing.yml urlList JSON strings.
"""
import os

YML = r'C:\Users\19522\Documents\ranklocal-deploy-push\.github\workflows\google-indexing.yml'

NEW_SLUGS = [
    'hvac-leads', 'ac-repair-leads', 'heating-leads', 'plumbing-leads',
    'emergency-plumbing-leads', 'water-heater-leads',
    'fence-leads-texas', 'fence-leads-florida', 'fence-leads-arizona', 'fence-leads-california',
    'garage-door-spring-repair-leads', 'garage-door-opener-leads', 'garage-door-replacement-leads',
    'outdoor-lighting-leads',
    'roofing-leads-ohio', 'roofing-leads-illinois', 'roofing-leads-colorado',
    'roofing-leads-north-carolina', 'roofing-leads-arizona',
    'painting-leads', 'window-replacement-leads', 'siding-leads', 'gutter-leads',
    'pressure-washing-leads', 'electrical-leads',
]

new_url_fragments = ''.join(f', "https://ranklocall.com/{s}/"' for s in NEW_SLUGS)

with open(YML, encoding='utf-8') as f:
    content = f.read()

# Exact tail from file inspection:
OLD_TAIL = 'ai-appointment-setting-for-contractors/"]}\')'
NEW_TAIL = 'ai-appointment-setting-for-contractors/"' + new_url_fragments + ']}\')'

count_before = content.count(OLD_TAIL)
print(f'Found {count_before} occurrences of tail pattern (expect 2)')

if count_before == 0:
    print('ERROR: pattern not found')
    exit(1)

content = content.replace(OLD_TAIL, NEW_TAIL)

# Update the count in echo statements (158 old + 25 new = 183)
content = content.replace('128 URLs', '183 URLs')
content = content.replace('Submitting 128 URLs', 'Submitting 183 URLs')
# Also check for the "Done — X URLs submitted" line
content = content.replace('Done -- 128 URLs submitted', 'Done -- 183 URLs submitted')
content = content.replace('Done — 128 URLs submitted', 'Done — 183 URLs submitted')

with open(YML, 'w', encoding='utf-8') as f:
    f.write(content)

print('Done — google-indexing.yml updated with 25 new URLs')

# Verify
with open(YML, encoding='utf-8') as f:
    verify = f.read()
print(f'electrical-leads in yml: {"electrical-leads" in verify}')
print(f'hvac-leads in yml: {"hvac-leads" in verify}')
