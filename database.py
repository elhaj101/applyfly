import os
import psycopg2
from psycopg2 import errors as pg_errors
from werkzeug.security import generate_password_hash, check_password_hash


def _get_db_url():
    """Read the Postgres connection string from Streamlit secrets or the
    environment. On Streamlit Cloud add it under Settings → Secrets as:

        DATABASE_URL = "postgresql://...supabase.com:6543/postgres"

    (Use the Supabase *connection pooling* string, port 6543.)
    """
    try:
        import streamlit as st
        if "DATABASE_URL" in st.secrets:
            return st.secrets["DATABASE_URL"]
    except Exception:
        pass
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError(
            "DATABASE_URL is not configured. Add it to Streamlit secrets "
            "(or the environment) using your Supabase connection string."
        )
    return url


def get_connection():
    return psycopg2.connect(_get_db_url())


def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS sender_profiles (
            id SERIAL PRIMARY KEY,
            user_email TEXT NOT NULL,
            profile_name TEXT NOT NULL,
            name TEXT NOT NULL,
            street TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            city TEXT DEFAULT '',
            zip_code TEXT DEFAULT '',
            signature TEXT DEFAULT ''
        )
    ''')
    # Migration for adding signature to pre-existing profile tables
    c.execute("ALTER TABLE sender_profiles ADD COLUMN IF NOT EXISTS signature TEXT DEFAULT ''")
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
        c.execute(
            'INSERT INTO users (email, first_name, last_name, password_hash) VALUES (%s, %s, %s, %s)',
            (email, first_name, last_name, password_hash),
        )
        conn.commit()
        return True
    except (pg_errors.UniqueViolation, psycopg2.IntegrityError):
        conn.rollback()
        return False
    finally:
        conn.close()


def verify_user(email, password):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT password_hash FROM users WHERE email = %s', (email,))
    row = c.fetchone()
    conn.close()
    if row and check_password_hash(row[0], password):
        return True
    return False


def save_profile(user_email, profile_name, name, street, phone, email, city, zip_code, signature=''):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO sender_profiles (user_email, profile_name, name, street, phone, email, city, zip_code, signature)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (user_email, profile_name, name, street, phone, email, city, zip_code, signature))
    conn.commit()
    conn.close()


def get_all_profiles(user_email):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        'SELECT id, profile_name, name, street, phone, email, city, zip_code, signature '
        'FROM sender_profiles WHERE user_email = %s ORDER BY id',
        (user_email,),
    )
    rows = c.fetchall()
    conn.close()
    profiles = []
    for row in rows:
        profiles.append({
            'id': row[0],
            'profile_name': row[1],
            'name': row[2],
            'street': row[3],
            'phone': row[4],
            'email': row[5],
            'city': row[6],
            'zip_code': row[7],
            'signature': row[8] or '',
        })
    return profiles


def delete_profile(profile_id, user_email):
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM sender_profiles WHERE id = %s AND user_email = %s', (profile_id, user_email))
    conn.commit()
    conn.close()


def save_locked_field(user_email, field_key, field_value):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO user_locked_fields (user_email, field_key, field_value)
        VALUES (%s, %s, %s)
        ON CONFLICT (user_email, field_key) DO UPDATE SET field_value = EXCLUDED.field_value
    ''', (user_email, field_key, field_value))
    conn.commit()
    conn.close()


def get_locked_fields(user_email):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT field_key, field_value FROM user_locked_fields WHERE user_email = %s', (user_email,))
    rows = c.fetchall()
    conn.close()
    return {row[0]: row[1] for row in rows}


def delete_locked_field(user_email, field_key):
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM user_locked_fields WHERE user_email = %s AND field_key = %s', (user_email, field_key))
    conn.commit()
    conn.close()
