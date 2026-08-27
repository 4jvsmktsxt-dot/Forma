import sqlite3
import pandas as pd
from datetime import datetime

DB_NAME = "forma_master.db"

def init_db():
    """Alustaa tietokannan ja luo tarvittavat taulut, jos niitä ei vielä ole."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # 1. Kohteet-taulu (Properties)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS properties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            address TEXT NOT NULL,
            property_type TEXT,
            asking_price REAL,
            status TEXT DEFAULT 'Aktiivinen',
            created_at TEXT
        )
    """)

    # 2. Ostajien mikrokyselyt -taulu (Buyer Intake - Live Data)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS buyer_intake (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            property_id INTEGER,
            timeline_score INTEGER,
            financing_status TEXT,
            renovation_readiness INTEGER,
            main_concern TEXT,
            created_at TEXT,
            FOREIGN KEY (property_id) REFERENCES properties (id)
        )
    """)

    # 3. Anonymisoitu metadata-arkisto (Master Dashboard & Bisneksen kehitys)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS market_metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            property_id INTEGER,
            avg_timeline_score REAL,
            avg_renovation_score REAL,
            conversion_rate REAL,
            archived_at TEXT
        )
    """)

    conn.commit()
    conn.close()

def add_property(address, property_type, asking_price):
    """Lisää uuden kohteen tietokantaan."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO properties (address, property_type, asking_price, created_at)
        VALUES (?, ?, ?, ?)
    """, (address, property_type, asking_price, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def get_properties():
    """Hakee kaikki kohteet."""
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM properties", conn)
    conn.close()
    return df

def save_buyer_response(property_id, timeline_score, financing_status, renovation_readiness, main_concern):
    """Tallentaa ostajan mikrokyselyn vastaukset (liukusäätimet & monivalinnat)."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO buyer_intake (property_id, timeline_score, financing_status, renovation_readiness, main_concern, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (property_id, timeline_score, financing_status, renovation_readiness, main_concern, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def get_buyer_responses(property_id):
    """Hakee tietyn kohteen ostajavastaukset LKV:n tai remonttimyyjän näkymään."""
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM buyer_intake WHERE property_id = ?", conn, params=(property_id,))
    conn.close()
    return df

if __name__ == "__main__":
    init_db()
    print("Tietokanta forma_master.db alustettu onnistuneesti!")
