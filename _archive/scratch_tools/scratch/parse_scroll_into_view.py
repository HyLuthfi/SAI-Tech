import re

txt = open('d:/Area_Antigravity/SAI Tech/SAI Tech/assets/ritovex/webflow.schunk.1f51a299c4a843e1.js', 'r', encoding='utf-8', errors='ignore').read()
index_page_id = '6877e02f5387b6bdd6d338ed'

print("SCROLL_INTO_VIEW actions in index.html:")
for m in re.finditer(r'\{id:"(e-\d+)",name:"([^"]*)",animationType:"([^"]*)",eventTypeId:"SCROLL_INTO_VIEW",action:\{id:"[^"]*",actionTypeId:"([^"]*)",instant:(![01]),config:(\{.*?\})\},mediaQueries:\[([^\]]*)\],target:\{id:"([^"]+)"', txt):
    print(f"Event: {m.group(1)}, ActionType: {m.group(4)}, Target: {m.group(8)}, Config: {m.group(6)[:60]}")
