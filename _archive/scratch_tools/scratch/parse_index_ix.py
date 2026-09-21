import re, json

txt = open('d:/Area_Antigravity/SAI Tech/SAI Tech/assets/ritovex/webflow.schunk.1f51a299c4a843e1.js', 'r', encoding='utf-8', errors='ignore').read()
index_page_id = '6877e02f5387b6bdd6d338ed'

matches = [m.start() for m in re.finditer(re.escape(index_page_id), txt)]
print(f"Index page occurrences: {len(matches)}")

event_types = set()
for pos in matches:
    sub = txt[max(0, pos-200): min(len(txt), pos+300)]
    m_ev = re.search(r'eventTypeId:"([^"]+)"', sub)
    m_act = re.search(r'actionTypeId:"([^"]+)"', sub)
    if m_ev or m_act:
        event_types.add((m_ev.group(1) if m_ev else None, m_act.group(1) if m_act else None))

print("\nEvent types and action types in index.html:")
for et, at in sorted(event_types, key=lambda x: str(x)):
    print(f"  Event: {et}, Action: {at}")
