import os, json, re

BASE = r'C:\Users\19522\Documents\ranklocal-deploy-push'
ORG  = 'https://ranklocall.com/#organization'
PERSON = 'https://ranklocall.com/about/#person'
DATE = '2026-07-05'

# slug -> ('Service'|'Article', name, description, areaServed)
SERVICE_PAGES = {
    'roofing-leads-texas': (
        'Exclusive Roofing Leads — Texas',
        'Exclusive pay-per-call roofing leads for Texas contractors across Dallas-Fort Worth, Houston, San Antonio, and Austin. Storm damage, insurance, and replacement calls.',
        ['Texas','Dallas','Houston','San Antonio','Austin']
    ),
    'roofing-leads-florida': (
        'Exclusive Roofing Leads — Florida',
        'Exclusive pay-per-call roofing leads for Florida contractors. Hurricane, storm damage, and year-round replacement across Miami, Tampa, Orlando, and Jacksonville.',
        ['Florida','Miami','Tampa','Orlando','Jacksonville']
    ),
    'roofing-leads-georgia': (
        'Exclusive Roofing Leads — Georgia',
        'Exclusive pay-per-call roofing leads for Georgia contractors across Atlanta, Savannah, Augusta, and statewide.',
        ['Georgia','Atlanta','Savannah','Augusta']
    ),
    'insurance-roofing-leads': (
        'Insurance Roofing Leads',
        'Exclusive pay-per-call leads for insurance-approved roofing work. Homeowners with active storm damage claims, pre-qualified for insurance coverage.',
        'United States'
    ),
    'tree-service-leads': (
        'Exclusive Tree Service Leads',
        'Pay-per-call tree removal, trimming, and emergency tree service leads for certified arborists and tree service companies nationwide.',
        'United States'
    ),
    'solar-roofing-leads': (
        'Solar Roofing Leads',
        'Exclusive pay-per-call leads for solar roofing installations. Homeowners actively researching solar panels and energy-efficient roofing upgrades.',
        'United States'
    ),
    'irrigation-leads': (
        'Irrigation System Leads',
        'Exclusive pay-per-call leads for irrigation installation and repair. Homeowners and commercial property managers seeking irrigation services.',
        'United States'
    ),
    'hardscaping-leads': (
        'Hardscaping Leads',
        'Exclusive pay-per-call leads for patios, retaining walls, walkways, and outdoor living spaces. Qualified homeowners ready for estimates.',
        'United States'
    ),
    'mosquito-control-leads': (
        'Mosquito Control Leads',
        'Exclusive pay-per-call mosquito treatment and prevention leads for pest control companies. Residential and commercial inquiries.',
        'United States'
    ),
    'bee-removal-leads': (
        'Bee Removal Leads',
        'Exclusive pay-per-call bee removal and hive relocation leads for licensed pest control operators and beekeepers.',
        'United States'
    ),
    'roofing-leads-in-winter': (
        'Winter Roofing Leads',
        'Exclusive pay-per-call roofing leads during winter. Ice dam removal, emergency leak repair, and storm damage calls that continue year-round.',
        'United States'
    ),
    'appointment-setting-cost': (
        'Contractor Appointment Setting Service',
        'Pre-qualified roofing and home service appointments booked directly to your calendar. Confirmed estimate visits, not raw form fills.',
        'United States'
    ),
    'ai-appointment-setting-for-contractors': (
        'AI Appointment Setting for Contractors',
        'AI-powered appointment setting for home service contractors. Automated lead follow-up, qualification, and calendar booking.',
        'United States'
    ),
    'google-local-services-ads-for-contractors': (
        'Google Local Services Ads for Contractors',
        'Google Local Services Ads setup and management for home service contractors. Google Guaranteed badge, dispute management, and budget optimization.',
        'United States'
    ),
}

ARTICLE_PAGES = [
    'what-is-exclusive-lead-generation',
    'angi-alternatives',
    'ranklocall-vs-angi',
    'ranklocall-vs-homeadvisor',
    'ranklocall-vs-thumbtack',
    'homeadvisor-alternatives',
    'google-lsa-vs-pay-per-call',
    'google-lsa-cost-per-lead-roofing',
    'speed-to-lead-for-contractors',
    'how-to-close-more-roofing-estimates',
    'lead-follow-up-sequence-for-contractors',
    'contractor-lead-generation-guide',
    'what-is-cost-per-lead',
    'contractor-lead-generation-glossary',
    'contractor-marketing-metrics-guide',
    'how-to-scale-a-roofing-company',
]

def make_area(area):
    if isinstance(area, list):
        return [{'@type':'State' if len(a) > 10 else 'City', 'name': a} for a in area]
    return {'@type':'Country','name': area}

def process_page(slug, page_dir):
    path = os.path.join(page_dir, 'index.html')
    if not os.path.exists(path):
        print(f'  SKIP (no index.html): {slug}')
        return False

    html = open(path, encoding='utf-8').read()

    # Find existing JSON-LD block
    pattern = r'(<script type="application/ld\+json">\s*)([\s\S]*?)(\s*</script>)'
    m = re.search(pattern, html)
    if not m:
        print(f'  SKIP (no JSON-LD): {slug}')
        return False

    # Check if already upgraded
    if '"Service"' in m.group(2) or '"Article"' in m.group(2):
        print(f'  SKIP (already has Service/Article): {slug}')
        return False

    try:
        data = json.loads(m.group(2))
    except Exception as e:
        print(f'  ERROR parsing JSON in {slug}: {e}')
        return False

    graph = data.get('@graph', [])
    page_url = f'https://ranklocall.com/{slug}/'

    # Find title from WebPage node
    title = next((n.get('name','') for n in graph if n.get('@type')=='WebPage'), '')
    desc  = next((n.get('description','') for n in graph if n.get('@type')=='WebPage'), '')

    if slug in SERVICE_PAGES:
        svc_name, svc_desc, area = SERVICE_PAGES[slug]
        graph.append({
            '@type': 'Service',
            '@id': f'{page_url}#service',
            'name': svc_name,
            'description': svc_desc,
            'provider': {'@id': ORG},
            'serviceType': 'Lead Generation',
            'areaServed': make_area(area),
            'url': page_url,
        })
        print(f'  + Service: {slug}')
    elif slug in ARTICLE_PAGES:
        graph.append({
            '@type': 'Article',
            '@id': f'{page_url}#article',
            'headline': title,
            'description': desc,
            'author': {'@id': PERSON},
            'publisher': {'@id': ORG},
            'datePublished': DATE,
            'dateModified': DATE,
            'mainEntityOfPage': {'@id': f'{page_url}#webpage'},
        })
        print(f'  + Article: {slug}')
    else:
        print(f'  SKIP (not in map): {slug}')
        return False

    data['@graph'] = graph
    new_json = json.dumps(data, separators=(',',':'))
    new_block = m.group(1) + new_json + m.group(3)
    new_html = html[:m.start()] + new_block + html[m.end():]
    open(path, 'w', encoding='utf-8').write(new_html)
    return True

all_slugs = list(SERVICE_PAGES.keys()) + ARTICLE_PAGES
updated = 0
for slug in all_slugs:
    page_dir = os.path.join(BASE, slug)
    print(f'Processing: {slug}')
    if process_page(slug, page_dir):
        updated += 1

print(f'\nDone. {updated}/{len(all_slugs)} pages updated.')
