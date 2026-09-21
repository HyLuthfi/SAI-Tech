import re

txt = open('d:/Area_Antigravity/SAI Tech/SAI Tech/assets/ritovex/webflow.schunk.1f51a299c4a843e1.js', 'r', encoding='utf-8', errors='ignore').read()

for m in re.finditer(r'SLIDE_EFFECT', txt):
    idx = m.start()
    print("Found SLIDE_EFFECT handler:")
    print(txt[max(0, idx-50): min(len(txt), idx+300)])
    break
