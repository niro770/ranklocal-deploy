import sys, re
sys.stdout.reconfigure(encoding="utf-8")
p = open(r"C:\Users\19522\Documents\ranklocal-deploy-push\what-is-a-billable-call\index.html", encoding="utf-8").read()
i = p.find("<main")
h = p[:i]
k = h.rfind("</script>")
print("=== after ld+json to main (len %d) ===" % (i - k))
print(h[k:k + 400])
print("...")
print(h[-1500:])
print("=== apply links in main ===")
j = p.find("</main>")
for m in re.finditer(r'<a[^>]*href="/apply/"[^>]*>[^<]*</a>', p[i:j]):
    print(m.group(0)[:400]); break
print("=== faq markup in main ===")
m = re.search(r"<h2[^>]*>[^<]*(FAQ|Frequently)[^<]*</h2>.{0,700}", p[i:j], re.S)
print(m.group(0) if m else "none")
print("css links:", re.findall(r'<link[^>]*stylesheet[^>]*>', p))
print("n style blocks:", p.count("<style"))
