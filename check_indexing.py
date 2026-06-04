import os, json, requests
from datetime import datetime, timezone

CLIENT_ID = os.environ["GOOGLE_CLIENT_ID"]
CLIENT_SECRET = os.environ["GOOGLE_CLIENT_SECRET"]
REFRESH_TOKEN = os.environ["GOOGLE_REFRESH_TOKEN"]
SITE_URL = "https://ranklocall.com/"

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
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN,
        "grant_type": "refresh_token"
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
        "robots_txt": data.get("robotsTxtState", "UNKNOWN"),
        "indexing_state": data.get("indexingState", "UNKNOWN"),
    }

print("Getting access token...")
token = get_access_token()
print("Token OK")

results = {}
for url in URLS:
    result = inspect_url(token, url)
    results[url] = result
    status = result["verdict"]
    print(f"  {status:10} {url}")

output = {
    "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "urls": results
}

with open("indexing-status.json", "w") as f:
    json.dump(output, f, indent=2)

indexed = sum(1 for v in results.values() if v["verdict"] == "PASS")
print(f"\nDone: {indexed}/{len(URLS)} indexed")
