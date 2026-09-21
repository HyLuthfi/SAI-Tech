import re

js_content = open('d:/Area_Antigravity/SAI Tech/SAI Tech/assets/ritovex/webflow.104d0b61.8689d13c72490845.js', 'r', encoding='utf-8').read()

target_id = '5d27e77a-fd0c-68cd-5e8d-32e7d50a78f5'
print(f"Target ID in index JS: {target_id in js_content}")

if target_id in js_content:
    idx = js_content.find(target_id)
    snippet = js_content[max(0, idx - 200): min(len(js_content), idx + 500)]
    print("\nSnippet around target ID:")
    print(snippet)
else:
    # Let's find any GUID in js_content
    guids = re.findall(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', js_content)
    print(f"Total GUIDs in index JS: {len(guids)}")
    print("Sample GUIDs:", guids[:10])
