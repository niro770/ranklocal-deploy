import os
import glob

root = r'C:\Users\19522\Documents\ranklocal-deploy-push'

old_nav = '    <li><a href="/#services">Services</a></li>\n    <li><a href="/#results">Results</a></li>\n    <li><a href="/pay-per-call-marketplace/" style="color:var(--blue);font-weight:600;">Marketplace</a></li>'

new_nav = '    <li><a href="/appointment-setting/">Appointment Setting</a></li>\n    <li><a href="/pay-per-call/">Pay-Per-Call</a></li>\n    <li><a href="/contractor-leads/">Contractor Leads</a></li>\n    <li><a href="/blog/">Blog</a></li>'

count = 0
skipped = 0
for html_file in glob.glob(os.path.join(root, '**', 'index.html'), recursive=True):
    rel = os.path.relpath(html_file, root)
    if rel == 'index.html':
        skipped += 1
        continue
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    if old_nav in content:
        new_content = content.replace(old_nav, new_nav)
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1

print(f'Updated: {count} files | Skipped root: {skipped}')
