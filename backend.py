
import sqlite3
import hashlib


def validate_url(url):
    return url.startswith('https://www.youtube.com/watch?v=') or \
           url.startswith('https://youtu.be/')


def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS videos
                 (username TEXT, url TEXT)''')
    conn.commit()
    conn.close()


def sha256(input):
    hash = hashlib.sha256()
    hash.update(bytes(input, 'utf-8'))
    return hash.hexdigest()


def add_user(username, password):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO users VALUES (?, ?)", (username, sha256(password)))
    conn.commit()
    conn.close()


def user_exists(username):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username, ))
    user = c.fetchone()
    conn.close()
    return user


def check_login(username, password):
    pw_hash = sha256(password)
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, pw_hash))
    user = c.fetchone()
    conn.close()
    return user and user[1] == pw_hash


def add_video(username, url):
    video_id = url.split('v=')[-1]
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO videos VALUES (?, ?)", (username, video_id))
    conn.commit()
    conn.close()


def get_videos(username):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT url FROM videos WHERE username = ?", (username, ))
    videos = c.fetchall()
    conn.close()
    return [video[0] for video in videos]

