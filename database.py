import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DB_FILE = 'applyfly_local.db'

def get_connection():
    return sqlite3.connect(DB_FILE, check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    # Create sender_profiles table
    c.execute('''
        CREATE TABLE IF NOT EXISTS sender_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            profile_name TEXT NOT NULL,
            name TEXT NOT NULL,
            street TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            city_zip TEXT NOT NULL,
            FOREIGN KEY (user_email) REFERENCES users (email)
        )
    ''')
    
    # Migrations for splitting city and zip
    try:
        c.execute('ALTER TABLE sender_profiles ADD COLUMN city TEXT DEFAULT ""')
        c.execute('ALTER TABLE sender_profiles ADD COLUMN zip_code TEXT DEFAULT ""')
    except sqlite3.OperationalError:
        pass # Columns already exist
        
    # Create user_locked_fields table
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_locked_fields (
            user_email TEXT NOT NULL,
            field_key TEXT NOT NULL,
            field_value TEXT NOT NULL,
            PRIMARY KEY (user_email, field_key)
        )
    ''')
    
    conn.commit()
    conn.close()

def create_user(email, first_name, last_name, password):
    conn = get_connection()
    c = conn.cursor()
    try:
        password_hash = generate_password_hash(password)
        c.execute('INSERT INTO users (email, first_name, last_name, password_hash) VALUES (?, ?, ?, ?)',
                  (email, first_name, last_name, password_hash))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verify_user(email, password):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT password_hash FROM users WHERE email = ?', (email,))
    row = c.fetchone()
    conn.close()
    if row and check_password_hash(row[0], password):
        return True
    return False

def save_profile(user_email, profile_name, name, street, phone, email, city, zip_code):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO sender_profiles (user_email, profile_name, name, street, phone, email, city_zip, city, zip_code)
        VALUES (?, ?, ?, ?, ?, ?, '', ?, ?)
    ''', (user_email, profile_name, name, street, phone, email, city, zip_code))
    conn.commit()
    conn.close()

def get_all_profiles(user_email):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT id, profile_name, name, street, phone, email, city, zip_code, city_zip FROM sender_profiles WHERE user_email = ?', (user_email,))
    rows = c.fetchall()
    conn.close()
    # Convert to list of dicts for easier use in Streamlit
    profiles = []
    for row in rows:
        db_city = row[6]
        db_zip = row[7]
        legacy_city_zip = row[8]
        
        # If the new columns are empty but legacy is not, try to parse it
        if not db_city and not db_zip and legacy_city_zip:
            parts = legacy_city_zip.strip().split(maxsplit=1)
            if len(parts) > 1 and parts[0].isdigit():
                db_zip = parts[0]
                db_city = parts[1]
            else:
                db_city = legacy_city_zip
                
        profiles.append({
            'id': row[0],
            'profile_name': row[1],
            'name': row[2],
            'street': row[3],
            'phone': row[4],
            'email': row[5],
            'city': db_city,
            'zip_code': db_zip
        })
    return profiles

def delete_profile(profile_id, user_email):
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM sender_profiles WHERE id = ? AND user_email = ?', (profile_id, user_email))
    conn.commit()
    conn.close()

def save_locked_field(user_email, field_key, field_value):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO user_locked_fields (user_email, field_key, field_value)
        VALUES (?, ?, ?)
        ON CONFLICT(user_email, field_key) DO UPDATE SET field_value=excluded.field_value
    ''', (user_email, field_key, field_value))
    conn.commit()
    conn.close()

def get_locked_fields(user_email):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT field_key, field_value FROM user_locked_fields WHERE user_email = ?', (user_email,))
    rows = c.fetchall()
    conn.close()
    return {row[0]: row[1] for row in rows}

def delete_locked_field(user_email, field_key):
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM user_locked_fields WHERE user_email = ? AND field_key = ?', (user_email, field_key))
    conn.commit()
    conn.close()
