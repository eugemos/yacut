from flask import flash, redirect, render_template, request

from . import app, db
from .forms import URLMapForm
from .models import URLMap
from .utils import create_url_id, url_id_to_link
from .exceptions import ShortLinkAlreadyExists


@app.route('/', methods=['GET', 'POST'])
def create_short_link_view():
    form = URLMapForm()
    if form.validate_on_submit():
        try:
            url_id = create_url_id(dict(
                url=form.original_link.data, custom_id=form.custom_id.data
            ))
        except ShortLinkAlreadyExists as error:
            flash(error.message, category='error')
            return render_template('create_short_link.html', form=form)

        flash('Ваша новая ссылка готова:')
        flash(url_id_to_link(url_id), category='link')
        return render_template('create_short_link.html', form=form)

    return render_template('create_short_link.html', form=form)


@app.route('/<string:short_link>')
def access_short_link(short_link):
    return redirect(
        URLMap.query.filter_by(short=short_link).first_or_404().original
    )
