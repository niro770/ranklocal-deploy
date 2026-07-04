import os, glob

root = r'C:\Users\19522\Documents\ranklocal-deploy-push'

NEW_DIV = ('      <a href="/appointment-setting/">Appointment Setting</a>\n'
           '      <a href="/pay-per-call/">Pay-Per-Call</a>\n'
           '      <a href="/contractor-leads/">Contractor Leads</a>\n'
           '      <a href="/blog/" class="active">Blog</a>\n'
           '      <a href="/apply/" class="btn-outline">Apply Now</a>')

NEW_UL_6 = ('      <li><a href="/appointment-setting/">Appointment Setting</a></li>\n'
            '      <li><a href="/pay-per-call/">Pay-Per-Call</a></li>\n'
            '      <li><a href="/contractor-leads/">Contractor Leads</a></li>\n'
            '      <li><a href="/blog/">Blog</a></li>')

replacements = [
    # Blog pages with "btn btn-outline" + Get Started (slightly different from btn-outline)
    ('      <a href="/#services">Services</a>\n'
     '      <a href="/pay-per-call-marketplace/">Marketplace</a>\n'
     '      <a href="/blog/" class="active">Blog</a>\n'
     '      <a href="/#contact" class="btn btn-outline" style="padding:8px 18px;">Get Started</a>',
     NEW_DIV),

    # Citations page (unique nav)
    ('      <li><a href="/#services">Services</a></li>\n'
     '      <li><a href="/#results">Results</a></li>\n'
     '      <li><a href="/citations/" style="color:#00AAFF;">Citations</a></li>\n'
     '      <li><a href="/#faq">FAQ</a></li>',
     NEW_UL_6),
]

count = 0
for html_file in glob.glob(os.path.join(root, '**', 'index.html'), recursive=True):
    if os.path.relpath(html_file, root) == 'index.html':
        continue
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    new_content = content
    for old, new in replacements:
        new_content = new_content.replace(old, new)
    if new_content != content:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1

print(f'Updated: {count} additional files')
