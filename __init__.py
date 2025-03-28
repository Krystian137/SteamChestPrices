from flask import Flask
from flask_bootstrap import Bootstrap

def create_app():
    app = Flask(__name__)

    Bootstrap(app)

    # Załaduj konfigurację (możesz dodać plik config.py, jeśli masz)
    app.config.from_object('config.Config')

    # Możesz tutaj dodać rozszerzenia (np. baza danych, migracje, sesje itp.)
    # Przykład: db.init_app(app)

    # Zarejestruj blueprinty
    from routes import main
    app.register_blueprint(main)

    return app