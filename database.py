import sqlite3
import hashlib
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('codequest.db')
        self.create_tables()
        
    def create_tables(self):
        cursor = self.conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            level INTEGER,
            score INTEGER,
            time_taken REAL,
            completed_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')
        
        self.conn.commit()
        
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, username, password):
        try:
            cursor = self.conn.cursor()
            hashed_password = self.hash_password(password)
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                         (username, hashed_password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
            
    def login_user(self, username, password):
        cursor = self.conn.cursor()
        hashed_password = self.hash_password(password)
        cursor.execute('SELECT id FROM users WHERE username = ? AND password = ?',
                      (username, hashed_password))
        result = cursor.fetchone()
        return result[0] if result else None
        
    def save_score(self, user_id, level, score, time_taken):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO scores (user_id, level, score, time_taken, completed_at)
        VALUES (?, ?, ?, ?, ?)
        ''', (user_id, level, score, time_taken, datetime.now()))
        self.conn.commit()
        
    def get_user_scores(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT level, score, time_taken FROM scores
        WHERE user_id = ? ORDER BY level
        ''', (user_id,))
        return cursor.fetchall()
