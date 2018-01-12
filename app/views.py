# coding=utf-8
import base64
import urllib2
import bcrypt, string, random
import mimetypes, urllib2
import math

import datetime
from flask_login import login_user, login_required, current_user, logout_user
from wtforms import ValidationError

from app import app, db, mail
from flask import Flask, render_template, request, redirect, url_for, flash
import logging
from logging import Formatter, FileHandler

from app.forms import *
import os
from flask_mail import Mail, Message
from Crypto.Cipher import AES
from schwifty import IBAN
from config import BLOCK_SIZE, PADDING, secret_key, ADMINS

pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
cipher = AES.new(secret_key)
# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#
from app.models import User, Bankdetails, Confirmation, Forgotpassword

memberType = ['']
endl = '\n\n'
chars = (string.letters + string.digits + string.punctuation)


# Custom Functions
def sendAcceptancemail(user_id, selected=True):
    # TODO: Yet to do
    return redirect(url_for('index'))


def is_image_url(url):
    check = url[:4]
    check2 = url[:5]
    if check == '.jpg' or check == '.png' or check2 == '.jpeg':
        ret = urllib2.urlopen(url)
        if url.status == 200:
            return True
        else:
            return False
    else:
        return False


@app.route('/', methods=['GET'])
def index():
    form = LoginForm()
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
    return render_template('forms/login.html',form=form)

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


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit() and (int(form.membertype.data) in [1, 2]) and (int(form.persontype.data) in [1.2]):
        passwordTemp = ''.join((random.choice(chars)) for x in range(app.config['PWS_SIZE']))
        first_fee = 9
        form.membertype.data = int(form.membertype.data)
        form.persontype.data = int(form.persontype.data)

        if form.membertype.data == 1 and form.fee.data in [3, 6, 30]:
            first_fee = 9
        elif form.membertype.data == 2 and form.fee.data in [25, 35, 100]:
            first_fee = 50
        else:
            flash('Fee Validation Error', 'error')
            return redirect(url_for('register'))
        if (form.persontype.data == 1):
            userObj = User(email=form.email.data, password=passwordTemp, membertype=form.membertype.data,
                           persontype=form.persontype.data, fee=form.fee.data,
                           company=form.company.data, firstname=form.firstname.data, lastname=form.lastname.data,
                           bday=form.bday.data, road=form.road.data, town=form.town.data, postcode=form.postcode.data,
                           phone=form.phone.data, mobile=form.mobile.data)
        else:
            userObj = User(email=form.email.data, password=passwordTemp, membertype=form.membertype.data,
                           persontype=form.persontype.data, fee=form.fee.data,
                           firstname=form.firstname.data, lastname=form.lastname.data,
                           bday=form.bday.data, road=form.road.data, town=form.town.data, postcode=form.postcode.data,
                           phone=form.phone.data, mobile=form.mobile.data)

        bankObj = Bankdetails()
        bankObj.account_holder = (form.firstname.data + " " + form.lastname.data).title()
        iban = form.iban.data.replace(" ", "")
        ibanobj = IBAN(iban)
        bic = ibanobj.bic.compact
        bankObj.blz = ibanobj.bank_code
        bankObj.account_no = ibanobj.account_code
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

        bic_visible = bic[:2] + 'X' * (digits - 4) + bic[-2:]
        bankObj.iban_visible = iban_visible
        bankObj.bic_visible = bic_visible
        bankObj.iban = EncodeAES(cipher, iban)
        bankObj.bic = EncodeAES(cipher, bic)
        bankObj.sepa_date = datetime.datetime.now
        rows = User.query.count()
        bankObj.sepa_ref = 'FraKeKueV'
        if not form.membertype.data:
            bankObj.sepa_ref += 'OrdM'
        else:
            bankObj.sepa_ref += 'FoeM'
        bankObj.sepa_ref += iban_visible[:6]
        bankObj.sepa_ref += str((5 - len(str(rows))) * '0') + str(rows)
        bankObj.user = userObj;
        db.session.add(userObj)
        db.session.add(bankObj)
        db.session.commit()

        # Sending Email
        msg = Message('Anmeldung Frankfurter Kelterei Kultur e.V.', sender=ADMINS[0], recipients=[userObj.email])
        msg.body = 'Halle ' + userObj.firstname + endl
        msg.body += 'Wir freuen über dein Interesse an der Frankfurter Kelterei Kultur! Du hast folgende Daten für die Anmeldungübermittelt. Aus Gründen des Datenschutzes, musst du diese Daten ein zweites Mal aktiv bestätigen (double opt-in):' + endl
        msg.body += 'Mitgliedsart: ' + userObj.membertype + endl
        msg.body += 'Firma:' + userObj.company + endl
        msg.body += 'Name: ' + (userObj.firstname + ' ' + userObj.lastname).title() + endl
        msg.body += 'Addresse: ' + userObj.road + endl + 'Zipcode: ' + userObj.postcode + endl + 'City: ' + userObj.town
        msg.body += 'Alter: ' + userObj.bday.strftime("%Y-%m-%d") + endl * 3
        msg.body += 'Kontodaten' + endl * 4 + '================='
        msg.body += 'Kontoinhaber :' + bankObj.account_holder + endl
        msg.body += 'IBAN :' + bankObj.iban_visible + endl
        msg.body += 'BIC :' + bankObj.bic_visible + endl
        msg.body += 'Monatsbeitrag :' + userObj.fee + '€' + endl
        msg.body += 'Please confirm the correctness of the data by clicking on the following link:' + endl
        confirmationSequence = ''.join((random.choice(chars)) for x in range(250))
        while Confirmation.query.filter_by(confirmation_code=confirmationSequence).count() > 0:
            confirmationSequence = ''.join((random.choice(chars)) for x in range(250))
        msg.body += app.config['BASE_URL'] + 'verifyaccount/' + confirmationSequence + endl
        msg.body += 'Löschen der Anmeldung ' + endl
        msg.body += app.config['BASE_URL'] + 'deleteaccount/' + confirmationSequence + endl
        msg.body += 'Beste Grüße'
        mail.send(msg)
        confirmobj = Confirmation(confirmation_code=confirmationSequence, user=userObj)
        db.session.add(confirmationSequence)
        db.session.commit()
        flash('Registered Id Successfully! Please verify using link sent to your email', 'success')
        return redirect(url_for('index'))
    return render_template('forms/register.html',form=form)


@app.route('/verifyaccount/<confirmation_sequence>', methods=['GET'])
def confirm_account(confirmation_sequence):
    confirmObj = Confirmation.query.filter_by(confirmation_code=confirmation_sequence)
    if confirmObj == None:
        # Invalid Code
        flash('Incorrect Validation Code', 'warning')
        return redirect(url_for('index'))
    confirmObj.user_id.confirmed = True
    db.session.add(confirmObj)
    db.session.commit()

    # Sending Email to the Admin
    msg = Message('Mitgliedsanmeldung von Website', sender=ADMINS[0], recipients=[ADMINS[0]])
    msg.body = 'Folgende Mitgliedsdaten wurden in unserem Anmeldformular eingegeben und per E-Mail bestätigt: '
    userObj = confirmObj.user_id
    bankObj = confirmObj.user_id.bankdetails.first()
    msg.body += 'Mitgliedsart: ' + userObj.membertype + endl
    msg.body += 'Firma:' + userObj.company + endl
    msg.body += 'Name: ' + (userObj.firstname + ' ' + userObj.lastname).title() + endl
    msg.body += 'Addresse: ' + userObj.road + endl + 'Zipcode: ' + userObj.postcode + endl + 'City: ' + userObj.town
    msg.body += 'Alter: ' + userObj.bday.strftime("%Y-%m-%d") + endl * 3
    msg.body += 'Kontodaten' + endl * 4 + '================='
    msg.body += 'Kontoinhaber :' + bankObj.account_holder + endl
    msg.body += 'IBAN :' + bankObj.iban_visible + endl
    msg.body += 'BIC :' + bankObj.bic_visible + endl
    msg.body += 'Monatsbeitrag :' + userObj.fee + '€' + endl
    msg.body += 'Mitglied in Verein aufnehmen:' + endl
    msg.body += app.config['BASE_URL'] + 'acceptuser/' + confirmation_sequence + endl
    msg.body += 'Antrag ablehnen::' + endl
    msg.body += app.config['BASE_URL'] + 'rejectuser/' + confirmation_sequence
    mail.send(msg)
    flash('User Validated Successfully!', 'success')
    return redirect(url_for('index'))  # Will Change this to profile Page


@app.route('/deleteaccount/<deletion_sequence>', methods=['GET'])
def delete_account(deletion_sequence):
    confirmObj = Confirmation.query.filter_by(confirmation_code=deletion_sequence)
    if confirmObj == None:
        # Invalid Code
        flash('Incorrect Validation Code', 'warning')
        return redirect(url_for('index'))
    confirmObj.user_id.confirmed = True
    db.session.delete(confirmObj.user_id)
    db.session.delete(confirmObj)
    db.session.commit()
    flash('User Deleted Successfully', 'warning')
    return redirect(url_for('index'))


@login_required
@app.route('/acceptuser/<confirmation_code>', methods=['GET'])
def accept_request(confirmation_code):
    user = current_user
    if user.admin is not True:
        flash('Admin Access required', 'warning')
        return redirect(url_for('logout'))
    confirmObj = Confirmation.query.filter_by(confirmation_code=confirmation_code).first()
    if confirmObj is None:
        flash('Wrong Acceptance Code', 'error')
        return redirect(url_for('index'))  # Or any Other
    confirmObj.user_id.confirmed = True
    sendAcceptancemail(confirmObj.user_id.id)
    db.session.add(confirmObj.user_id)
    db.session.delete(confirmObj)
    db.session.commit()
    flash('User Accepted to the Organisation', 'success')
    return redirect(url_for('index'))


@login_required
@app.route('/rejectuser/<confirmation_code>', methods=['GET'])
def reject_user(confirmation_code):
    user = current_user
    if user.admin is not True:
        flash('Admin Access required', 'warning')
        return redirect(url_for('logout'))
    confirmObj = Confirmation.query.filter_by(confirmation_code=confirmation_code).first()
    if confirmObj is None:
        flash('Wrong Acceptance Code', 'error')
        return redirect(url_for('index'))  # Or any Other

    sendAcceptancemail(confirmObj.user_id.id, False)
    db.session.delete(confirmObj.user_id)
    db.session.delete(confirmObj)
    db.session.commit()
    flash('User Rejected from the Organisation', 'warning')
    return redirect(url_for('index'))


@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    form = ForgotForm()
    if form.validate_on_submit():
        email = form.email.data
        userObj = User.query.filter_by(email=email)
        if userObj is None:
            flash('Wrong Email Id Provided! Please signup first.', 'error')
            return redirect(url_for('index'))
        reset_token = ''.join((random.choice(chars)) for x in range(250))
        forgotobj = Forgotpassword(forgot_code=reset_token, user=userObj)
        db.session.add(forgotobj)
        msg = Message('Password Reset Email.', sender=ADMINS[0], recipients=[email])
        msg.body = 'Click the Below Link to Reset Password ' + endl + app.config[
            'BASE_URL'] + '/resetpassword/' + reset_token;
        mail.send(msg)
        flash('Reset Password Mail sent to your Email Id!', 'success')
        return redirect(url_for('index'))
    return render_template('forms/forgot.html')


# Error handlers.

@app.errorhandler(500)
def internal_error(error):
    # db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.route('/test')
def test():
    form = RegisterForm()
    return render_template('forms/register.html',form=form)


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
