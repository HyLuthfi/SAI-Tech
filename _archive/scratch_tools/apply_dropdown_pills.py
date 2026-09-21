import re

products_data = [
    {
        "id": "netflix",
        "category": "streaming",
        "name": "Netflix Premium 4K",
        "search_terms": "netflix premium 4k uhd film movie streaming",
        "img": "assets/ritovex/Image_Placeholder_Square.png",
        "desc": "Streaming film & series kualitas 4K UHD + HDR tanpa jeda iklan dengan audio spasial.",
        "options": [
            {"label": "1 Bln Sharing — Rp 28.000", "duration": "1 Bulan (Sharing 1 User)", "price": "Rp 28.000"},
            {"label": "1 Bln Private — Rp 120.000", "duration": "1 Bulan (Private 4 User)", "price": "Rp 120.000"},
            {"label": "3 Bln Sharing — Rp 78.000", "duration": "3 Bulan (Sharing 1 User)", "price": "Rp 78.000"}
        ]
    },
    {
        "id": "canva",
        "category": "creative",
        "name": "Canva Pro Premium",
        "search_terms": "canva pro premium desain grafis template magic studio ai",
        "img": "assets/ritovex/Image_Placeholder_Square.png",
        "desc": "Akses 100+ juta template premium, Magic Studio AI, Brand Kit, dan background remover 1-klik.",
        "options": [
            {"label": "1 Bulan — Rp 15.000", "duration": "1 Bulan Private Email", "price": "Rp 15.000"},
            {"label": "1 Tahun — Rp 45.000", "duration": "1 Tahun Private Email", "price": "Rp 45.000"},
            {"label": "Lifetime — Rp 75.000", "duration": "Lifetime Edu Pro", "price": "Rp 75.000"}
        ]
    },
    {
        "id": "youtube",
        "category": "streaming",
        "name": "YouTube Premium",
        "search_terms": "youtube premium yt music bebas iklan background play",
        "img": "assets/ritovex/Image_Placeholder_Square.png",
        "desc": "Bebas iklan, download offline, putar di latar belakang, plus akses YouTube Music Premium.",
        "options": [
            {"label": "1 Bulan — Rp 15.000", "duration": "1 Bulan Family Plan", "price": "Rp 15.000"},
            {"label": "3 Bulan — Rp 38.000", "duration": "3 Bulan Family Plan", "price": "Rp 38.000"},
            {"label": "6 Bulan — Rp 70.000", "duration": "6 Bulan Family Plan", "price": "Rp 70.000"}
        ]
    },
    {
        "id": "chatgpt",
        "category": "ai",
        "name": "ChatGPT Plus (GPT-4o)",
        "search_terms": "chatgpt plus gpt-4o openai ai assistant dalle 3",
        "img": "assets/ritovex/Image_Placeholder_Square.png",
        "desc": "Akses model GPT-4o pintar, DALL-E 3, analisis data dokumen mendalam, dan browsing internet real-time.",
        "options": [
            {"label": "1 Bln Sharing — Rp 65.000", "duration": "1 Bulan Sharing", "price": "Rp 65.000"},
            {"label": "1 Bln Private — Rp 330.000", "duration": "1 Bulan Private Akun", "price": "Rp 330.000"}
        ]
    },
    {
        "id": "spotify",
        "category": "streaming",
        "name": "Spotify Premium",
        "search_terms": "spotify premium music streaming podcast lagu hq",
        "img": "assets/ritovex/Image_Placeholder_Square.png",
        "desc": "Bebas jeda iklan, skip lagu tanpa batas, kualitas audio sangat tinggi, dan mode offline.",
        "options": [
            {"label": "1 Bulan — Rp 18.000", "duration": "1 Bulan Individual/Family", "price": "Rp 18.000"},
            {"label": "3 Bulan — Rp 45.000", "duration": "3 Bulan Individual/Family", "price": "Rp 45.000"},
            {"label": "6 Bulan — Rp 85.000", "duration": "6 Bulan Individual/Family", "price": "Rp 85.000"}
        ]
    },
    {
        "id": "capcut",
        "category": "creative",
        "name": "CapCut Pro",
        "search_terms": "capcut pro video editor template efek transisi tiktok",
        "img": "assets/ritovex/Image_Placeholder_Square.png",
        "desc": "Buka semua fitur dan efek pro, transisi viral, auto-caption otomatis AI, dan export tanpa watermark.",
        "options": [
            {"label": "1 Bln Sharing — Rp 25.000", "duration": "1 Bulan Sharing", "price": "Rp 25.000"},
            {"label": "1 Bln Private — Rp 75.000", "duration": "1 Bulan Private 1 Device", "price": "Rp 75.000"},
            {"label": "1 Thn Private — Rp 280.000", "duration": "1 Tahun Private 1 Device", "price": "Rp 280.000"}
        ]
    },
    {
        "id": "microsoft365",
        "category": "ai",
        "name": "Microsoft 365 + 1TB",
        "search_terms": "microsoft 365 office word excel powerpoint onedrive cloud",
        "img": "assets/ritovex/Image_Placeholder_Square.png",
        "desc": "Word, Excel, PowerPoint resmi + 1TB penyimpanan cloud OneDrive aman untuk 5 perangkat.",
        "options": [
            {"label": "1 Tahun — Rp 45.000", "duration": "1 Tahun Family Invite", "price": "Rp 45.000"},
            {"label": "Lifetime — Rp 95.000", "duration": "Lifetime Pro Plus Akun", "price": "Rp 95.000"}
        ]
    },
    {
        "id": "disney",
        "category": "streaming",
        "name": "Disney+ Hotstar",
        "search_terms": "disney hotstar marvel star wars pixar film streaming",
        "img": "assets/ritovex/Image_Placeholder_Square.png",
        "desc": "Streaming film & serial blockbuster Disney, Marvel, Pixar, Star Wars, dan National Geographic.",
        "options": [
            {"label": "1 Bulan — Rp 35.000", "duration": "1 Bulan Sharing", "price": "Rp 35.000"},
            {"label": "3 Bulan — Rp 95.000", "duration": "3 Bulan Sharing", "price": "Rp 95.000"}
        ]
    },
    {
        "id": "claude",
        "category": "ai",
        "name": "Claude Pro (Anthropic)",
        "search_terms": "claude pro sonnet 3.5 anthropic ai coding dev",
        "img": "assets/ritovex/Image_Placeholder_Square.png",
        "desc": "Model Claude 3.5 Sonnet terbaik untuk coding tingkat lanjut, riset panjang, dan analisis dokumen.",
        "options": [
            {"label": "1 Bln Sharing — Rp 70.000", "duration": "1 Bulan Sharing", "price": "Rp 70.000"},
            {"label": "1 Bln Private — Rp 340.000", "duration": "1 Bulan Private", "price": "Rp 340.000"}
        ]
    },
    {
        "id": "turnitin",
        "category": "tools",
        "name": "Turnitin No-Repository",
        "search_terms": "turnitin no-repo plagiarisme cek skripsi jurnal mahasiswa",
        "img": "assets/ritovex/Image_Placeholder_Square.png",
        "desc": "Cek plagiarisme akurat tanpa tersimpan di database repositori (*no-repo*), 100% aman.",
        "options": [
            {"label": "1 File — Rp 10.000", "duration": "1 File Pengecekan", "price": "Rp 10.000"},
            {"label": "Paket 5 File — Rp 40.000", "duration": "Paket 5 File Pengecekan", "price": "Rp 40.000"},
            {"label": "Akun 1 Bln — Rp 60.000", "duration": "Akun Student 1 Bulan", "price": "Rp 60.000"}
        ]
    },
    {
        "id": "vpn",
        "category": "tools",
        "name": "ExpressVPN / NordVPN",
        "search_terms": "vpn expressvpn nordvpn privasi sekuriti ip luar negeri",
        "img": "assets/ritovex/Image_Placeholder_Square.png",
        "desc": "Koneksi terenkripsi tingkat tinggi, akses ribuan server global ultra cepat, dan privasi penuh.",
        "options": [
            {"label": "1 Bulan — Rp 30.000", "duration": "1 Bulan Sharing", "price": "Rp 30.000"},
            {"label": "3 Bulan — Rp 75.000", "duration": "3 Bulan Sharing", "price": "Rp 75.000"},
            {"label": "1 Tahun — Rp 210.000", "duration": "1 Tahun Sharing", "price": "Rp 210.000"}
        ]
    },
    {
        "id": "googleone",
        "category": "ai",
        "name": "Google One Storage",
        "search_terms": "google one storage gdrive drive gmail photos cloud backup",
        "img": "assets/ritovex/Image_Placeholder_Square.png",
        "desc": "Penyimpanan cloud resmi untuk Google Drive, Gmail, dan Google Photos original tanpa kompresi.",
        "options": [
            {"label": "100 GB (1 Thn) — Rp 45.000", "duration": "100 GB Storage (1 Tahun)", "price": "Rp 45.000"},
            {"label": "200 GB (1 Thn) — Rp 75.000", "duration": "200 GB Storage (1 Tahun)", "price": "Rp 75.000"},
            {"label": "2 TB (1 Thn) — Rp 195.000", "duration": "2 TB Storage (1 Tahun)", "price": "Rp 195.000"}
        ]
    }
]

def make_card_html(p):
    opts_html = []
    initial_price = p["options"][0]["price"]
    for opt in p["options"]:
        opts_html.append(f'<option value="{opt["price"]}" data-duration="{opt["duration"]}">{opt["label"]}</option>')
    opts_joined = "\n                    ".join(opts_html)

    return f"""          <!-- {p['name']} -->
          <div class="product-box" data-category="{p['category']}" data-name="{p['search_terms']}">
            <div class="product-img-wrap">
              <img src="{p['img']}" alt="{p['name']}" class="product-img" loading="lazy" />
            </div>
            <div class="product-body">
              <h3 class="product-title">{p['name']}</h3>
              <p class="product-desc">{p['desc']}</p>
              <div class="dur-dropdown-wrap">
                <span class="dur-label">Pilihan Paket:</span>
                <div class="custom-select-wrapper">
                  <select class="dur-select" data-target="{p['id']}" onchange="onPackageSelectChange(this)">
                    {opts_joined}
                  </select>
                  <span class="select-chevron">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#00004d" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>
                  </span>
                </div>
              </div>
            </div>
            <div class="product-action-row">
              <div class="product-price-wrap">
                <span class="product-price-label">Harga Paket</span>
                <span class="product-price" id="price-{p['id']}">{initial_price}</span>
              </div>
              <a href="#" class="btn-pesan" onclick="orderProduct(event, '{p['name']}', '{p['id']}')">Beli</a>
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
      object-position: center;
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
      margin: 0 0 14px 0;
    }

    /* Pilihan Paket Dropdown Pill (100% Uniform & Neat) */
    .dur-dropdown-wrap {
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

    .custom-select-wrapper {
      position: relative;
      width: 100%;
    }

    .dur-select {
      width: 100%;
      padding: 10px 36px 10px 14px;
      border-radius: 10px;
      background-color: #f6f6f9;
      border: 1.5px solid rgba(0, 0, 77, 0.1);
      color: #00004d;
      font-family: Satoshi, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      font-size: 13px;
      font-weight: 600;
      outline: none;
      cursor: pointer;
      appearance: none;
      -webkit-appearance: none;
      -moz-appearance: none;
      transition: all 0.2s ease;
      box-sizing: border-box;
    }

    .dur-select:hover {
      background-color: #ededf5;
      border-color: #00004d;
    }

    .dur-select:focus {
      background-color: #ffffff;
      border-color: #00004d;
      box-shadow: 0 0 0 3px rgba(0, 0, 77, 0.08);
    }

    .select-chevron {
      position: absolute;
      right: 14px;
      top: 50%;
      transform: translateY(-50%);
      pointer-events: none;
      display: flex;
      align-items: center;
      justify-content: center;
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

new_script = """  <!-- Interactive Catalog Script -->
  <script>
    // 1. Dropdown Package Change Handler
    function onPackageSelectChange(selectElem) {
      var targetKey = selectElem.getAttribute('data-target');
      var newPrice = selectElem.value;
      var priceElem = document.getElementById('price-' + targetKey);
      if (priceElem && newPrice) {
        priceElem.textContent = newPrice;
      }
    }

    // 2. Category Filter & Search Handlers
    (function() {
      var catButtons = document.querySelectorAll('.cat-pill-btn');
      var searchInput = document.getElementById('catalogSearch');

      catButtons.forEach(function(btn) {
        btn.addEventListener('click', function() {
          catButtons.forEach(function(b) { b.classList.remove('active'); });
          this.classList.add('active');
          filterProducts();
        });
      });

      if (searchInput) {
        searchInput.addEventListener('input', filterProducts);
      }

      function filterProducts() {
        var activeBtn = document.querySelector('.cat-pill-btn.active');
        var activeCat = activeBtn ? activeBtn.getAttribute('data-category') : 'all';
        var query = (searchInput ? searchInput.value : '').toLowerCase().trim();
        var cards = document.querySelectorAll('.product-box');
        var visibleCount = 0;

        cards.forEach(function(card) {
          var cardCat = card.getAttribute('data-category');
          var searchKeywords = (card.getAttribute('data-name') || '').toLowerCase();

          var matchCat = (activeCat === 'all' || activeCat === cardCat);
          var matchQuery = (!query || searchKeywords.indexOf(query) !== -1);

          if (matchCat && matchQuery) {
            card.style.display = 'flex';
            visibleCount++;
          } else {
            card.style.display = 'none';
          }
        });

        var emptyNotice = document.getElementById('emptySearchNotice');
        if (emptyNotice) {
          emptyNotice.style.display = (visibleCount === 0) ? 'block' : 'none';
        }
      }
    })();

    // 3. Order via WhatsApp Deep-Link Generator
    function orderProduct(e, productName, targetKey) {
      if (e) e.preventDefault();
      var selectElem = document.querySelector('.dur-select[data-target="' + targetKey + '"]');
      var duration = '1 Paket';
      var price = '';

      if (selectElem) {
        var selectedOpt = selectElem.options[selectElem.selectedIndex];
        duration = selectedOpt.getAttribute('data-duration') || selectedOpt.text;
        price = selectElem.value;
      } else {
        var priceElem = document.getElementById('price-' + targetKey);
        price = priceElem ? priceElem.textContent : '';
      }

      var lines = [
        'Halo Admin SAI Tech, saya ingin beli produk digital:',
        '',
        '- Produk: ' + productName,
        '- Pilihan Paket: ' + duration,
        '- Harga: ' + price,
        '',
        'Apakah stok akun masih tersedia dan bagaimana metode pembayarannya? Terima kasih!'
      ];
      var message = lines.join('\\n');
      var waUrl = 'https://wa.me/6282163732969?text=' + encodeURIComponent(message);
      window.open(waUrl, '_blank', 'noopener,noreferrer');
    }

    // 4. FAQ Accordion Toggle
    function toggleFaq(el) {
      var item = el.closest('.faq-card-item');
      if (!item) return;
      var wasActive = item.classList.contains('active');
      document.querySelectorAll('.faq-card-item').forEach(function(i) { i.classList.remove('active'); });
      if (!wasActive) {
        item.classList.add('active');
      }
    }
  </script>"""

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

# Replace Script
script_pattern = re.compile(r'<!-- Interactive Catalog Script -->[\s\S]*?</script>', re.DOTALL)
content = script_pattern.sub(new_script, content)

with open("katalog.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Dropdown Pill layout applied successfully to all cards!")
