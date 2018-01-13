# coding=utf-8
from flask_wtf import Form
from wtforms import TextField, PasswordField, StringField, IntegerField, DateField, RadioField
from wtforms.validators import DataRequired, EqualTo, Length, email, NumberRange, Required, Email, URL, Optional


class RegisterForm(Form):
    membertype = RadioField(
        [DataRequired()],
        choices=[('1', 'Ordinary Member'), ('2', 'Sustaining Member')], default=1
    )
    email = StringField(
        'Email', validators=[DataRequired(), Length(min=6, max=254), Email()]
    )
    firstname = StringField(
        'Firstname', validators=[DataRequired(), Length(min=2, message="Too short First Name")]
    )
    lastname = StringField(
        'Lastname', validators=[DataRequired(), Length(min=2, message="Too short Last Name")]
    )
    bday = DateField(
        'Bday',
    )
    road = StringField(
        'Road', validators=[Length(min=1, max=400), Optional()]
    )
    postcode = IntegerField(
        'Postcode', validators=[DataRequired()]
    )
    town = StringField(
        'Town', validators=[Length(max=400)]
    )
    persontype = IntegerField(
        'Persontype', validators=[NumberRange(0, 2, message="Person Type is Invalid")]
    )
    company = StringField(
        'Company', validators=[Length(max=300), Optional()]
    )
    phone = StringField(
        'Phone', validators=[Optional()]
    )
    mobile = StringField(
        'Mobile', validators=[Optional()]
    )
    image_url = StringField(
        'Image Url', validators=[Optional()]
    )
    account_holder = StringField(
        'Accountname', validators=[DataRequired(), Length(min=10, max=200, message="Invalid Account Name")]
    )
    iban = StringField(
        'IBAN', validators=[DataRequired(), Length(min=16, max=30)]
    )
    bic = StringField(
        'BIC', validators=[DataRequired(), Length(min=9, max=15)]
    )
    fee = IntegerField(
        'Fee', validators=[DataRequired()]
    )


class LoginForm(Form):
    email = StringField('Email', [DataRequired(), Length(min=6, max=254), Email()])
    password = PasswordField('Password', [DataRequired()])


class ForgotForm(Form):
    email = StringField(
        'Email', validators=[DataRequired(), Length(min=6, max=254), Email()]
    )


class ResetForm(Form):
    password = PasswordField('New Password', [
        DataRequired(),
        EqualTo('confirm', message='Passwords must match'),
        Length(min=8,max=300,message="Your password must be between 8 and 300 characters!")
    ])
    confirm = PasswordField('Repeat Password')
    reset_token = StringField(
        'Token',
        [Length(min=40,message="Invalid Token")]
    )

class UpdateProfile(Form):
    firstname = StringField(
        'Firstname', validators=[DataRequired(), Length(min=2, message="Too short First Name")]
    )
    lastname = StringField(
        'Lastname', validators=[DataRequired(), Length(min=2, message="Too short Last Name")]
    )
    bday = DateField(
        'Bday',
    )
    road = StringField(
        'Road', validators=[Length(min=1, max=400), Optional()]
    )
    postcode = IntegerField(
        'Postcode', validators=[DataRequired()]
    )
    town = StringField(
        'Town', validators=[Length(max=400)]
    )
    company = StringField(
        'Company', validators=[Length(max=300), Optional()]
    )
    phone = StringField(
        'Phone', validators=[Optional()]
    )
    mobile = StringField(
        'Mobile', validators=[Optional()]
    )
    image_url = StringField(
        'Image Url', validators=[Optional()]
    )

class EditBank(Form):
    account_holder = StringField(
        'Accountname', validators=[DataRequired(), Length(min=10, max=200, message="Invalid Account Name")]
    )
    iban = StringField(
        'IBAN', validators=[DataRequired(), Length(min=16, max=30)]
    )
    bic = StringField(
        'BIC', validators=[DataRequired(), Length(min=9, max=15)]
    )
    account_no = IntegerField(
        'Account No', validators=[DataRequired()]
    )
