/**
 * SAI Tech | Universal Cart & Checkout Engine (Zero-Slop Standard)
 * Clean, tactile state management for index.html.
 */

(function () {
  'use strict';

  const STORAGE_KEY = 'sai_tech_cart_v1';
  const fmtRp = n => 'Rp ' + Number(n).toLocaleString('id-ID');
  const genId = () => 'SAI-' + Date.now().toString(36).toUpperCase().slice(-7);

  // SVG Icons to replace emojis
  const ICONS = {
    cartEmpty: `<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="8" cy="21" r="1"/><circle cx="19" cy="21" r="1"/><path d="M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12"/></svg>`,
    qris: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="3" height="3"/><rect x="18" y="18" width="3" height="3"/></svg>`,
    va: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75"><path d="M3 21h18M3 10h18M5 10v11M9 10v11M15 10v11M19 10v11M12 2 2 7h20L12 2z"/></svg>`,
    ewallet: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75"><rect x="5" y="2" width="14" height="20" rx="2"/><path d="M12 18h.01"/></svg>`
  };

  // Cart State
  let cart = [];
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) cart = JSON.parse(saved);
  } catch (e) {
    cart = [];
  }

  function saveCart() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(cart));
    } catch (e) {}
    renderCart();
  }

  // Ensure Drawer markup exists in the document
  function ensureDrawerMarkup() {
    if (document.getElementById('drawer')) return;

    const container = document.createElement('div');
    container.innerHTML = `
      <div class="veil" id="veil"></div>
      <aside class="drawer" id="drawer" aria-modal="true" aria-label="Checkout">
        <div class="drawer-head">
          <span class="drawer-head-title">Keranjang & Checkout</span>
          <button class="drawer-close" id="drawerClose" aria-label="Tutup">✕</button>
        </div>
        <div class="drawer-body" id="drawerBody">
          <div>
            <div class="drawer-sect-head">Daftar Pesanan</div>
            <div class="cart-list" id="cartList" style="display:none"></div>
            <div class="cart-empty" id="cartEmpty">
              <div class="cart-empty-icon">${ICONS.cartEmpty}</div>
              <div class="cart-empty-title">Keranjang Anda kosong</div>
              <div class="cart-empty-sub">Pilih produk langganan dari Digital Store untuk memulai order.</div>
            </div>
          </div>
          <div id="summaryWrap" style="display:none">
            <div class="drawer-sect-head">Ringkasan Biaya</div>
            <div class="summary">
              <div class="summary-row"><span>Subtotal</span><span class="sv" id="sumSub">Rp 0</span></div>
              <div class="summary-row"><span>Biaya Layanan & Pajak</span><span class="sv" style="color:var(--green)">Gratis (Rp 0)</span></div>
              <div class="summary-row total"><span>Total Pembayaran</span><span class="sv" id="sumTotal">Rp 0</span></div>
            </div>
          </div>
          <div id="payWrap" style="display:none">
            <div class="drawer-sect-head">Metode Pembayaran</div>
            <div class="pay-list">
              <div class="pay-opt selected" data-method="qris" tabindex="0" role="button" aria-pressed="true">
                <div class="pay-radio"></div>
                <div class="pay-icon">${ICONS.qris}</div>
                <div class="pay-info">
                  <div class="pay-name">QRIS (Semua Pembayaran)</div>
                  <div class="pay-desc">BCA, Mandiri, GoPay, OVO, DANA, ShopeePay</div>
                </div>
                <span class="pay-note">Instan</span>
              </div>
              <div class="pay-opt" data-method="va" tabindex="0" role="button" aria-pressed="false">
                <div class="pay-radio"></div>
                <div class="pay-icon">${ICONS.va}</div>
                <div class="pay-info">
                  <div class="pay-name">Virtual Account Bank</div>
                  <div class="pay-desc">BCA, Mandiri, BNI, BRI, Permata</div>
                </div>
                <span class="pay-note">&lt;5 Menit</span>
              </div>
              <div class="pay-opt" data-method="ewallet" tabindex="0" role="button" aria-pressed="false">
                <div class="pay-radio"></div>
                <div class="pay-icon">${ICONS.ewallet}</div>
                <div class="pay-info">
                  <div class="pay-name">E-Wallet Direct</div>
                  <div class="pay-desc">GoPay, OVO, DANA, LinkAja</div>
                </div>
                <span class="pay-note">Instan</span>
              </div>
            </div>
          </div>
          <div id="contactWrap" style="display:none">
            <label style="font-size:12.5px;font-weight:600;color:var(--slate);display:block;margin-bottom:8px" for="contactIn">
              Nomor WhatsApp / Email Penerima Akun
            </label>
            <input class="input" type="text" id="contactIn" placeholder="Contoh: 081234567890 atau pengadaan@kantor.co.id">
          </div>
          <div class="drawer-success" id="drawerSuccess">
            <div class="success-check">✓</div>
            <div class="success-title">Pesanan Diterima!</div>
            <div class="success-sub">Tim operasional SAI Tech akan mengirimkan kredensial akun dan panduan aktivasi ke kontak Anda dalam &lt;15 menit.</div>
            <div class="success-id" id="successId">SAI-XXXXXXX</div>
            <button class="btn-secondary" id="successClose" style="margin-top:8px;font-size:13px">Tutup Keranjang</button>
          </div>
        </div>
        <div class="drawer-foot" id="drawerFoot">
          <button class="btn-order" id="btnOrder" disabled>Konfirmasi & Bayar Sekarang</button>
          <div class="order-note">Aktivasi resmi &lt;15 menit · Garansi penggantian 30 hari penuh</div>
        </div>
      </aside>
    `;
    document.body.appendChild(container);
    attachDrawerEvents();
  }

  function openDrawer() {
    ensureDrawerMarkup();
    const veil = document.getElementById('veil');
    const drawer = document.getElementById('drawer');
    if (veil && drawer) {
      veil.classList.add('open');
      drawer.classList.add('open');
      document.body.style.overflow = 'hidden';
    }
  }

  function closeDrawer() {
    const veil = document.getElementById('veil');
    const drawer = document.getElementById('drawer');
    if (veil && drawer) {
      veil.classList.remove('open');
      drawer.classList.remove('open');
      document.body.style.overflow = '';
    }
  }

  function renderCart() {
    ensureDrawerMarkup();
    // Update navbar badge counters
    document.querySelectorAll('.cart-pip').forEach(el => {
      el.textContent = cart.length;
      el.classList.toggle('show', cart.length > 0);
    });

    const list = document.getElementById('cartList');
    const empty = document.getElementById('cartEmpty');
    const sw = document.getElementById('summaryWrap');
    const pw = document.getElementById('payWrap');
    const cw = document.getElementById('contactWrap');
    const btn = document.getElementById('btnOrder');

    if (!list) return;

    list.innerHTML = '';
    if (cart.length === 0) {
      list.style.display = 'none';
      empty.style.display = '';
      if (sw) sw.style.display = 'none';
      if (pw) pw.style.display = 'none';
      if (cw) cw.style.display = 'none';
      if (btn) btn.disabled = true;
      return;
    }

    empty.style.display = 'none';
    list.style.display = 'flex';
    if (sw) sw.style.display = '';
    if (pw) pw.style.display = '';
    if (cw) cw.style.display = '';
    if (btn) btn.disabled = false;

    let total = 0;
    cart.forEach((item, i) => {
      total += item.price;
      const d = item.dur === 1 ? '1 Bulan' : item.dur === 3 ? '3 Bulan (Hemat)' : '1 Tahun (Hemat)';
      const row = document.createElement('div');
      row.className = 'cart-item';
      
      const iconMarkup = item.icon || `<div class="brand-monogram">${item.name.charAt(0)}</div>`;
      
      row.innerHTML = `
        <div class="cart-item-icon">${iconMarkup}</div>
        <div class="cart-item-info">
          <div class="cart-item-name">${item.name}</div>
          <div class="cart-item-sub">${d}</div>
        </div>
        <div class="cart-item-price">${fmtRp(item.price)}</div>
        <button class="cart-item-rm" data-index="${i}" title="Hapus item">✕</button>
      `;
      list.appendChild(row);
    });

    const subEl = document.getElementById('sumSub');
    const totEl = document.getElementById('sumTotal');
    if (subEl) subEl.textContent = fmtRp(total);
    if (totEl) totEl.textContent = fmtRp(total);

    list.querySelectorAll('.cart-item-rm').forEach(b => {
      b.addEventListener('click', e => {
        const idx = +e.currentTarget.dataset.index;
        cart.splice(idx, 1);
        saveCart();
      });
    });
  }

  function attachDrawerEvents() {
    const closeBtn = document.getElementById('drawerClose');
    const veil = document.getElementById('veil');
    if (closeBtn) closeBtn.addEventListener('click', closeDrawer);
    if (veil) veil.addEventListener('click', closeDrawer);

    document.addEventListener('keydown', e => {
      if (e.key === 'Escape') closeDrawer();
    });

    // Payment options select
    document.querySelectorAll('.pay-opt').forEach(opt => {
      const selectOpt = () => {
        document.querySelectorAll('.pay-opt').forEach(o => {
          o.classList.remove('selected');
          o.setAttribute('aria-pressed', 'false');
        });
        opt.classList.add('selected');
        opt.setAttribute('aria-pressed', 'true');
      };
      opt.addEventListener('click', selectOpt);
      opt.addEventListener('keydown', e => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          selectOpt();
        }
      });
    });

    // Order submit
    const btnOrder = document.getElementById('btnOrder');
    if (btnOrder) {
      btnOrder.addEventListener('click', () => {
        const input = document.getElementById('contactIn');
        const val = input ? input.value.trim() : '';
        if (!val || val.length < 5) {
          if (input) {
            input.focus();
            input.style.borderColor = 'var(--red)';
            setTimeout(() => { input.style.borderColor = ''; }, 1600);
          }
          return;
        }

        const body = document.getElementById('drawerBody');
        if (body) {
          body.querySelectorAll(':scope > div:not(#drawerSuccess)').forEach(el => {
            el.style.display = 'none';
          });
        }
        const foot = document.getElementById('drawerFoot');
        if (foot) foot.style.display = 'none';

        const succ = document.getElementById('drawerSuccess');
        const sid = document.getElementById('successId');
        if (sid) sid.textContent = genId();
        if (succ) succ.style.display = 'block';

        cart = [];
        try { localStorage.removeItem(STORAGE_KEY); } catch (e) {}
        document.querySelectorAll('.cart-pip').forEach(el => {
          el.textContent = '0';
          el.classList.remove('show');
        });
      });
    }

    const sc = document.getElementById('successClose');
    if (sc) {
      sc.addEventListener('click', () => {
        closeDrawer();
        setTimeout(() => {
          const body = document.getElementById('drawerBody');
          const foot = document.getElementById('drawerFoot');
          const succ = document.getElementById('drawerSuccess');
          if (succ) succ.style.display = 'none';
          if (foot) foot.style.display = '';
          if (body) {
            body.querySelectorAll(':scope > div:not(#drawerSuccess)').forEach(el => {
              el.style.display = '';
            });
          }
          renderCart();
        }, 300);
      });
    }
  }

  function addToCart(name, price, dur, icon) {
    cart.push({ name, price, dur, icon, id: Date.now() });
    saveCart();
    openDrawer();
  }

  // Global API
  window.SAICart = {
    add: addToCart,
    open: openDrawer,
    close: closeDrawer,
    render: renderCart,
    items: () => cart
  };

  document.addEventListener('DOMContentLoaded', () => {
    ensureDrawerMarkup();
    renderCart();

    const navCart = document.getElementById('navCartBtn');
    if (navCart) navCart.addEventListener('click', openDrawer);

    // Bind all Add to Cart buttons
    document.addEventListener('click', e => {
      const btn = e.target.closest('.btn-buy-card, .btn-add-cart');
      if (!btn) return;
      const card = btn.closest('[data-name]');
      if (!card) return;

      const name = card.dataset.name;
      const prices = JSON.parse(card.dataset.prices || '{}');
      const activeDurBtn = document.querySelector('.dur-btn.active');
      const dur = activeDurBtn ? activeDurBtn.dataset.dur : '1';
      const price = prices[dur] || prices['1'] || 0;
      const iconEl = card.querySelector('.brand-tile');
      const icon = iconEl ? iconEl.outerHTML : '';

      addToCart(name, price, Number(dur), icon);
    });
  });
})();
