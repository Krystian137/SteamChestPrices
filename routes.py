from flask import Blueprint, render_template
import json
from prices_data import cases

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('chest.html', cases=cases)