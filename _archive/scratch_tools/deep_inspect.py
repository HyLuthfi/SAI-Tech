import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

root_dir = r"d:\Area_Antigravity\SAI Tech\SAI Tech"
active_html = [
    'index.html', 'about.html', 'services.html', 'service-single.html',
    'portfolio.html', 'portfolio-single.html', 'pricing.html',
    'blog.html', 'blog-single.html', 'team.html', 'contact.html'
]

print("=== CHECKING CSS REFERENCES IN HTML ===")
for h in active_html:
    with open(os.path.join(root_dir, h), 'r', encoding='utf-8') as f:
        content = f.read()
    css_links = re.findall(r'<link[^>]+rel=["\']stylesheet["\'][^>]*href=["\']([^"\']+)["\']', content, re.IGNORECASE)
    css_links += re.findall(r'<link[^>]+href=["\']([^"\']+)["\'][^>]*rel=["\']stylesheet["\']', content, re.IGNORECASE)
    print(f"{h}: {css_links}")

print("\n=== CHECKING IF shared.css IS USED ANYWHERE ===")
for h in active_html:
    with open(os.path.join(root_dir, h), 'r', encoding='utf-8') as f:
        c = f.read()
        if 'shared.css' in c:
            print(f"  FOUND shared.css in {h}")

print("\n=== CHECKING DUPLICATE KINETIC SUITE IN about.html ===")
with open(os.path.join(root_dir, 'about.html'), 'r', encoding='utf-8') as f:
    about_content = f.read()
ks_matches = re.findall(r'<script id="sai-kinetic-suite">[\s\S]*?</script>', about_content)
print(f"sai-kinetic-suite script count in about.html: {len(ks_matches)}")

print("\n=== CHECKING EXACT IMAGE REFERENCES IN HTML ===")
# Collect all img src and bg url
all_img_refs = set()
for h in active_html:
    with open(os.path.join(root_dir, h), 'r', encoding='utf-8') as f:
        c = f.read()
    srcs = re.findall(r'src=["\']([^"\']+\.(?:png|jpg|jpeg|svg|gif|ico|webp))(?:\?[^"\']*)?["\']', c, re.IGNORECASE)
    bgs = re.findall(r'url\(["\']?([^"\'\)]+\.(?:png|jpg|jpeg|svg|gif|ico|webp))(?:\?[^"\'\)]*)?["\']?\)', c, re.IGNORECASE)
    for s in srcs + bgs:
        all_img_refs.add((h, s))

# Group by path pattern
root_refs = [r for r in all_img_refs if '/' not in r[1] and '\\' not in r[1]]
print(f"Images referenced directly in root without folder prefix: {len(root_refs)}")
for page, ref in sorted(root_refs):
    print(f"  {page} -> {ref}")

print("\n=== CHECKING WHAT shared.js CONTAINS ===")
shared_js_path = os.path.join(root_dir, 'shared.js')
if os.path.exists(shared_js_path):
    with open(shared_js_path, 'r', encoding='utf-8') as f:
        sjs = f.read()
    print(f"shared.js size: {len(sjs)} bytes, preview: {sjs[:200]}")
