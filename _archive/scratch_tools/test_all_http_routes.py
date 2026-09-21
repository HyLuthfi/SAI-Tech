import urllib.request
import urllib.error

routes = [
    '/',
    '/about',
    '/services',
    '/service-single',
    '/portfolio',
    '/portfolio-single',
    '/pricing',
    '/blog',
    '/blog-single',
    '/team',
    '/contact',
    '/katalog',
    '/assets/ritovex/hamburger-black.json'
]

print("=== TESTING HTTP SERVER ROUTES (PORT 3000) ===")
all_pass = True

for r in routes:
    url = f"http://127.0.0.1:3000{r}"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as resp:
            status = resp.status
            x_frame = resp.headers.get('x-frame-options')
            ct = resp.headers.get('content-type', '').split(';')[0]
            print(f"{r:<38} -> {status} [{ct}] (X-Frame: {x_frame})")
            if status != 200:
                all_pass = False
    except urllib.error.HTTPError as e:
        print(f"{r:<38} -> HTTPError {e.code}")
        all_pass = False

print("\nServer Routes Status:", "ALL 200 OK [PASSED]" if all_pass else "SOME FAILED")
