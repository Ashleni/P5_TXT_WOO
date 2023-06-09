#TXT peeps

import sqlite3
import random
import requests
import json

DB_FILE="database.db"
db = sqlite3.connect(DB_FILE)
code = "000000000000"

def wipe_db():
    db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
    c = db.cursor()
    c.execute("DROP TABLE if exists authentication")

def creationist(): #wipe then create the leaderboard
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("DROP TABLE if exists leaderB")
    c.execute("CREATE TABLE IF NOT EXISTS leaderB (id TEXT, owner TEXT NOT NULL, connections INTEGER, answer INTEGER, points INTEGE, imagery TEXT)")
    db.commit()
    db.close()

def four_by_four(): 
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    res = requests.get("https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1")
    response = json.loads(res.text)
    if (response['success']):
        code = response['deck_id']
    else:
        print ("error")
    coordinates = [0,0,0,0] # top, down, left, right
    availability = ["C", "A", "C", "A"] 
    for i in range(16):
        if coordinates[3] == 1:
            availability[2] = "A" # make left available when right first increments 
        if coordinates[3] == 3:
            availability[3] = "C" # make right unavailable when right-most

        if (coordinates[3] > 3):
            coordinates[3] = 0 # reset right coordinates
            availability[2] = "C" # make left unavailable when left-most 
            availability[3] = "A" # make right available when left-most 
            coordinates[1] += 1 # increment down coordinates
            if coordinates[1] == 1:
                availability[0] = "A" # make top available when down first increments 
            if coordinates[1] == 3:
                availability[1] = "C" # make down unavailable when downmost
        id = f"{availability[0]}{coordinates[0]} {availability[1]}{coordinates[1]} {availability[2]}{coordinates[2]} {availability[3]}{coordinates[3]}"
        rand = random.randint(1,52)
        # print (id)
        res_1 = requests.get(f'https://deckofcardsapi.com/api/deck/{code}/draw/?count=1')
        response_1 = json.loads(res_1.text)
        if (response_1['success']):
            cards = response_1['cards'][0]
            rand = cards['value'] + ' of ' + cards['suit']
            image = cards['image']
            reloaded = requests.get(f'https://deckofcardsapi.com/api/deck/{code}/return/')
        else:
            rand = 'government subsidized'
        c.execute("INSERT into leaderB VALUES(?,?,?,?,?,?)", (id, "Proletariat", 16, rand, 100, image))
        results = c.execute("SELECT id from leaderB").fetchall()
        # print(results)
        coordinates[3] += 1 # increment right 
    db.commit()
    db.close()

def creationism(): # wipeout and make a clean 4 by 4 grid of unclaimed nodes
    creationist()
    four_by_four()
    print("success!!")

def government_drone(): # return all node ids
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    results = c.execute("SELECT id from leaderB").fetchall()  
    db.close();  
    return results

def alien_spaceship(arr):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    results = c.execute("SELECT * from leaderB WHERE id = ?", (arr,)).fetchall()    
    db.close()
    return results

def update_owner(id, newOwner, column): # column needs to be set as "owner"
    try:
        db = sqlite3.connect(DB_FILE, check_same_thread=False)
        c = db.cursor()
        if (column == "owner"):
            results_0 = e.execute("SELECT connections from leaderB WHERE owner = ?", (newOwner,)).fetchall() # select new owner connections
            print ("object: " + results_0)
            if results_0[0] == '':
                results_0 = [0]
            results = e.execute("SELECT owner, connections from leaderB WHERE id = ?", (id,)).fetchall() # select old owner connections
            # print(results)
            loser = results[1] - 1
            winner = results_0[0] + 1
            c.execute("UPDATE leaderB SET owner = ? WHERE id = ?", (newOwner, id,)) # update node to new owner 
            c.execute("UPDATE leaderB set connections = ? WHERE owner = ?", (loser, results[0],)) # update connections on old owner
            c.execute("UPDATE leaderB set connections = ? WHERE owner = ?", (winner, newOwner,)) # update connections on new owner
        db.commit()
        db.close()
    except:
        print("error!")

def user_exists(username):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS authentication (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT NOT NULL, spaces INTEGER, token INTEGER)")
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
        c.execute("CREATE TABLE IF NOT EXISTS authentication (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT NOT NULL, spaces INTEGER, token INTEGER)")
        c.execute("INSERT INTO authentication VALUES(?, ?, ?, ?, ?)", (None, username, password, 0, 0,))
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

def add_tokens(username, amount):
    user_spaces=get_user_spaces(username)
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("UPDATE authentication SET token = token + ? WHERE username = ?", (amount, username))
    db.commit()
    db.close()
    return True

def get_tokens(username):
    user_spaces=get_user_spaces(username)
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    results = c.execute("SELECT token from authentication WHERE username = ?", (amount, username)).fetchall()
    db.commit()
    db.close()
    return results

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
creationism()
government_drone()