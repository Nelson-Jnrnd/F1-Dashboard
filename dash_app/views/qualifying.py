from multiprocessing import Event
from app_init import app
from flask import Flask, render_template, request, flash, url_for, redirect
from flask_cors import CORS, cross_origin
from PIL import ImageColor
import data.data as ff1_datatypes
from views.forms import EventForm

current_session = ff1_datatypes.session_data(2022, 1, 'Q')
current_session.load_session()
ff1_datatypes.session_data.set_current(current_session)


def hex_to_rgba(hex_color, alpha):
    return str(ImageColor.getrgb(hex_color))[:len(str(ImageColor.getrgb(hex_color))) - 1] + ', ' + str(alpha) + ')'

@app.route('/', methods=['GET', 'POST'])
@cross_origin()
def index():
    # todo - check if the session is loaded
    fastest_laps = ff1_datatypes.session_data.current_session.get_fastest_laps(ff1_datatypes.session_data.current_session.get_all_drivers())
    team_colors = ff1_datatypes.session_data.current_session.get_team_colors()
    chart_options = {
        'title': ff1_datatypes.session_data.current_session.session.event['EventName'] + ' ' + ff1_datatypes.session_data.current_session.session.event.get_session_name(ff1_datatypes.session_data.current_session.session_type),
        'x_axis_title': 'Driver',
        'y_axis_title': 'Lap Time (s)',
        'labels': fastest_laps['Driver'].tolist(),
        'values': [time.seconds + time.microseconds / 1000000 for time in fastest_laps['LapTime'].tolist()],
        'colors': ['rgba' +  hex_to_rgba('#' + team_colors[team], 0.3) for team in fastest_laps['Team'].tolist()],
    }
    return render_template('graph.html', form=EventForm(request.form), **chart_options)

@app.route('/loading')
def loading(url = '/'):
    return render_template('loading.html', destination=url)
    
@app.route('/session_select_handler', methods=['POST'])
@cross_origin()
def session_select_handler():
    form = EventForm(request.form)
    if form.validate_on_submit():
        year = form.year
        week = form.week
        session = form.session
        data = ff1_datatypes.session_data.get_session(year, week, session)
        if not data:
            data = ff1_datatypes.session_data(int(form.year.data), int(form.week.data), form.session.data)

        ff1_datatypes.session_data.set_current(data)
        return loading(request.form['target'])
    
    return redirect(request.form['callback']) # TODO - security issue
    

@app.route('/load_session')
@cross_origin()
def load_session():
    ff1_datatypes.session_data.current_session.load_session()
    return index()