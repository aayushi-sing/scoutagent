import sqlite3, json
from datetime import datetime

DB_PATH = "scout_history.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            topic     TEXT,
            startups  TEXT,
            scores    TEXT,
            report    TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_run(topic, startups, scores, report):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO runs (timestamp, topic, startups, scores, report) VALUES (?,?,?,?,?)",
        (datetime.now().strftime("%Y-%m-%d %H:%M"), topic,
         json.dumps(startups), json.dumps(scores), report)
    )
    conn.commit()
    conn.close()

def get_history(limit=15):
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT id, timestamp, topic, startups, scores FROM runs ORDER BY id DESC LIMIT ?",
        (limit,)
    ).fetchall()
    conn.close()
    return [{"id":r[0],"timestamp":r[1],"topic":r[2],
             "startups":json.loads(r[3] or "[]"),
             "scores":json.loads(r[4] or "{}")} for r in rows]

def get_report_by_id(run_id):
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute("SELECT report FROM runs WHERE id=?", (run_id,)).fetchone()
    conn.close()
    return row[0] if row else ""