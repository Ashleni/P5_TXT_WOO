from flask import Flask, render_template, session, request, redirect 
from tools import b64

# importing blueprints
# from routes.home import home_bp

app = Flask(__name__)#ls, static_url_path = '/static')

# registering blueprints
# app.register_blueprint(home_bp)

app.secret_key = b64.base64_encode("secret key in b64 lol")

@app.route('/')
def home_page():
    return render_template('login.html')

@app.route('/register')
def home_page():
    return render_template('register.html')

@app.route('/homepage')
def home_page():
    return render_template('homepage.html')

@app.route('/leaderboard')
def home_page():
    return render_template('leaderboard.html')

@app.route('/games')
def home_page():
    return render_template('games.html')

if __name__ == '__main__':
	app.debug = True
	app.run()