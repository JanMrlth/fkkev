# coding=utf-8
import base64
import logging
import random
import string
import urllib2
from Crypto.Cipher import AES
from functools import wraps
from logging import Formatter, FileHandler
from flask import render_template, request, redirect, url_for, flash, g
from flask_login import login_user, login_required, current_user, logout_user
from flask_mail import Message
from schwifty import IBAN

from app import app, db, mail, bcrypt, login_manager
from app.forms import *
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
endl = '<br>'
chars = (string.letters + string.digits)


# Custom Functions
def sendAcceptancemail(user_id, selected=True):
    # TODO: Yet to do
    return redirect(url_for('index'))


def is_image_url(url):
    check = url[-4:]
    check2 = url[-5:]
    if check == '.jpg' or check == '.png' or check2 == '.jpeg':
        ret = urllib2.urlopen(url).getcode()
        if ret == 200:
            return True
        else:
            return False
    else:
        return False

def is_admin(f):
    @wraps(f)
    def _decorator(request, *args, **kwargs):
        if g.user is not None and  not g.admin:
            flash('Please Login with a Admin ID!','error')
            return redirect(url_for('profile', next=request.url))
        elif g.user is None:
          return redirect(url_for('index'),next=request.url)
        return f(*args, **kwargs)
    return _decorator

@login_manager.user_loader
def get_user(ident):
  return User.query.get(int(ident))


@app.route('/', methods=['GET'])
def index():
    user = current_user
    if user.is_authenticated and user.authenticated:
        return redirect(url_for('profile'))
    form = LoginForm()
    return render_template('forms/login.html', form=form)

@login_required
@app.route('/profile',methods=['GET'])
def profile():
    if current_user.is_authenticated:
        return render_template('pages/show-user.html',user=current_user)
    else:
        flash('Please Login again!','warning')
        return redirect(url_for('index'))

@login_required
@app.route('/editprofile',methods=['GET','POST'])
def update_profile():
    if current_user.is_authenticated:
        form = UpdateProfile()
        if form.validate_on_submit():
            user = current_user
            user.firstname = form.firstname.data if form.firstname.data else user.firstname
            user.lastname = form.lastname.data if form.lastname.data else user.lastname
            user.bday = form.bday.data if form.bday.data else user.bday
            user.road = form.road.data if form.road.data else user.road
            user.postcode = form.postcode.data if form.postcode.data else user.postcode
            user.town = form.town.data if form.town.data else user.town
            user.company = form.company.data if form.company.data else user.company
            user.phone = form.phone.data if form.phone.data else user.phone
            user.mobile = form.mobile.data if form.mobile.data else user.mobile
            if form.image_url and  not is_image_url(form.image_url.data):
                    print form.image_url.data
                    flash('Image URL Invalid','error')
                    return redirect(url_for('update_profile'))
            user.image_url = form.image_url.data if form.image_url.data else user.image_url

            if form.password.data and current_user.is_authenticated:
                user.password = bcrypt.generate_password_hash(form.password.data)
                flash('Password Updated','success')
            db.session.add(current_user)
            db.session.commit()
            flash('Updated Profile Successfully','success')
        else:
            flash('Incorrect or Invalid Details','warning')
        return render_template('forms/edit-user.html', user=current_user,form=form)
    else:
        return redirect(url_for('index'))
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        userData = User.query.filter_by(email=form.email.data).first()
        if userData is None:
            flash('Invalid Email Provided', 'error')
            return redirect(url_for('index'))
        if bcrypt.check_password_hash(userData.password,form.password.data):
            userData.authenticated = True
            db.session.add(userData)
            db.session.commit()
            print 'In'
            login_user(userData, remember=True)
            return redirect(url_for('profile'))
        else:
            flash('Password Incorrect','error')
            return redirect(url_for('index'))
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
    flash('Logged out successfully', 'success')
    return redirect(url_for('logout_check'))


@app.route('/checkLogout', methods=['GET'])
def logout_check():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for('index'))
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit() and (int(form.membertype.data) in [1,2]) and (int(form.persontype.data) in [0,1,2]):
        passwordReal = ''.join((random.choice(chars)) for x in range(app.config['PWS_SIZE']))
        passwordTemp = bcrypt.generate_password_hash(passwordReal)
        form.membertype.data = int(form.membertype.data)
        form.persontype.data = int(form.persontype.data)
        image_url=None
        if form.image_url and is_image_url(form.image_url.data):
            image_url = form.image_url.data
        if (form.persontype.data == 1):
            userObj = User(email=form.email.data, password=passwordTemp, membertype=form.membertype.data,
                           persontype=form.persontype.data, fee=form.fee.data,
                           company=form.company.data, firstname=form.firstname.data, lastname=form.lastname.data,
                           bday=form.bday.data, town=form.town.data,road=form.road.data ,postcode=form.postcode.data,
                           phone=form.phone.data, mobile=form.mobile.data,image_url=image_url)
        else:
            userObj = User(email=form.email.data, password=passwordTemp, membertype=form.membertype.data,
                           persontype=form.persontype.data, fee=form.fee.data,
                           firstname=form.firstname.data, lastname=form.lastname.data,
                           bday=form.bday.data, town=form.town.data,road=form.road.data, postcode=form.postcode.data,
                           phone=form.phone.data, mobile=form.mobile.data,image_url=image_url)

        userObj.town = (userObj.town).encode('utf-8')
        bankObj = Bankdetails()
        bankObj.account_holder = (form.firstname.data + " " + form.lastname.data).title()
        iban = form.iban.data.replace(" ", "")
        ibanobj = IBAN(iban)
        bic = form.bic.data
        bankObj.blz = ibanobj.bank_code
        bankObj.account_no = ibanobj.account_code
        digits = len(iban)
        if not (digits >= 16 and digits <= 34):
            flash('Invalid IBAN Number', 'error')
            return redirect(url_for('register'))
        iban_visible = iban[:6] + 'X' * (digits - 10) + iban[-4:]
        digits = len(bic)
        bic_visible = bic[:2] + 'X' * (digits - 4) + bic[-2:]
        bankObj.iban_visible = iban_visible
        bankObj.bic_visible = bic_visible
        bankObj.iban = EncodeAES(cipher, iban)
        bankObj.bic = EncodeAES(cipher, bic)
        rows = User.query.count()
        bankObj.sepa_ref = 'FraKeKueV'
        if not form.membertype.data:
            bankObj.sepa_ref += 'OrdM'
        else:
            bankObj.sepa_ref += 'FoeM'
        bankObj.sepa_ref += iban_visible[:6]
        bankObj.sepa_ref += str((5 - len(str(rows))) * '0') + str(rows)
        userObj.bankdetails.append(bankObj)
        db.session.add(userObj)
        db.session.add(bankObj)

        # Sending Email
        msg = Message('Anmeldung Frankfurter Kelterei Kultur e.V.', sender=ADMINS[0], recipients=[userObj.email])

        body = 'Halle ' + userObj.firstname + endl
        body += 'Login Details:' + endl + 'Email:' + userObj.email + endl + 'Password: ' + passwordReal + endl*3
        body += ('Wir freuen uber dein Interesse an der Frankfurter Kelterei Kultur! Du hast folgende Daten fur die Anmeldungubermittelt. Aus Grunden des Datenschutzes, musst du diese Daten ein zweites Mal aktiv bestatigen (double opt-in):') + endl
        body += ('Mitgliedsart: ' + str(userObj.membertype)) + endl
        if userObj.company:
            body += 'Firma:' + userObj.company + endl
        body += 'Name: ' + (userObj.firstname + ' ' + userObj.lastname).title() + endl
        body += 'Addresse: ' + userObj.town.decode("windows-1252").encode('utf-8') + endl + 'Zipcode: ' + str(userObj.postcode) + endl
        body += 'Alter: ' + userObj.bday.strftime("%Y-%m-%d") + endl * 3
        body += 'Kontodaten' + endl * 4 + '================='
        body += 'Kontoinhaber :' + bankObj.account_holder + endl
        body += 'IBAN :' + bankObj.iban_visible + endl
        body += 'BIC :' + bankObj.bic_visible + endl
        body += 'Monatsbeitrag:' + str(userObj.fee) + 'Euros' + endl
        body += 'Please confirm the correctness of the data by clicking on the following link:' + endl
        confirmationSequence = ''.join((random.choice(chars)) for x in range(50))
        while Confirmation.query.filter_by(confirmation_code=confirmationSequence).count() > 0:
            confirmationSequence = ''.join((random.choice(chars)) for x in range(50))
        body += app.config['BASE_URL'] + 'verifyaccount/' + confirmationSequence + endl*3
        body += 'Loschen der Anmeldung ' + endl
        body += app.config['BASE_URL'] + 'deleteaccount/' + confirmationSequence + endl*3
        body += 'Beste Grube'
        msg.html = body.encode('utf-8')
        confirmobj = Confirmation(confirmation_code=confirmationSequence)
        db.session.add(confirmobj)
        userObj.confirmation.append(confirmobj)
        db.session.commit()
        mail.send(msg)
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
    body = 'Folgende Mitgliedsdaten wurden in unserem Anmeldformular eingegeben und per E-Mail bestatigt: '
    userObj = confirmObj.user_id
    bankObj = confirmObj.user_id.bankdetails.first()
    body += 'Mitgliedsart: ' + str(userObj.membertype) + endl
    if userObj.company:
        body += 'Firma:' + userObj.company + endl
    body += 'Name: ' + (userObj.firstname + ' ' + userObj.lastname).title() + endl
    body += 'Addresse: ' + userObj.town + endl + 'Zipcode: ' + str(userObj.postcode) + endl
    body += 'Alter: ' + userObj.bday.strftime("%Y-%m-%d") + endl * 3
    body += 'Kontodaten' + endl * 4 + '================='
    body += 'Kontoinhaber :' + bankObj.account_holder + endl
    body += 'IBAN :' + bankObj.iban_visible + endl
    body += 'BIC :' + bankObj.bic_visible + endl
    body += 'Monatsbeitrag :' + str(userObj.fee) + 'Euros' + endl
    body += 'Mitglied in Verein aufnehmen:' + endl
    body += app.config['BASE_URL'] + 'acceptuser/' + confirmation_sequence + endl
    body += 'Antrag ablehnen::' + endl
    body += app.config['BASE_URL'] + 'rejectuser/' + confirmation_sequence
    msg.html = body.encode('utf-8')
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
        reset_token = ''.join((random.choice(chars)) for x in range(50))
        forgotobj = Forgotpassword(forgot_code=reset_token, user_id=userObj)
        db.session.add(forgotobj)
        msg = Message('Password Reset Email.', sender=ADMINS[0], recipients=[email])
        msg.body = 'Click the Below Link to Reset Password ' + endl + app.config[
            'BASE_URL'] + '/resetpassword/' + reset_token
        mail.send(msg)
        flash('Password Reset Email sent to your Email Id!', 'success')
        return redirect(url_for('index'))
    return render_template('forms/forgot.html',form=form)


@app.route('/resetpassword/<reset_token>',methods=['GET','POST'])
def reset_pass(reset_token):
    form = ResetForm()
    if request.method == 'GET':
        forgotObj = Forgotpassword.query.filter_by(forgot_code=reset_token)
        if forgot is None:
            flash('Invalid Reset Token!','error')
            return redirect(url_for('index'))
        return render_template('forms/final_reset.html',reset_token=reset_token,form=form)
    elif form.validate_on_submit():
        forgotObj = Forgotpassword.query.filter_by(forgot_code=reset_token)
        if forgot is None:
            flash('Invalid Reset Token!', 'error')
            return redirect(url_for('index'))
        forgotObj.user_id.password = bcrypt.generate_password_hash(form.password.data)
        db.session.add(forgotObj)
        db.session.commit()
        flash('Password Updated Successfully','success')
        return redirect(url_for('index'))

@login_required
@app.route('/bankprofile',methods=['GET'])
def bank_profile():
    if current_user.is_authenticated and current_user.authenticated:
        return render_template('pages/show-bank.html',user=current_user)
    return redirect(url_for('index'))

@login_required
@app.route('/editbank',methods=['GET','POST'])
def edit_bank_profile():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    form = EditBank()
    if form.validate_on_submit():
        user = current_user
        user.bankdetails[0].account_no = form.account_no.data
        user.bankdetails[0].account_holder = form.account_holder.data
        iban = form.iban.data
        iban = form.iban.data.replace(" ", "")
        bic = form.bic.data
        digits = len(iban)
        iban_visible = iban[:6] + 'X' * (digits - 10) + iban[-4:]
        digits = len(bic)
        bic_visible = bic[:2] + 'X' * (digits - 4) + bic[-2:]
        user.bankdetails[0].iban_visible = iban_visible
        user.bankdetails[0].iban = EncodeAES(cipher,iban)
        user.bankdetails[0].bic_visible = bic_visible
        user.bankdetails[0].bic = EncodeAES(cipher,bic)
        db.session.add(user)
        db.session.commit()
        flash('Bank Details update successfully','success')
    return render_template('forms/edit-bank.html',form=form,user=current_user)

@login_required
@is_admin
@app.route('/memberslist')
def admin_list():
    user = current_user
    if user.is_authenticated and user.admin:
        #2nd Verification after decorator
        user_all = User.query.all()
        return render_template('pages/admin-landing.html',user_all=user_all,user=current_user)
    else:
        flash('Re Login as Admin!','error')
        return redirect(url_for('profile'))

@login_required
@is_admin
@app.route('/getmemberprofile/<user_id>',methods=['GET'])
def get_member_profile(user_id):
    userobj = User.query.filter_by(id=15).first()
    if userobj is None:
        flash('Member Profile ID Invalid')
        return redirect(url_for('admin_list'))
    return render_template('pages/show-user.html',user=userobj,next="/memberslist")

@login_required
@is_admin
@app.route('/makeadmin/<user_id>')
def make_admin(user_id):
    user = User.query.filter_by(id=user_id)
    if user is not None:
        user.admin = True
        db.session.add(user)
        db.session.commit()
        flash('Admin Account Added For Profile Id'+str(user.id),'success')
        return redirect(url_for('admin_list'))
    flash('User Id Invalid','error')
    return redirect(url_for('admin_list'))

# Error handlers.

@app.errorhandler(500)
def internal_error(error):
    # db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@login_required
@app.route('/test')
def test():
    return render_template('pages/admin-landing.html',user=current_user)


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
