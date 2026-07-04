"""Check which gap pages already have the required links."""
import os

checks = [
    (r'pay-per-appointment\index.html', '/appointment-setting/'),
    (r'exclusive-vs-shared-leads\index.html', '/contractor-leads/'),
    (r'roofing-leads-cost\index.html', '/roofing-leads/'),
    (r'ranklocall-vs-servicedirect\index.html', '/contractor-leads/'),
    (r'case-studies\proplumb\index.html', '/pay-per-call/'),
    (r'case-studies\proplumb\index.html', '/appointment-setting/'),
    (r'blog\how-to-get-roofing-customers\index.html', '/roofing-leads/'),
    (r'blog\how-to-get-fencing-customers\index.html', '/fence-leads/'),
    (r'blog\how-to-get-landscaping-customers\index.html', '/landscaping-leads/'),
    (r'blog\how-to-get-pest-control-customers\index.html', '/pest-control-leads/'),
    (r'blog\how-to-get-garage-door-customers\index.html', '/garage-door-repair-leads/'),
    (r'blog\how-to-grow-a-roofing-business\index.html', '/roofing-leads/'),
    (r'blog\how-to-grow-a-fencing-business\index.html', '/fence-leads/'),
    (r'blog\how-to-grow-a-landscaping-business\index.html', '/landscaping-leads/'),
    (r'blog\how-to-grow-a-pest-control-business\index.html', '/pest-control-leads/'),
    (r'blog\how-to-grow-a-garage-door-business\index.html', '/garage-door-repair-leads/'),
]

base = r'C:\Users\19522\Documents\ranklocal-deploy-push'
missing = []
present = []

for rel_path, target_link in checks:
    full_path = os.path.join(base, rel_path)
    if not os.path.exists(full_path):
        print(f"FILE NOT FOUND: {rel_path}")
        continue
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()
    if target_link in content:
        present.append(f"  OK  {rel_path} -> {target_link}")
    else:
        missing.append(f"MISSING {rel_path} -> {target_link}")

print("\n=== ALREADY LINKED ===")
for p in present:
    print(p)

print("\n=== NEED LINKING ===")
for m in missing:
    print(m)
