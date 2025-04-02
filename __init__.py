from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

# Inicjalizacja SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Załaduj konfigurację
    app.config.from_object('config.Config')

    # Inicjalizowanie db
    db.init_app(app)

    # Inicjalizowanie bootstrap
    Bootstrap(app)

    # Importowanie blueprintów
    from routes import main
    app.register_blueprint(main)

    return app
