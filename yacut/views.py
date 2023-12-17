from flask import abort, flash, redirect, render_template

from . import app
from .forms import URLMapForm
from .utils import (
    create_url_map, convert_url_id_to_short_link, get_original_link,
    validate_data
)
from .exceptions import ShortLinkAlreadyExists


@app.route('/', methods=['GET', 'POST'])
def create_short_link_view():
    form = URLMapForm()
    if form.validate_on_submit():
        try:
            url_id = create_url_map(validate_data(dict(
                url=form.original_link.data, custom_id=form.custom_id.data
            ))).short
        except ShortLinkAlreadyExists as error:
            flash(error.message, category='error')
            return render_template('create_short_link.html', form=form)

        flash('Ваша новая ссылка готова:')
        flash(convert_url_id_to_short_link(url_id), category='link')
        return render_template('create_short_link.html', form=form)

    return render_template('create_short_link.html', form=form)


@app.route('/<string:url_id>')
def access_short_link(url_id):
    url = get_original_link(url_id)
    if not url:
        abort(404)

    return redirect(url)
