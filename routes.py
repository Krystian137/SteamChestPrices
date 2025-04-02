from flask import Blueprint, render_template, request, flash, redirect, url_for
import json
from prices_data import cases, load_data
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
from flask_login import login_user, login_required, current_user, logout_user
from models import db, User

main = Blueprint('main', __name__)

FILENAME = "prices.json"


@main.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]
        user = User.query.filter_by(name=name).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("main.index"))
        else:
            flash("Nieprawidłowy login lub hasło", "danger")

    return render_template("login.html")


@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.login"))


@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')

        if not name or not password:
            flash("Wprowadź nazwę użytkownika i hasło", "danger")
            return redirect(url_for('main.register'))

        if User.query.filter_by(name=name).first():
            flash("Nazwa użytkownika już istnieje", "danger")
            return redirect(url_for('main.register'))

        new_user = User(name=name, password=generate_password_hash(password, method='pbkdf2:sha256'))
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        flash("Konto zostało założone i zalogowane", "success")
        return redirect(url_for('main.home'))  # Przekierowanie po rejestracji

    return render_template('register.html')


@main.route('/')
def home():
    try:
        # Wczytujemy najnowsze ceny z pliku latest_prices.json
        with open("latest_prices.json", "r") as f:
            latest_prices = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        latest_prices = {}

    # Przypisujemy ceny do skrzyń
    for chest_name, chest_info in cases.items():
        latest_price = latest_prices.get(chest_name)
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




