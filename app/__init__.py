from flask import Flask, render_template, session, request, redirect 
from tools import b64

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
        session['username'] = request.form.get('username')
        session['password'] - request.form.get('password')
        if(user_exists(request.form['username'], request.form['password'])):
            return redirect('/home_page')
        else:
            return render_template('login.html', exception = "Wrong username or password")
    else:
        if(session != {}):
            return redirect("/home")
        else:
            return render_template('login.html')
    
    
@app.route('/register')
def register():
    return render_template('register.html')

#@app.route('/homepage')
#def homepage():
#    return render_template('homepage.html')

@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')

@app.route('/games')
def games():
    return render_template('games.html')

if __name__ == '__main__':
	app.debug = True
	app.run()