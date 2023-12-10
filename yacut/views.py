from flask import flash, redirect, render_template, request

from . import app, db
from .forms import URLMapForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def create_short_link_view():
    form = URLMapForm()
    if form.validate_on_submit():
        url_map = URLMap(original=form.original_link.data)
        custom_id = form.custom_id.data
        if custom_id is not None:
            custom_id = custom_id.strip()
        if custom_id:
            if URLMap.query.filter_by(short=custom_id).first():
                flash(
                    'Предложенный вариант короткой ссылки уже существует.',
                    category='error'
                )
                return render_template('create_short_link.html', form=form)
            url_map.short = custom_id

        db.session.add(url_map)
        db.session.commit()
        flash('Ваша новая ссылка готова:')
        flash(f'{request.base_url}{url_map.short}', category='link')
        return render_template('create_short_link.html', form=form)

    return render_template('create_short_link.html', form=form)


@app.route('/<string:short_link>')
def access_short_link(short_link):
    return redirect(
        URLMap.query.filter_by(short=short_link).first_or_404().original
    )
