from flask_wtf import FlaskForm, CSRFProtect
from wtforms import IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired

csrf = CSRFProtect()

class EventForm(FlaskForm):
    year = IntegerField('Year', validators=[DataRequired()])
    week = IntegerField('Week', validators=[DataRequired()])
    session = SelectField('Session', choices=[('FP1'), ('FP2'), ('FP3'), ('Q'), ('R')])
    submit = SubmitField('Submit')
