import re
from urllib.parse import urlparse, urlunparse

from flask import request
from . import db
from .constants import SHORT_LINK_REGEXP
from .exceptions import InvalidInputData, ShortLinkAlreadyExists
from .models import URLMap


def url_id_to_short_link(id):
    """Возвращает короткий URL, созданный на основании заданного
    идентификатора.
    """
    scheme, netloc, *_ = urlparse(request.base_url)
    return urlunparse((scheme, netloc, id, '', '', ''))


def url_id_to_original_link(id):
    """Возвращает оригинальный URL, соответствующий заданному идентификатору,
    или None, если такого идентификатора нет в БД.
    """
    url_map = URLMap.query.filter_by(short=id).first()
    if url_map:
        return url_map.original


def validate_data(data):
    """Выполняет валидацию данных, содержащихся в словаре data с ключами
    'url' и 'custom_id' (необязательный).
    Возвращает словарь валидированных данных с ключами 'original' и 'short'
    (необязательный).
    """
    if not data:
        raise InvalidInputData('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidInputData('"url" является обязательным полем!')

    url = data['url']
    if not (isinstance(url, str) and url):
        raise InvalidInputData('Поле "url" должно быть непустой строкой.')

    validated_data = dict(original=url)
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

            validated_data['short'] = custom_id

    return validated_data


def create_url_map(data):
    """Создаёт в БД объект модели URLMap на основании словаря data
    с ключами 'original' и 'short' (необязательный). При этом, выполняется
    проверка уникальности значения, заданного ключём 'short' (при наличии).
    """
    if ('short' in data
            and URLMap.query.filter_by(short=data['short']).first()):
        raise ShortLinkAlreadyExists()

    url_map = URLMap(**data)
    db.session.add(url_map)
    db.session.commit()
    return url_map
