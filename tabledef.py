from sqlalchemy import *
from sqlalchemy.ext.declarative import *
from sqlalchemy.orm import *
from sqlalchemy.dialects.sqlite import *

from flask import Flask
from flask_wtf import CSRFProtect 
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

debug = False

# SQLITE Database Location 
dbLocation = 'sqlite:///users.db'

# Set encryption
bcrypt = Bcrypt()
	
# Define app with database
app = Flask(__name__)

# Protect from Cross-Site Request Forgery
csrf = CSRFProtect(app)
csrf.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = dbLocation
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = debug

# Create SQL engine
engine = create_engine(dbLocation, echo=debug)

db = SQLAlchemy(app)
migrate = Migrate(app,db)
 
class User(db.Model):
	__tablename__ = "users"
	id = Column(db.Integer, primary_key=True)
	username = db.Column(String)
	password = db.Column(String)

	def __init__(self, username, password):
		self.username = username
		self.password = bcrypt.generate_password_hash(password).decode('UTF-8')
	
	@classmethod
	def checkUser(cls, username):
		found_user = cls.query.filter_by(username = username).first()
		
		if found_user:
			return False
		return True
	
	@classmethod
	def authUser(cls, username, password):
		found_user = cls.query.filter_by(username = username).first()
		
		if found_user:
			authenticated_user = bcrypt.check_password_hash(found_user.password, password)
			if authenticated_user:
				return found_user			
		return False

# create tables
db.Model.metadata.create_all(engine)
