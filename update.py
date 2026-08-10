from __init__ import create_app
from prices_data import update_prices_in_db

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        update_prices_in_db()