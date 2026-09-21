import re

svg_search = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block;vertical-align:middle;"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>'

svg_search_large = '<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#9291a0" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>'

svg_box = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#00004d" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>'

svg_lock = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#0284c7" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>'

svg_scissors = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="6" cy="6" r="3"></circle><circle cx="6" cy="18" r="3"></circle><line x1="20" y1="4" x2="8.12" y2="15.88"></line><line x1="14.47" y1="14.48" x2="20" y2="20"></line><line x1="8.12" y1="8.12" x2="12" y2="12"></line></svg>'

svg_music = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#1ed760" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18V5l12-2v13"></path><circle cx="6" cy="18" r="3"></circle><circle cx="18" cy="16" r="3"></circle></svg>'

svg_sparkle = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#10a37f" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/></svg>'

with open('katalog.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Search icon
c = c.replace('<span class="search-icon-img">🔍</span>', f'<span class="search-icon-img">{svg_search}</span>')

# 2. Categories
c = c.replace('>✨ Semua Produk<', '>Semua Produk<')
c = c.replace('>🎬 Streaming &amp; Hiburan<', '>Streaming &amp; Hiburan<')
c = c.replace('>🎨 Desain &amp; Kreatif<', '>Desain &amp; Kreatif<')
c = c.replace('>🤖 AI &amp; Produktivitas<', '>AI &amp; Produktivitas<')
c = c.replace('>⚡ Tools &amp; VPN<', '>Tools &amp; VPN<')

# 3. Status Tags
c = c.replace('🔥 Terlaris', 'Terlaris')
c = c.replace('⭐ Populer', 'Populer')
c = c.replace('⚡ Instan', 'Instan')
c = c.replace('🤖 Flagship', 'Flagship')
c = c.replace('🎧 Audio HQ', 'Audio HQ')
c = c.replace('🔥 Viral Tool', 'Pilihan Editor')
c = c.replace('💼 Kantor &amp; Kampus', 'Produktivitas')
c = c.replace('🎬 Movie Hub', 'Resmi')
c = c.replace('⚡ Coding &amp; Dev', 'Developer Choice')
c = c.replace('🎓 Mahasiswa &amp; Dosen', 'Akademik')
c = c.replace('🛡️ Privasi &amp; Sekuriti', 'Privasi &amp; Sekuriti')
c = c.replace('💾 Cloud Backup', 'Cloud Storage')

# 4. Guarantee Tags
c = c.replace('🛡️ Garansi Full', 'Garansi Full')
c = c.replace('🛡️ Aman No-Repo', 'Aman No-Repo')

# 5. WhatsApp and Admin Buttons
c = c.replace('<span>💬 Pesan WA</span>', '<span>Pesan via WhatsApp</span>')
c = c.replace('<span>💬 Tanya Produk Khusus ke Admin</span>', '<span>Tanya Produk Khusus ke Admin</span>')

# 6. Brand Icons
c = c.replace('<div class="brand-icon-box tint-chatgpt">✦</div>', f'<div class="brand-icon-box tint-chatgpt">{svg_sparkle}</div>')
c = c.replace('<div class="brand-icon-box tint-spotify">♫</div>', f'<div class="brand-icon-box tint-spotify">{svg_music}</div>')
c = c.replace('<div class="brand-icon-box tint-capcut">✂</div>', f'<div class="brand-icon-box tint-capcut">{svg_scissors}</div>')
c = c.replace('<div class="brand-icon-box tint-vpn">🔒</div>', f'<div class="brand-icon-box tint-vpn">{svg_lock}</div>')

# 7. Empty state and modal box
c = c.replace('<div style="font-size: 36px; margin-bottom: 10px;">🔍</div>', f'<div style="margin-bottom: 12px;">{svg_search_large}</div>')
c = re.sub(r'<div style="width: 48px; height: 48px; border-radius: 12px; background: rgba\(224, 189, 106, 0.15\); border: 1px solid rgba\(224, 189, 106, 0.4\); display: flex; align-items: center; justify-content: center; font-size: 24px;">.*?</div>', f'<div style="width: 48px; height: 48px; border-radius: 12px; background: rgba(224, 189, 106, 0.15); border: 1px solid rgba(224, 189, 106, 0.4); display: flex; align-items: center; justify-content: center;">{svg_box}</div>', c)

with open('katalog.html', 'w', encoding='utf-8') as f:
    f.write(c)

print('Transformation successfully written to katalog.html')
