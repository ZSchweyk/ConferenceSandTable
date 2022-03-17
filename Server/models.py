from server import db
from useful_functions import *
from datetime import datetime


# Create the Users table
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    salt = db.Column(db.String(64), unique=True, nullable=False)
    salted_password_hash = db.Column(db.String(64), nullable=False, unique=True)
    date_added = db.Column(db.String(len("dd/mm/yyyy hh:mm:ss")), nullable=False)

    def __init__(self, first_name, last_name, email, password, timestamp: datetime):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email.lower()
        self.salt = sha256(self.email)
        self.salted_password_hash = sha256(self.salt + password)
        self.date_added = timestamp.strftime("%m/%d/%Y %H:%M:%S")

    def __repr__(self):
        return "<Name %r>" % (self.first_name + " " + self.last_name)


# Create the Equations table
class Equations(db.Model):
    row = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    id = db.Column(db.Integer, nullable=False)
    equation = db.Column(db.String(100), nullable=False)
    date_added = db.Column(db.String(len("dd/mm/yyyy hh:mm:ss")), nullable=False)

    def __init__(self, user_id, equation, timestamp: datetime):
        self.id = user_id
        self.equation = equation
        self.date_added = timestamp.strftime("%m/%d/%Y %H:%M:%S")
