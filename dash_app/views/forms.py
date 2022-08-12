from email.policy import default
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import IntegerField, SubmitField, SelectField, SelectMultipleField, widgets
from wtforms.validators import DataRequired
import data.data as ff1_datatypes

csrf = CSRFProtect()

class EventForm(FlaskForm):
    year = IntegerField('Year', validators=[DataRequired()])
    week = IntegerField('Week', validators=[DataRequired()])
    session = SelectField('Session', choices=[('FP1'), ('FP2'), ('FP3'), ('Q'), ('R')])
    submit = SubmitField('Submit')

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


def DynamicDriverForm(f, drivers):
    class DriverForm(EventForm):
        pass

    names = [(x, x) for x in drivers]
    DriverForm.drivers = MultiCheckboxField('Drivers', choices=names)
    return DriverForm(f)

