# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from apps import db 
from flask import render_template, request, jsonify
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
from apps.iot.models import Verbruik
import json


@blueprint.route('/index', methods=["GET", "POST"])
@login_required
def index():
    info = Verbruik.query.filter_by(user=current_user.username).all()
    data = []
    days = []
    dates = db.session.query(Verbruik.date).all()
    dates = [date.strftime('%A') for (date,) in dates] 
    for i in info:
        id = i.id
        verbruik = i.verbruik
        user = i.user
        date = i.date.strftime('%A')
        data.append(verbruik)
        days.append(date)

    data = json.dumps(data)
    days = json.dumps(days)
        
    return render_template('home/index.html', segment='index', data=data, days=days, dates=dates)



@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500

@blueprint.route('/data', methods=["GET", "POST"])
def data():
    data = request.json
    if data:
        with open('data.txt', 'w') as f:
            f.write(str(data))
    return render_template('home/data.html', data=data)

# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
