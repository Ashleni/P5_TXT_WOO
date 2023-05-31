from flask import Flask, request
from tools import b64

# importing blueprints
from routes.home import home_bp

app = Flask(__name__, static_url_path = '/static')

# registering blueprints
app.register_blueprint(home_bp)

app.secret_key = b64.base64_encode("secret key in b64 lol")