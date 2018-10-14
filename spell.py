from spellchecker import SpellChecker
from contextlib import suppress
import easygui
import sys

#Compiled using Python 3.6 to use Variable Annotation -- https://www.python.org/dev/peps/pep-0526/

try:
	#Set allowed file type to ".txt" and define SpellChecker
	fileType: str   = ".txt"
	fileEnd : str   = "*"+fileType
	spellChecker : SpellChecker  = SpellChecker()

	#Create pop-up for file selection
	#filePathList = "MyWords.txt"   
	filePathList: [] = easygui.fileopenbox("Select the "+fileType+" file you would like to spellcheck.",
	"Adam Klinger's File Spell Checker",fileEnd,fileEnd,"False")

	#Convert to String
	with suppress(TypeError):	
		filePathStr: str = ''.join(filePathList)

	#Check that a file was selected
	if (filePathList == None):
		print("\n**Error! No file has been selected to spellcheck! Aborting. **")	
		sys.exit()
		
	#Check that the file extension is allowed
	elif (filePathStr.endswith(fileType) == False):
		print("Selected file: "+filePathStr)
		print("\n** Invalid file extension! Only "+fileType+" is supported. Aborting. **") 

	#Process the file	
	else:
		print("\nAnalyzing File: "+ filePathStr+"\n")
		
		# Open the file, and read  into an array
		file: file = open(filePathStr,"r")
		fileContentList: [] = file.read().split(' ')
		file.close()
		
		#Print File Contents
		print("File Contents: ")
		print(fileContentList)
		print("\n")
		
		#Check that file is not blank and only contains A-Z,a-z, and spaces
		fileContentsStr: str = ''.join(fileContentList)
		if( (fileContentsStr).isalpha() == False):
			print("** Error! File contains non alpha characters. Aborting.. **\n")
			sys.exit()
		
		#Check for misspellings
		misspelled: [] = spellChecker.unknown(fileContentList)

		#Compute/display statistics
		wordTotal: int = len(fileContentList)
		wordTypo: int = len(misspelled)
		percTypo: str = "{:.1%}".format(wordTypo/wordTotal)

		print("Total words:      "+str(wordTotal) )
		print("Misspelled words: "+str(wordTypo) )
		print("=============================")
		print("Percentage Misspelled: "+ str(percTypo)+"\n")

		#Display misspelled words and possible corrections
		for word in misspelled:
			print("\nWord misspelled:     "+ word)
			print("Possible correction: "+ spellChecker.correction(word))
			#print(spellChecker.correction(word))
			#print(spellChecker.candidates(word))
except:
	raise