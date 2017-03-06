import PIL
import pytesseract
from wand.image import Image

#some primitive spellcheck for tesseract
#strA is considered the "canonical" string -- the correct one
def stringSimilarityScore(strA, strB):
	wordsA = strA.split()
	wordsB = strB.split()
	
	#returns 0 if the number of words is different
	matchingLetters = 0
	if len(wordsA)==len(wordsB):
		for j in range(0,min(len(wordsA),len(wordsB))):
			if wordsA[j]==wordsB[j]:
				matchingLetters+=len(wordsA[j])
			else:
				for i in range(0,min(len(wordsA[j]),len(wordsB[j]))):
					if wordsA[j][i]==wordsB[j][i]:
						matchingLetters+=1
		
	return matchingLetters/float(len(strA))

# checks two fields - 'The Ultimate QT Infograph' and 'Version 3'
chartFilename = 'qt.png'
baseDimensions = {'x': 3828, 'y': 4587}

baseTitleLocation = {'x': 716, 'y': 234}
baseTitleDimensions = {'x': 2390, 'y': 234}
baseTitleString = 'The Ultimate QT Infograph'

baseVersionLocation = {'x': 3404, 'y': 236}
baseVersionDimensions = {'x': 416, 'y': 112}
baseVersionString = 'Version 3'

#first use imagemagick to crop two separate images out of the chart
with Image(filename=chartFilename) as chartImage:
	expansionRatio = chartImage.width / float(baseDimensions['x'])
	
	dimensions = {'x': int(baseDimensions['x']*expansionRatio), 'y': int(baseDimensions['y']*expansionRatio)}

	#generate the expansion-adjusted dimensions and coordinates
	#TODO: there must be a cleaner way of doing this...
	titleLocation   = {'x': int(baseTitleLocation['x']*expansionRatio), 'y': int(baseTitleLocation['y']*expansionRatio)}
	titleDimensions = {'x': int(baseTitleDimensions['x']*expansionRatio), 'y': int(baseTitleDimensions['y']*expansionRatio)}
	
	versionLocation   = {'x': int(baseVersionLocation['x']*expansionRatio), 'y': int(baseVersionLocation['y']*expansionRatio)}
	versionDimensions = {'x': int(baseVersionDimensions['x']*expansionRatio), 'y': int(baseVersionDimensions['y']*expansionRatio)}

#generate the title image
with Image(filename=chartFilename) as chartImage:
	chartImage.format = 'png'
	chartImage.crop(titleLocation['x'],titleLocation['y']-titleDimensions['y'],titleLocation['x']+titleDimensions['x'],titleLocation['y'])
	chartImage.save(filename=chartFilename+'-'+'title.png')
	
#generate the version image
with Image(filename=chartFilename) as chartImage:
	chartImage.format = 'png'
	chartImage.crop(versionLocation['x'],versionLocation['y']-versionDimensions['y'],versionLocation['x']+versionDimensions['x'],versionLocation['y'])
	chartImage.save(filename=chartFilename+'-'+'version.png')

#now run Tesseract on both of the subimages
readTitleString   = pytesseract.image_to_string(PIL.Image.open(chartFilename+'-'+'title.png'))
readVersionString = pytesseract.image_to_string(PIL.Image.open(chartFilename+'-'+'version.png'))

#run spellcheck on the tesseract results
similarityLimit = 0.7

titleSimilarityScore   = stringSimilarityScore(baseTitleString,readTitleString)
versionSimilarityScore = stringSimilarityScore(baseVersionString,readVersionString)

#confirm that the chart title and version number are correct, according to Tesseract
if titleSimilarityScore>similarityLimit and versionSimilarityScore>similarityLimit:
	print("YES")
