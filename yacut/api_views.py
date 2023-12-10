import re

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .constants import SHORT_LINK_REGEXP


def json_to_url_map(data):
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    url = data['url']
    if not (isinstance(url, str) and url):
        raise InvalidAPIUsage('Поле "url" должно быть непустой строкой.')

    url_map = URLMap(original=url)
    if 'custom_id' in data and data['custom_id'] is not None:
        custom_id = data['custom_id']
        if not isinstance(custom_id, str):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки'
            )

        custom_id = custom_id.strip()
        if custom_id:
            if not re.match(SHORT_LINK_REGEXP, custom_id):
                raise InvalidAPIUsage(
                    'Указано недопустимое имя для короткой ссылки'
                )

            if URLMap.query.filter_by(short=custom_id).first():
                raise InvalidAPIUsage(
                    'Предложенный вариант короткой ссылки уже существует.'
                )

            url_map.short = custom_id

    return url_map


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    url_map = json_to_url_map(request.get_json())
    db.session.add(url_map)
    db.session.commit()
    short_link = (
        request.base_url.removesuffix('api/id/') + url_map.short
    )
    return (
        jsonify(dict(url=url_map.original, short_link=short_link)), 
        201
    )

@app.route('/api/id/<string:short_link>/', methods=['GET'])
def get_original_link(short_link):
    url_map = URLMap.query.filter_by(short=short_link).first()
    if not url_map:
        raise InvalidAPIUsage('Указанный id не найден', 404)

    return jsonify(dict(url=url_map.original))
