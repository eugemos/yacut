import re

from .constants import SHORT_LINK_REGEXP
from .exceptions import InvalidInputData
from .models import URLMap


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
                raise InvalidInputData(
                    'Предложенный вариант короткой ссылки уже существует.'
                )

            url_map.short = custom_id

    return url_map
