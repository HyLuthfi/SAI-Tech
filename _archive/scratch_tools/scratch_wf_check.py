import glob, re

for f in ['index.html', 'about.html', 'services.html', 'portfolio.html', 'blog.html', 'pricing.html', 'contact.html']:
    with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
        c = fp.read()
    site = re.findall(r'data-wf-site="([^"]+)"', c)
    page = re.findall(r'data-wf-page="([^"]+)"', c)
    scripts = re.findall(r'src="([^"]+)"', c)
    js_scripts = [s for s in scripts if s.endswith('.js') or '.js?' in s]
    print(f, 'site:', site, 'page:', page)
    print('  scripts:', js_scripts)
