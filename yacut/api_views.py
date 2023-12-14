from flask import jsonify, request

from . import app, db
from .exceptions import InvalidAPIUsage, InvalidInputData, ShortLinkAlreadyExists
from .models import URLMap
from .utils import create_url_id, url_id_to_link


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    request_data = request.get_json()
    try:
        url_id = create_url_id(request_data)
    except (InvalidInputData, ShortLinkAlreadyExists) as error:
        raise InvalidAPIUsage(error.message)

    return (
        jsonify(dict(url=request_data['url'], short_link=url_id_to_link(url_id))),
        201
    )


@app.route('/api/id/<string:short_link>/', methods=['GET'])
def get_original_link(short_link):
    url_map = URLMap.query.filter_by(short=short_link).first()
    if not url_map:
        raise InvalidAPIUsage('Указанный id не найден', 404)

    return jsonify(dict(url=url_map.original))
