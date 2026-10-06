import json, os, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
REPO = r"C:\Users\19522\Documents\ranklocal-deploy-push"
os.chdir(REPO)
import weekly_seo_batch as w
rep = json.load(open("_v2_build_report.json"))
built, touched = rep["built"], rep["touched"]
print("sitemap added:", w.update_sitemap(built), "| yml added:", w.update_yml(built))

def git(*a):
    r = subprocess.run(["git"] + list(a), capture_output=True, text=True, encoding="utf-8", errors="replace")
    print("$ git", " ".join(a)[:90], "->", r.returncode)
    out = (r.stdout + r.stderr).strip()
    if out: print(out[-600:])
    return r.returncode

paths = [s + "/index.html" for s in built + touched] + ["sitemap.xml", ".github/workflows/google-indexing.yml"]
if git("add", "--", *paths): sys.exit("add failed")
git("status", "--short", "--untracked-files=no")
if git("commit", "-m", "v2 topical map: 63 new semantic pages + cluster/hub internal links on 14 existing pages"): sys.exit("commit failed")
if git("pull", "--rebase", "--autostash", "origin", "main"): sys.exit("pull failed - not pushed")
if git("push", "origin", "main"): sys.exit("push failed")
print("PUSH OK")
print("Google ping:", "OK" if w.ping_google() else "skipped/failed")
