#from flask import Flask             #facilitate flask webserving
#from flask import render_template   #facilitate jinja templating
import requests           #facilitate form submission
from pprint import pprint

# app = Flask(__name__)    #create Flask object


def randcard():
    link = 'https://deckofcardsapi.com/api/deck/new/draw/?count=1'
    r = requests.get(link)
    info = r.json()
    card_id = info['cards'][0]['code']
    return card_id

    
def card_png(card_id):
    return "https://deckofcardsapi.com/static/img/"+str(card_id)+".png"
    
def card_svg(card_id):
    return "https://deckofcardsapi.com/static/img/"+str(card_id)+".svg"
