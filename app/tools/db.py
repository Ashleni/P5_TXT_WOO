#TXT peeps

import sqlite3
DB_FILE="database.db"
db = sqlite3.connect(DB_FILE)

def wipe_db():
    db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
    c = db.cursor()
    c.execute("DROP TABLE if exists authentication")

def user_exists(username):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS authentication (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT NOT NULL, spaces INTEGER)")
    results = c.execute("SELECT username FROM authentication WHERE username = ?", (username,)).fetchall()
    db.close()
    if len(results) > 0:
        return True
    else:
        return False

def add_user(username, password):
    if user_exists(username):
        return "be more original"
    else:
        db = sqlite3.connect(DB_FILE, check_same_thread=False)
        c = db.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS authentication (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT NOT NULL, spaces INTEGER)")
        c.execute("INSERT INTO authentication VALUES(?, ?, ?, ?)", (None, username, password, 0))
        db.commit()
        db.close()
        return "success"

def login_user(username, password):
    if user_exists(username):
        db = sqlite3.connect(DB_FILE, check_same_thread=False)
        c = db.cursor()
        results = c.execute("SELECT password FROM authentication WHERE username = ?", (username,)).fetchall()
        db.close()
        return password == results[0][0]
    return False

def get_user_spaces(username):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    results = c.execute("SELECT spaces FROM authentication WHERE username = ?", (username,)).fetchall()
    return results[0][0]

def add_space(username):
    user_spaces=get_user_spaces(username)
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("UPDATE authentication SET spaces = ? WHERE username = ?", (user_spaces+1, username))
    db.commit()
    db.close()
    return True

def remove_space(username):
    user_spaces=get_user_spaces(username)
    if (user_spaces<=0):
        return False
    else:
        db = sqlite3.connect(DB_FILE, check_same_thread=False)
        c = db.cursor()
        c.execute("UPDATE authentication SET spaces = ? WHERE username = ?", (user_spaces-1, username))
        db.commit()
        db.close()
        return True

def top_spaces():
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    results = c.execute("SELECT username, spaces FROM authentication ORDER BY spaces DESC").fetchall()
    return results

wipe_db()
print(add_user('billybob','billybobrules'))
print(login_user('billybob','billybobrules'))
print(get_user_spaces('billybob'))
add_space('billybob')
print(add_user('billybob2','billybobrules'))
print(add_user('billybob3','billybobrules'))
add_space('billybob3')
add_space('billybob3')

print(top_spaces())
