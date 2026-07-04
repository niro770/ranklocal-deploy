import os, glob

root = r'C:\Users\19522\Documents\ranklocal-deploy-push'

NEW_UL = ('    <li><a href="/appointment-setting/">Appointment Setting</a></li>\n'
          '    <li><a href="/pay-per-call/">Pay-Per-Call</a></li>\n'
          '    <li><a href="/contractor-leads/">Contractor Leads</a></li>\n'
          '    <li><a href="/blog/">Blog</a></li>')

NEW_UL_6 = ('      <li><a href="/appointment-setting/">Appointment Setting</a></li>\n'
            '      <li><a href="/pay-per-call/">Pay-Per-Call</a></li>\n'
            '      <li><a href="/contractor-leads/">Contractor Leads</a></li>\n'
            '      <li><a href="/blog/">Blog</a></li>')

NEW_DIV = ('      <a href="/appointment-setting/">Appointment Setting</a>\n'
           '      <a href="/pay-per-call/">Pay-Per-Call</a>\n'
           '      <a href="/contractor-leads/">Contractor Leads</a>\n'
           '      <a href="/blog/" class="active">Blog</a>\n'
           '      <a href="/apply/" class="btn-outline">Apply Now</a>')

NEW_INLINE = ('<ul class="nav-links">'
              '<li><a href="/appointment-setting/">Appointment Setting</a></li>'
              '<li><a href="/pay-per-call/">Pay-Per-Call</a></li>'
              '<li><a href="/contractor-leads/">Contractor Leads</a></li>'
              '<li><a href="/blog/">Blog</a></li>'
              '</ul>')

replacements = [
    # Pattern 1: minified inline nav
    ('<ul class="nav-links">'
     '<li><a href="/#services">Services</a></li>'
     '<li><a href="/#results">Results</a></li>'
     '<li><a href="/pay-per-call-marketplace/" style="color:var(--blue);font-weight:600;">Marketplace</a></li>'
     '</ul>',
     NEW_INLINE),

    # Pattern 2: blog subpages with Apply Now
    ('      <a href="/#services">Services</a>\n'
     '      <a href="/pay-per-call-marketplace/">Marketplace</a>\n'
     '      <a href="/blog/" class="active">Blog</a>\n'
     '      <a href="/apply/" class="btn-outline">Apply Now</a>',
     NEW_DIV),

    # Pattern 3: blog index with Get Started
    ('      <a href="/#services">Services</a>\n'
     '      <a href="/pay-per-call-marketplace/">Marketplace</a>\n'
     '      <a href="/blog/" class="active">Blog</a>\n'
     '      <a href="/#contact" class="btn-outline">Get Started</a>',
     NEW_DIV),

    # Pattern 4: local-seo/pay-per-call style (/#process /#testimonials /citations/)
    ('      <li><a href="/#services">Services</a></li>\n'
     '      <li><a href="/#results">Results</a></li>\n'
     '      <li><a href="/#process">Process</a></li>\n'
     '      <li><a href="/#testimonials">Reviews</a></li>\n'
     '      <li><a href="/citations/">Citations</a></li>',
     NEW_UL_6),

    # Pattern 5: marketplace style (/#process /#faq /pay-per-call-marketplace/)
    ('      <li><a href="/#services">Services</a></li>\n'
     '      <li><a href="/#results">Results</a></li>\n'
     '      <li><a href="/#process">Process</a></li>\n'
     '      <li><a href="/#faq">FAQ</a></li>\n'
     '      <li><a href="/pay-per-call-marketplace/" style="color:#00AAFF;font-weight:600;">Pay Per Call Marketplace</a></li>',
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
