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


class Case(db.Model):
    __tablename__ = "cases"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False, index=True)
    market_code = db.Column(db.String(200), unique=True, nullable=False)
    image_url = db.Column(db.String(500))

    prices = db.relationship(
        "PriceEntry",
        back_populates="case",
        order_by="PriceEntry.recorded_at",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<Case {self.name}>"


class PriceEntry(db.Model):
    __tablename__ = "price_entries"

    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey("cases.id"), nullable=False, index=True)
    recorded_at = db.Column(db.DateTime, nullable=False, index=True)
    price = db.Column(db.Numeric(10, 3), nullable=False)

    case = db.relationship("Case", back_populates="prices")

    __table_args__ = (
        db.UniqueConstraint("case_id", "recorded_at", name="uq_case_date"),
    )

    def __repr__(self):
        return f"<PriceEntry {self.case_id} {self.recorded_at:%Y-%m-%d} {self.price}>"