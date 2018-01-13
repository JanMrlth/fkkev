#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
# from flask_wtf.csrf import CSRFProtect
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
# csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.session_protection = "strong"

mail = Mail(app)
manager = Manager(app)
bcrypt = Bcrypt(app)
manager.add_command('db', MigrateCommand)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
from app import models
from app import views