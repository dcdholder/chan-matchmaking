#it looks like the coordinate is simply a tuple
#a cell may have the color 'unselected', 'invalid', or one of six others

#TODO: determine whether color testing needs some "fuzziness" by testing with multiple jpeg qualities

import yaml

class ColorDataField:
	__unselectedColor   = 0xFFFFFF
	__singleSelectIndex = 2
	__neutralIndex      = 3
	__colorNames = ['pink', 'blue', 'green', 'yellow', 'orange', 'red']
	__colorCodes = [0xFF00FF, 0x0000FF, 0x00FF00, 0xFFFF00, 0xFF7200, 0xFF0000]
	__importanceScoreMapping = [-1.0, -0.5, 0.0, 0.33, 0.67, 1.0]
	__traitScoreMapping      = [-1.0, -0.5, 0.0, 0.5, 1.0]
	
	def __init__(self, colorCode, isYou, isMulticolor)
		self.isYou        = isYou #tells us whether this is a trait or importance score
		self.isMulticolor = isMulticolor
		self.isSelected   = False
		self.colorScore   = colorScoreFromCode(colorCode) #TODO: would be nice to have an alternate constructor for colorIndex rather than colorCode...
		
		if !isYou and !isMulticolor
			raise ValueError('Them cells are always multicolor.')
		
	def colorScoreFromCode(colorCode)
		for i in range(0,len(colorValues))
			if __colorCodes[i]==colorCode
				self.isSelected = True
				return i
		
		if colorCode==__unselectedColor
			if isMulticolor
				self.isSelected = True
				return __neutralIndex #for multicolor cells, an unfilled cell can be assumed yellow
			else
				self.isSelected = False
				return 0
		
		raise ValueError('Could not map color code ' + colorCode + 'to a valid color score.')
		
	def singleColorTraitSelected()
		return __colorNames[self.colorScore]=='green'
		
	def yourTraitVsTheirImportance(theirImportance)
		if !isYou
			raise ValueError('Must be executed on a You color data field.')
		
		if isMulticolor
			return multiColorYouScoring(theirImportance.colorScore)
		else
			return singleColorYouScoring(singleColorTraitSelected(),theirImportance.colorScore)
		
	def multiColorYouScoring(importanceScoreIndex) #min possible score is 0, max possible score is 1.0	
		importanceScore = __importanceScoreMapping[importanceScoreIndex]
		traitScore      = __traitScoreMapping[self.colorScore]

		scoreDelta = importanceScore - traitScore
		if importanceScore*traitScore > 0: #true if they're the same sign
			scoreDelta=abs(scoreDelta)
		else:
			scoreDelta=-abs(scoreDelta)

		finalScore = scoreDelta * importanceScore #increases importance of delta for extreme scores, makes score 0 if importance is neutral
		finalScore = (finalScore+1.0) / 2.0       #normalize final answer to a range between 0 and 1.0
	
		return finalScore
	
	def singleColorYouScoring(traitIsSelected,importanceScoreIndex) #trait score is either 1.0 or 0.0, no in-betweens
		if traitIsSelected:
			traitScoreIndex = len(__traitScoreMapping)-1 #just set to either extreme trait score
		else:
			traitScoreIndex = 0
		
		return multiColorYouScoring(traitScoreIndex,importanceScoreIndex)

#Cells
class Cell: #an indivisble component of an image element
	def __init__(self,label,pixelMap,coordinates)
		self.pixelMap       = pixelMap
		self.coordinates    = coordinates
		self.colorDataField = self.__setColor()
	
	def __setColor() #just select color from the given coordinates -- is different for square cell
		#TODO: figure out how to handle invalid cell colors
		centerPixelCoordinates = self.__getCenterPixel()
		
		rgb          = self.pixelMap.getPixel(centerPixelCoordinates)
		hexColorCode = '#{:02x}{:02x}{:02x}'.format(rgb[0],rgb[1],rgb[2])
		
		return ColorDataField(hexColorCode)
	
	def __getCenterPixel(): #the default is just to return the 'coordinates' -- overriden in SquareCell, but not PictographicCell
		return coordinates
	
	def fillCell(coordinates, colorCode):
		pass	

#TODO: allow for multiple color sampling points, since users don't fill in pictographic cells all the same way
class PictographicCell(Cell): #subclass is really just for readability right now
	def __init__(self,label,pixelMap,coordinates)
		super().__init__(self,label,pixelMap,coordinates)

class SquareCell(Cell):
	def __init__(self,label,pixelMap,coordinates,size)
		self.size = size
		super().__init__(self,label,pixelMap,coordinates)
	
	def genRow(pixelMap,baseCoordinates,cellSize,numCells) #create a horizontal row of cells
		cells = []
		for i in range(0,numCells)
			cellCoordinates[0] = baseCoordinates[0] + cellSize[0] * i
			cellCoordinates[1] = baseCoordinates[1]
			cells[i] = SquareCell(pixelMap,cellCoordinates,cellSize)
			
		return cells
	
	def genSquare(pixelMap,coordinates,cellSize,cellDimensions)
		for j in range(0,cellDimensions) #assume all 2D cell arrays are square
			for i in range(0,cellDimensions)
				cells[j][i] = SquareCells(pixelMap,cellCoordinates,cellSize)
	
	def __getCenterPixel()
		middleX = self.coordinates[0] + self.size[0] / 2
		middleY = self.coordinates[1] + self.size[1] / 2

		return (middleX, middleY)

#Elements
class Element: #a chart element is a collection of individual cells, has a non-configurable weighting within a category
	def __init__(self, elementYaml, pixelMap, isYou)
		self.elementYaml = elementYaml
		self.name        = elementYaml['name']
		self.weighting   = elementYaml['weighting']
		self.pixelMap    = pixelMap
		self.isYou       = isYou #specify whether to get 'You' or 'Them'
		self.cells       = self.__getCells()

	def __youOrThemString():
		if self.isYou:
			return 'you'
		else:
			return 'them'

	def __coordinatesFromString(coordinates):
		coordsAsStringArray = coordinates.split("x")
		coordsAsIntTuple    = tuple(list(map(int,coordsAsStringArray)))

	def getYouAndThemElementsFromYaml(elementYaml)
		pass

	def __getCells():
		pass

#TODO: figure out how abstract classes work in Python
class CheckboxSet(Element):
	def __init__(self, elementYaml, pixelMap, isYou)
		super().__init__(self,elementYaml,pixelMap,isYou)

class PictographicCheckboxSet(CheckboxSet):
	def __init__(self, elementYaml, pixelMap, isYou)
		super().__init__(self,elementYaml,pixelMap,isYou)
	
	def __getCells():
		cells = {}
		for cellYaml in elementYaml['checkboxes']
			label           = cellYaml['label']
			cellCoordinates = cellYaml['coordinates'][__youOrThemString()]
			cells[cellYaml['label']] = PictographicCell(self,label,pixelMap,cellCoordinates)

class SquareCheckboxSet(CheckboxSet):
	def __init__(self, elementYaml, pixelMap, isYou)
		super().__init__(self,elementYaml,pixelMap,isYou)
		self.isMulticolor = self.elementYaml['isMulticolor']
		self.checkboxSize = self.elementYaml['size']
	
	#TODO: DRY
	def __getCells():
		cells = {}
		for cellYaml in elementYaml['checkboxes']
			label           = cellYaml['label']
			cellCoordinates = cellYaml['coordinates'][__youOrThemString()]
			cells[cellYaml['label']] = SquareCell(self,label,pixelMap,cellCoordinates,checkboxSize)
			
		return cells

#TODO: figure out how abstract classes work in Python
class Bar(Element):
	def __init__(self, elementYaml, pixelMap, isYou)
		super().__init__(self,elementYaml,pixelMap,isYou)
		self.coordinates = elementYaml['coordinates'][__youOrThemString()]
		self.size        = elementYaml['size']

class BooleanBar(Bar):
	def __init__(self, elementYaml, pixelMap, isYou)
		super().__init__(self,elementYaml,pixelMap,isYou)
		self.yesPosition = elementYaml['yesPosition']
			
	def __getCells():
		cells = {}

		cellSize = ()
		cellSize[0] = self.size[0] / 2
		cellSize[1] = self.size[1]
		
		rightCoordinates = ()
		rightCoordinates[0] = coordinates[0] / cellSize[0]
		rightCoordinates[1] = coordinates[1]
		
		if yesPosition=='left'
			yesCell = SquareCell(pixelMap, coordinates, cellSize)
			noCell  = SquareCell(pixelMap, rightCoordinates, cellSize)
		else
			yesCell = SquareCell(pixelMap, rightCoordinates, cellSize)
			noCell  = SquareCell(pixelMap, coordinates, cellSize)
		
		cells['yes'] = yesCell
		cells['no']  = noCell
		
		return cells

#TODO: DRY -- numerical, binary, fuzzy might be better suited as subclasses of a 'bar' class
class NumericalRangeBar(Bar):
	def __init__(self, elementYaml, pixelMap, isYou)
		super().__init__(self,elementYaml,pixelMap,isYou)
		self.numCells     = elementYaml['numCells']
		self.leftQuality  = elementYaml['min']
		self.rightQuality = elementYaml['max']
	
	#TODO: DRY
	def __getCells():
		cells     = {}
		cellArray = SquareCell.genRow(pixelMap,coordinates,cellSize,numCells)
		
		for i in range(0,len(cellArray))
			cells[i] = cellArray[i] #TODO: maybe there's a better way to do this than with a for loop
			
		return cells
	
	def getNumericalValue()
		#TODO:
		#go through cells from left to right, find the max which has been selected
		#check if a single cell is selected, two adjacent cells only, or all cells up to a final cell (and no other cells beyond that)
		#throw an exception if any weirdness is encountered

class FuzzyRangeBar(Bar):
	def __init__(self, elementYaml, pixelMap, isYou)
		super().__init__(self,elementYaml,pixelMap,isYou)
		self.numCells     = elementYaml['numCells']
		self.leftQuality  = elementYaml['left']
		self.rightQuality = elementYaml['right']
	
	def __getCells():
		cells     = {}
		cellArray = SquareCell.genRow(pixelMap,coordinates,cellSize,numCells)
		
		for i in range(0,len(cellArray))
			cells[str(i)] = cellArray[i] #TODO: maybe there's a better way to do this than with a for loop
	
		return cells
	
	def getPercentScoreLeft()
		pass
		#TODO: generate a key-value pair corresponding to the "matching percentage" of the left attribute
	
	def getPercentScoreRight()
		pass
		#TODO: generate a key-value pair corresponding to the "matching percentage" of the right attribute

class TwoDFuzzyRangeBar(Bar):
	def __init__(self, elementYaml, pixelMap, isYou)
		super().__init__(self,elementYaml,pixelMap,isYou)
		self.numCells      = elementYaml['cellDimensions']
		self.leftQuality   = elementYaml['free']
		self.rightQuality  = elementYaml['regulated']
		self.topQuality    = elementYaml['capitalist']
		self.bottomQuality = elementYaml['socialist']
		
	def __getCells():
		cells       = {}
		cell2DArray = SquareCell.genSquare(pixelMap,coordinates,cellSize,cellDimensions)
		
		for j in range(0,len(cell2DArray)):
			for i in range(0,len(cell2DArray[0])):
				cells[str(i) + "," + str(j)] = cell2DArray[j][i]
		
		return cells

class Category:
	def __init__(self, categoryYaml, weighting, pixelMap) #category weighting must be passed in by chart, not set in stone
		self.categoryYaml      = categoryYaml
		self.name              = categoryYaml['category']
		self.weighting         = weighting
		self.pixelMap          = pixelMap
		self.elements          = self.__getElements() #hash of tuples -- each key corresponds to the 'You' and 'Them' versions of an element
		self.elementWeightings = self.__getElementWeightings()
		
	#TODO: pretty ugly
	def __getElements(): #Yaml format is different for each element type
		elements = {}
	
		checkboxSetsYaml = categoryYaml['checkboxSets']
		for checkboxSetYaml in checkboxSetsYaml
			elements[checkboxSetYaml['name']] = CheckboxSet.getYouAndThemElementsFromYaml(checkboxSetYaml)
		
		pictographicCheckboxSetsYaml = categoryYaml['pictographicCheckboxSets']
		for pictographicCheckboxSetYaml in pictographicCheckboxSetsYaml
			elements[pictographicCheckboxSetYaml['name']] = PictographicCheckboxSet.getYouAndThemElementsFromYaml(pictographicCheckboxSetYaml)
		
		numericalRangeBars = categoryYaml['numericalRangeBars']
		for numericalRangeBarYaml in numericalRangeBarsYaml
			elements[numericalRangeBarYaml['name']] = NumericalRangeBar.getYouAndThemElementsFromYaml(numericalRangeBarYaml)
		
		fuzzyRangeBars = categoryYaml['fuzzyRangeBars']
		for fuzzyRangeBarYaml in fuzzyRangeBarsYaml
			elements[fuzzyRangeBarYaml['name']] = FuzzyRangeBar.getYouAndThemElementsFromYaml(fuzzyRangeBarYaml)
		
		twoDFuzzyRangeBars = categoryYaml['twoDFuzzyRangeBars']
		for twoDFuzzyRangeBarYaml in twoDFuzzyRangeBarsYaml
			elements[twoDFuzzyRangeBarYaml['name']] = TwoDFuzzyRangeBar.getYouAndThemElementsFromYaml(twoDFuzzyRangeBarYaml)
	
	def __getElementWeightings():
		for elementTypeYaml in categoryYaml
			for elementYaml in elementTypeYaml
				elementRelativeWeightings[elementYaml['name']] = elementYaml['weighting']
				
		return Chart.weightingsFromRelativeWeightings(elementRelativeWeightings)
		
	def scoreCategory(theirCategory):
		totalCategoryScore = 0.0
		for elementName,elementPair in self.elements
			totalCategoryScore += elementPair[0].scoreElement(elementPair[1]) #'You' scores 'Them'
			totalCategoryScore *= self.weighting
			
		return totalCategoryScore

#TODO: I should only have to load config.yaml ONCE -- fix this
class Chart:
	def __init__(self, filename, categoryRelativeWeightings)
		self.filename           = filename
		self.categoryWeightings = self.weightingsFromRelativeWeightings(categoryRelativeWeightings)
		self.pixelMap           = self.__getPixelMap()
		self.categories         = self.__getCategories() #indexed by category name
		
	def __getCategories():
		with open('config.yaml', 'r') as f:
    		try:
    			categories = {}
    			categoriesYaml = yaml.load(f)
        		for categoryYaml in categoriesYaml
        			categories[categoryYaml['category']] = Category(categoryYaml,categoryWeighting[categoryYaml['category']],self.pixelMap)
        			
    		except yaml.YAMLError:
        		print('Could not open config file.')
	
	def __getPixelMap():
		im = Image.open(self.filename)
		im.convert('RGB')
	
	#relativeWeightings are integers -- the fractional weightings are relative to the sum of the relativeWeightings
	def weightingsFromRelativeWeightings(relativeWeightings):
		totalRelative = 0
		for weightingName,relativeWeighting in relativeWeightings:
			totalRelative += relativeWeighting
			
		weightings = {}
		for weightingName,relativeWeighting in relativeWeightings:
			weightings[weightingName] = (float)relativeWeighting / (float)totalRelative
			
		return weightings
	
	def scoreChart():
		totalChartScore = 0.0
		for categoryName,category in categories:
			totalChartScore += category.scoreCategory() #each category takes care of its weighting
			
		return totalChartScore
	
	#TODO: improve this so that fewer 'one-sided' high compatibility scores occur -- should not be simply an average of two compatibility scores
	def compareCharts(chartB):
		chartAScore = scoreChart()
		chartBScore = chartB.scoreChart()
		
		return (chartAScore + chartBScore) / 2.0
