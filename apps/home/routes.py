
from datetime import datetime
from apps.home import blueprint
from apps import db 
from flask import render_template, request, jsonify
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
from apps.iot.models import Verbruik
from datetime import datetime, date
from apps.dataprocessing.read_data import extract_data
import json

today = date.today()

print(today)

@blueprint.route('/index', methods=["GET", "POST"])
@login_required
def index():
    info = Verbruik.query.filter_by(user="user").all()
    data = []
    days = []
    dates = db.session.query(Verbruik.date).all()
    dates = [date.strftime('%A') for (date,) in dates] 
    for i in info:
        verbruik = i.verbruik
        date = i.date.strftime('%d/%m/%y')
        dagen = i.date.strftime('%A')
        data.append(verbruik)
        days.append(date)
        dates.append(dagen)

    data = json.dumps(data)
    days = json.dumps(days)
    dates = json.dumps(dates)

    return render_template('home/index.html', segment='index', data=data, days=days, dates=dates)


@blueprint.route('/charts', methods=["GET", "POST"])
def charts():
    info = db.session.query(Verbruik).filter(db.func.date(Verbruik.date) == today).all()
    data = []
    days = []
    hourly_averages = {}
    for i in info:
        id = i.id
        verbruik = i.verbruik
        user = i.user
        date = i.date.strftime('%H:%M')

        # only show 10 most recent values
        # remove first item from the list before adding a new one
        if len(data) > 9:
            data.pop(0)
            days.pop(0)
            data.append(verbruik)
            days.append(date)
        else:
            data.append(verbruik)
            days.append(date)
        
        print(len(data))

        hour = i.date.strftime('%H')
        hours = hour + ":00"
        if hours in hourly_averages:
            hourly_averages[hours].append(verbruik)
        else:
            hourly_averages[hours] = [verbruik]

    hourly_labels = []
    hourly_data = []
    for hours, verbruik_list in hourly_averages.items():
        average_verbruik = sum(verbruik_list) / len(verbruik_list)

        # only show 24 most recent hours
        if len(hourly_labels) and len(hourly_averages) > 23:
            hourly_labels.pop(0)
            hourly_data.pop(0)
            hourly_labels.append(hours)
            hourly_data.append(average_verbruik)
        else:
            hourly_labels.append(hours)
            hourly_data.append(average_verbruik)

    data = json.dumps(data)
    days = json.dumps(days)
    hourly_data = json.dumps(hourly_data)
    hourly_labels = json.dumps(hourly_labels)

    return render_template('home/charts.html', segment='index', data=data, days=days, hourly_data=hourly_data, hourly_labels=hourly_labels)

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
        with open('data.txt', 'a') as f:
            f.write('\n' + str(data))

    insert_data()
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

# Insert values from data.txt into the database
def insert_data():
    # Using extract_data() from \apps\dataprocessing\read_data.py to extract the values from data.txt
    values = extract_data()
    print(values)
    print("Inserting values into the database...")
    # Inserts values into the database
    for value in values:
        verbruik_obj = Verbruik(verbruik=value, user="user", date=datetime.now())
        db.session.add(verbruik_obj)
        db.session.commit()

    print(f"Values inserted into verbruik table: {len(values)}")
