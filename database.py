import sqlite3
import pandas as pd
import uuid

DB_NAME = "forma_master.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Kohteiden taulu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS properties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            address TEXT NOT NULL,
            property_type TEXT,
            asking_price REAL,
            owner TEXT DEFAULT 'Herra Välittäjä',
            status TEXT DEFAULT 'Aktiivinen',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Varmistetaan että owner-sarake löytyy olemassa olevasta taulusta
    try:
        cursor.execute("ALTER TABLE properties ADD COLUMN owner TEXT DEFAULT 'Herra Välittäjä'")
    except sqlite3.OperationalError:
        pass # Sarake on jo olemassa
    
    # Käyttäjien taulu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            role TEXT DEFAULT 'LKV'
        )
    """)

    # Ostajien vastauksien taulu mittareille ja lomakkeelle
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS buyer_responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            property_id INTEGER,
            data TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Kutsulinkkien ja B2B-rekisteröinnin taulu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS invites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL,
            full_name TEXT,
            company TEXT,
            role TEXT DEFAULT 'LKV',
            credits INTEGER DEFAULT 10,
            status TEXT DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Tarkistetaan onko käyttäjiä olemassa, jos ei, luodaan oletukset
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        default_users = [
            ("herra", "lkv2026", "Herra Välittäjä", "LKV"),
            ("maija", "myyja2026", "Maija Myyjä", "LKV"),
            ("master", "admin", "Master Dashboard", "Master")
        ]
        cursor.executemany("INSERT INTO users (username, password, full_name, role) VALUES (?, ?, ?, ?)", default_users)
    
    conn.commit()
    conn.close()

def add_property(address, asking_price, property_type="Kerrostalo", owner="Herra Välittäjä"):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO properties (address, property_type, asking_price, owner, status)
        VALUES (?, ?, ?, ?, 'Aktiivinen')
    """, (address, property_type, asking_price, owner))
    conn.commit()
    conn.close()

def get_properties(owner=None):
    conn = sqlite3.connect(DB_NAME)
    if owner and owner != "Master Dashboard & Ingest Hub":
        df = pd.read_sql_query("SELECT * FROM properties WHERE owner = ?", conn, params=(owner,))
    else:
        df = pd.read_sql_query("SELECT * FROM properties", conn)
    conn.close()
    return df

def authenticate_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT username, full_name, role FROM users WHERE username = ? AND password = ?", (username.strip().lower(), password))
    user = cursor.fetchone()
    conn.close()
    if user:
        return {"username": user[0], "name": user[1], "role": user[2]}
    return None

def add_user(username, password, full_name, role="LKV"):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, full_name, role) VALUES (?, ?, ?, ?)", 
                       (username.strip().lower(), password, full_name, role))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    conn.close()
    return success

def get_all_users():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT username, full_name, role FROM users", conn)
    conn.close()
    return df

def get_buyer_responses(property_id):
    """Hakee ostajien vastaukset mittareita varten."""
    conn = sqlite3.connect(DB_NAME)
    try:
        df = pd.read_sql_query("SELECT * FROM buyer_responses WHERE property_id = ?", conn, params=(property_id,))
    except Exception:
        df = pd.DataFrame()
    conn.close()
    return df

def save_buyer_response(property_id, data):
    """Tallentaa ostajan antaman vastauksen tietokantaan."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO buyer_responses (property_id, data)
        VALUES (?, ?)
    """, (property_id, str(data)))
    conn.commit()
    conn.close()

def create_invite(email, full_name, company, role="LKV", credits=10):
    """Luo uuden token-pohjaisen kutsulinkin välittäjälle tai pomolle."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    token = uuid.uuid4().hex
    cursor.execute("""
        INSERT INTO invites (token, email, full_name, company, role, credits, status)
        VALUES (?, ?, ?, ?, ?, ?, 'Pending')
    """, (token, email, full_name, company, role, credits))
    conn.commit()
    conn.close()
    return token

def get_recent_invites():
    """Hakee viimeisimmät kutsut Master Dashboardia tai hallintaa varten."""
    conn = sqlite3.connect(DB_NAME)
    try:
        df = pd.read_sql_query("SELECT * FROM invites ORDER BY created_at DESC LIMIT 10", conn)
    except Exception:
        df = pd.DataFrame()
    conn.close()
    return df
