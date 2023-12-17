from datetime import datetime

from yacut import db
from .constants import SHORT_LINK_MAX_LENGTH


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String, nullable=False)
    short = db.Column(
        db.String(SHORT_LINK_MAX_LENGTH),
        unique=True,
        nullable=False
    )
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
