#!/usr/bin/env python3
"""
One-time sitewide update for ranklocal-deploy:
adds Cookie Policy + SMS Disclosure links to every page footer,
and patches the weekly batch template so future pages include them.

Run from the ROOT of the ranklocal-deploy repo (where you have git push access):
    python3 apply_footer_links.py          # apply + commit + push
    python3 apply_footer_links.py --dry    # just report what would change
"""
import os, re, sys, subprocess

DRY = "--dry" in sys.argv

# Pattern 1: SEO batch pages — plain footer "Privacy • Terms"
OLD = '<a href="/terms/">Terms</a></p>'
NEW = ('<a href="/terms/">Terms</a> &bull; '
       '<a href="/cookie-policy/">Cookie Policy</a> &bull; '
       '<a href="/sms-disclosure/">SMS Disclosure</a></p>')

# Pattern 2: hub pages — styled footer link list ending in "Apply"
STYLE = 'style="color:#aac4e0;text-decoration:none;font-size:.88rem"'
OLD2 = f'<a href="/apply/" {STYLE}>Apply</a>'
NEW2 = (OLD2
        + f'\n<a href="/privacy/" {STYLE}>Privacy Policy</a>'
        + f'\n<a href="/terms/" {STYLE}>Terms of Use</a>'
        + f'\n<a href="/cookie-policy/" {STYLE}>Cookie Policy</a>'
        + f'\n<a href="/sms-disclosure/" {STYLE}>SMS Disclosure</a>')

changed = changed2 = skipped = 0
for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in ('.git', 'node_modules', '__pycache__')]
    for fn in files:
        if not fn.endswith('.html'):
            continue
        path = os.path.join(root, fn)
        try:
            s = open(path, encoding='utf-8').read()
        except Exception:
            continue
        if '/cookie-policy/' in s:
            skipped += 1
            continue
        if OLD in s:
            if not DRY:
                open(path, 'w', encoding='utf-8').write(s.replace(OLD, NEW, 1))
            changed += 1
        elif OLD2 in s:
            if not DRY:
                open(path, 'w', encoding='utf-8').write(s.replace(OLD2, NEW2, 1))
            changed2 += 1

print(f"SEO pages updated: {changed}  hub pages updated: {changed2}  (already done/skipped: {skipped})")

# Patch the generator template so NEW pages get the links too
tpl_changed = 0
for script in ('weekly_seo_batch.py', 'gen_pages.py', 'gen_batch2.py', 'gen_batch3.py'):
    if not os.path.exists(script):
        continue
    s = open(script, encoding='utf-8').read()
    old_tpl = "'<a href=\"/terms/\">Terms</a></p>'"
    new_tpl = ("'<a href=\"/terms/\">Terms</a> &bull; '\n"
               "          '<a href=\"/cookie-policy/\">Cookie Policy</a> &bull; '\n"
               "          '<a href=\"/sms-disclosure/\">SMS Disclosure</a></p>'")
    if old_tpl in s and '/cookie-policy/' not in s:
        if not DRY:
            open(script, 'w', encoding='utf-8').write(s.replace(old_tpl, new_tpl, 1))
        tpl_changed += 1
        print(f"template patched: {script}")

if DRY:
    print("(dry run — nothing written)")
    sys.exit(0)

if changed or tpl_changed:
    def run(*cmd):
        print('+', ' '.join(cmd))
        subprocess.run(cmd, check=True)
    # safe push pattern: stash nothing-else, pull --rebase, push
    run('git', 'add', '-A')
    run('git', 'commit', '-m',
        'Footer: add Cookie Policy + SMS Disclosure links sitewide (10DLC)')
    run('git', 'pull', '--rebase', 'origin', 'main')
    run('git', 'push', 'origin', 'main')
    print("Done — pushed.")
else:
    print("Nothing to do.")
