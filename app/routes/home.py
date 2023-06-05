import sys
sys.path.append("..")

from flask import Blueprint, render_template, request, session

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    
    if "username" in session:
        return render_template("index.html")
