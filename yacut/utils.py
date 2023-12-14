import re
from urllib.parse import urlparse, urlunparse

from flask import request
from . import db
from .constants import SHORT_LINK_REGEXP
from .exceptions import InvalidInputData, ShortLinkAlreadyExists
from .models import URLMap


def create_url_id(data):
    url_map = json_to_url_map(data)
    db.session.add(url_map)
    db.session.commit()
    return url_map.short


def url_id_to_link(id):
    scheme, netloc, *_ = urlparse(request.base_url)
    return urlunparse((scheme, netloc, id, '', '', ''))


def json_to_url_map(data):
    if not data:
        raise InvalidInputData('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidInputData('"url" является обязательным полем!')

    url = data['url']
    if not (isinstance(url, str) and url):
        raise InvalidInputData('Поле "url" должно быть непустой строкой.')

    url_map = URLMap(original=url)
    if 'custom_id' in data and data['custom_id'] is not None:
        custom_id = data['custom_id']
        if not isinstance(custom_id, str):
            raise InvalidInputData(
                'Указано недопустимое имя для короткой ссылки'
            )

        custom_id = custom_id.strip()
        if custom_id:
            if not re.match(SHORT_LINK_REGEXP, custom_id):
                raise InvalidInputData(
                    'Указано недопустимое имя для короткой ссылки'
                )

            if URLMap.query.filter_by(short=custom_id).first():
                raise ShortLinkAlreadyExists()

            url_map.short = custom_id

    return url_map
