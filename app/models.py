import datetime

from config import MIN_FEE
from app import app,db

class User(db.Model):
    #login
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(254),nullable=False)
    password = db.Column(db.String(400),nullable=False)
    authenticated = db.Column(db.Boolean, default=False)

    #Membership Details
    membertype = db.Column(db.Integer,default=1) # 1 = Ordinary Member, 2 =Sustaining Member
    persontype = db.Column(db.Integer,default=2) #1 = Legal Person , 2 = Natural Person
    first_fee = db.Column(db.Integer,nullable=False)
    fee = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer,default=2) #1 = Active,2=Inactive,3=Leaked,4=Deceased

    #Company
    company = db.Column(db.String(300),nullable=True,default="No Company") #No Company for Natural Person Valid for persontype 1

    #Personal
    firstname = db.Column(db.String(100),nullable=False)
    lastname = db.Column(db.String(100),nullable=False)
    bday = db.Column(db.DateTime,nullable=True)
    road = db.Column(db.String(500))
    town = db.Column(db.String(400))
    postcode = db.Column(db.Integer,nullable=False)
    phone = db.Column(db.Integer)
    mobile = db.Column(db.Integer,nullable=False)

    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)

    bankdetails = db.relationship('Bankdetails', backref='user',lazy='dynamic')

class Bankdetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_holder = db.Column(db.String(200), nullable=False)
    iban = db.Column(db.String(200), unique=True,nullable=False)
    iban_visible = db.Column(db.String(34),nullable=False)
    blz = db.Column(db.Integer,nullable=False)
    bic = db.Column(db.String(200),nullable=False) #Autogenerated from IBAN(https://openiban.com/validate/<IBAN>?getBIC=true)(https://openiban.com/validate/DE89370400440532013000?getBIC=true)
    bic_visible = db.Column(db.String(34),nullable=False)
    sepa_date = db.Column(db.DateTime,default=datetime.datetime.utcnow)
    sepa_ref = db.Column(db.String(200),nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

# class subscription(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     type = db.Column(db.Integer,default=1) #1 = Ordinary Member ,2 = Conveyer Member
#     fee = db.Column(db.Integer,nullable=False,default=MIN_FEE)
#     created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
#     updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)