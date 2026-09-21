import os

html_files = [
    'index.html', 'about.html', 'services.html', 'service-single.html',
    'portfolio.html', 'portfolio-single.html', 'pricing.html',
    'blog.html', 'blog-single.html', 'team.html', 'contact.html'
]

old_footer_snippet = '<a class="footer-menu-text-link" href="services">Layanan</a><a class="nav-link w-nav-link" href="katalog">Katalog</a>'
correct_footer_snippet = '<a class="footer-menu-text-link" href="services">Layanan</a>\n</li>\n<li class="footer-menu-list-item">\n<a class="footer-menu-text-link" href="katalog">Katalog Digital</a>'

for hf in html_files:
    with open(hf, 'r', encoding='utf-8') as f:
        content = f.read()

    if old_footer_snippet in content:
        content = content.replace(old_footer_snippet, correct_footer_snippet)
        with open(hf, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed footer in {hf}")
    else:
        print(f"Old snippet not found in {hf} (checking if already fixed)")

print("Footer styling fixed across all files!")
