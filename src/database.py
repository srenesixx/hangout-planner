import sqlite3
import json
from src.config import DB_FILE

def get_connection():
    """Returns a connection to the SQLite database with foreign keys enabled."""
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON;")
    # Return dictionary-like rows for easier access
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database schema if it doesn't already exist."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # 1. users
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        nama            TEXT NOT NULL,
        username        TEXT NOT NULL UNIQUE,
        email           TEXT UNIQUE,
        password_hash   TEXT NOT NULL,
        saldo           INTEGER NOT NULL DEFAULT 0,
        created_at      TEXT DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    # 2. plans
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS plans (
        id                  INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id             INTEGER NOT NULL,
        nama_rencana        TEXT,
        tanggal             TEXT NOT NULL,
        jumlah_teman        INTEGER NOT NULL DEFAULT 0,
        budget              INTEGER NOT NULL,
        transportasi        TEXT,
        transport_cost      INTEGER DEFAULT 0,
        mood                TEXT DEFAULT '😐',
        mood_efek_persen    REAL DEFAULT 0,
        status              TEXT DEFAULT 'draft',
        created_at          TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)
    
    # 3. plan_locations
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS plan_locations (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        plan_id      INTEGER NOT NULL,
        nama_tempat  TEXT NOT NULL,
        kategori     TEXT,
        urutan       INTEGER DEFAULT 0,
        FOREIGN KEY (plan_id) REFERENCES plans(id) ON DELETE CASCADE
    );
    """)
    
    # 4. plan_items
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS plan_items (
        id             INTEGER PRIMARY KEY AUTOINCREMENT,
        location_id    INTEGER NOT NULL,
        nama_item      TEXT NOT NULL,
        harga_satuan   INTEGER NOT NULL,
        jumlah         INTEGER NOT NULL DEFAULT 1,
        FOREIGN KEY (location_id) REFERENCES plan_locations(id) ON DELETE CASCADE
    );
    """)
    
    # 5. split_bills
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS split_bills (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        plan_id         INTEGER NOT NULL UNIQUE,
        total_tagihan   INTEGER NOT NULL,
        jumlah_orang    INTEGER NOT NULL,
        per_orang       INTEGER NOT NULL,
        created_at      TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (plan_id) REFERENCES plans(id) ON DELETE CASCADE
    );
    """)
    
    # 6. mood_logs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mood_logs (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        plan_id       INTEGER NOT NULL,
        mood          TEXT NOT NULL,
        efek_persen   REAL NOT NULL,
        catatan       TEXT,
        created_at    TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (plan_id) REFERENCES plans(id) ON DELETE CASCADE
    );
    """)
    
    # 7. budget_health_scores
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS budget_health_scores (
        id               INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id          INTEGER NOT NULL,
        periode          TEXT NOT NULL,
        score            INTEGER NOT NULL,
        breakdown_json   TEXT,
        created_at       TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)
    
    # Create indexes for performance
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_plans_user_id ON plans(user_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_plan_locations_plan_id ON plan_locations(plan_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_plan_items_location_id ON plan_items(location_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_mood_logs_plan_id ON mood_logs(plan_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_health_scores_user_periode ON budget_health_scores(user_id, periode);")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully at:", DB_FILE)
