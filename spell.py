from spellchecker import SpellChecker

# Define file location of words to spellcheck
spellFile    = "MyWords.txt"   
spellChecker = SpellChecker()

# Read the file into an array
file = open(spellFile,"r")
fileContents = file.read().split(' ')
file.close()

# Check for misspellings
misspelled = spellChecker.unknown(fileContents)

#print(fileContents)
for word in misspelled:
	print(" ")
	print("The following word was misspelled: "+ word)
	print("...possible correction(s) include: "+ spellChecker.correction(word))
	#print(spellChecker.correction(word))
	#print(spellChecker.candidates(word))
	#.
#print(file.read())