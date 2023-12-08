from datetime import datetime

from yacut import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String)
    short = db.Column(db.String, unique=True)
    timestamp = db.Column(db.DateTime)
