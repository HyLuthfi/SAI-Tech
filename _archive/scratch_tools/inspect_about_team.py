import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('about.html', 'r', encoding='utf-8') as f:
    about = f.read()

m = re.search(r'<section class="section team-members[^"]*">([\s\S]*?)</section>', about)
if m:
    print("=== TEAM SECTION IN about.html ===")
    print(m.group(0))
else:
    print("Could not find section team-members")
