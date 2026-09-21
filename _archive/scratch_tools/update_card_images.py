import re

with open('katalog.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Replace all assets/katalog/*.png image sources with assets/ritovex/Image_Placeholder_Square.png
c = re.sub(r'src="assets/katalog/[a-zA-Z0-9_]+\.png"', 'src="assets/ritovex/Image_Placeholder_Square.png"', c)

with open('katalog.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Updated images successfully!")
