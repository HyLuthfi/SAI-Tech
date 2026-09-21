import os
import re

html_files = [
    'index.html', 'about.html', 'services.html', 'service-single.html',
    'portfolio.html', 'portfolio-single.html', 'pricing.html',
    'blog.html', 'blog-single.html', 'team.html', 'contact.html'
]

old_lottie = 'https://cdn.prod.website-files.com/6649cc3a1ea038d81fed488f/665c6513d8d80fdb4ba4cd55_Hamburger%20Black%20(1).json'
new_lottie = 'assets/ritovex/hamburger-black.json'

preconnect_pattern = re.compile(r'\s*<link crossorigin="anonymous" href="https://cdn\.prod\.website-files\.com" rel="preconnect"/>\n?', re.MULTILINE)

for hf in html_files:
    with open(hf, 'r', encoding='utf-8') as f:
        content = f.read()

    count_lottie = content.count(old_lottie)
    new_content = content.replace(old_lottie, new_lottie)
    new_content = preconnect_pattern.sub('', new_content)

    with open(hf, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"Updated {hf}: replaced {count_lottie} lottie URL(s)")

print("\nAll 11 HTML files successfully updated!")
