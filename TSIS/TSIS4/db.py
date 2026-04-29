# db.py - database functions for leaderboard

import psycopg2
import psycopg2.extras
from config import DB

def get_conn():
    return psycopg2.connect(**DB)

# create tables if not exist
def init_db():
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id       SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL
        );
        CREATE TABLE IF NOT EXISTS game_sessions (
            id            SERIAL PRIMARY KEY,
            player_id     INTEGER REFERENCES players(id),
            score         INTEGER NOT NULL,
            level_reached INTEGER NOT NULL,
            played_at     TIMESTAMP DEFAULT NOW()
        );
    """)
    conn.commit()
    conn.close()

# get player id, create if not exists
def get_or_create_player(username):
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute("SELECT id FROM players WHERE username = %s", (username,))
    row = cur.fetchone()
    if row:
        conn.close()
        return row[0]
    cur.execute("INSERT INTO players(username) VALUES(%s) RETURNING id", (username,))
    pid = cur.fetchone()[0]
    conn.commit()
    conn.close()
    return pid

# save one game result
def save_session(username, score, level):
    pid  = get_or_create_player(username)
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute(
        "INSERT INTO game_sessions(player_id, score, level_reached) VALUES(%s,%s,%s)",
        (pid, score, level)
    )
    conn.commit()
    conn.close()

# get top 10 scores sorted by score
def get_top10():
    conn = get_conn()
    cur  = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT p.username, gs.score, gs.level_reached,
               TO_CHAR(gs.played_at, 'YYYY-MM-DD') AS date
        FROM game_sessions gs
        JOIN players p ON p.id = gs.player_id
        ORDER BY gs.score DESC
        LIMIT 10
    """)
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

# get personal best score for one player
def get_best(username):
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute("""
        SELECT COALESCE(MAX(gs.score), 0)
        FROM game_sessions gs
        JOIN players p ON p.id = gs.player_id
        WHERE p.username = %s
    """, (username,))
    val = cur.fetchone()[0]
    conn.close()
    return val