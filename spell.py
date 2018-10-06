from spellchecker import SpellChecker
from contextlib import suppress
import easygui
import sys

try:
	# Set default variable contents
	fileType      = ".txt"
	fileEnd       = "*"+fileType
	spellChecker  = SpellChecker()

	# Create pop-up for file selection.
	#filePathList = "MyWords.txt"   
	filePathList = easygui.fileopenbox("Select the "+fileType+" file you would like to spellcheck.",
	"Adam Klinger's File Spell Checker",fileEnd,fileEnd,"False")

	#Convert to String
	with suppress(TypeError):	
		filePathStr = ''.join(filePathList)

	#Check that a file was selected
	if (filePathList == None):
		print("\n**Error! No file has been selected to spellcheck! Aborting. **")	
		sys.exit()
		
	#Check that the file extension is correct
	elif (filePathStr.endswith(fileType) == False):
		print("Selected file: "+filePathStr)
		print("\n** Invalid file extension! Only "+fileType+" is supported. Aborting. **") 

	#Process the file	
	else:
		print("\nAnalyzing File: "+ filePathStr+"\n")
		
		# Read the file into an array
		file = open(filePathStr,"r")
		fileContentList = file.read().split(' ')
		file.close()
		
		#Print File Contents
		print("File Contents: ")
		print(fileContentList)
		print("\n")
		
		#Check that file is not blank and only contains characters
		fileContentsStr = ''.join(fileContentList)
		if( (fileContentsStr).isalpha() == False):
			print("** Error! File contains non alpha characters. Aborting.. **\n")
			sys.exit()
		
		# Check for misspellings
		misspelled = spellChecker.unknown(fileContentList)

		# Compute counts
		wordTotal = len(fileContentList)
		wordTypo  = len(misspelled)
		percTypo  = "{:.1%}".format(wordTypo/wordTotal)

		print("Total words:      "+str(wordTotal) )
		print("Misspelled words: "+str(wordTypo) )
		print("=============================")
		print("Percentage Misspelled: "+ str(percTypo)+"\n")

		# Display misspelled words and possible corrections
		for word in misspelled:
			print("\nWord misspelled:     "+ word)
			print("Possible correction: "+ spellChecker.correction(word))
			#print(spellChecker.correction(word))
			#print(spellChecker.candidates(word))
			#.
		#print(file.read())
except:
	raise