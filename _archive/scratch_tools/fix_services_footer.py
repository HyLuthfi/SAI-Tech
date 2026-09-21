for fname in ['services.html', 'service-single.html']:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()

    content = content.replace(
        '<a aria-current="page" class="footer-menu-text-link w--current" href="services">Layanan</a><a class="nav-link w-nav-link" href="katalog">Katalog</a>',
        '<a aria-current="page" class="footer-menu-text-link w--current" href="services">Layanan</a>\n</li>\n<li class="footer-menu-list-item">\n<a class="footer-menu-text-link" href="katalog">Katalog Digital</a>'
    )
    content = content.replace(
        '<a aria-current="page" class="footer-menu-text-link" href="services">Layanan</a><a class="nav-link w-nav-link" href="katalog">Katalog</a>',
        '<a aria-current="page" class="footer-menu-text-link" href="services">Layanan</a>\n</li>\n<li class="footer-menu-list-item">\n<a class="footer-menu-text-link" href="katalog">Katalog Digital</a>'
    )

    with open(fname, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated", fname)
