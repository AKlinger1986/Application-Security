from spellchecker import SpellChecker
import easygui

# Set 
#msg 	= "Select the file you would like to spellcheck."
#title 	= "File Selection" 
#default   = "*.txt"
#filetypes = "*.txt"
#multiple  = "False"

spellChecker = SpellChecker()

spellFile = ""
# Create pop-up for file selection.
#spellFile    = "MyWords.txt"   
spellFile = easygui.fileopenbox("Select the .txt file you would like to spellcheck.",
"Adam's Text File Spell Checker","*.txt","*.txt","False")

if (spellFile == None):
	print("")
	print("** No file has been selected to spellcheck! Aborting. **")

else:
	print("")
	print("Analyzing File "+ str(spellFile))
	print("")
	# Read the file into an array
	file = open(''.join(spellFile),"r")
	fileContents = file.read().split(' ')
	file.close()

	# Check for misspellings
	misspelled = spellChecker.unknown(fileContents)

	# Compute counts
	wordTotal = len(fileContents)
	wordTypo  = len(misspelled)
	percTypo  = "{:.1%}".format(wordTypo/wordTotal)

	print("")
	print("Total words:      "+str(wordTotal) )
	print("Misspelled words: "+str(wordTypo) )
	print("=============================")
	print("Percentage Misspelled: "+ str(percTypo) )
	print("")

	# Display misspelled words and possible corrections
	for word in misspelled:
		print(" ")
		print("Word misspelled:     "+ word)
		print("Possible correction: "+ spellChecker.correction(word))
		#print(spellChecker.correction(word))
		#print(spellChecker.candidates(word))
		#.
	#print(file.read())
