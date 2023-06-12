from flask import Flask, render_template, session, request, redirect
from tools import b64
from tools import db
from random import randrange, choice
import json
import requests
import os


app = Flask(__name__)
app.secret_key = b64.base64_encode("secret key in b64 lol")

secret = 'lgb1ns28jzza'

@app.route('/', methods=['GET'])
def home_page():
    if 'username' in session:
        return redirect('/home')
    else:
        return render_template('login.html')

@app.route("/login", methods=['GET','POST'])
def authenticate():
    if 'username' in session:
        return redirect('/')
    if(db.login_user(request.form['username'], request.form['password'])):
        session['username'] = request.form.get('username')
        session['password'] = request.form.get('password')
        return redirect('/')
    else:
        return render_template('login.html', exception = "Wrong username or password")

@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template('home.html',user=session['username'], score=db.get_user_spaces(session['username']))

@app.route('/register', methods=['GET','POST'])
def register():
    if (request.method == 'POST'):
        if (request.form['password1'] == request.form['password2']):
            if db.user_exists(request.form['username']):
                return render_template('register.html', exception = "Username already exists")
            db.add_user(request.form['username'], request.form['password1'])
            return redirect('/')
        else:
            return render_template('register.html', exception = "Passwords do not match")
    return render_template('register.html')

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect('/')

@app.route('/leaderboard')
def leaderboard():
    results = db.government_drone()
    print(results)
    return render_template('leaderboard.html', results = results, user = session['username'])

@app.route('/leaderboard_setup', methods = ['GET', 'POST'])
def leaderboard_setup():
    if request.method == 'GET':
        results = db.government_drone()
        clean_res = []
        for result in results:
            clean_res.append(result[0])
        return json.dumps(clean_res)
    else:
        return '400'

@app.route('/info/<id>', methods = ['GET', 'POST']) # Get information on a node specified by id, called via fetch in leaderBoard.js
def info(id):
    if request.method == 'GET':
        results = db.alien_spaceship(id)
        print (results)
        clean_res = []
        for result in results[0]:
            clean_res.append(result)
        return json.dumps(clean_res)
    else:
        return '400'

@app.route('/upload_tokens/<amount>', methods = ['GET', 'POST']) # Get information on a node specified by id, called via fetch in leaderBoard.js
def upload_tokens(amount):
    if request.method == 'GET':
        db.add_tokens(session['username'], amount)
        results = db.get_tokens(session['username'])
        clean_res = results[0][0]
        return json.dumps(clean_res)
    else:
        return '400'

@app.route('/games')
def games():
    return render_template('games.html')

@app.route('/cards', methods=['GET', 'POST'])
def cards():
    if request.method == 'POST':
        if 'click' in request.form:
            print ("AAAA")
            number = db.get_tokens(session['username'])
            print(number)
            if number > 0:
                db.add_tokens(session['username'], -1)
                print("BBB")
                res = requests.get(f'https://deckofcardsapi.com/api/deck/{secret}/draw/?count=1')
                response = json.loads(res.text)
                print(response)
                cards = response['cards'][0]
                rand = cards['value'] + ' of ' + cards['suit']
                image = cards['image']
                res = requests.get(f'https://deckofcardsapi.com/api/deck/{secret}/return/')
                if rand == session['answer_in_question']: #rand == session['answer_in_question']
                    print("engage: " + session['node_in_play'])
                    db.update_owner(session['node_in_play'], session['username'], "owner")
                    return render_template('cards.html', image = image, text = "What have you done?", coconuts = db.get_tokens(session['username'])) 
                else:
                    return render_template('cards.html', image = image, text = "What are you doing?", coconuts = db.get_tokens(session['username'])) 
            else:
                return render_template('cards.html', image = choice(["image_3Gc6ulsB_1686153675740_raw.jpg", "image_m7cPFtd3_1686153472054_raw.jpg", "image_vU4XFDUJ_1686153544980_raw.jpg"]), text = "You have no more souls to give.", coconuts = db.get_tokens(session['username']))
    return render_template('cards.html', image = choice(["image_3Gc6ulsB_1686153675740_raw.jpg", "image_m7cPFtd3_1686153472054_raw.jpg", "image_vU4XFDUJ_1686153544980_raw.jpg"]), text = "Dost one play?", coconuts = db.get_tokens(session['username']))

@app.route('/Samantha',methods=['GET', 'POST'])
def Samantha():
    if request.method == 'GET':
        if 'id' in request.args:
            print ('Recieved node id! ' + request.args['id'])
            session['node_in_play'] = request.args['id']
            session['answer_in_question'] = request.args['answy']
        else:
            return redirect('/leaderboard')
        if 'choice1' in request.args:
            return redirect('/guess')
        elif 'choice2' in request.args:
            return redirect('/snake_realness')

@app.route('/guess',methods=['GET', 'POST'])
def guess():
    if 'username' not in session:
        return redirect('/login')
    if 'guess_number' in session and 'guess_attempts' in session:
        #If form is being used
        if request.method == 'POST':
            print(session['guess_number'])
            try:
                user_number = int(request.form['user_number'])
            except:
                return render_template('guess.html', right_or_wrong='Please Use a NUMBER!!!!', factory = session['node_in_play'], fakeness = False)

            if (user_number == session['guess_number']):
                #If user guesses correct number
                session['guess_attempts']=0
                session['guess_number']=randrange(10)
                db.add_space(session['username'])
                db.add_tokens(session['username'], 1)
                results = db.get_tokens(session['username'])
                return render_template('guess.html', right_or_wrong='Coolio you guessed right!', factory = session['node_in_play'], fakeness = False)
            else:
                session['guess_attempts']+=1
                message='You have '  + str(5-session['guess_attempts']) + ' attempts remaining'
                #If user runs out of attempts
                if (session['guess_attempts']>=5):
                    session['guess_number']=randrange(10)
                    session['guess_attempts']=0
                    return render_template('guess.html', right_or_wrong='Number Reset. The number was ' + str(session['guess_number']) + '!', factory = session['node_in_play'], fakeness = False)
                return render_template('guess.html', right_or_wrong='Not Coolio you guessed wrong!', attempts_message=message, factory = session['node_in_play'], fakeness = False)
    else:
        session['guess_number']=randrange(10)
        session['guess_attempts']=0
    return render_template('guess.html', factory = session['node_in_play'], fakeness = False)

@app.route('/guess_fake',methods=['GET', 'POST'])
def guess_fake():
    if 'username' not in session:
        return redirect('/login')
    if 'guess_number' in session and 'guess_attempts' in session:
        #If form is being used
        if request.method == 'POST':
            print(session['guess_number'])
            try:
                user_number = int(request.form['user_number'])
            except:
                return render_template('guess.html', right_or_wrong='Please Use a NUMBER!!!!', factory = '', fakeness = True)

            if (user_number == session['guess_number']):
                #If user guesses correct number
                session['guess_attempts']=0
                session['guess_number']=randrange(10)
                db.add_space(session['username'])
                return render_template('guess.html', right_or_wrong='Coolio you guessed right!', factory = '', fakeness = True)
            else:
                session['guess_attempts']+=1
                message='You have '  + str(5-session['guess_attempts']) + ' attempts remaining'
                #If user runs out of attempts
                if (session['guess_attempts']>=5):
                    session['guess_number']=randrange(10)
                    session['guess_attempts']=0
                    return render_template('guess.html', right_or_wrong='Number Reset. The number was ' + str(session['guess_number']) + '!', factory = '', fakeness = True)
                return render_template('guess.html', right_or_wrong='Not Coolio you guessed wrong!', attempts_message=message, factory = '', fakeness = True)
    else:
        session['guess_number']=randrange(10)
        session['guess_attempts']=0
    return render_template('guess.html', fakeness = True)

@app.route('/snake',methods=['GET', 'POST'])
def snake():
    message=''
    score1 = 0
    if request.method == 'POST':
        print(request.form['snakeScore'])
        score=request.form['snakeScore']
        db.add_spaces(session['username'],int(score))
        message="You get this score: " + score
        score1 = int(score)
    return render_template('snake.html',score_Message=message, fakeness = True, score = score1)

@app.route('/snake_realness',methods=['GET', 'POST'])
def snake_realness():
    message=''
    score1 = 0
    if request.method == 'POST':
        print(request.form['snakeScore'])
        score=request.form['snakeScore']
        db.add_spaces(session['username'],int(score))
        message=f"You have gathered {score} souls!"
        db.add_tokens(session['username'], score)
        score1 = int(score)
    return render_template('snake.html',score_Message=message, fakeness = False, score = score1)

@app.route('/get_cards', methods=['GET', 'POST'])
def get_cards():
    res = requests.get('https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1')
    response = json.loads(res.text)
    print(res.text)
    return('te')

@app.route('slapjack', methods=['GET', 'POST'])
def slapjack():
    new_deck = requests.get('https://deckofcardsapi.com/api/deck/new/')
    temp_dict = json.loads(new_deck.text)
    deck_id = temp_dict['deck_id']
    draw_a_card = requests.get(f'https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count=1')
    return('')

if __name__ == '__main__':
	app.debug = True
	app.run()
