# -*- coding: utf-8 -*-
"""
Alifba AI Studio - Ma'lumotlar Bazasi va Foydalanuvchilar Boshqaruvi
SQLite3 orqali xavfsiz va tezkor ma'lumotlar bazasi
Muallif: Ismoilov Nodir
"""

import os
import sqlite3
import hashlib
import time
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database.db')


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def hash_password(password):
    return hashlib.sha256(password.strip().encode('utf-8')).hexdigest()


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # 1. Foydalanuvchilar jadvali
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            is_vip INTEGER DEFAULT 0,
            vip_until TEXT DEFAULT NULL,
            is_blocked INTEGER DEFAULT 0,
            created_at TEXT NOT NULL
        )
    ''')

    # 2. Foydalanish jurnali (kunlik limitlarni hisoblash uchun)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usage_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER DEFAULT NULL,
            ip_address TEXT NOT NULL,
            action_type TEXT NOT NULL,
            file_name TEXT DEFAULT '',
            date_str TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')

    # 3. Tizim sozlamalari
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    ''')

    # 4. Saytga tashriflar jurnali (nechta odam kirganini hisoblagich uchun)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS page_visits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address TEXT NOT NULL,
            user_agent TEXT DEFAULT '',
            date_str TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')

    # Boshlang'ich sozlamalar
    default_settings = {
        'require_login': 'false',            # true bo'lsa ro'yxatdan o'tish majburiy
        'daily_free_limit': '5',             # Kuniga 5 ta bepul
        'vip_monthly_price': '25 000',       # Oyiga 25 000 so'm
        'admin_username': 'admin',
        'admin_password_hash': hash_password('admin123'),
        'telegram_admin': 'alifbauz',        # Chek yuborish uchun telegram
        'card_number': '5614 6819 0834 3415',
        'card_holder': 'ISMOILOV NODIR',
        'announcement_text': '',
        'announcement_active': 'false'
    }

    for k, v in default_settings.items():
        cursor.execute('INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)', (k, v))

    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# Sozlamalar bilan ishlash
# ---------------------------------------------------------------------------

def get_setting(key, default=None):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
    row = cursor.fetchone()
    conn.close()
    return row['value'] if row else default


def get_all_settings():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT key, value FROM settings')
    rows = cursor.fetchall()
    conn.close()
    return {r['key']: r['value'] for r in rows}


def update_setting(key, value):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO settings (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = ?',
                   (key, str(value), str(value)))
    conn.commit()
    conn.close()


def update_settings_dict(settings_dict):
    conn = get_db()
    cursor = conn.cursor()
    for k, v in settings_dict.items():
        cursor.execute('INSERT INTO settings (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = ?',
                       (k, str(v), str(v)))
    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# Foydalanuvchilar (Auth)
# ---------------------------------------------------------------------------

def register_user(name, username, password):
    name = (name or '').strip()
    username = (username or '').strip().lower()
    password = (password or '').strip()

    if not name or len(name) < 2:
        return False, "Ism kamida 2 ta belgidan iborat bo'lishi kerak!"
    if not username or len(username) < 3:
        return False, "Login kamida 3 ta belgidan iborat bo'lishi kerak!"
    if not password or len(password) < 4:
        return False, "Parol kamida 4 ta belgidan iborat bo'lishi kerak!"

    # Faqat lotin harf, son va pastki chiziq
    if not username.replace('_', '').isalnum():
        return False, "Loginda faqat lotin harflari va sonlar ruxsat etiladi!"

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
    if cursor.fetchone():
        conn.close()
        return False, "Bu login allaqachon band. Boshqa login tanlang!"

    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    p_hash = hash_password(password)

    cursor.execute('''
        INSERT INTO users (name, username, password_hash, is_vip, vip_until, is_blocked, created_at)
        VALUES (?, ?, ?, 0, NULL, 0, ?)
    ''', (name, username, p_hash, now_str))

    user_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return True, get_user_by_id(user_id)


def authenticate_user(username, password):
    username = (username or '').strip().lower()
    password = (password or '').strip()

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return False, "Login yoki parol noto'g'ri!"

    if row['password_hash'] != hash_password(password):
        return False, "Login yoki parol noto'g'ri!"

    if row['is_blocked'] == 1:
        return False, "Sizning hisobingiz admin tomonidan bloklangan!"

    return True, dict(row)


def get_user_by_id(user_id):
    if not user_id:
        return None
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None

    data = dict(row)
    # VIP muddati tugaganini avtomatik tekshirish
    if data['is_vip'] == 1 and data['vip_until']:
        try:
            vip_date = datetime.strptime(data['vip_until'], '%Y-%m-%d %H:%M:%S')
            if datetime.now() > vip_date:
                # Muddat tugagan
                revoke_user_vip(user_id)
                data['is_vip'] = 0
                data['vip_until'] = None
        except Exception:
            pass

    return data


# ---------------------------------------------------------------------------
# Admin boshqaruvi: VIP qo'shish, muddat belgilash, qidiruv
# ---------------------------------------------------------------------------

def update_user_vip_months(user_id, months, is_unlimited=False):
    """
    Foydalanuvchiga to'loviga qarab oy hisobida VIP faollashtirish
    """
    conn = get_db()
    cursor = conn.cursor()

    now = datetime.now()
    if is_unlimited:
        vip_until = '2099-12-31 23:59:59'
    else:
        # Agar foydalanuvchida hozir ham VIP faol bo'lsa, mavjud muddat ustiga qo'shadi
        cursor.execute('SELECT is_vip, vip_until FROM users WHERE id = ?', (user_id,))
        cur = cursor.fetchone()
        start_date = now
        if cur and cur['is_vip'] == 1 and cur['vip_until']:
            try:
                existing_until = datetime.strptime(cur['vip_until'], '%Y-%m-%d %H:%M:%S')
                if existing_until > now:
                    start_date = existing_until
            except Exception:
                pass

        # months * 30 kun qo'shish
        end_date = start_date + timedelta(days=int(months) * 30)
        vip_until = end_date.strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute('UPDATE users SET is_vip = 1, vip_until = ? WHERE id = ?', (vip_until, user_id))
    conn.commit()
    conn.close()
    return True


def revoke_user_vip(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET is_vip = 0, vip_until = NULL WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    return True


def toggle_user_block(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT is_blocked FROM users WHERE id = ?', (user_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return False
    new_state = 0 if row['is_blocked'] == 1 else 1
    cursor.execute('UPDATE users SET is_blocked = ? WHERE id = ?', (new_state, user_id))
    conn.commit()
    conn.close()
    return True, new_state


def delete_user(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
    cursor.execute('DELETE FROM usage_logs WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()
    return True


def search_users(query='', filter_type='all', limit=100):
    conn = get_db()
    cursor = conn.cursor()

    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    today_str = datetime.now().strftime('%Y-%m-%d')

    sql = '''
        SELECT u.*,
               COALESCE((SELECT COUNT(*) FROM usage_logs WHERE user_id = u.id AND date_str = ?), 0) as today_usage,
               COALESCE((SELECT COUNT(*) FROM usage_logs WHERE user_id = u.id), 0) as total_usage
        FROM users u
        WHERE 1=1
    '''
    params = [today_str]

    if query:
        query_pattern = f"%{query.strip()}%"
        sql += " AND (u.name LIKE ? OR u.username LIKE ?)"
        params.extend([query_pattern, query_pattern])

    if filter_type == 'vip':
        sql += " AND u.is_vip = 1"
    elif filter_type == 'free':
        sql += " AND u.is_vip = 0"
    elif filter_type == 'blocked':
        sql += " AND u.is_blocked = 1"

    sql += " ORDER BY u.id DESC LIMIT ?"
    params.append(limit)

    cursor.execute(sql, params)
    rows = cursor.fetchall()
    conn.close()

    result = []
    for r in rows:
        d = dict(r)
        # Qolgan kunlarni hisoblash
        if d['is_vip'] == 1 and d['vip_until']:
            try:
                vip_dt = datetime.strptime(d['vip_until'], '%Y-%m-%d %H:%M:%S')
                days_left = (vip_dt - datetime.now()).days
                d['days_left'] = max(0, days_left)
                d['is_expired'] = datetime.now() > vip_dt
            except Exception:
                d['days_left'] = 0
                d['is_expired'] = False
        else:
            d['days_left'] = 0
            d['is_expired'] = False
        result.append(d)

    return result


# ---------------------------------------------------------------------------
# Kunlik Limit va Foydalanishni Tekshirish
# ---------------------------------------------------------------------------

def get_today_usage_count(user_id=None, ip_address=None):
    conn = get_db()
    cursor = conn.cursor()
    today_str = datetime.now().strftime('%Y-%m-%d')

    if user_id:
        cursor.execute('SELECT COUNT(*) as cnt FROM usage_logs WHERE user_id = ? AND date_str = ?',
                       (user_id, today_str))
    else:
        cursor.execute('SELECT COUNT(*) as cnt FROM usage_logs WHERE user_id IS NULL AND ip_address = ? AND date_str = ?',
                       (ip_address, today_str))

    row = cursor.fetchone()
    conn.close()
    return row['cnt'] if row else 0


def log_usage(user_id, ip_address, action_type, file_name=''):
    conn = get_db()
    cursor = conn.cursor()
    now_dt = datetime.now()
    today_str = now_dt.strftime('%Y-%m-%d')
    now_str = now_dt.strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute('''
        INSERT INTO usage_logs (user_id, ip_address, action_type, file_name, date_str, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, ip_address, action_type, file_name or '', today_str, now_str))

    conn.commit()
    conn.close()


def check_can_process(user_id=None, ip_address=None):
    """
    Foydalanuvchi hozir o'girish qila oladimi?
    Hozircha saytdan barcha cheklovlar va ro'yxatdan o'tish talabi olib tashlangan -
    har bir tashrif buyuruvchi bepul va cheksiz foydalana oladi.
    """
    return True, "", 999999, True


# ---------------------------------------------------------------------------
# Tashriflar Jurnali va Hisoblagich (Page Visits & Counter)
# ---------------------------------------------------------------------------

def log_page_visit(ip_address, user_agent=''):
    """
    Saytga tashrif buyurgan foydalanuvchini qayd qilish
    """
    try:
        conn = get_db()
        cursor = conn.cursor()
        now = datetime.now()
        today_str = now.strftime('%Y-%m-%d')
        now_str = now.strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute('''
            INSERT INTO page_visits (ip_address, user_agent, date_str, created_at)
            VALUES (?, ?, ?, ?)
        ''', (ip_address or '127.0.0.1', (user_agent or '')[:250], today_str, now_str))

        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error logging visit: {e}")


def get_recent_visits(limit=50):
    """
    So'nggi tashrif buyuruvchilar ro'yxati
    """
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, ip_address, user_agent, date_str, created_at
        FROM page_visits
        ORDER BY id DESC LIMIT ?
    ''', (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ---------------------------------------------------------------------------
# Admin Dashboard Metrikalari (Hisoblagich)
# ---------------------------------------------------------------------------

def get_admin_dashboard_metrics():
    conn = get_db()
    cursor = conn.cursor()
    today_str = datetime.now().strftime('%Y-%m-%d')

    # 1. Tashriflar hisoblagichi (Nechta odam kirgani)
    cursor.execute('SELECT COUNT(DISTINCT ip_address) as today_visitors FROM page_visits WHERE date_str = ?', (today_str,))
    row = cursor.fetchone()
    today_visitors = row['today_visitors'] if row and row['today_visitors'] else 0

    cursor.execute('SELECT COUNT(*) as today_pageviews FROM page_visits WHERE date_str = ?', (today_str,))
    row = cursor.fetchone()
    today_pageviews = row['today_pageviews'] if row and row['today_pageviews'] else 0

    cursor.execute('SELECT COUNT(DISTINCT ip_address) as total_visitors FROM page_visits')
    row = cursor.fetchone()
    total_visitors = row['total_visitors'] if row and row['total_visitors'] else 0

    cursor.execute('SELECT COUNT(*) as total_pageviews FROM page_visits')
    row = cursor.fetchone()
    total_pageviews = row['total_pageviews'] if row and row['total_pageviews'] else 0

    # 2. O'girishlar / Hujjatlar amallari
    cursor.execute('SELECT COUNT(*) as today_actions FROM usage_logs WHERE date_str = ?', (today_str,))
    row = cursor.fetchone()
    today_actions = row['today_actions'] if row and row['today_actions'] else 0

    cursor.execute('SELECT COUNT(*) as total_actions FROM usage_logs')
    row = cursor.fetchone()
    total_actions = row['total_actions'] if row and row['total_actions'] else 0

    # 3. Foydalanuvchilar
    cursor.execute('SELECT COUNT(*) as total_users FROM users')
    row = cursor.fetchone()
    total_users = row['total_users'] if row and row['total_users'] else 0

    cursor.execute('SELECT COUNT(*) as vip_users FROM users WHERE is_vip = 1')
    row = cursor.fetchone()
    vip_users = row['vip_users'] if row and row['vip_users'] else 0

    cursor.execute('SELECT COUNT(*) as today_users FROM users WHERE created_at LIKE ?', (f"{today_str}%",))
    row = cursor.fetchone()
    today_users = row['today_users'] if row and row['today_users'] else 0

    conn.close()

    # Disk hajmini o'lchash
    uploads_size_mb = 0
    converted_size_mb = 0
    uploads_dir = os.path.join(BASE_DIR, 'uploads')
    converted_dir = os.path.join(BASE_DIR, 'converted')

    if os.path.exists(uploads_dir):
        uploads_size_mb = sum(os.path.getsize(os.path.join(r, f)) for r, d, fs in os.walk(uploads_dir) for f in fs) / (1024 * 1024)
    if os.path.exists(converted_dir):
        converted_size_mb = sum(os.path.getsize(os.path.join(r, f)) for r, d, fs in os.walk(converted_dir) for f in fs) / (1024 * 1024)

    return {
        'today_visitors': today_visitors,
        'today_pageviews': today_pageviews,
        'total_visitors': total_visitors,
        'total_pageviews': total_pageviews,
        'today_actions': today_actions,
        'total_actions': total_actions,
        'today_users': today_users,
        'total_users': total_users,
        'vip_users': vip_users,
        'uploads_size_mb': round(uploads_size_mb, 2),
        'converted_size_mb': round(converted_size_mb, 2),
        'total_storage_mb': round(uploads_size_mb + converted_size_mb, 2)
    }


def get_recent_usage_logs(limit=40):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT l.*, u.name as user_name, u.username as user_login, u.is_vip
        FROM usage_logs l
        LEFT JOIN users u ON l.user_id = u.id
        ORDER BY l.id DESC LIMIT ?
    ''', (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def clean_storage_files():
    """
    Vaqtinchalik yuklangan va o'girilgan fayllarni tozalash
    """
    cleaned_count = 0
    freed_bytes = 0

    for folder_name in ['uploads', 'converted', 'temp_media']:
        folder_path = os.path.join(BASE_DIR, folder_name)
        if not os.path.exists(folder_path):
            continue
        for fname in os.listdir(folder_path):
            fpath = os.path.join(folder_path, fname)
            try:
                if os.path.isfile(fpath):
                    freed_bytes += os.path.getsize(fpath)
                    os.remove(fpath)
                    cleaned_count += 1
                elif os.path.isdir(fpath):
                    freed_bytes += sum(os.path.getsize(os.path.join(r, f)) for r, d, fs in os.walk(fpath) for f in fs)
                    shutil.rmtree(fpath)
                    cleaned_count += 1
            except Exception:
                pass

    return cleaned_count, round(freed_bytes / (1024 * 1024), 2)


# Dastur ishga tushganda bazani ishga tushirish
init_db()
