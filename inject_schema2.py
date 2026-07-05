"""
Inject Service JSON-LD schema nodes into the 25 new batch-2 pages.
All batch-2 pages are Service type.
"""
import os, re, json

BASE = r'C:\Users\19522\Documents\ranklocal-deploy-push'
SITE = 'https://ranklocall.com'
ORG  = f'{SITE}/#organization'

# slug → (service_name, description, area)
PAGES = {
    'hvac-leads':             ('HVAC Leads', 'Exclusive pay-per-call HVAC leads for heating and cooling contractors.', 'United States'),
    'ac-repair-leads':        ('AC Repair Leads', 'Live inbound AC repair leads for HVAC companies.', 'United States'),
    'heating-leads':          ('Heating & Furnace Leads', 'Exclusive heating and furnace repair leads for contractors.', 'United States'),
    'plumbing-leads':         ('Plumbing Leads', 'Pay-per-call plumbing leads for residential and commercial plumbers.', 'United States'),
    'emergency-plumbing-leads':('Emergency Plumbing Leads', 'Live inbound emergency plumbing leads for plumbers.', 'United States'),
    'water-heater-leads':     ('Water Heater Leads', 'Exclusive water heater installation and repair leads.', 'United States'),
    'fence-leads-texas':      ('Fence Leads Texas', 'Exclusive fence contractor leads in Texas.', 'Texas, United States'),
    'fence-leads-florida':    ('Fence Leads Florida', 'Exclusive fence contractor leads in Florida.', 'Florida, United States'),
    'fence-leads-arizona':    ('Fence Leads Arizona', 'Exclusive fence contractor leads in Arizona.', 'Arizona, United States'),
    'fence-leads-california': ('Fence Leads California', 'Exclusive fence contractor leads in California.', 'California, United States'),
    'garage-door-spring-repair-leads': ('Garage Door Spring Repair Leads', 'Live pay-per-call garage door spring repair leads.', 'United States'),
    'garage-door-opener-leads':        ('Garage Door Opener Leads', 'Exclusive garage door opener installation and repair leads.', 'United States'),
    'garage-door-replacement-leads':   ('Garage Door Replacement Leads', 'Live inbound garage door replacement leads.', 'United States'),
    'outdoor-lighting-leads': ('Outdoor Lighting Leads', 'Exclusive outdoor and landscape lighting installation leads.', 'United States'),
    'roofing-leads-ohio':           ('Roofing Leads Ohio', 'Exclusive roofing leads in Ohio.', 'Ohio, United States'),
    'roofing-leads-illinois':       ('Roofing Leads Illinois', 'Exclusive roofing leads in Illinois.', 'Illinois, United States'),
    'roofing-leads-colorado':       ('Roofing Leads Colorado', 'Exclusive roofing leads in Colorado.', 'Colorado, United States'),
    'roofing-leads-north-carolina': ('Roofing Leads North Carolina', 'Exclusive roofing leads in North Carolina.', 'North Carolina, United States'),
    'roofing-leads-arizona':        ('Roofing Leads Arizona', 'Exclusive roofing leads in Arizona.', 'Arizona, United States'),
    'painting-leads':         ('Painting Leads', 'Exclusive interior and exterior painting leads for contractors.', 'United States'),
    'window-replacement-leads':('Window Replacement Leads', 'Live pay-per-call window replacement leads.', 'United States'),
    'siding-leads':           ('Siding Leads', 'Exclusive siding installation and replacement leads.', 'United States'),
    'gutter-leads':           ('Gutter Leads', 'Live gutter installation and repair leads for contractors.', 'United States'),
    'pressure-washing-leads': ('Pressure Washing Leads', 'Exclusive pressure washing service leads.', 'United States'),
    'electrical-leads':       ('Electrical Leads', 'Pay-per-call electrical contractor leads.', 'United States'),
}

PATTERN = re.compile(r'(<script type="application/ld\+json">\s*)([\s\S]*?)(\s*</script>)')

updated = 0
skipped = 0

for slug, (svc_name, svc_desc, area) in PAGES.items():
    path = os.path.join(BASE, slug, 'index.html')
    if not os.path.exists(path):
        print(f'  MISSING: {slug}')
        continue
    with open(path, encoding='utf-8') as f:
        html = f.read()
    m = PATTERN.search(html)
    if not m:
        print(f'  NO SCHEMA BLOCK: {slug}')
        continue
    raw_json = m.group(2)
    if '"Service"' in raw_json:
        print(f'  SKIP (Service exists): {slug}')
        skipped += 1
        continue
    try:
        data = json.loads(raw_json)
    except json.JSONDecodeError as e:
        print(f'  JSON ERROR: {slug}: {e}')
        continue

    page_url = f'{SITE}/{slug}/'
    service_node = {
        '@type': 'Service',
        '@id': f'{page_url}#service',
        'name': svc_name,
        'description': svc_desc,
        'provider': {'@id': ORG},
        'serviceType': 'Lead Generation',
        'areaServed': area,
        'url': page_url,
    }
    if isinstance(data.get('@graph'), list):
        data['@graph'].append(service_node)
    else:
        data['@graph'] = [service_node]

    new_json = json.dumps(data, separators=(',', ':'))
    new_html = html[:m.start()] + m.group(1) + new_json + m.group(3) + html[m.end():]
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print(f'  UPDATED: {slug}')
    updated += 1

print(f'\nSchema injection: {updated} updated, {skipped} skipped.')
