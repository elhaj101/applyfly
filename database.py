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

def save_profile(user_email, profile_name, name, street, phone, email, city_zip):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO sender_profiles (user_email, profile_name, name, street, phone, email, city_zip)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (user_email, profile_name, name, street, phone, email, city_zip))
    conn.commit()
    conn.close()

def get_all_profiles(user_email):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT id, profile_name, name, street, phone, email, city_zip FROM sender_profiles WHERE user_email = ?', (user_email,))
    rows = c.fetchall()
    conn.close()
    # Convert to list of dicts for easier use in Streamlit
    profiles = []
    for row in rows:
        profiles.append({
            'id': row[0],
            'profile_name': row[1],
            'name': row[2],
            'street': row[3],
            'phone': row[4],
            'email': row[5],
            'city_zip': row[6]
        })
    return profiles

def delete_profile(profile_id, user_email):
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM sender_profiles WHERE id = ? AND user_email = ?', (profile_id, user_email))
    conn.commit()
    conn.close()
