from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp, URL

from .constants import (
    SHORT_LINK_REGEXP, SHORT_LINK_MAX_LENGTH
)


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Это обязательное поле'),
            Length(1, -1),
            URL(message='Это поле должно содержать URL')
        ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки', 
        validators=[
            Length(1, SHORT_LINK_MAX_LENGTH),
            Optional(),
            Regexp(
                SHORT_LINK_REGEXP,
                message='Это поле может содержать только символы: 0-9, a-z, A-Z, -, _'
            )
        ]
    )
    submit = SubmitField('Создать')