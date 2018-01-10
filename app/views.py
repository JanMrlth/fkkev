import base64

import bcrypt, string, random
import math

import datetime
from flask_login import login_user, login_required, current_user, logout_user

from app import app, db
from flask import Flask, render_template, request, redirect, url_for, flash
import logging
from logging import Formatter, FileHandler

from app.forms import *
import os
from flask_mail import Mail
from Crypto.Cipher import AES

from config import BLOCK_SIZE, PADDING, secret_key

pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
cipher = AES.new(secret_key)
# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#
from app.models import User, Bankdetails


@app.route('/', methods=['GET'])
def index():
    form = LoginForm(request.form)
    return render_template('forms/login.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        userData = User.query.filter_by(email=form.email.data).first()
        if userData is None:
            flash('Invalid Email Provided', 'error')
            return redirect(url_for('index'))
        if bcrypt.checkpw(form.password.data, userData.password):
            userData.authenticated = True
            db.session.add(userData)
            db.session.commit()
            login_user(userData, remember=True)

    return redirect(url_for('index'))


@app.route('/logout', methods=["GET"])
@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect(url_for('/checkLogout'))


@app.route('/checkLogout', methods=['GET'])
def logout_check():
    if current_user.is_authenticated:
        logout_user()
    return redirect('/')


@app.route('/register')
def register():
    form = RegisterForm()
    if form.validate_on_submit() and (form.membertype.data in [1, 2]) and (form.persontype.data in [1.2]):
        chars = (string.letters + string.digits + string.punctuation)
        passwordTemp = ''.join((random.choice(chars)) for x in range(app.config['PWS_SIZE']))
        first_fee = 9
        if form.membertype.data == 1 and form.fee.data in [3, 6, 30]:
            first_fee = 9
        elif form.membertype.data == 2 and form.fee.data in [25, 35, 100]:
            first_fee = 50
        else:
            flash('Fee Validation Error', 'error')
            return redirect(url_for('register'))
        if (form.persontype.data == 1):
            userObj = User(email=form.email.data, password=passwordTemp, membertype=form.membertype.data,
                           persontype=form.persontype.data, first_fee=first_fee, fee=form.fee.data,
                           company=form.company.data, firstname=form.firstname.data, lastname=form.lastname.data,
                           bday=form.bday.data, road=form.road.data, town=form.town.data, postcode=form.postcode.data,
                           phone=form.phone.data, mobile=form.mobile.data)
        else:
            userObj = User(email=form.email.data, password=passwordTemp, membertype=form.membertype.data,
                           persontype=form.persontype.data, first_fee=first_fee, fee=form.fee.data,
                           firstname=form.firstname.data, lastname=form.lastname.data,
                           bday=form.bday.data, road=form.road.data, town=form.town.data, postcode=form.postcode.data,
                           phone=form.phone.data, mobile=form.mobile.data)

        bankObj = Bankdetails()
        bankObj.account_holder = (form.firstname.data + " " + form.lastname.data).title()
        iban = form.iban.data
        bic = form.bic.data
        digits = 0
        if iban > 0:
            digits = int(math.log10(iban)) + 1
        elif not iban:
            digits = 1
        else:
            digits = int(math.log10(-iban)) + 2
        if not (digits >= 16 and digits <= 34):
            flash('Invalid IBAN Number', 'error')
            return redirect(url_for('register'))
        iban_visible = iban[:6] + 'X' * (digits - 10) + iban[-4:]

        if bic > 0:
            digits = int(math.log10(bic)) + 1
        elif not bic:
            digits = 1
        else:
            digits = int(math.log10(-bic)) + 2
        if not (digits >= 5 and digits <= 15):
            flash('Invalid BIC Number', 'error')
            return redirect(url_for('register'))

        bic_visible = bic[:2] + 'X' * (digits - 4) + bic[-2:]
        bankObj.iban_visible = iban_visible
        bankObj.bic_visible = bic_visible
        bankObj.iban = EncodeAES(cipher, iban)
        bankObj.bic = EncodeAES(cipher, bic)
        bankObj.blc = form.bic.data
        bankObj.sepa_date = datetime.datetime.now
        bankObj.sepa_ref = 'FraKeKueV'
        if not form.membertype.data:
            bankObj.sepa_ref += 'OrdM'
        else:
            bankObj.sepa_ref += 'FoeM'
        bankObj.sepa_ref += iban_visible[:6]

        userObj.bankdetails.append(bankObj)
        db.session.add(userObj)
        db.session.add(bankObj)
        db.session.commit()
        flash('Registered Id Successfully','success')
        return redirect(url_for('index'))

@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)


# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    # db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')
