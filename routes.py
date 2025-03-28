from flask import Blueprint, render_template
import json
from prices_data import cases, get_latest_price_from_file
from flask import jsonify

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


@main.route("/chest_info/<string:case_code>")
def chest_info(case_code):
    chest_info = cases.get(case_code)
    return render_template('chest_info.html', chest_info=chest_info, case_code=case_code)


@main.route("/get_price_history/<case_code>")
def get_price_history(case_code):
    try:
        with open("prices.json", "r") as f:
            data = json.load(f)

        # Znajdź kod odpowiadający case_code
        for chest_name, chest_info in cases.items():
            if chest_info["code"] == case_code:
                if case_code in data:
                    return jsonify(data[case_code])
                else:
                    return jsonify([])  # Pusta lista, jeśli nie ma danych

        return jsonify([])  # Jeśli kod nie istnieje
    except Exception as e:
        return jsonify({"error": str(e)})
