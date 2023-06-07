from flask import Flask, render_template, session, request, redirect
from tools import b64
from tools import db
from random import randrange
import json


app = Flask(__name__)
app.secret_key = b64.base64_encode("secret key in b64 lol")


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

@app.route('/info/<id>', methods = ['GET', 'POST'])
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

@app.route('/games')
def games():
    return render_template('games.html')

@app.route('/guess',methods=['GET', 'POST'])
def guess():
    if 'guess_number' in session and 'guess_attempts' in session:
        #If form is being used
        if request.method == 'POST':
            print(session['guess_number'])
            try:
                user_number = int(request.form['user_number'])
            except:
                return render_template('guess.html', right_or_wrong='Please Use a NUMBER!!!!')

            if (user_number == session['guess_number']):
                #If user guesses correct number
                session['guess_attempts']=0
                session['guess_number']=randrange(10)
                db.add_space(session['username'])
                return render_template('guess.html', right_or_wrong='Coolio you guessed right!')
            else:
                session['guess_attempts']+=1
                message='You have '  + str(5-session['guess_attempts']) + ' attempts remaining'
                #If user runs out of attempts
                if (session['guess_attempts']>=5):
                    session['guess_number']=randrange(10)
                    session['guess_attempts']=0
                    return render_template('guess.html', right_or_wrong='Number Reset. The number was ' + str(session['guess_number']) + '!')
                return render_template('guess.html', right_or_wrong='Not Coolio you guessed wrong!', attempts_message=message)
    else:
        session['guess_number']=randrange(10)
        session['guess_attempts']=0
    return render_template('guess.html')
    
@app.route('/card')

if __name__ == '__main__':
	app.debug = True
	app.run()
