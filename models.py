from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from __init__ import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    password = Column(String(256), nullable=False)
    cases = relationship('UserCase', backref='owner', lazy=True)

    def __init__(self, name, password):
        self.name = name
        self.password = password

class UserCase(db.Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    case_code = Column(String(100))
    quantity = Column(Integer)
    latest_price = Column(db.Float, nullable=True)  # Dodane pole

