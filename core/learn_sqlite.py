# core/learn_sqlite.py
# 🦉 SleepingOwl SQL Layer — 儲存語義分數與學習修正

import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path("homophone_space.db")

# core/learn_sqlite.py
import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path("homophone_space.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
    CREATE TABLE IF NOT EXISTS words (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        word TEXT UNIQUE,
        bopomofo TEXT
    );

    CREATE TABLE IF NOT EXISTS homophones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bopomofo TEXT UNIQUE
    );

    CREATE TABLE IF NOT EXISTS pairs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        word_a TEXT,
        word_b TEXT,
        score REAL,
        bopomofo TEXT,
        UNIQUE(word_a, word_b)
    );

    CREATE TABLE IF NOT EXISTS adjustments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        word_a TEXT,
        word_b TEXT,
        delta REAL DEFAULT 0,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.commit()
    conn.close()
    print(f"✅ Database initialized at {DB_PATH}")

def import_homophones(csv_path):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_csv(csv_path)

    total = 0
    for _, row in df.iterrows():
        bopomofo = row["bopomofo"]
        w1, w2 = row["word1"], row["word2"]
        s1, s2 = float(row["cosine_true"]), float(row["cosine_model"])

        conn.execute("INSERT OR IGNORE INTO homophones (bopomofo) VALUES (?)", (bopomofo,))
        conn.execute("INSERT OR IGNORE INTO words (word, bopomofo) VALUES (?, ?)", (w1, bopomofo))
        conn.execute("INSERT OR IGNORE INTO words (word, bopomofo) VALUES (?, ?)", (w2, bopomofo))

        conn.execute(
            "INSERT OR REPLACE INTO pairs (word_a, word_b, score, bopomofo) VALUES (?, ?, ?, ?)",
            (w1, w2, (s1 + s2) / 2, bopomofo)
        )
        total += 1

    conn.commit()
    conn.close()
    print(f"✅ Imported {total} homophone pairs from {csv_path}")

