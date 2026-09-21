import urllib.request
import re
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

routes = [
    '/', '/about', '/services', '/service-single',
    '/portfolio', '/portfolio-single', '/pricing',
    '/blog', '/blog-single', '/team', '/contact'
]

print("=== 1. VERIFYING ALL 11 ROUTES ===")
for r in routes:
    path = r if r.startswith('/') else '/' + r
    url = f"http://127.0.0.1:3000{path}"
    try:
        res = urllib.request.urlopen(url, timeout=3)
        print(f"ROUTE {path:<20} -> {res.status} OK")
    except Exception as e:
        print(f"ROUTE {path:<20} -> ERROR: {e}")

print("\n=== 2. VERIFYING ASSET LINKS ON DISK ===")
root = r"d:\Area_Antigravity\SAI Tech\SAI Tech"
active_html = [
    'index.html', 'about.html', 'services.html', 'service-single.html',
    'portfolio.html', 'portfolio-single.html', 'pricing.html',
    'blog.html', 'blog-single.html', 'team.html', 'contact.html'
]

missing_assets = set()
for h in active_html:
    with open(os.path.join(root, h), 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all asset references (img, link, script)
    srcs = re.findall(r'(?:src|href)=["\'](assets/[^"\']+)["\']', content)
    for s in srcs:
        clean = s.split('?')[0].replace('%20', ' ')
        full_p = os.path.join(root, clean)
        if not os.path.exists(full_p):
            missing_assets.add((h, s))

if missing_assets:
    print(f"WARNING: {len(missing_assets)} missing asset references found:")
    for h, s in missing_assets:
        print(f"  {h} -> {s}")
else:
    print("SUCCESS: 100% of asset references exist on disk!")

print("\n=== 3. VERIFYING ZERO CURRENCY SCRIPTS ===")
currency_found = []
for h in active_html:
    with open(os.path.join(root, h), 'r', encoding='utf-8') as f:
        if '__WEBFLOW_CURRENCY_SETTINGS' in f.read():
            currency_found.append(h)
if currency_found:
    print(f"Currency scripts still in: {currency_found}")
else:
    print("SUCCESS: All 11 pages have clean, zero-redundant scripts!")
