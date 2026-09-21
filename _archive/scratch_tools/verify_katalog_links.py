import os

all_html_files = [
    'index.html', 'about.html', 'services.html', 'service-single.html',
    'portfolio.html', 'portfolio-single.html', 'pricing.html',
    'blog.html', 'blog-single.html', 'team.html', 'contact.html', 'katalog.html'
]

print("=== VERIFYING KATALOG INTEGRATION ACROSS ALL 12 PAGES ===")
all_pass = True

for hf in all_html_files:
    if not os.path.exists(hf):
        print(f"MISSING FILE: {hf}")
        all_pass = False
        continue

    with open(hf, 'r', encoding='utf-8') as f:
        content = f.read()

    has_nav = 'href="katalog"' in content or 'href="/katalog"' in content
    has_footer = 'Katalog Digital' in content or 'katalog' in content.lower()
    nav_count = content.count('href="katalog"')

    print(f"{hf:<22} | Nav: {'[OK]' if has_nav else '[FAIL]'} (count={nav_count}) | Footer: {'[OK]' if has_footer else '[FAIL]'}")
    if not has_nav or not has_footer:
        all_pass = False

print("\nOverall Status:", "ALL PASSED [OK]" if all_pass else "SOME FAILED [FAIL]")
