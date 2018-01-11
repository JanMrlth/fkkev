import datetime

from validators import md5

from config import MIN_FEE
from app import app,db

class User(db.Model):
    #login
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(254),unique=True,nullable=False)
    password = db.Column(db.String(400),nullable=False)
    authenticated = db.Column(db.Boolean, default=False)

    #admin
    admin = db.Coloumn(db.Boolean,default=False)

    #Membership Details
    membertype = db.Column(db.Integer,default=1) # 1 = Ordinary Member, 2 =Sustaining Member
    persontype = db.Column(db.Integer,default=2) #1 = Legal Person , 2 = Natural Person
    first_fee = db.Column(db.Integer,nullable=False)
    monthlyfee = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer,default=2) #1 = Active,2=Inactive,3=Leaked,4=Deceased
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    #Company
    company = db.Column(db.String(300),nullable=True,default="No Company") #No Company for Natural Person Valid for persontype 1

    #Personal
    firstname = db.Column(db.String(100),nullable=False)
    lastname = db.Column(db.String(100),nullable=False)
    bday = db.Column(db.DateTime,nullable=True) #only valid for personype = 2 (Natural Person)
    road = db.Column(db.String(500))
    town = db.Column(db.String(400))
    postcode = db.Column(db.Integer,nullable=False)
    phone = db.Column(db.Integer)
    mobile = db.Column(db.Integer,nullable=False)
    
    def avatar(self, size):   # https://en.gravatar.com/site/implement/ and https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vi-profile-page-and-avatars
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow) #on website

    bankdetails = db.relationship('Bankdetails', backref='user',lazy='dynamic')
    confirmed = db.Column(db.Boolean,default=False)
    confirmation = db.relationship("Confirmation", backref="User",lazy='dynamic')

class Bankdetails(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    account_holder = db.Column(db.String(200), nullable=False)
    account_no = db.Column(db.Integer,nullable=False)
    iban = db.Column(db.String(200), unique=True,nullable=False)
    iban_visible = db.Column(db.String(34),nullable=False) 
    bic = db.Column(db.String(200),nullable=False) #Autogenerated from IBAN(https://openiban.com/validate/<IBAN>?getBIC=true)(https://openiban.com/validate/DE89370400440532013000?getBIC=true)
    bic_visible = db.Column(db.String(34),nullable=False)
    sepa_accepted = db.Column(db.Boolean, default=False)
    sepa_date = db.Column(db.DateTime,default=datetime.datetime.utcnow)
    sepa_ref = db.Column(db.String(200),nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))


class Confirmation(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    confirmation_code = db.Column(db.String(300),nullable=False,unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
##############  Pictures & References  ##############  

### Table to link multiple pictures to multiple posts
#pictureUsage = db.Table('pictures',
#    db.Column('pic_id', db.Integer, db.ForeignKey('Picture.id'), primary_key=True),
#    db.Column('page_id', db.Integer, db.ForeignKey('page.id'), primary_key=True)
#)


#class Picture(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
#    ### do be finished
    

# Wrapper to add multiple pictures to Newselements and Reports
#class Post(db.Model): 
#    id = db.Column(db.Integer, primary_key=True)
#    post_type = db.Column(db.Integer)
#    ##################################################################
#    ### 1, Blog/News Entry
#    ##### Tree Realated
#    ### 2, PruningReport 
#    ### 3, PickingReport 
#    ### 4, TreeDocumentation
#    ##################################################################
#    pictures = db.relationship('Picture', secondary=pictures, lazy='subquery',
#        backref=db.backref('pages', lazy=True))


    
##############  Blog/News-Entrys  ##############  
# class Blogentry(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    date_created = db.Column(db.DateTime,default=datetime.datetime.utcnow)
#    title = db.Column(db.String(200), nullable=False)
#    content = db.Column(db.String(200), nullable=False)
#    user_id_author = db.Column(db.Integer,db.ForeignKey('user.id'))
   
##############  Trees and Reports  ##############  
#  class Tree(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    tpye = db.Column(db.String(200)
#    age = db.Column(db.Integer)
#    location = db.Column(db.String(200)
#    date_last_pruned = db.Column(db.DateTime,default=datetime.datetime.utcnow)
#    date_last_picked = db.Column(db.DateTime,default=datetime.datetime.utcnow)
#    
#    
#  class Pruningreport(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    title = db.Column(db.String(200), nullable=False)
#    body = db.Column(db.String(2000))                    
#    date_pruned = db.Column(db.DateTime,default=datetime.datetime.utcnow)
#    date_submitted = db.Column(db.DateTime,default=datetime.datetime.utcnow)
#    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))                         
#    tree_id = db.Column(db.Integer,db.ForeignKey('tree.id'))
#    
#  class Pickingreport(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    title = db.Column(db.String(200), nullable=False)
#    body = db.Column(db.String(2000))
#    weight_picked = db.Column(db.Integer)
#    date_picked = db.Column(db.DateTime,default=datetime.datetime.utcnow)
#    date_submitted = db.Column(db.DateTime,default=datetime.datetime.utcnow)
#    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))                         
#    tree_id = db.Column(db.Integer,db.ForeignKey('tree.id'))

# class subscription(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     type = db.Column(db.Integer,default=1) #1 = Ordinary Member ,2 = Conveyer Member
#     fee = db.Column(db.Integer,nullable=False,default=MIN_FEE)
#     created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
#     updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)
