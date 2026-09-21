txt = open('d:/Area_Antigravity/SAI Tech/SAI Tech/assets/ritovex/webflow.schunk.1f51a299c4a843e1.js', 'r', encoding='utf-8', errors='ignore').read()

idx = txt.find('slideInBottom')
print("slideInBottom definition:")
print(txt[max(0, idx-100): min(len(txt), idx+600)])
