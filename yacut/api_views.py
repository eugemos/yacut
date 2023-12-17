from flask import jsonify, request

from . import app
from .exceptions import (
    InvalidAPIUsage, InvalidInputData, ShortLinkAlreadyExists)
from .utils import (
    create_url_map, convert_url_id_to_short_link, get_original_link,
    validate_data
)


@app.route('/api/id/', methods=['POST'])
def create_short_link_api():
    request_data = request.get_json()
    try:
        url_id = create_url_map(validate_data(request_data)).short
    except (InvalidInputData, ShortLinkAlreadyExists) as error:
        raise InvalidAPIUsage(error.message)

    return (
        jsonify(dict(
            url=request_data['url'],
            short_link=convert_url_id_to_short_link(url_id)
        )),
        201
    )


@app.route('/api/id/<string:url_id>/', methods=['GET'])
def get_original_link_api(url_id):
    url = get_original_link(url_id)
    if not url:
        raise InvalidAPIUsage('Указанный id не найден', 404)

    return jsonify(dict(url=url))
