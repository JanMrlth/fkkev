import os,pass1
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

WTF_CSRF_ENABLED = True
SECRET_KEY = os.urandom(24)

# Connect to the database
SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@localhost:3306/fkkevdb'
# SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
# SQLALCHEMY_DATABASE_URI = 'mysql://<username>:<password>@<hostname>:<port>/<db_name>'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False
MIN_FEE = 3

# email server
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = int(os.environ.get('MAIL_PORT', '465'))
MAIL_USE_TLS = int(os.environ.get('MAIL_USE_TLS', False))
MAIL_USE_SSL = int(os.environ.get('MAIL_USE_SSL', True))
MAIL_USERNAME = os.environ.get('MAIL_USERNAME','sanudatta12@gmail.com')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD',pass1.PASSWORD)
MAIL_SENDER = os.environ.get('MAIL_SENDER', 'Admin<sanudatta12@gmail.com>')

# administrator list
ADMINS = ['sanudatta12@gmail.com']
PROTOCOL = 'http://'
BASE_URL = PROTOCOL + 'www.xyz.com/'

# AES
PWS_SIZE = 10
BLOCK_SIZE = 16
PADDING = '{'

secret_key = 'KdHAkFFhXXvkwMoG'
