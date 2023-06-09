from flask import Flask, render_template, session, request, redirect
from tools import b64
from tools import db
from random import randrange, choice
import json
import os

# importing blueprints
# from routes.home import home_bp

app = Flask(__name__)#ls, static_url_path = '/static')

# registering blueprints
# app.register_blueprint(home_bp)

app.secret_key = b64.base64_encode("secret key in b64 lol")

@app.route('/', methods=['GET'])
def home_page():
    if 'username' in session:
        return redirect('/home')
    else:
        return render_template('login.html')

@app.route("/login", methods=['GET', 'POST'])
def authenticate():
    if (request.method == "POST"):
        if(db.login_user(request.form['username'], request.form['password'])):
            session['username'] = request.form.get('username')
            session['password'] = request.form.get('password')
            return redirect('/home')
        else:
            return render_template('login.html', exception = "Wrong username or password")
    else:
        if 'username' in session:
            return redirect("/home")
        else:
            return render_template('login.html')

@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template('home.html',user=session['username'],score=db.get_user_spaces(session['username']))

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/leaderboard')
def leaderboard():
    results = db.government_drone()
    print(results)
    return render_template('leaderboard.html', results = results)

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

@app.route('/cards')
def cards():
    for root, dirs, files in os.walk("./static/assets/"):
        for name in files:
            print(os.path.join(root, name))
    return render_template('cards.html', image = choice(["image_3Gc6ulsB_1686153675740_raw.jpg", "image_m7cPFtd3_1686153472054_raw.jpg", "image_vU4XFDUJ_1686153544980_raw.jpg"]))

@app.route('/guess',methods=['GET', 'POST'])
def guess():
    if request.method == 'GET':
        if 'id' in request.args:
            print ('Recieved node id! ' + request.args['id'])
            session['node_in_play'] = request.args['id']
        else:
            return redirect('/leaderboard')
    if 'username' not in session:
        return redirect('/login')
    if 'guess_number' in session and 'guess_attempts' in session:
        #If form is being used
        if request.method == 'POST':
            print(session['guess_number'])
            try:
                user_number = int(request.form['user_number'])
            except:
                return render_template('guess.html', right_or_wrong='Please Use a NUMBER!!!!', factory = session['node_in_play'])

            if (user_number == session['guess_number']):
                #If user guesses correct number
                session['guess_attempts']=0
                session['guess_number']=randrange(10)
                db.add_space(session['username'])
                db.add_tokens(session['username'], 1)
                results = db.get_tokens(session['username'])
                print("POINT ON ATTENTION: " + results)
                return render_template('guess.html', right_or_wrong='Coolio you guessed right!', factory = session['node_in_play'])
            else:
                session['guess_attempts']+=1
                message='You have '  + str(5-session['guess_attempts']) + ' attempts remaining'
                #If user runs out of attempts
                if (session['guess_attempts']>=5):
                    session['guess_number']=randrange(10)
                    session['guess_attempts']=0
                    return render_template('guess.html', right_or_wrong='Number Reset', factory = session['node_in_play'])
                return render_template('guess.html', right_or_wrong='Not Coolio you guessed wrong!', attempts_message=message, factory = session['node_in_play'])
    else:
        session['guess_number']=randrange(10)
        session['guess_attempts']=0
    return render_template('guess.html', factory = session['node_in_play'])

if __name__ == '__main__':
	app.debug = True
	app.run()
