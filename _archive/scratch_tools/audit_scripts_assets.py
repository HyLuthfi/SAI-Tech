import os
import re
import sys
import glob

sys.stdout.reconfigure(encoding='utf-8')

root_dir = r"d:\Area_Antigravity\SAI Tech\SAI Tech"
active_html = [
    'index.html', 'about.html', 'services.html', 'service-single.html',
    'portfolio.html', 'portfolio-single.html', 'pricing.html',
    'blog.html', 'blog-single.html', 'team.html', 'contact.html'
]

print("=" * 70)
print("1. SCRIPT USAGE AUDIT")
print("=" * 70)

# Collect all JS files in root and assets
js_files = []
for r, d, files in os.walk(root_dir):
    if 'node_modules' in r or '.git' in r:
        continue
    for f in files:
        if f.endswith('.js'):
            rel = os.path.relpath(os.path.join(r, f), root_dir)
            js_files.append(rel)

print(f"Total JS files found in repository: {len(js_files)}")
for jf in js_files:
    print(f"  - {jf}")

# Check which HTML files reference which JS files
print("\nScanning active HTML files for script tags...")
html_scripts = {}
inline_scripts_summary = {}

for h in active_html:
    hpath = os.path.join(root_dir, h)
    if not os.path.exists(hpath):
        continue
    with open(hpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # External scripts
    srcs = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', content, re.IGNORECASE)
    html_scripts[h] = srcs

    # Inline script patterns
    inlines = re.findall(r'<script(?![^>]*src=)[^>]*>([\s\S]*?)</script>', content, re.IGNORECASE)
    inline_types = []
    for s in inlines:
        s_clean = s.strip()
        if '__WEBFLOW_CURRENCY_SETTINGS' in s_clean:
            inline_types.append('Webflow Currency Settings (E-commerce cart template)')
        elif 'DocumentTouch' in s_clean:
            inline_types.append('Touch / JS detection helper')
        elif 'sai-kinetic-suite' in s_clean or 'IntersectionObserver' in s_clean:
            inline_types.append('SAI Kinetic Motion Suite')
        elif 'initBannerCenterReveal' in s_clean:
            inline_types.append('Banner Center Reveal Animation')
        elif 'Contact-Form' in s_clean:
            inline_types.append('WhatsApp Contact Form Dispatcher')
        else:
            first_line = s_clean.split('\n')[0][:50]
            inline_types.append(f'Other inline: {first_line}...')
    inline_scripts_summary[h] = inline_types

print("\n--- Script references per page ---")
all_referenced_js = set()
for h, srcs in html_scripts.items():
    print(f"{h}:")
    for s in srcs:
        clean_src = s.split('?')[0].replace('/', '\\')
        all_referenced_js.add(clean_src)
        print(f"  -> {s}")

print("\n--- JS Files in disk vs Referenced ---")
for jf in js_files:
    # Normalize
    norm_jf = jf.replace('/', '\\')
    is_ref = any(norm_jf in ref or os.path.basename(norm_jf) in ref for ref in all_referenced_js)
    status = "REFERENCED & ACTIVE" if is_ref else "UNUSED / DEAD SCRIPT"
    print(f"  [{status}] {jf}")

print("\n--- Inline scripts breakdown ---")
for h, inlines in inline_scripts_summary.items():
    print(f"{h}: {inlines}")

print("\n" + "=" * 70)
print("2. ASSET / IMAGE AUDIT")
print("=" * 70)

# Check root images
root_images = [f for f in os.listdir(root_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.svg', '.gif', '.ico'))]
print(f"Images in ROOT directory ({len(root_images)}):")
for img in root_images:
    # Check if referenced in HTML/CSS
    ref_count = 0
    ref_pages = []
    for h in active_html:
        hpath = os.path.join(root_dir, h)
        if os.path.exists(hpath):
            with open(hpath, 'r', encoding='utf-8') as f:
                if img in f.read():
                    ref_count += 1
                    ref_pages.append(h)
    print(f"  - {img} (referenced in {ref_count} pages: {ref_pages})")

# Check assets/ root images
assets_dir = os.path.join(root_dir, 'assets')
assets_images = [f for f in os.listdir(assets_dir) if os.path.isfile(os.path.join(assets_dir, f)) and f.lower().endswith(('.png', '.jpg', '.jpeg', '.svg', '.gif', '.ico'))]
print(f"\nImages directly in 'assets/' root ({len(assets_images)}):")
for img in assets_images:
    ref_count = 0
    ref_pages = []
    for h in active_html:
        hpath = os.path.join(root_dir, h)
        if os.path.exists(hpath):
            with open(hpath, 'r', encoding='utf-8') as f:
                if img in f.read():
                    ref_count += 1
                    ref_pages.append(h)
    print(f"  - assets/{img} (referenced in {ref_count} pages: {ref_pages})")

print("=" * 70)
