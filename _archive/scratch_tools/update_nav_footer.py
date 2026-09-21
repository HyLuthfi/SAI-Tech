import os
import re

html_files = [
    'index.html', 'about.html', 'services.html', 'service-single.html',
    'portfolio.html', 'portfolio-single.html', 'pricing.html',
    'blog.html', 'blog-single.html', 'team.html', 'contact.html'
]

# In Navbar: insert <a class="nav-link w-nav-link" href="katalog">Katalog</a> right after services link or before portfolio
# Pattern 1: <a class="nav-link w-nav-link" href="services">Layanan</a>
# If on services page: <a aria-current="page" class="nav-link w-nav-link w--current" href="services">Layanan</a>

for hf in html_files:
    with open(hf, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if already has katalog in nav
    if 'href="katalog"' in content:
        print(f"{hf} already has katalog link")
        continue

    # Navbar replacement
    nav_old_pattern = re.compile(r'(<a[^>]*href=["\']services["\'][^>]*>Layanan</a>)')
    if nav_old_pattern.search(content):
        content = nav_old_pattern.sub(r'\1<a class="nav-link w-nav-link" href="katalog">Katalog</a>', content)
        print(f"Updated Navbar in {hf}")
    else:
        print(f"WARNING: Navbar pattern not found in {hf}")

    # Footer replacement: insert after Layanan in footer
    # Pattern: <li class="footer-menu-list-item">\s*<a[^>]*href=["\']services["\'][^>]*>Layanan</a>\s*</li>
    footer_old_pattern = re.compile(r'(<li class="footer-menu-list-item">\s*<a[^>]*href=["\']services["\'][^>]*>Layanan</a>\s*</li>)', re.MULTILINE)
    katalog_footer_item = '\n<li class="footer-menu-list-item">\n<a class="footer-menu-text-link" href="katalog">Katalog Digital</a>\n</li>'
    
    if footer_old_pattern.search(content):
        content = footer_old_pattern.sub(r'\1' + katalog_footer_item, content)
        print(f"Updated Footer in {hf}")
    else:
        print(f"WARNING: Footer pattern not found in {hf}")

    with open(hf, 'w', encoding='utf-8') as f:
        f.write(content)

print("\nFinished updating all 11 HTML files!")
