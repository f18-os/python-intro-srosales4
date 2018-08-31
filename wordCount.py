import sys        # command line arguments
import re         # regular expression tools

# take in the two arguments
textFname = sys.argv[1]
outputFname = sys.argv[2]

# stats
words  = []

#dictionary of words with appearance
wordAppearance = dict()

# attempt to open input file
with open(textFname, 'r') as inputFile:
    for line in inputFile:

        line = line.strip()

        tokens = re.compile('\W+')
        listOfTokens = tokens.split(line.lower() )

        for t in listOfTokens:
        	newWord = str(t)
        	words.append(newWord)

# add words to hashmap with the number of times they show up
for i in range(0, len(words) ):
	wString = str(words[i])
	wString.strip()
	wString = re.sub(r'[^\w\s]','',wString)

	if wString == '':
		continue
	else:
		if wString not in wordAppearance:
			wordAppearance[wString] = 0
		if wString in wordAppearance:
			wordAppearance[wString] += 1

# write the hashmap to the output file
outputFile = open(outputFname, 'w')

for key,val in sorted(wordAppearance.items() ):
	outputFile.write("%s %d\n" % (key, val) )
	# print(key, "=>", val)

outputFile.close()
