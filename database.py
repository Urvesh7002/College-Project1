import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    
    # टेबल्स बनाएँ
    c.execute('''CREATE TABLE IF NOT EXISTS students (
                 student_id TEXT PRIMARY KEY,
                 name TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS attendance (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 student_id TEXT,
                 date TEXT,
                 status TEXT,
                 timestamp TEXT)''')
    
    # टेस्ट डेटा डालें
    try:
        c.execute("INSERT INTO students VALUES ('STU001', 'राहुल शर्मा')")
    except:
        pass
    
    conn.commit()
    conn.close()

def mark_attendance(student_id, status):
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    c.execute('''INSERT INTO attendance (student_id, date, status, timestamp)
                 VALUES (?, ?, ?, ?)''', 
              (student_id, today, status, timestamp))
    
    conn.commit()
    conn.close()