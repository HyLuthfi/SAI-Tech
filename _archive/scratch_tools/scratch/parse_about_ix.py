import re, json

txt = open('d:/Area_Antigravity/SAI Tech/SAI Tech/assets/ritovex/webflow.schunk.1f51a299c4a843e1.js', 'r', encoding='utf-8', errors='ignore').read()
page_id = '6877e02f5387b6bdd6d338f2'

# Find all events mentioning this page ID
matches = [m.start() for m in re.finditer(re.escape(page_id), txt)]
print(f"Total occurrences: {len(matches)}")

for i, pos in enumerate(matches[:15]):
    sub = txt[max(0, pos-150): min(len(txt), pos+350)]
    print(f"\n--- Event {i+1} ---")
    print(sub)
