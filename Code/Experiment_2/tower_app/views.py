from flask import render_template, request, make_response, session
from . import app, db
from .models import Subject, Trial
import datetime


@app.route('/', methods=['GET', 'POST'])
def experiment():
    if request.method == 'GET':
        return render_template('experiment.html')

    if request.method == 'POST':
        d = request.get_json(force=True)[0]

        return make_response("", 200)

