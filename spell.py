from flask import *
from sqlalchemy import * 
from sqlalchemy.orm import *
from tabledef import *			# Custom tabledef file
from passlib.hash import *
from spellchecker import SpellChecker
from contextlib import suppress

import hashlib
import os
import easygui

app = Flask(__name__)

# SQLITE Database Location 
engine = create_engine('sqlite:///tutorial.db', echo=True)

SessionMaker = sessionmaker(bind=engine)
s = SessionMaker()

@app.route("/")
def home():
	#session['logged_in'] = True
	
	# Display login page if user is not authenticated
	if not session.get('logged_in'):
		return render_template('login.html')
		
	# Display spellchecker page once authenticated
	else:
		return render_template('spellcheck.html')
	return
	
@app.route("/login", methods=['POST'])
def do_Login():
	error = None
	
	#Obtain values from form
	username = request.form['username']
	#password = sha256_crypt.encrypt(request.form['password'])
	password = request.form['password']

	if "Login" in request.form:
	
		#Check Credentials Against Database 			
		if(password_Check(username,password)) == true:	
			session['logged_in'] = True
			return home()
		else:
			return render_template('login.html', error='Login Error -- Invalid Username or Password.')
		
	elif "Register" in request.form:
	
		#Check to make sure the Username does not already exist is not already found
		if (username_Check(username)) == false:
		
			if(len(password)) < 8: 
				return render_template('login.html', error='Register Error -- Password value is too short. Please select a minimum length of 8.')
			else:				
				user = User(username,password)
				s.add(user)
				s.commit()
				return render_template('login.html', error='Username '+username+' successfully registered.')
		else:
			return render_template('login.html', error='Username '+username+' already registered. Please select a new value.')
	else:
		pass	
	return home()

@app.route("/spellcheck", methods=['POST'])
def do_spellCheck():
	if "OpenFile" in request.form:
		try:
			#Set allowed file type to ".txt" and define SpellChecker
			fileType      = ".txt"
			fileEnd       = "*"+fileType
			spellChecker  = SpellChecker()
			misspelledStr = ""
	
			#Create pop-up for file selection
			filePathList = easygui.fileopenbox("Select the "+fileType+" file you would like to spellcheck.",
			"Adam Klinger's File Spell Checker",fileEnd,fileEnd,"False")

			#Convert to String
			with suppress(TypeError):	
				filePathStr = ''.join(filePathList)

			#Check that a file was selected
			if (filePathList == None):
				return render_template('spellcheck.html',error='No file has been selected to spellcheck')
				
			#Check that the file extension is allowed
			elif (filePathStr.endswith(fileType) == False):
				return render_template('spellcheck.html',error='Invalid file extension! Only '+fileType+' is supported. Aborting.')

			#Process the file	
			else:			
				# Open the file, and read  into an array
				file = open(filePathStr,"r")
				fileContentList = file.read().split(' ')
				file.close()
					
				#Check that file is not blank and only contains A-Z,a-z, and spaces
				fileContentsStr = ''.join(fileContentList)
				if( (fileContentsStr).isalpha() == False):
					return render_template('spellcheck.html',error='File contains non alpha characters. Aborting.')
				
				#Check for misspellings
				misspelled = spellChecker.unknown(fileContentList)

				#Compute statistics
				wordTotal = len(fileContentList)
				wordTypo  = len(misspelled)
				percTypo  = "{:.1%}".format(wordTypo/wordTotal)

				#Display misspelled words and possible corrections
				for word in misspelled:
					misspelledStr = '\n\n'+misspelledStr +''+word+' -->'+spellChecker.correction(word)+'   '			
				
				#Return results to HTML
				return render_template('spellcheck.html', contentList=fileContentList, typoList=misspelledStr,
				                       totalCount=wordTotal, typoCount=wordTypo, typoPercent=percTypo)
		except:
			raise
	
	elif "Logout" in request.form:	
		session.pop('logged_in', None)
		return render_template('login.html', error='You have been logged out successfully.')
	else:
		pass
	return 
	
def username_Check(POST_USERNAME):
	query = s.query(User).filter(User.username.in_([POST_USERNAME]))
	result = query.first()
	if result:
		return true
	else:
		return false
 
def password_Check(POST_USERNAME,POST_PASSWORD):
	query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
	result = query.first()
	if result:
		return true
	else:
		return false

if __name__ == "__main__":
	app.secret_key = os.urandom(12)
	app.run(host='0.0.0.0', port=4000, debug=True)
    #app.run(host='0.0.0.0', port=4000,ssl_context='adhoc',debug=True)
