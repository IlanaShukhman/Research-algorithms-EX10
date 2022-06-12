from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField,
                     RadioField)
from wtforms.validators import InputRequired, Length

class CourseForm(FlaskForm):
    size = IntegerField('Size', validators=[InputRequired()])
    k = IntegerField('k', validators=[InputRequired()])