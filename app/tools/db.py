#TXT peeps

import sqlite3
DB_FILE="database.db"
db = sqlite3.connect(DB_FILE)

def wipeDB():
    db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
    c = db.cursor()
    c.execute("DROP TABLE if exists authentication")

def userExists(username):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS authentication (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT NOT NULL, spaces INTEGER);")
    results = c.execute("SELECT username, password FROM authentication WHERE username = ?", (username,)).fetchall()
    db.close()
    if len(results) > 0:
        return True
    else:
        return False

def addUser(username, password):
    if userExists(username):
        return "be more original"
    else:
        db = sqlite3.connect(DB_FILE, check_same_thread=False)
        c = db.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS authentication (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT NOT NULL, spaces INTEGER);")
        c.execute("INSERT INTO authentication VALUES(?, ?, ?, ?)", (None, username, password, 0))
        db.commit()
        db.close()
        return "success"

wipeDB()
print(addUser('bob','123'))
print(addUser('bob','123'))
print(addUser('bb3','123'))
