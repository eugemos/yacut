# from random import randrange

from flask import abort, flash, redirect, render_template, url_for

from . import app, db
# from .forms import OpinionForm
# from .models import Opinion


# def random_opinion():
#     quantity = Opinion.query.count()
#     if quantity:
#         offset_value = randrange(quantity)
#         opinion = Opinion.query.offset(offset_value).first()
#         return opinion


@app.route('/')
def index_view():
    return render_template('index.html')
