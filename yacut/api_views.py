from flask import jsonify, request

from . import app, db
from .exceptions import InvalidAPIUsage, InvalidInputData
from .models import URLMap
from .utils import json_to_url_map


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    try:
        url_map = json_to_url_map(request.get_json())
    except InvalidInputData as error:
        raise InvalidAPIUsage(error.message)

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
