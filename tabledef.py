from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import (Column, Integer, Unicode, DateTime, ForeignKey,
    Boolean, Numeric, Time)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import * 
from sqlalchemy.orm import *

from flask import Flask 
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy.dialects.sqlite

# Set encryption
bcrypt = Bcrypt()
	
# create tables
app = Flask(__name__)

# SQLITE Database Location 
engine = create_engine('sqlite:///tutorial.db', echo=True)

SessionMaker = sessionmaker(bind=engine)
s = SessionMaker()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tutorial.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app,db)
 
########################################################################
class User(db.Model):
	__tablename__ = "users"
	id = Column(db.Integer, primary_key=True)
	username = db.Column(String)
	password = db.Column(String)

	def __init__(self, username, password):
		self.username = username
		self.password = bcrypt.generate_password_hash(password).decode('UTF-8')
	
	@classmethod
	def authenticate(cls, username, password):
		found_user = cls.query.filter_by(username = username).first()
		
		if found_user:
			authenticated_user = bcrypt.check_password_hash(found_user.password, password)
			if authenticated_user:
				return found_user
				
		return False


# create tables
db.Model.metadata.create_all(engine)
