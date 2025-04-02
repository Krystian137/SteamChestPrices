class Config:
    SECRET_KEY = 'secret'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # opcjonalnie, żeby wyłączyć ostrzeżenia o zmianach w bazie
