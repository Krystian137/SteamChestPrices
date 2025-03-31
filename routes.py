from flask import Blueprint, render_template, request
import json
from prices_data import cases, get_latest_price_from_file, load_data
from flask import jsonify

main = Blueprint('main', __name__)

FILENAME = "prices.json"

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
        data = load_data()

        for chest_name, chest_info in cases.items():
            if chest_info["code"] == case_code:
                if case_code in data:
                    cleaned_data = [[entry[0].split(" +")[0], entry[1]] for entry in data[case_code]]

                    if period == "Monthly":
                        cleaned_data = [entry for entry in cleaned_data if "Jun" in entry[0]]
                    elif period == "Yearly":
                        cleaned_data = cleaned_data[:10]
                    elif period == "Total":
                        pass

                    return jsonify(cleaned_data)
                else:
                    return jsonify([])

        return jsonify([])
    except Exception as e:
        print("Błąd:", str(e))
        return jsonify({"error": str(e)})


@main.route("/calculate", methods=['GET', 'POST'])
def calculate():
    prices_data = load_data()

    # Aktualizacja danych o cenach dla skrzyń
    for chest_name, chest_info in cases.items():
        case_code = chest_info["code"]
        if case_code in prices_data:
            latest_price = prices_data[case_code][-1][1]  # Pobierz ostatnią cenę
            chest_info['latest_price'] = f"{latest_price:.2f} zł"
        else:
            chest_info['latest_price'] = "Brak danych"

    total_value = None
    form_data = {'case_code': [], 'quantity': []}  # Inicjalizacja pustych tablic

    if request.method == 'POST':
        case_codes = request.form.getlist('case_code[]')
        quantities = request.form.getlist('quantity[]')

        # Przypisanie danych do form_data
        form_data['case_code'] = case_codes
        form_data['quantity'] = quantities

        total_value = 0
        # Obliczanie wartości dla każdej skrzyni
        for case_code, quantity in zip(case_codes, quantities):
            for chest_name, chest_info in cases.items():
                if chest_info["code"] == case_code:
                    price = float(chest_info['latest_price'].replace(' zł', '').replace(',', '.'))
                    total_value += price * int(quantity)

    return render_template(
        'calculate.html',
        cases=cases,
        total_value=total_value,
        form_data=form_data  # Przekazanie danych do szablonu
    )




