#it looks like the coordinate is simply a tuple
#a cell may have the color 'unselected', 'invalid', or one of six others

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
		if importanceScore*traitScore > 0: #same sign
			scoreDelta=abs(scoreDelta)
		else:
			scoreDelta=-abs(scoreDelta)

		finalScore = scoreDelta * importanceScore #increases importance of delta for extreme scores, makes score 0 if importance is neutral
		finalScore = (finalScore+1.0) / 2.0       #normalize final answer to a range between 0 and 1.0
	
		return finalScore
	
	def singleColorYouScoring(traitSelected,importanceScoreIndex) #trait score is either 1.0 or 0.0, no in-betweens
		if traitSelected:
			traitScoreIndex = len(__traitScoreMapping)-1 #just set to either extreme trait score
		else:
			traitScoreIndex = 0
		
		return multiColorYouScoring(traitScoreIndex,importanceScoreIndex)

class Cell: #an indivisble component of an image element
	def __init__(self,pixelMap,coordinates)
		self.pixelMap       = pixelMap
		self.coordinates    = coordinates
		self.colorDataField = self.__setColor()
	
	def __setColor() #just select color from the given coordinates -- is different for square cell
		#TODO: figure out how to handle invalid cell colors
		#TODO: write ImageMagick code to get color from pixel
		return ColorDataField(colorCode)
			

class PictographicCell(Cell):
	

class SquareCell(Cell):
	def __init__(self, pixelMap, coordinates, size)
		self.pixelMap       = pixelMap
		self.coordinates    = coordinates
		self.size           = size
		self.colorDataField = self.__setColor()
	
	def __setColor() #this guy samples the color and assigns it the correct color name string
		centerPixelCoordinates = self.getCenterPixel()
		#TODO: colorValue = #feed the coordinates into imagemagick or whatever, get the color at that point
		colorFound = False
		if colorValue==self.__unselectedColor
			colorFound = true
			colorName  = 'unselected'
		else
			for name, value in self.__colorValues
				if value==colorValue
					colorFound = True
					colorName  = name
					break
				
		if colorFound
			return colorName
		else
			return 'invalid'
	
	def genRow(pixelMap,baseCoordinates,cellSize,numCells) #create a horizontal row of cells
		cells = []
		for i in range(numCells)
			cellCoordinates['x'] = baseCoordinates['x'] + cellSize['x'] * i
			cellCoordinates['y'] = baseCoordinates['y']
			cells.append(Cell(pixelMap,cellCoordinates,cellSize))
			
		return cells
		
	def isColored() #this guy checks that the color is not the default color
		return self.color!='unselected'
	
	def isDefaultSelectedColor() 
		return self.color=='green'
	
	def getColorScore()
		return self.__colorScores[self.color]
	
	def getCenterPixel()
		middleX = self.coordinates['x'] + self.size['x'] / 2
		middleY = self.coordinates['y'] + self.size['y'] / 2

		return {'x': middleX, 'y': middleY}

class Element #a chart element is a collection of individual cells
		
class CheckboxSet(Element):
	def __init__(self, checkboxes, category, label)
		self.checkboxes = checkboxes
		self.category   = category
		self.label      = label

class BooleanBar(Element):
	def __init__(self, pixelMap, coordinates, size, yesPosition, category, label)
		self.pixelMap    = pixelMap
		self.coordinates = coordinates
		self.size        = size
		self.category    = category
		self.label       = label
		
		cellSize['x'] = size['x'] / 2
		cellSize['y'] = size['y']
		
		rightCoordinates['x'] = coordinates['x'] / cellSize['x']
		rightCoordinates['y'] = coordinates['y']
		
		if yesPosition=='left'
			self.yesCell = Cell(pixelMap, coordinates, cellSize)
			self.noCell  = Cell(pixelMap, rightCoordinates, cellSize)
		else
			self.yesCell = Cell(pixelMap, rightCoordinates, cellSize)
			self.noCell  = Cell(pixelMap, coordinates, cellSize)

class NumericalRangeBar(Element):
	#generate the cells
	def __init__(self, pixelMap, coordinates, cellSize, numCells, minValue, maxValue, category, label)
		self.pixelMap    = pixelMap
		self.coordinates = coordinates
		self.minValue    = minValue
		self.maxValue    = maxValue
		self.cells       = Cell.genRow(pixelMap,coordinates,cellSize,numCells)
		self.category    = category
		self.label       = label
			
	def getNumericalValue()
		#TODO:
		#go through cells from left to right, find the max which has been selected
		#check if a single cell is selected, two adjacent cells only, or all cells up to a final cell (and no other cells beyond that)
		#throw an exception if any weirdness is encountered

class FuzzyRangeBar(Element):
	def __init__(self, pixelMap, coordinates, cellSize, numCells, leftQuality, rightQuality, category, label)
		self.pixelMap     = pixelMap
		self.coordinates  = coordinates
		self.leftQuality  = leftQuality
		self.rightQuality = rightQuality
		self.cells        = Cell.genRow(pixelMap,coordinates,cellSize,numCells)
		self.category     = category
		self.label        = label
		
	def getPercentScoreLeft()
		#TODO: generate a key-value pair corresponding to the "matching percentage" of the left attribute
	
	def getPercentScoreRight()
		#TODO: generate a key-value pair corresponding to the "matching percentage" of the right attribute

class Category:
	def __init__(self, name, elements)
		self.name     = name
		self.elements = elements
		
class Chart
	def __init__(self, name, categories)
		self.name     = name
		self.elements = categories
