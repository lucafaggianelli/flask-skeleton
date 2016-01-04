from datetime import datetime

from flask import g
from flask_sqlalchemy import SQLAlchemy
from {[ name ]} import app

db = SQLAlchemy(app)

class MyModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    def __repr__(self):
        return '<MyModel %r>' % self.name

# Reset all the database tables
db.create_all()
