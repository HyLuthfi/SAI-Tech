from bs4 import BeautifulSoup

soup = BeautifulSoup(open('d:/Area_Antigravity/SAI Tech/SAI Tech/index.html', 'r', encoding='utf-8').read(), 'html.parser')

print("--- Cards on index.html ---")
card_classes = [
    'services-single',
    'about-us-card',
    'pricing-single-card',
    'portfolio-card',
    'blog-single',
    'features-single',
    'why-chooses-us-typography-single',
    'testimonial-card'
]

for cls in card_classes:
    items = soup.find_all(class_=cls)
    if items:
        print(f"\nClass: {cls} (found {len(items)} items)")
        for i, it in enumerate(items[:3]):
            print(f"  Item {i+1}:")
            print(f"    tag: {it.name}")
            print(f"    classes: {it.get('class')}")
            print(f"    data-w-id: {it.get('data-w-id')}")
            print(f"    data-ix: {it.get('data-ix')}")
            print(f"    style: {it.get('style')}")
            # check parents up to 3 levels
            p = [parent.name + ('.' + '.'.join(parent.get('class', [])) if parent.get('class') else '') for parent in it.parents if parent.name != '[document]'][:3]
            print(f"    parents: {p}")
