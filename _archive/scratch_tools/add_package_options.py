import re
import urllib.parse

products_data = [
    {
        "id": "netflix",
        "category": "streaming",
        "name": "Netflix Premium 4K",
        "search_terms": "netflix premium 4k uhd film movie streaming",
        "img": "assets/katalog/netflix.png",
        "desc": "Streaming film & series kualitas 4K UHD + HDR tanpa jeda iklan dengan audio spasial.",
        "packages": [
            {"label": "1 Bln Sharing", "duration": "1 Bulan (Sharing 1 User)", "price": "Rp 28.000", "active": True},
            {"label": "1 Bln Private", "duration": "1 Bulan (Private 4 User)", "price": "Rp 120.000", "active": False},
            {"label": "3 Bln Sharing", "duration": "3 Bulan (Sharing 1 User)", "price": "Rp 78.000", "active": False}
        ]
    },
    {
        "id": "canva",
        "category": "creative",
        "name": "Canva Pro Premium",
        "search_terms": "canva pro premium desain grafis template magic studio ai",
        "img": "assets/katalog/canva.png",
        "desc": "Akses 100+ juta template premium, Magic Studio AI, Brand Kit, dan background remover 1-klik.",
        "packages": [
            {"label": "1 Bulan", "duration": "1 Bulan Private Email", "price": "Rp 15.000", "active": True},
            {"label": "1 Tahun", "duration": "1 Tahun Private Email", "price": "Rp 45.000", "active": False},
            {"label": "Lifetime", "duration": "Lifetime Edu Pro", "price": "Rp 75.000", "active": False}
        ]
    },
    {
        "id": "youtube",
        "category": "streaming",
        "name": "YouTube Premium",
        "search_terms": "youtube premium yt music bebas iklan background play",
        "img": "assets/katalog/youtube.png",
        "desc": "Bebas iklan, download offline, putar di latar belakang, plus akses YouTube Music Premium.",
        "packages": [
            {"label": "1 Bulan", "duration": "1 Bulan Family Plan", "price": "Rp 15.000", "active": True},
            {"label": "3 Bulan", "duration": "3 Bulan Family Plan", "price": "Rp 38.000", "active": False},
            {"label": "6 Bulan", "duration": "6 Bulan Family Plan", "price": "Rp 70.000", "active": False}
        ]
    },
    {
        "id": "chatgpt",
        "category": "ai",
        "name": "ChatGPT Plus (GPT-4o)",
        "search_terms": "chatgpt plus gpt-4o openai ai assistant dalle 3",
        "img": "assets/katalog/chatgpt.png",
        "desc": "Akses model GPT-4o pintar, DALL-E 3, analisis data dokumen mendalam, dan browsing internet real-time.",
        "packages": [
            {"label": "1 Bln Sharing", "duration": "1 Bulan Sharing", "price": "Rp 65.000", "active": True},
            {"label": "1 Bln Private", "duration": "1 Bulan Private Akun", "price": "Rp 330.000", "active": False}
        ]
    },
    {
        "id": "spotify",
        "category": "streaming",
        "name": "Spotify Premium",
        "search_terms": "spotify premium music streaming podcast lagu hq",
        "img": "assets/katalog/spotify.png",
        "desc": "Bebas jeda iklan, skip lagu tanpa batas, kualitas audio sangat tinggi, dan mode offline.",
        "packages": [
            {"label": "1 Bulan", "duration": "1 Bulan Individual/Family", "price": "Rp 18.000", "active": True},
            {"label": "3 Bulan", "duration": "3 Bulan Individual/Family", "price": "Rp 45.000", "active": False},
            {"label": "6 Bulan", "duration": "6 Bulan Individual/Family", "price": "Rp 85.000", "active": False}
        ]
    },
    {
        "id": "capcut",
        "category": "creative",
        "name": "CapCut Pro",
        "search_terms": "capcut pro video editor template efek transisi tiktok",
        "img": "assets/katalog/capcut.png",
        "desc": "Buka semua fitur dan efek pro, transisi viral, auto-caption otomatis AI, dan export tanpa watermark.",
        "packages": [
            {"label": "1 Bln Sharing", "duration": "1 Bulan Sharing", "price": "Rp 25.000", "active": True},
            {"label": "1 Bln Private", "duration": "1 Bulan Private 1 Device", "price": "Rp 75.000", "active": False},
            {"label": "1 Thn Private", "duration": "1 Tahun Private 1 Device", "price": "Rp 280.000", "active": False}
        ]
    },
    {
        "id": "microsoft365",
        "category": "ai",
        "name": "Microsoft 365 + 1TB",
        "search_terms": "microsoft 365 office word excel powerpoint onedrive cloud",
        "img": "assets/katalog/microsoft365.png",
        "desc": "Word, Excel, PowerPoint resmi + 1TB penyimpanan cloud OneDrive aman untuk 5 perangkat.",
        "packages": [
            {"label": "1 Tahun", "duration": "1 Tahun Family Invite", "price": "Rp 45.000", "active": True},
            {"label": "Lifetime", "duration": "Lifetime Pro Plus Akun", "price": "Rp 95.000", "active": False}
        ]
    },
    {
        "id": "disney",
        "category": "streaming",
        "name": "Disney+ Hotstar",
        "search_terms": "disney hotstar marvel star wars pixar film streaming",
        "img": "assets/katalog/disney.png",
        "desc": "Streaming film & serial blockbuster Disney, Marvel, Pixar, Star Wars, dan National Geographic.",
        "packages": [
            {"label": "1 Bulan", "duration": "1 Bulan Sharing", "price": "Rp 35.000", "active": True},
            {"label": "3 Bulan", "duration": "3 Bulan Sharing", "price": "Rp 95.000", "active": False}
        ]
    },
    {
        "id": "claude",
        "category": "ai",
        "name": "Claude Pro (Anthropic)",
        "search_terms": "claude pro sonnet 3.5 anthropic ai coding dev",
        "img": "assets/katalog/claude.png",
        "desc": "Model Claude 3.5 Sonnet terbaik untuk coding tingkat lanjut, riset panjang, dan analisis dokumen.",
        "packages": [
            {"label": "1 Bln Sharing", "duration": "1 Bulan Sharing", "price": "Rp 70.000", "active": True},
            {"label": "1 Bln Private", "duration": "1 Bulan Private", "price": "Rp 340.000", "active": False}
        ]
    },
    {
        "id": "turnitin",
        "category": "tools",
        "name": "Turnitin No-Repository",
        "search_terms": "turnitin no-repo plagiarisme cek skripsi jurnal mahasiswa",
        "img": "assets/katalog/turnitin.png",
        "desc": "Cek plagiarisme akurat tanpa tersimpan di database repositori (*no-repo*), 100% aman.",
        "packages": [
            {"label": "1 File", "duration": "1 File Pengecekan", "price": "Rp 10.000", "active": True},
            {"label": "5 File", "duration": "Paket 5 File Pengecekan", "price": "Rp 40.000", "active": False},
            {"label": "Akun 1 Bln", "duration": "Akun Student 1 Bulan", "price": "Rp 60.000", "active": False}
        ]
    },
    {
        "id": "vpn",
        "category": "tools",
        "name": "ExpressVPN / NordVPN",
        "search_terms": "vpn expressvpn nordvpn privasi sekuriti ip luar negeri",
        "img": "assets/katalog/vpn.png",
        "desc": "Koneksi terenkripsi tingkat tinggi, akses ribuan server global ultra cepat, dan privasi penuh.",
        "packages": [
            {"label": "1 Bulan", "duration": "1 Bulan Sharing", "price": "Rp 30.000", "active": True},
            {"label": "3 Bulan", "duration": "3 Bulan Sharing", "price": "Rp 75.000", "active": False},
            {"label": "1 Tahun", "duration": "1 Tahun Sharing", "price": "Rp 210.000", "active": False}
        ]
    },
    {
        "id": "googleone",
        "category": "ai",
        "name": "Google One Storage",
        "search_terms": "google one storage gdrive drive gmail photos cloud backup",
        "img": "assets/katalog/googleone.png",
        "desc": "Penyimpanan cloud resmi untuk Google Drive, Gmail, dan Google Photos original tanpa kompresi.",
        "packages": [
            {"label": "100 GB", "duration": "100 GB Storage (1 Tahun)", "price": "Rp 45.000", "active": True},
            {"label": "200 GB", "duration": "200 GB Storage (1 Tahun)", "price": "Rp 75.000", "active": False},
            {"label": "2 TB", "duration": "2 TB Storage (1 Tahun)", "price": "Rp 195.000", "active": False}
        ]
    }
]

def make_card_html(p):
    chips_html = []
    active_price = p["packages"][0]["price"]
    for pkg in p["packages"]:
        act_class = " active" if pkg["active"] else ""
        chips_html.append(f'<span class="dur-chip{act_class}" data-duration="{pkg["duration"]}" data-price="{pkg["price"]}">{pkg["label"]}</span>')
    chips_joined = "\n                ".join(chips_html)

    return f"""          <!-- {p['name']} -->
          <div class="product-box" data-category="{p['category']}" data-name="{p['search_terms']}">
            <div class="product-img-wrap">
              <img src="{p['img']}" alt="{p['name']}" class="product-img" loading="lazy" />
            </div>
            <div class="product-body">
              <h3 class="product-title">{p['name']}</h3>
              <p class="product-desc">{p['desc']}</p>
              <div class="dur-selector-wrap">
                <span class="dur-label">Pilihan Paket:</span>
                <div class="dur-chips-group" data-target="{p['id']}">
                  {chips_joined}
                </div>
              </div>
            </div>
            <div class="product-action-row">
              <div class="product-price-wrap">
                <span class="product-price-label">Harga Paket</span>
                <span class="product-price" id="price-{p['id']}">{active_price}</span>
              </div>
              <a href="#" class="btn-pesan" onclick="orderProduct(event, '{p['name']}', '{p['id']}')">Pesan</a>
            </div>
          </div>"""

new_css = """    /* Product Cards Grid: Clean Minimalist with 1:1 Aspect Ratio */
    .catalog-products-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 28px;
      margin-bottom: 70px;
    }

    .product-box {
      background: #ffffff;
      border: 1.5px solid rgba(0, 0, 77, 0.08);
      border-radius: 18px;
      padding: 16px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-shadow: 0 4px 18px rgba(0, 0, 77, 0.04);
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .product-box:hover {
      transform: translateY(-5px);
      box-shadow: 0 16px 36px rgba(0, 0, 77, 0.09);
      border-color: rgba(224, 189, 106, 0.55);
    }

    .product-img-wrap {
      width: 100%;
      aspect-ratio: 1 / 1;
      border-radius: 12px;
      overflow: hidden;
      background: #f6f6f9;
      margin-bottom: 16px;
    }

    .product-img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
      transition: transform 0.4s ease;
    }

    .product-box:hover .product-img {
      transform: scale(1.03);
    }

    .product-body {
      display: flex;
      flex-direction: column;
      flex-grow: 1;
    }

    .product-title {
      font-family: Satoshi, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      font-size: 18px;
      font-weight: 800;
      color: #00004d;
      margin: 0 0 6px 0;
      line-height: 1.3;
      letter-spacing: -0.3px;
    }

    .product-desc {
      font-size: 13.5px;
      color: #5d5c6b;
      line-height: 1.5;
      margin: 0 0 12px 0;
    }

    /* Pilihan Paket Chips */
    .dur-selector-wrap {
      margin-top: auto;
      margin-bottom: 16px;
    }

    .dur-label {
      font-size: 11px;
      font-weight: 700;
      color: #71707d;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 6px;
      display: block;
    }

    .dur-chips-group {
      display: flex;
      gap: 6px;
      flex-wrap: wrap;
    }

    .dur-chip {
      padding: 5px 11px;
      border-radius: 6px;
      background: #f6f6f9;
      border: 1px solid #e2e2ec;
      font-size: 12px;
      font-weight: 600;
      color: #00004d;
      cursor: pointer;
      transition: all 0.2s ease;
      user-select: none;
    }

    .dur-chip:hover {
      border-color: #00004d;
      background: #ededf5;
    }

    .dur-chip.active {
      background: #00004d;
      border-color: #00004d;
      color: #ffffff;
      box-shadow: 0 2px 8px rgba(0, 0, 77, 0.15);
    }

    .product-action-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding-top: 14px;
      border-top: 1px solid rgba(0, 0, 77, 0.06);
      gap: 12px;
    }

    .product-price-wrap {
      display: flex;
      flex-direction: column;
    }

    .product-price-label {
      font-size: 11px;
      color: #8c8b98;
      font-weight: 500;
      margin-bottom: 1px;
    }

    .product-price {
      font-family: Satoshi, sans-serif;
      font-size: 19px;
      font-weight: 800;
      color: #00004d;
      letter-spacing: -0.4px;
    }

    .btn-pesan {
      background-color: #00004d;
      color: #ffffff;
      border-radius: 8px;
      padding: 10px 24px;
      font-size: 14px;
      font-weight: 700;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      transition: all 0.25s ease;
    }

    .btn-pesan:hover {
      background-color: #22c55e;
      color: #ffffff;
      box-shadow: 0 4px 14px rgba(34, 197, 94, 0.35);
      transform: translateY(-1px);
    }"""

cards_html = "\n\n".join([make_card_html(p) for p in products_data])

with open("katalog.html", "r", encoding="utf-8") as f:
    content = f.read()

# Replace CSS block
old_css_pattern = re.compile(r'/\* Product Cards Grid: Clean Minimalist with 1:1 Aspect Ratio \*/.*?/\* Steps Section \*/', re.DOTALL)
replacement_css = new_css + "\n\n    /* Steps Section */"
content = old_css_pattern.sub(replacement_css, content)

# Replace Grid Content
grid_pattern = re.compile(r'(<div class="catalog-products-grid" id="productsGrid">).*?(</div>\s*<!-- Empty Search Notice -->)', re.DOTALL)
new_grid = f"\\1\n\n{cards_html}\n\n        \\2"
content = grid_pattern.sub(new_grid, content)

# Update orderProduct JS function to format cleanly
js_order_pattern = re.compile(r'function orderProduct\(e, productName, targetKey\) \{.*?window\.open\(waUrl, \'_blank\', \'noopener,noreferrer\'\);\s*\}', re.DOTALL)
new_js_order = """function orderProduct(e, productName, targetKey) {
      if (e) e.preventDefault();
      var activeChip = document.querySelector('.dur-chips-group[data-target="' + targetKey + '"] .dur-chip.active');
      var duration = activeChip ? activeChip.getAttribute('data-duration') : '1 Paket';
      var priceElem = document.getElementById('price-' + targetKey);
      var price = priceElem ? priceElem.textContent : '';

      var message = 'Halo Admin SAI Tech, saya ingin order produk digital:\\n\\n' +
                    '• Produk: *' + productName + '*\\n' +
                    '• Pilihan Paket: *' + duration + '*\\n' +
                    '• Harga: *' + price + '*\\n\\n' +
                    'Apakah stok akun masih tersedia dan bagaimana metode pembayarannya? Terima kasih!';

      var waUrl = 'https://wa.me/6282163732969?text=' + encodeURIComponent(message);
      window.open(waUrl, '_blank', 'noopener,noreferrer');
    }"""
content = js_order_pattern.sub(new_js_order, content)

with open("katalog.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Package options added back to 1:1 cards successfully!")
