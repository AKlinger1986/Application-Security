from contextlib import suppress
from flask import *
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from spellchecker import *
from tabledef import *

import os
import easygui
import re
import logging
import logging.config

@app.route("/")
def home():
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

	#Obtain values from form and build User object
	username = request.form['username']
	password = request.form['password']	
	session['username'] = username
	user = User(username,password)
	
	if "Login" in request.form:
		#Check to see if the username and password exist in the database and match
		if User.authUser(username, password):
			app.logger.info('Login Successful. Username: '+username) 
			session['logged_in'] = True
			return home()
		else:
			app.logger.error('Login Failed. Username: '+username)
			return render_template('login.html', error='Error! Invalid username or password.')

	elif "Register" in request.form:			
		# Validate that the Username  contains only Alphanumeric characters
		if (username.isalnum() == False):
			app.logger.error('Registration Error (Allowed characters). Username: '+username)
			return render_template('login.html', error='Error! Username may only contain A-Z, a-z, 0-9.')
		elif (( len(username) < 4) | (len(username) > 20) ):
			app.logger.error('Registration Error (Length). Username: '+username)
			return render_template('login.html', error='Error! Username must be between 4 to 20 characters in length')

		# Validate the password chosen meets syntax rules
		validPwd, errorMsg = password_Quality_Check(password)
		if validPwd == False:
			app.logger.error('Registration Error (Password Quality). Username: '+username)
			return render_template('login.html', error=errorMsg)
		
		#Check to make sure the Username does not already exist
		if User.checkUser(username):				
			db.session.add(user)
			db.session.commit()
			app.logger.info('Registration Successful. Username: '+username+ 'added to database.')
			return render_template('login.html', error='Username '+username+' successfully registered.')
		else:
			app.logger.info('Registration Error (Already Registered). Username: '+username)
			return render_template('login.html', error='Username '+username+' already registered. Please select a new value.')
	return home()

@app.route("/spellcheck", methods=['POST'])
def do_spellCheck():
	username = session.get('username',None)

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
				app.logger.error('File Selection Error (No file selected) Username: '+username)
				return render_template('spellcheck.html',error='No file has been selected to spellcheck')
				
			#Check that the file extension is allowed
			elif (filePathStr.endswith(fileType) == False):
				app.logger.error('File Selection Error (Invalid extension) Username: '+username)
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
					app.logger.error('File Selection Error (Invalid Contents) Username: '+username)
					return render_template('spellcheck.html',error='File contains non alpha characters. Aborting.')
				
				app.logger.info('File spell-checked: '+filePathStr+'. Username: '+username)
				
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
		app.logger.info('Logout Successful. Username: '+username)
		return render_template('login.html', error='You have been logged out successfully.')
	else:
		pass
	return 
	
def password_Quality_Check(POST_PASSWORD):
	errorMsg = ("Password Rules not met. Length must be between 8-20 and contain at least"
		        " one Uppercase [A-Z], one Lowercase [a-z], one Number [0-9], "  
				" and one special character [@#$]. No other characters allowed.")
				
	if (len(POST_PASSWORD)<8):
		return False, errorMsg
	elif (len(POST_PASSWORD)>20):
		return False, errorMsg
	elif not re.search("[a-z]", POST_PASSWORD): 
		return False, errorMsg
	elif not re.search("[A-Z]", POST_PASSWORD): 
		return False, errorMsg
	elif not re.search("[0-9]", POST_PASSWORD): 
		return False, errorMsg
	elif not re.search("[_@#$]", POST_PASSWORD): 
		return False, errorMsg
	elif re.search("\s", POST_PASSWORD): 
		return False, errorMsg	 
	return True, ""
		
if __name__ == "__main__":
	#Configure Logger
	logger = logging.getLogger('werkzeug')
	handler = logging.FileHandler('access.log')
	formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

	handler.setFormatter(formatter)
	#handler.setLevel(logging.ERROR) 	
	logger.addHandler(handler)
	app.logger.addHandler(handler)
	
	app.secret_key = os.urandom(12)
	app.run(host='localhost', port=4000, ssl_context='adhoc',debug=True)
	#app.run(host='0.0.0.0', port=4000, debug=True)

	
