import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from config import MIN_FEE
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(254),nullable=False)
    password = db.Column(db.String(400),nullable=False)

    membertype = db.Column(db.Integer,default=1) # 1 = Ordinary Member, Sustaining Member
    persontype = db.Column(db.Integer,default=2) #1 = Legal Person , 2 = Natural Person

    status = db.Column(db.Integer,default=3) #1 = Active,2=Inactive,3=Leaked,4=Deceased

    company = db.Column(db.String(300),nullable=True,default="No Company")

    firstname = db.Column(db.String(100),nullable=False)
    lastname = db.Column(db.String(100),nullable=False)

    bday = db.Column(db.DateTime,nullable=True)

    road = db.Column(db.String(500))
    town = db.Column(db.String(400))
    postcode = db.Column(db.Integer,nullable=False)

    phone = db.Column(db.Integer)
    mobile = db.Column(db.Integer,nullable=False)

    fee = db.Column(db.Integer, nullable=False, default=MIN_FEE)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)

    bankdetails = relationship("Bankdetails", uselist=False, back_populates="User")

class Bankdetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_holder = db.Column(db.String(200), nullable=False)
    account_number = db.Column(db.Integer, nullable=False,unique=True)
    blz = db.Column(db.Integer,nullable=False)
    iban = db.Column(db.String(50),unique=True)
    bic = db.Column(db.String(15))

    user_id = db.Column(db.Integer, ForeignKey('user.id'),nullable=False)
    user = relationship("User", back_populates="bankdetails")

class subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer,default=1) #1 = Ordinary Member ,2 = Conveyer Member
    fee = db.Column(db.Integer,nullable=False,default=MIN_FEE)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)