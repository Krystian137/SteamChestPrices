from flask import Blueprint, render_template
import json
from prices_data import cases, get_latest_price_from_file

main = Blueprint('main', __name__)

@main.route('/')
def home():
    for chest_name, chest_info in cases.items():
        case_code = chest_info["code"]
        latest_price = get_latest_price_from_file(case_code)
        if latest_price is not None:
            chest_info['latest_price'] = f"{latest_price:.2f} zł"
        else:
            chest_info['latest_price'] = "Brak danych"
    return render_template('home.html', cases=cases)

