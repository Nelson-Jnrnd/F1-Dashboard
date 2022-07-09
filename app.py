from asyncio import current_task
from flask import Flask, render_template, request, flash
from PIL import ImageColor
import data.data as f1_data
import urllib.parse


current_session = {
    'year': 2022,
    'race': 2,
    'session': 'Q'
}

app = Flask(__name__)

def hex_to_rgba(hex_color, alpha):
    return str(ImageColor.getrgb(hex_color))[:len(str(ImageColor.getrgb(hex_color))) - 1] + ', ' + str(alpha) + ')'

@app.route('/')
def index():
    session = f1_data.session_data(current_session['year'], current_session['race'], current_session['session'])
    fastest_laps = session.get_fastest_laps(session.get_all_drivers())
    team_colors = session.get_team_colors()
    chart_options = {
        'title': 'Fastest Laps',
        'x_axis_title': 'Driver',
        'y_axis_title': 'Lap Time (s)',
        'labels': fastest_laps['Driver'].tolist(),
        'values': [time.seconds + time.microseconds / 1000000 for time in fastest_laps['LapTime'].tolist() if time is not 'nan'],
        'colors': ['rgba' +  hex_to_rgba('#' + team_colors[team], 0.3) for team in fastest_laps['Team'].tolist() if team in team_colors],
    }
    return render_template('graph.html', **chart_options)

@app.route('/test')
def test():
    return render_template('loading.html')