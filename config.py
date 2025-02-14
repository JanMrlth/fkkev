import os
from pass1 import PASSWORD, IBAN-KEY
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

WTF_CSRF_ENABLED = True
SECRET_KEY = os.urandom(24)

# Connect to the database
# Local DB
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
#
# SQLALCHEMY_DATABASE_URI = 'mysql://<username>:<password>@<hostname>:<port>/<db_name>'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False
MIN_FEE = 3

# email server
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = int(os.environ.get('MAIL_PORT', '465'))
MAIL_USE_TLS = int(os.environ.get('MAIL_USE_TLS', False))
MAIL_USE_SSL = int(os.environ.get('MAIL_USE_SSL', True))
MAIL_USERNAME = os.environ.get('MAIL_USERNAME','gude@frankfurterkeltereikultur.org')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD','<PASSWORD>')
MAIL_SENDER = os.environ.get('MAIL_SENDER', 'Admin<gude@frankfurterkeltereikultur.org>')

# administrator list
ADMINS = ['marloth@outlook.com']   # Add your admin URL Here
PROTOCOL = 'https://'
BASE_URL = PROTOCOL + 'www.frankfurterkeltereikultur.org/'

# AES
PWS_SIZE = 10
BLOCK_SIZE = 16
PADDING = '{'

DEFAULT_IMG = "https://stroops.com/wp-content/uploads/2016/11/placeholder-profile-male-500x500.png"

# Required For decrypting IBAN and BIC - AES 128 Bit Encryption Used
secret_key = '<IBAN-KEY>'

