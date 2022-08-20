from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, InputRequired


class LoginForm(FlaskForm):
    email = StringField('Email: ', validators=[Email(message='Invalid email')])
    password = PasswordField('Password: ', validators=[DataRequired(), Length(min=4, max=10)])
    remember = BooleanField('Remember me: ', default=False)
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    name = StringField('Name: ', validators=[Length(min=4, max=10)])
    email = StringField('Email: ', validators=[Email()])
    password = PasswordField(
        'Password: ',
        validators=[InputRequired(), Length(min=4, max=5), EqualTo('confirm', message='Passwords must match')]
    )
    confirm = PasswordField(
        'Repeat password: ',
        validators=[InputRequired(), EqualTo('password', message='Passwords must match')]
    )
    submit = SubmitField('Register')
