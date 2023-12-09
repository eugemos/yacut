from datetime import datetime
import random

from yacut import db


SHORT_LINK_DEFAULT_CHARS = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
SHORT_LINK_DEFAULT_LENGTH = 6
SHORT_LINK_MAX_LENGTH = 16
SHORT_LINK_REGEXP = r'[-_0-9a-zA-Z]+'

def generate_short_link():
    link = ''.join(random.choices(
        SHORT_LINK_DEFAULT_CHARS, k=SHORT_LINK_DEFAULT_LENGTH
    ))
    if URLMap.query.filter_by(short=link).first():
        return generate_short_link()
    
    return link


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String, nullable=False)
    short = db.Column(
        db.String(SHORT_LINK_MAX_LENGTH),
        unique=True,
        default=generate_short_link
    )
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
