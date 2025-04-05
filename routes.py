from flask import Blueprint, render_template, request, flash, redirect, url_for
import json
from prices_data import cases, load_data, load_latest_prices
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
from flask_login import login_user, login_required, current_user, logout_user
from models import db, User, UserCase

main = Blueprint('main', __name__)


@main.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]
        user = User.query.filter_by(name=name).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("main.home"))
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
        return redirect(url_for('main.home'))

    return render_template('register.html')


@main.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    if query:
        filtered_cases = {name: info for name, info in cases.items() if query.lower() in name.lower()}
    else:
        filtered_cases = {}

    return render_template('home.html', cases=filtered_cases, query=query)


@main.route('/')
def home():
    latest_prices = load_latest_prices()

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
    period = request.args.get("period", "Weekly")
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

    for chest_name, chest_info in cases.items():
        case_code = chest_info["code"]
        if case_code in prices_data:
            latest_price = prices_data[case_code][-1][1]
            chest_info['latest_price'] = f"{latest_price:.2f} zł"
        else:
            chest_info['latest_price'] = "Brak danych"

    total_value = None
    total_value_after_tax = None
    form_data = {'case_code': [], 'quantity': []}

    if request.method == 'POST':
        case_codes = request.form.getlist('case_code[]')
        quantities = request.form.getlist('quantity[]')

        form_data['case_code'] = case_codes
        form_data['quantity'] = quantities

        total_value = 0
        for case_code, quantity in zip(case_codes, quantities):
            for chest_name, chest_info in cases.items():
                if chest_info["code"] == case_code:
                    price = float(chest_info['latest_price'].replace(' zł', '').replace(',', '.'))
                    total_value += price * int(quantity)

        total_value_after_tax = round((total_value * 0.95) * 0.90, 2)

    return render_template(
        'calculate.html',
        cases=cases,
        total_value=round(total_value, 2) if total_value is not None else None,
        form_data=form_data,
        total_value_after_tax=total_value_after_tax
    )


@main.route("/user_chests", methods=['GET', 'POST'])
@login_required
def user_chests():
    latest_prices = load_latest_prices()
    price_history = load_data()
    user_cases = UserCase.query.filter_by(user_id=current_user.id).all()

    total_value = 0
    total_value_after_tax = 0

    if request.method == 'POST':
        case_codes = request.form.getlist('case_code[]')
        quantities = request.form.getlist('quantity[]')

        for case_code, quantity in zip(case_codes, quantities):
            if not quantity.isdigit():
                continue
            quantity = int(quantity)

            existing_case = UserCase.query.filter_by(user_id=current_user.id, case_code=case_code).first()

            if existing_case:
                existing_case.quantity += quantity
            else:
                new_case = UserCase(user_id=current_user.id, case_code=case_code, quantity=quantity)
                db.session.add(new_case)
        db.session.commit()
        flash("Skrzynie zostały dodane!", "success")
        return redirect(url_for('main.user_chests'))

    user_cases_data = []

    for case in user_cases:
        chest_name = next((name for name, info in cases.items() if info["code"] == case.case_code), None)
        if not chest_name:
            continue

        quantity = case.quantity
        current_price = latest_prices.get(chest_name, 0.0)
        total_case_value = round(quantity * current_price, 2)

        price_list = price_history.get(case.case_code, [])
        if len(price_list) >= 2:
            prev_price = price_list[-2][1]
            change_percent = round(((current_price - prev_price) / prev_price) * 100, 2)
        else:
            change_percent = 0.0

        user_cases_data.append({
            'id': case.id,
            'name': chest_name,
            'quantity': quantity,
            'unit_price': round(current_price, 2),
            'total_price': total_case_value,
            'total_price_after_tax': round((total_case_value * 0.95) * 0.90, 2),
            'change_percent': change_percent
        })

        total_value += total_case_value
        total_value_after_tax = (total_value * 0.95) * 0.90

    return render_template("user_chests.html",
                           user_cases=user_cases_data,
                           total_value=round(total_value, 2),
                           cases=cases,
                           total_value_after_tax=round(total_value_after_tax, 2))


@main.route("/user_chests/edit/<int:case_id>", methods=['POST'])
@login_required
def edit_chest(case_id):
    case = UserCase.query.get_or_404(case_id)
    if case.user_id != current_user.id:
        flash("Brak dostępu!", "danger")
        return redirect(url_for('main.user_chests'))

    new_quantity = request.form.get("new_quantity")
    if new_quantity and int(new_quantity) > 0:
        case.quantity = int(new_quantity)
        db.session.commit()
        flash("Zaktualizowano ilość!", "success")
    return redirect(url_for('main.user_chests'))


@main.route("/user_chests/delete/<int:case_id>", methods=['POST'])
@login_required
def delete_chest(case_id):
    case = UserCase.query.get_or_404(case_id)
    if case.user_id != current_user.id:
        flash("Brak dostępu!", "danger")
        return redirect(url_for('main.user_chests'))

    db.session.delete(case)
    db.session.commit()
    flash("Skrzynia usunięta!", "success")
    return redirect(url_for('main.user_chests'))
