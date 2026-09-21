import re, json

def find_ix_data(js_path):
    txt = open(js_path, 'r', encoding='utf-8', errors='ignore').read()
    # Webflow IX2 stores its data in a JSON-like object or ixData
    matches = re.findall(r'"site":\s*\{.*?"events":', txt)
    print(f"File {js_path}: matches found = {len(matches)}")
    # Look for action definitions or interaction names
    interactions = re.findall(r'"name":"([^"]+)"', txt)
    print(f"  Interaction names in {js_path}: {len(interactions)}")
    print("  Sample names:", interactions[:15])

find_ix_data('d:/Area_Antigravity/SAI Tech/SAI Tech/assets/ritovex/webflow.104d0b61.8689d13c72490845.js')
find_ix_data('d:/Area_Antigravity/SAI Tech/SAI Tech/assets/ritovex/webflow.25f2ca81.7fe17f96845fbe0e.js')
