from datetime import datetime
import random

from yacut import db
from .constants import (
    SHORT_LINK_DEFAULT_CHARS, SHORT_LINK_DEFAULT_LENGTH, SHORT_LINK_MAX_LENGTH
)


def get_unique_short_id():
    link = ''.join(random.choices(
        SHORT_LINK_DEFAULT_CHARS, k=SHORT_LINK_DEFAULT_LENGTH
    ))
    if URLMap.query.filter_by(short=link).first():
        return get_unique_short_id()

    return link


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String, nullable=False)
    short = db.Column(
        db.String(SHORT_LINK_MAX_LENGTH),
        unique=True,
        default=get_unique_short_id
    )
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
