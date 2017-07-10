from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

class UserForm(Form):
    username = StringField('first_name', validators=[DataRequired()])
    password = PasswordField('last_name', validators=[DataRequired()])