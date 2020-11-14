from flask_sqlalchemy import SQLAlchemy

from .routes import app
db = SQLAlchemy(app)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

    def __init__(self, name):
        self.name = name


db.create_all()