from asyncio import current_task
from crypt import methods
from flask import Flask, render_template, request, flash, url_for, redirect
from flask_cors import CORS, cross_origin
from PIL import ImageColor
import data.data as ff1_datatypes
import urllib.parse

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = 'secret' # Change this to a more secure key

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
        'title': ff1_datatypes.session_data.current_session.session.event['EventName'] + ' Qualifying',
        'x_axis_title': 'Driver',
        'y_axis_title': 'Lap Time (s)',
        'labels': fastest_laps['Driver'].tolist(),
        'values': [time.seconds + time.microseconds / 1000000 for time in fastest_laps['LapTime'].tolist()],
        'colors': ['rgba' +  hex_to_rgba('#' + team_colors[team], 0.3) for team in fastest_laps['Team'].tolist()],
    }
    return render_template('graph.html', **chart_options)

@app.route('/loading')
def loading(url = '/'):
    return render_template('loading.html', destination=url)

@app.route('/handler', methods=['POST'])
@cross_origin()
def handler():
    if not request.form['year']:
        flash('Please enter a year', 'error')
    elif not request.form['week']:
        flash('Please enter a week', 'error')
    elif not request.form['session']:
        flash('Please enter a session', 'error')
    else:
        year = request.form['year']
        week = request.form['week']
        session = request.form['session']
        data = ff1_datatypes.session_data.get_session(year, week, session)
        if not data:
            data = ff1_datatypes.session_data(int(request.form['year']), int(request.form['week']), request.form['session'])

        ff1_datatypes.session_data.set_current(data)
        return loading('/load_session')

    return redirect(url_for('index'))

@app.route('/load_session')
@cross_origin()
def load_session():
    ff1_datatypes.session_data.current_session.load_session()
    return index()