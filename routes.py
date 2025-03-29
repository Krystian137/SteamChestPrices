from flask import Blueprint, render_template, request
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
    for chest_name, chest_info in cases.items():
        if chest_info["code"] == case_code:
            return render_template('chest_info.html', chest_info=chest_info, case_code=case_code, chest_name=chest_name)
    return "Nie znaleziono skrzynki.", 404


@main.route("/get_price_history/<case_code>")
def get_price_history(case_code):
    period = request.args.get("period", "Weekly")  # Pobieramy wybrany okres
    try:
        with open("prices.json", "r") as f:
            data = json.load(f)

        for chest_name, chest_info in cases.items():
            if chest_info["code"] == case_code:
                if case_code in data:
                    # Czyszczenie daty (usunięcie wszystkiego po pierwszym "+")
                    cleaned_data = [[entry[0].split(" +")[0], entry[1]] for entry in data[case_code]]

                    # Filtracja według okresu
                    if period == "Monthly":
                        cleaned_data = [entry for entry in cleaned_data if "Jun" in entry[0]]  # Przykład
                    elif period == "Yearly":
                        cleaned_data = cleaned_data[:10]  # Ograniczenie do 10 wpisów jako przykład
                    elif period == "Total":
                        pass  # Pełne dane

                    return jsonify(cleaned_data)
                else:
                    return jsonify([])

        return jsonify([])  # Jeśli nie znaleziono case_code
    except Exception as e:
        print("Błąd:", str(e))
        return jsonify({"error": str(e)})


