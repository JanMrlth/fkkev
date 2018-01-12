# coding=utf-8
from flask_wtf import Form
from wtforms import TextField, PasswordField, StringField, IntegerField, DateField, RadioField
from wtforms.validators import DataRequired, EqualTo, Length, email, NumberRange, Required, Email,URL

class RegisterForm(Form):
    membertype = RadioField(
        [DataRequired()],
        choices=[('1', 'Ordinary Member'), ('2', 'Sustaining Member')], default=1
    )
    email = StringField(
        'Email', validators=[DataRequired(), Length(min=6, max=254),Email()]
    )
    firstname = StringField(
        'Firstname', validators=[DataRequired(), Length(min=2,message="Too short First Name")]
    )
    lastname = StringField(
        'Lastname', validators=[DataRequired(), Length(min=2,message="Too short Last Name")]
    )
    bday = DateField(
        'Bday',
    )
    road = StringField(
        'Road', validators=[Length(min=1,max=400)]
    )
    postcode = IntegerField(
        'Postcode',validators=[DataRequired()]
    )
    town = StringField(
        'Town',validators=[Length(max=400)]
    )
    persontype = IntegerField(
        'Persontype',validators=[NumberRange(0,2,message="Person Type is Invalid")]
    )
    company = StringField(
        'Company',validators=[Length(max=300)]
    )
    phone = StringField(
        'Phone',
    )
    mobile = StringField(
        'Mobile',validators=[DataRequired()]
    )
    image_url = StringField(
        'Image Url',validators=[URL(message='Image URL is invalid')]
    )
    account_holder = StringField(
        'Accountname',validators=[DataRequired(),Length(min=10,max=200,message="Invalid Account Name")]
    )
    iban = StringField(
        'IBAN',validators=[DataRequired(),Length(min=16,max=30)]
    )
    bic = StringField(
        'BIC', validators=[DataRequired(), Length(min=9, max=15)]
    )
    fee = IntegerField(
        'Fee',validators=[DataRequired()]
    )

class LoginForm(Form):
    email = StringField('Email', [DataRequired(),Length(min=6, max=254),Email()])
    password = PasswordField('Password', [DataRequired()])


class ForgotForm(Form):
    email = StringField(
        'Email', validators=[DataRequired(), Length(min=6, max=254),Email()]
    )
