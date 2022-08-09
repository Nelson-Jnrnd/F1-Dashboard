from app_init import app
from flask import Flask, render_template, request, flash, url_for, redirect
from flask_cors import CORS, cross_origin
from PIL import ImageColor
import data.data as ff1_datatypes
from views.forms import EventForm

def hex_to_rgba(hex_color, alpha):
    return str(ImageColor.getrgb(hex_color))[:len(str(ImageColor.getrgb(hex_color))) - 1] + ', ' + str(alpha) + ')'

@app.route('/telemetry', methods=['GET', 'POST'])
@cross_origin()
def telemetry():
    team_colors = ff1_datatypes.session_data.current_session.get_team_colors()
    drivers = ['HAM', 'BOT', 'LAT']
    # todo - check if the session is loaded
    charts_data = []
    for driver in drivers:
        fastest_lap = ff1_datatypes.session_data.current_session.get_fastest_lap(driver)
        distances = [x for x in fastest_lap.telemetry['Distance']]
        speed = [x for x in fastest_lap.telemetry['Speed']]
        values = [{'x': distances[x], 'y': speed[x]} for x in range(len(distances))]
        charts_data.append({
            'values': values,
            'colors': 'rgba' +  hex_to_rgba('#' + team_colors[fastest_lap['Team']], 0.9)
        })
    
    chart_options = {
        'title': ff1_datatypes.session_data.current_session.session.event['EventName'] + ' Speed',
        'x_axis_title': 'Distance (m)',
        'y_axis_title': 'Speed (km/h)',
        'labels': ff1_datatypes.session_data.current_session.session.event['EventName'] + ' Speed',
        'charts': charts_data
    }
    return render_template('telemetry.html', form=EventForm(request.form), **chart_options)

@app.route('/load_session_telemetry')
@cross_origin()
def load_session_telemetry():
    ff1_datatypes.session_data.current_session.load_session()
    return telemetry()