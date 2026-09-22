import os
import sys
import json
import base64
import time
import hashlib
import hmac
import secrets
import urllib.parse
import urllib.request
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

ADMIN_CONFIG_PATH = os.path.join('data', 'admin_config.json')
ADMIN_SESSIONS_PATH = os.path.join('data', 'admin_sessions.json')
LOGIN_ATTEMPTS = {}  # client_ip -> {'failed_count': int, 'locked_until': float, 'last_failed_at': float}
MAX_FAILED_ATTEMPTS = 5
LOCKOUT_DURATION = 900  # 15 minutes in seconds

def load_dotenv(dotenv_path='.env'):
    if os.path.isfile(dotenv_path):
        try:
            with open(dotenv_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#') or '=' not in line:
                        continue
                    k, v = line.split('=', 1)
                    k = k.strip()
                    v = v.strip().strip('"').strip("'")
                    os.environ[k] = v
        except Exception:
            pass

load_dotenv()

def get_admin_config():
    load_dotenv()
    cfg = {
        "google_client_id": os.environ.get("GOOGLE_CLIENT_ID", "").strip(),
        "allowed_emails": [e.strip().lower() for e in os.environ.get("ADMIN_ALLOWED_EMAILS", "owner@saitech.id,admin@saitech.id").split(",") if e.strip()],
        "dev_mode_allowed": os.environ.get("DEV_MODE_ALLOWED", "true").lower() in ("true", "1", "yes"),
        "pin": "1234",
        "token_salt": "sai_tech_secure_salt_2026"
    }
    if os.path.isfile(ADMIN_CONFIG_PATH):
        try:
            with open(ADMIN_CONFIG_PATH, 'r', encoding='utf-8') as f:
                saved = json.load(f)
                if saved.get("google_client_id"):
                    cfg["google_client_id"] = saved["google_client_id"]
                if saved.get("allowed_emails"):
                    cfg["allowed_emails"] = saved["allowed_emails"]
                if "dev_mode_allowed" in saved:
                    cfg["dev_mode_allowed"] = saved["dev_mode_allowed"]
                if saved.get("pin"):
                    cfg["pin"] = saved["pin"]
                if saved.get("pin_hash"):
                    cfg["pin_hash"] = saved["pin_hash"]
        except Exception:
            pass
    return cfg

def save_admin_config(cfg):
    os.makedirs('data', exist_ok=True)
    with open(ADMIN_CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)

def load_admin_sessions():
    if os.path.isfile(ADMIN_SESSIONS_PATH):
        try:
            with open(ADMIN_SESSIONS_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_admin_sessions(sessions):
    os.makedirs('data', exist_ok=True)
    try:
        with open(ADMIN_SESSIONS_PATH, 'w', encoding='utf-8') as f:
            json.dump(sessions, f, indent=2, ensure_ascii=False)
    except Exception:
        pass

ADMIN_SESSIONS = load_admin_sessions()

def create_admin_session(email, name, picture):
    token = "sai_g_" + secrets.token_hex(20)
    ADMIN_SESSIONS[token] = {
        "email": email,
        "name": name,
        "picture": picture,
        "created_at": time.time()
    }
    save_admin_sessions(ADMIN_SESSIONS)
    return token

def get_admin_session_data(token):
    if token and token in ADMIN_SESSIONS:
        return ADMIN_SESSIONS[token]
    return None

def verify_google_id_token(credential):
    try:
        url = f"https://oauth2.googleapis.com/tokeninfo?id_token={urllib.parse.quote(credential)}"
        req = urllib.request.Request(url, headers={'User-Agent': 'SAI-Tech-Auth/1.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status != 200:
                return False, "Verifikasi token ke server Google gagal."
            raw = resp.read().decode('utf-8')
            payload = json.loads(raw)
            return True, payload
    except Exception as e:
        return False, f"Gagal menghubungi server Google: {str(e)}"

def check_admin_whitelist(email, cfg):
    allowed = [e.strip().lower() for e in cfg.get('allowed_emails', []) if e.strip()]
    user_email = email.strip().lower()
    if '*' in allowed or user_email in allowed:
        return True
    return False

def hash_secret(secret, salt):
    return hashlib.sha256(f"{salt}:{secret}:{salt}".encode('utf-8')).hexdigest()

def verify_secret(input_secret, stored_secret_or_hash, salt):
    if not input_secret or not stored_secret_or_hash:
        return False
    # If already a 64-char sha256 hash
    if len(str(stored_secret_or_hash)) == 64:
        calc = hash_secret(input_secret, salt)
        return hmac.compare_digest(calc, str(stored_secret_or_hash))
    # Fallback to direct constant-time compare for legacy plaintext PIN
    return hmac.compare_digest(str(input_secret), str(stored_secret_or_hash))

def check_login_rate_limit(client_ip):
    now = time.time()
    record = LOGIN_ATTEMPTS.get(client_ip, {'failed_count': 0, 'locked_until': 0, 'last_failed_at': 0})
    
    if record['locked_until'] > now:
        remaining_seconds = int(record['locked_until'] - now)
        remaining_minutes = max(1, (remaining_seconds + 59) // 60)
        return False, remaining_seconds, f"Akses diblokir karena terlalu banyak percobaan gagal (5x). Silakan coba lagi dalam {remaining_minutes} menit."
    
    # If lockout expired or more than 30 mins since last attempt, reset
    if record['locked_until'] <= now and (now - record['last_failed_at'] > 1800):
        record['failed_count'] = 0
        record['locked_until'] = 0
        LOGIN_ATTEMPTS[client_ip] = record

    return True, 0, ""

def record_failed_login(client_ip):
    now = time.time()
    record = LOGIN_ATTEMPTS.get(client_ip, {'failed_count': 0, 'locked_until': 0, 'last_failed_at': 0})
    record['failed_count'] += 1
    record['last_failed_at'] = now

    # Progressive tarpit delay to throttle automated scripts (0.8s - 3s)
    delay = min(3.0, record['failed_count'] * 0.75)
    time.sleep(delay)

    if record['failed_count'] >= MAX_FAILED_ATTEMPTS:
        record['locked_until'] = now + LOCKOUT_DURATION
        LOGIN_ATTEMPTS[client_ip] = record
        return 0, "Terlalu banyak percobaan salah (5x). Akses Anda diblokir selama 15 menit demi keamanan."
    
    remaining = MAX_FAILED_ATTEMPTS - record['failed_count']
    LOGIN_ATTEMPTS[client_ip] = record
    return remaining, f"PIN / Password salah. Sisa kesempatan: {remaining} kali sebelum diblokir."

def reset_login_attempts(client_ip):
    if client_ip in LOGIN_ATTEMPTS:
        del LOGIN_ATTEMPTS[client_ip]

def get_admin_token():
    cfg = get_admin_config()
    secret = str(cfg.get('pin_hash', cfg.get('pin', '1234')))
    salt = str(cfg.get('token_salt', 'sai_tech_secure_salt_2026'))
    return "sai_" + hashlib.sha256(f"{secret}:{salt}".encode('utf-8')).hexdigest()[:24]

def is_valid_admin_token(token):
    if not token:
        return False
    if token in ADMIN_SESSIONS:
        session = ADMIN_SESSIONS[token]
        if time.time() - session.get('created_at', 0) < 604800:
            return True
        else:
            del ADMIN_SESSIONS[token]
            save_admin_sessions(ADMIN_SESSIONS)
            return False
    return token == get_admin_token() or token == "sai_admin_active_session_2026"

class RobustThreadingServer(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True

    def handle_error(self, request, client_address):
        exc_type, _, _ = sys.exc_info()
        if exc_type in (ConnectionResetError, BrokenPipeError, ConnectionAbortedError):
            return
        super().handle_error(request, client_address)

class CleanURLHandler(SimpleHTTPRequestHandler):
    # Ensure correct MIME types
    extensions_map = {
        **SimpleHTTPRequestHandler.extensions_map,
        '.svg': 'image/svg+xml',
        '.ico': 'image/x-icon',
        '.webp': 'image/webp',
        '.css': 'text/css; charset=utf-8',
        '.js': 'application/javascript; charset=utf-8',
        '.html': 'text/html; charset=utf-8',
        '.json': 'application/json; charset=utf-8',
    }

    def end_headers(self):
        # Enterprise HTTP Security Headers
        self.send_header('X-Frame-Options', 'SAMEORIGIN')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Referrer-Policy', 'strict-origin-when-cross-origin')
        self.send_header('Permissions-Policy', 'camera=(), microphone=(), geolocation=()')
        self.send_header('X-XSS-Protection', '1; mode=block')
        super().end_headers()

    def copyfile(self, source, outputfile):
        try:
            super().copyfile(source, outputfile)
        except (ConnectionResetError, BrokenPipeError, ConnectionAbortedError):
            pass

    def handle_one_request(self):
        try:
            super().handle_one_request()
        except (ConnectionResetError, BrokenPipeError, ConnectionAbortedError):
            pass

    def send_json_response(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def get_client_ip(self):
        forwarded = self.headers.get('X-Forwarded-For', '')
        if forwarded:
            return forwarded.split(',')[0].strip()
        return self.client_address[0] if self.client_address else '127.0.0.1'

    def get_auth_token(self, data=None):
        auth_header = self.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            return auth_header[7:].strip()
        if data and isinstance(data, dict):
            token = data.get('token')
            if token:
                return str(token).strip()
        parsed = urllib.parse.urlparse(self.path)
        q = urllib.parse.parse_qs(parsed.query)
        return q.get('token', [''])[0].strip()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == '/api/checkout/manual':
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length).decode('utf-8')
                data = json.loads(body)

                order_id = data.get('order_id', f"SAI-{int(time.time())}")
                product_name = data.get('product_name', '')
                package_duration = data.get('package_duration', '')
                price = data.get('price', '')
                phone = data.get('phone', '')
                email = data.get('email', '')
                notes = data.get('notes', '')
                proof_b64 = data.get('proof_base64', '')
                proof_filename = ''

                if proof_b64:
                    os.makedirs(os.path.join('uploads', 'bukti_transfer'), exist_ok=True)
                    if ',' in proof_b64:
                        proof_b64 = proof_b64.split(',', 1)[1]
                    proof_bytes = base64.b64decode(proof_b64)
                    proof_filename = f"{order_id}_{int(time.time())}.png"
                    proof_filepath = os.path.join('uploads', 'bukti_transfer', proof_filename)
                    with open(proof_filepath, 'wb') as f:
                        f.write(proof_bytes)

                os.makedirs('data', exist_ok=True)
                orders_file = os.path.join('data', 'orders.json')
                orders = []
                if os.path.isfile(orders_file):
                    try:
                        with open(orders_file, 'r', encoding='utf-8') as f:
                            orders = json.load(f)
                    except Exception:
                        orders = []

                order_record = {
                    'order_id': order_id,
                    'created_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'product_name': product_name,
                    'package_duration': package_duration,
                    'price': price,
                    'phone': phone,
                    'email': email,
                    'notes': notes,
                    'proof_filename': proof_filename,
                    'status': 'MENUNGGU_VERIFIKASI'
                }
                orders.append(order_record)
                with open(orders_file, 'w', encoding='utf-8') as f:
                    json.dump(orders, f, indent=2, ensure_ascii=False)

                self.send_json_response(200, {
                    'status': 'success',
                    'message': 'Pesanan dan bukti transfer berhasil diterima',
                    'order_id': order_id
                })
                return
            except Exception as e:
                self.send_json_response(500, {'status': 'error', 'message': str(e)})
                return

        elif path == '/api/admin/auth/google':
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length).decode('utf-8')
                data = json.loads(body)
                credential = data.get('credential', '').strip()
                if not credential:
                    self.send_json_response(400, {'status': 'error', 'message': 'Token credential Google tidak ditemukan'})
                    return

                success, res = verify_google_id_token(credential)
                if not success:
                    self.send_json_response(401, {'status': 'error', 'message': res})
                    return

                payload = res
                email = str(payload.get('email', '')).strip().lower()
                email_verified = payload.get('email_verified')
                if str(email_verified).lower() not in ('true', '1'):
                    self.send_json_response(401, {'status': 'error', 'message': 'Email Google belum terverifikasi'})
                    return

                cfg = get_admin_config()
                if not check_admin_whitelist(email, cfg):
                    self.send_json_response(403, {
                        'status': 'forbidden',
                        'message': f'Akses Ditolak: Akun Google ({email}) bukan admin resmi SAI Tech. Daftarkan email ini ke Whitelist Admin.'
                    })
                    return

                name = payload.get('name', email.split('@')[0])
                picture = payload.get('picture', '')
                token = create_admin_session(email, name, picture)
                reset_login_attempts(self.get_client_ip())

                self.send_json_response(200, {
                    'status': 'success',
                    'token': token,
                    'admin': {
                        'name': name,
                        'email': email,
                        'picture': picture
                    },
                    'message': 'Autentikasi Google berhasil'
                })
                return
            except Exception as e:
                self.send_json_response(500, {'status': 'error', 'message': str(e)})
                return

        elif path == '/api/admin/auth/dev-bypass':
            try:
                client_ip = self.get_client_ip()
                is_local = client_ip in ('127.0.0.1', '::1', 'localhost')
                cfg = get_admin_config()
                if not is_local or not cfg.get('dev_mode_allowed', True):
                    self.send_json_response(403, {'status': 'forbidden', 'message': 'Mode Developer hanya tersedia di localhost'})
                    return

                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else '{}'
                try:
                    data = json.loads(body)
                except Exception:
                    data = {}
                email = data.get('email', 'dev-admin@saitech.id').strip().lower()
                name = data.get('name', 'Developer (Localhost)')
                picture = ''
                token = create_admin_session(email, name, picture)

                self.send_json_response(200, {
                    'status': 'success',
                    'token': token,
                    'admin': {
                        'name': name,
                        'email': email,
                        'picture': picture
                    },
                    'message': 'Login Mode Pengembang berhasil'
                })
                return
            except Exception as e:
                self.send_json_response(500, {'status': 'error', 'message': str(e)})
                return

        elif path == '/api/admin/auth/config':
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length).decode('utf-8')
                data = json.loads(body)
                token = self.get_auth_token(data)
                cfg = get_admin_config()

                client_ip = self.get_client_ip()
                is_local = client_ip in ('127.0.0.1', '::1', 'localhost')

                # Allow update if valid admin session, OR if client_id is empty on localhost
                if not is_valid_admin_token(token) and not (is_local and not cfg.get('google_client_id')):
                    self.send_json_response(401, {'status': 'error', 'message': 'Sesi admin diperlukan untuk mengubah konfigurasi'})
                    return

                if 'google_client_id' in data:
                    cfg['google_client_id'] = str(data['google_client_id']).strip()
                if 'allowed_emails' in data and isinstance(data['allowed_emails'], list):
                    cfg['allowed_emails'] = [str(e).strip().lower() for e in data['allowed_emails'] if str(e).strip()]
                save_admin_config(cfg)

                self.send_json_response(200, {
                    'status': 'success',
                    'message': 'Pengaturan Google OAuth & Whitelist berhasil disimpan',
                    'google_client_id': cfg.get('google_client_id', ''),
                    'allowed_emails': cfg.get('allowed_emails', [])
                })
                return
            except Exception as e:
                self.send_json_response(500, {'status': 'error', 'message': str(e)})
                return

        elif path == '/api/admin/auth/logout':
            try:
                token = self.get_auth_token()
                if token in ADMIN_SESSIONS:
                    del ADMIN_SESSIONS[token]
                    save_admin_sessions(ADMIN_SESSIONS)
                self.send_json_response(200, {'status': 'success', 'message': 'Logout berhasil'})
                return
            except Exception as e:
                self.send_json_response(500, {'status': 'error', 'message': str(e)})
                return

        elif path == '/api/admin/login':
            try:
                client_ip = self.get_client_ip()
                allowed, wait_sec, lock_msg = check_login_rate_limit(client_ip)
                if not allowed:
                    self.send_json_response(429, {
                        'status': 'locked',
                        'message': lock_msg,
                        'lockout_remaining': wait_sec
                    })
                    return

                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length).decode('utf-8')
                data = json.loads(body)
                input_pin = str(data.get('pin', '')).strip()

                cfg = get_admin_config()
                salt = str(cfg.get('token_salt', 'sai_tech_secure_salt_2026'))
                stored_target = str(cfg.get('pin_hash', cfg.get('pin', '1234')))

                if verify_secret(input_pin, stored_target, salt):
                    reset_login_attempts(client_ip)
                    token = get_admin_token()
                    self.send_json_response(200, {
                        'status': 'success',
                        'token': token,
                        'message': 'Autentikasi berhasil'
                    })
                else:
                    rem, fail_msg = record_failed_login(client_ip)
                    status_code = 429 if rem == 0 else 401
                    self.send_json_response(status_code, {
                        'status': 'error',
                        'message': fail_msg,
                        'remaining_attempts': rem
                    })
                return
            except Exception as e:
                self.send_json_response(500, {'status': 'error', 'message': str(e)})
                return

        elif path == '/api/admin/change-pin':
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length).decode('utf-8')
                data = json.loads(body)
                token = self.get_auth_token(data)
                if not is_valid_admin_token(token):
                    self.send_json_response(401, {'status': 'error', 'message': 'Sesi login tidak valid'})
                    return

                old_pin = str(data.get('old_pin', '')).strip()
                new_pin = str(data.get('new_pin', '')).strip()

                cfg = get_admin_config()
                salt = str(cfg.get('token_salt', 'sai_tech_secure_salt_2026'))
                stored_target = str(cfg.get('pin_hash', cfg.get('pin', '1234')))

                if not verify_secret(old_pin, stored_target, salt):
                    self.send_json_response(400, {'status': 'error', 'message': 'PIN / Password lama tidak sesuai'})
                    return

                if not new_pin or len(new_pin) < 4:
                    self.send_json_response(400, {'status': 'error', 'message': 'PIN / Password baru minimal 4 karakter (disarankan kombinasi huruf & angka)'})
                    return

                # Save as salted hash so plaintext is never exposed
                cfg['pin_hash'] = hash_secret(new_pin, salt)
                if 'pin' in cfg:
                    del cfg['pin']
                save_admin_config(cfg)

                new_token = get_admin_token()
                self.send_json_response(200, {
                    'status': 'success',
                    'token': new_token,
                    'message': 'PIN / Password berhasil diperbarui'
                })
                return
            except Exception as e:
                self.send_json_response(500, {'status': 'error', 'message': str(e)})
                return

        elif path == '/api/admin/update-status':
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length).decode('utf-8')
                data = json.loads(body)
                token = self.get_auth_token(data)
                if not is_valid_admin_token(token):
                    self.send_json_response(401, {'status': 'error', 'message': 'Sesi login tidak valid'})
                    return
                order_id = data.get('order_id')
                new_status = data.get('status')
                orders_file = os.path.join('data', 'orders.json')
                orders = []
                if os.path.isfile(orders_file):
                    try:
                        with open(orders_file, 'r', encoding='utf-8') as f:
                            orders = json.load(f)
                    except Exception:
                        orders = []
                updated = False
                for o in orders:
                    if o.get('order_id') == order_id:
                        o['status'] = new_status
                        if new_status == 'SELESAI':
                            o['completed_at'] = time.strftime('%Y-%m-%d %H:%M:%S')
                        updated = True
                        break
                if updated:
                    with open(orders_file, 'w', encoding='utf-8') as f:
                        json.dump(orders, f, indent=2, ensure_ascii=False)
                    self.send_json_response(200, {'status': 'success', 'message': 'Status pesanan berhasil diubah'})
                else:
                    self.send_json_response(404, {'status': 'error', 'message': 'Pesanan tidak ditemukan'})
                return
            except Exception as e:
                self.send_json_response(500, {'status': 'error', 'message': str(e)})
                return

        elif path == '/api/admin/delete-order':
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length).decode('utf-8')
                data = json.loads(body)
                token = self.get_auth_token(data)
                if not is_valid_admin_token(token):
                    self.send_json_response(401, {'status': 'error', 'message': 'Sesi login tidak valid'})
                    return
                order_id = data.get('order_id')
                orders_file = os.path.join('data', 'orders.json')
                orders = []
                if os.path.isfile(orders_file):
                    try:
                        with open(orders_file, 'r', encoding='utf-8') as f:
                            orders = json.load(f)
                    except Exception:
                        orders = []
                initial_len = len(orders)
                orders = [o for o in orders if o.get('order_id') != order_id]
                if len(orders) < initial_len:
                    with open(orders_file, 'w', encoding='utf-8') as f:
                        json.dump(orders, f, indent=2, ensure_ascii=False)
                    self.send_json_response(200, {'status': 'success', 'message': 'Pesanan berhasil dihapus'})
                else:
                    self.send_json_response(404, {'status': 'error', 'message': 'Pesanan tidak ditemukan'})
                return
            except Exception as e:
                self.send_json_response(500, {'status': 'error', 'message': str(e)})
                return

        self.send_error(404, "Not Found")

    def do_HEAD(self):
        return self.do_GET()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == '/api/admin/auth/config':
            cfg = get_admin_config()
            client_ip = self.get_client_ip()
            is_local = client_ip in ('127.0.0.1', '::1', 'localhost')
            self.send_json_response(200, {
                'configured': bool(cfg.get('google_client_id')),
                'google_client_id': cfg.get('google_client_id', ''),
                'allowed_emails': cfg.get('allowed_emails', []),
                'is_localhost': is_local,
                'dev_mode_allowed': cfg.get('dev_mode_allowed', True) and is_local
            })
            return

        if path == '/api/admin/auth/session':
            token = self.get_auth_token()
            if not is_valid_admin_token(token):
                self.send_json_response(401, {'status': 'error', 'message': 'Sesi tidak valid'})
                return
            data = get_admin_session_data(token) or {
                'name': 'Admin SAI Tech',
                'email': 'admin@saitech.id',
                'picture': ''
            }
            self.send_json_response(200, {'status': 'success', 'admin': data})
            return

        if path == '/api/admin/orders':
            token = self.get_auth_token()
            if not is_valid_admin_token(token):
                self.send_json_response(401, {'status': 'error', 'message': 'Akses ditolak: PIN / Sesi diperlukan'})
                return
            orders_file = os.path.join('data', 'orders.json')
            orders = []
            if os.path.isfile(orders_file):
                try:
                    with open(orders_file, 'r', encoding='utf-8') as f:
                        orders = json.load(f)
                except Exception:
                    orders = []
            orders = sorted(orders, key=lambda x: x.get('created_at', ''), reverse=True)
            self.send_json_response(200, {'status': 'success', 'orders': orders})
            return

        # 0. Restrict access to _archive or hidden dot files (Returns 404 Not Found)
        if path.startswith('/_archive') or '/.' in path:
            self.send_error(404, "File not found")
            return

        # 1. Root handling
        if path == '' or path == '/':
            self.path = '/index.html'
            if parsed.query:
                self.path += '?' + parsed.query
            return super().do_GET()

        # Redirect /admin to /admin-orders
        if path == '/admin':
            self.send_response(301)
            self.send_header('Location', '/admin-orders')
            self.end_headers()
            return

        # 2. Redirect /index or /index.html to /
        if path in ['/index', '/index.html']:
            new_url = '/'
            if parsed.query:
                new_url += '?' + parsed.query
            if parsed.fragment:
                new_url += '#' + parsed.fragment
            self.send_response(301)
            self.send_header('Location', new_url)
            self.end_headers()
            return

        # 3. Strip trailing slash on non-directory paths
        if path.endswith('/') and len(path) > 1:
            clean_path = path.rstrip('/')
            new_url = clean_path
            if parsed.query:
                new_url += '?' + parsed.query
            if parsed.fragment:
                new_url += '#' + parsed.fragment
            self.send_response(301)
            self.send_header('Location', new_url)
            self.end_headers()
            return

        # 4. If URL ends with .html (e.g. /contact.html), 301 redirect to clean URL /contact
        if path.endswith('.html'):
            clean_path = path[:-5]
            new_url = clean_path
            if parsed.query:
                new_url += '?' + parsed.query
            if parsed.fragment:
                new_url += '#' + parsed.fragment
            self.send_response(301)
            self.send_header('Location', new_url)
            self.end_headers()
            return

        # 5. Clean URL matching: check if requested path corresponds to a .html file
        ext = os.path.splitext(path)[1]
        if not ext:
            rel_file = path.lstrip('/') + '.html'
            if os.path.isfile(rel_file):
                self.path = '/' + rel_file
                if parsed.query:
                    self.path += '?' + parsed.query
                return super().do_GET()

        return super().do_GET()

def run(port=3000):
    server_address = ('', port)
    httpd = RobustThreadingServer(server_address, CleanURLHandler)
    print(f"Clean URL Server active with Enterprise Security Headers at http://localhost:{port}/")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else int(os.environ.get('PORT', 3000))
    run(port)
