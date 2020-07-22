from run import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.Text, unique=True, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return f"<User {self.username}>"

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.Text, nullable=False)
    price = db.Column(db.Numeric(precision=11, scale=2), nullable=False)
    amznlink = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, user_id, title, price, amznlink):
        self.user_id = user_id
        self.title = title
        self.price = price
        self.amznlink = amznlink

    def __repr__(self):
        return f"<Product {self.title}>"

class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    income = db.Column(db.Numeric, nullable=False)
    fixed_expenses = db.Column(db.Numeric, nullable=False)
    saving_money = db.Column(db.Numeric, nullable=False)
    spending_money = db.Column(db.Numeric, nullable=False)
    spending_left = db.Column(db.Numeric, nullable=False)
    graph_link = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now())