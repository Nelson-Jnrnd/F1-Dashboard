from flask import Flask, render_template, request, flash
from PIL import ImageColor
import data.data as f1_data

session = f1_data.session_data(2022, 1, 'Q')
app = Flask(__name__)

def hex_to_rgba(hex_color, alpha):
    return str(ImageColor.getrgb(hex_color))[:len(str(ImageColor.getrgb(hex_color))) - 1] + ', ' + str(alpha) + ')'

@app.route('/')
def index():
    fastest_laps = session.get_fastest_laps(session.get_all_drivers())
    team_colors = session.get_team_colors()


    name = '\'Qualifying\''
    labels = fastest_laps['Driver'].tolist()
    values = [time.seconds + time.microseconds / 1000000 for time in fastest_laps['LapTime'].tolist()]
    colors = ['rgba' +  hex_to_rgba('#' + team_colors[team], 0.3) for team in fastest_laps['Team'].tolist()]
    return render_template('graph.html', name=name, labels=labels, values=values, colors=colors)