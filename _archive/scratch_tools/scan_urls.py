import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html')]
results = {}

for hf in sorted(html_files):
    with open(hf, 'r', encoding='utf-8') as f:
        content = f.read()
    urls = re.findall(r'https?://[^\s"\'<>\)]+', content)
    filtered = []
    for u in urls:
        if any(d in u for d in ['wa.me', 'instagram.com', 'tiktok.com', 'webflow.com']):
            continue
        filtered.append(u)
    if filtered:
        results[hf] = sorted(list(set(filtered)))

for hf, ulist in results.items():
    print(f"=== {hf} ===")
    for u in ulist:
        print(f"  {u}")
