import os

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
