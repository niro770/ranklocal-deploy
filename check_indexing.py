import os, json, requests, base64, email.mime.text, email.mime.multipart
from datetime import datetime, timezone

CLIENT_ID     = os.environ["GOOGLE_CLIENT_ID"]
CLIENT_SECRET = os.environ["GOOGLE_CLIENT_SECRET"]
REFRESH_TOKEN = os.environ["GOOGLE_REFRESH_TOKEN"]
SITE_URL      = "https://ranklocall.com/"
NOTIFY_EMAIL  = "nir@marketing770.com"

URLS = [
  "https://ranklocall.com/",
  "https://ranklocall.com/local-seo/",
  "https://ranklocall.com/google-maps-ranking/",
  "https://ranklocall.com/google-business-profile/",
  "https://ranklocall.com/website-seo/",
  "https://ranklocall.com/reputation-management/",
  "https://ranklocall.com/citations/",
  "https://ranklocall.com/apply/",
  "https://ranklocall.com/ranklocall-vs-servicedirect/",
  "https://ranklocall.com/pay-per-call/",
  "https://ranklocall.com/pay-per-call-marketplace/",
  "https://ranklocall.com/pay-per-call-plumbers/",
  "https://ranklocall.com/pay-per-call-hvac/",
  "https://ranklocall.com/pay-per-call-roofing/",
  "https://ranklocall.com/pay-per-call-lawyers/",
  "https://ranklocall.com/pay-per-call-dentists/",
  "https://ranklocall.com/pay-per-call-contractors/",
  "https://ranklocall.com/pay-per-call-electricians/",
  "https://ranklocall.com/pay-per-call-pest-control/",
  "https://ranklocall.com/pay-per-call-locksmiths/",
  "https://ranklocall.com/pay-per-call-insurance/",
  "https://ranklocall.com/pay-per-call-water-damage/",
  "https://ranklocall.com/pay-per-call-garage-door/",
  "https://ranklocall.com/pay-per-call-tree-service/",
  "https://ranklocall.com/pay-per-call-landscaping/",
  "https://ranklocall.com/tools/",
  "https://ranklocall.com/tools/roi-calculator/",
  "https://ranklocall.com/tools/call-value-calculator/",
  "https://ranklocall.com/tools/local-seo-audit/",
  "https://ranklocall.com/tools/market-domination-planner/",
  "https://ranklocall.com/tools/geo-grid-scanner/",
  "https://ranklocall.com/tools/map-pack-anatomy/",
  "https://ranklocall.com/tools/rank-simulator/",
  "https://ranklocall.com/blog/",
  "https://ranklocall.com/blog/best-pay-per-call-networks/",
  "https://ranklocall.com/blog/best-local-seo-companies/",
  "https://ranklocall.com/blog/what-is-pay-per-call-advertising/",
  "https://ranklocall.com/blog/pay-per-call-vs-pay-per-lead/",
  "https://ranklocall.com/blog/how-does-pay-per-call-work/",
  "https://ranklocall.com/blog/pay-per-call-vs-google-ads/",
  "https://ranklocall.com/blog/pay-per-call-roi-tips/",
  "https://ranklocall.com/blog/best-industries-for-pay-per-call/",
]

def get_access_token():
    r = requests.post("https://oauth2.googleapis.com/token", data={
        "client_id": CLIENT_ID, "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN, "grant_type": "refresh_token"
    })
    r.raise_for_status()
    return r.json()["access_token"]

def inspect_url(access_token, url):
    r = requests.post(
        "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect",
        headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"},
        json={"inspectionUrl": url, "siteUrl": SITE_URL}
    )
    if r.status_code != 200:
        return {"verdict": "ERROR", "last_crawled": None, "coverage": f"API error {r.status_code}"}
    data = r.json().get("inspectionResult", {}).get("indexStatusResult", {})
    return {
        "verdict": data.get("verdict", "UNKNOWN"),
        "last_crawled": data.get("lastCrawlTime"),
        "coverage": data.get("coverageState", "Unknown"),
        "indexing_state": data.get("indexingState", "UNKNOWN"),
    }

def send_email(access_token, subject, body_html):
    msg = email.mime.multipart.MIMEMultipart("alternative")
    msg["From"] = NOTIFY_EMAIL
    msg["To"] = NOTIFY_EMAIL
    msg["Subject"] = subject
    msg.attach(email.mime.text.MIMEText(body_html, "html"))
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    r = requests.post(
        "https://gmail.googleapis.com/gmail/v1/users/me/messages/send",
        headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"},
        json={"raw": raw}
    )
    return r.status_code

# Load previous results
try:
    with open("indexing-status.json") as f:
        previous = json.load(f)
    prev_urls = previous.get("urls", {})
except Exception:
    prev_urls = {}

print("Getting access token...")
access_token = get_access_token()
print("Token OK — checking URLs...")

results = {}
newly_indexed = []

for url in URLS:
    result = inspect_url(access_token, url)
    results[url] = result
    prev_verdict = prev_urls.get(url, {}).get("verdict", "PENDING")
    is_new = result["verdict"] == "PASS" and prev_verdict != "PASS"
    if is_new:
        newly_indexed.append(url)
    icon = "✅" if result["verdict"] == "PASS" else "⏳"
    print(f"  {icon} {result['verdict']:10} {url}")

now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
output = {"last_updated": now, "urls": results}

with open("indexing-status.json", "w") as f:
    json.dump(output, f, indent=2)

indexed_total = sum(1 for v in results.values() if v["verdict"] == "PASS")
print(f"\nDone: {indexed_total}/{len(URLS)} indexed, {len(newly_indexed)} newly indexed")

# Send email if any newly indexed
if newly_indexed:
    rows = "".join(
        f'<tr><td style="padding:8px 12px;border-bottom:1px solid #eee;">' +
        f'<a href="{u}" style="color:#00aaff;text-decoration:none;">{u.replace("https://ranklocall.com","")}</a></td>' +
        f'<td style="padding:8px 12px;border-bottom:1px solid #eee;color:#00cc88;font-weight:600;">✅ Indexed</td></tr>'
        for u in newly_indexed
    )
    body = f"""
    <div style="font-family:sans-serif;max-width:600px;margin:0 auto;color:#222;">
      <div style="background:#07070a;padding:20px 24px;border-radius:8px 8px 0 0;">
        <h1 style="color:#fff;font-size:18px;margin:0;">
          <span style="color:#00aaff;">RANK</span><span style="color:#7b4fff;">LOCAL</span>
          — Indexing Update
        </h1>
      </div>
      <div style="background:#fff;border:1px solid #eee;border-radius:0 0 8px 8px;padding:24px;">
        <p style="font-size:15px;">
          <strong>{len(newly_indexed)} new page{"s" if len(newly_indexed)>1 else ""}</strong>
          just got indexed on Google!
        </p>
        <table style="width:100%;border-collapse:collapse;font-size:14px;">
          <thead>
            <tr style="background:#f5f5fa;">
              <th style="padding:8px 12px;text-align:left;">URL</th>
              <th style="padding:8px 12px;text-align:left;">Status</th>
            </tr>
          </thead>
          <tbody>{rows}</tbody>
        </table>
        <p style="margin-top:20px;font-size:13px;color:#888;">
          Total indexed: {indexed_total}/{len(URLS)} pages &nbsp;|&nbsp; 
          Checked: {now[:10]}
        </p>
        <a href="https://ranklocall.com" style="display:inline-block;margin-top:8px;padding:10px 20px;background:#00aaff;color:#fff;border-radius:6px;text-decoration:none;font-size:13px;font-weight:600;">
          View Site →
        </a>
      </div>
    </div>"""
    status = send_email(access_token, f"🎉 {len(newly_indexed)} new page(s) indexed — ranklocall.com", body)
    print(f"Email sent: {status}")
else:
    print("No new indexing — no email sent")
