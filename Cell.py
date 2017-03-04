#it looks like the coordinate is simply a tuple
#a cell may have the color 'unselected', 'invalid', or one of six others

class PictographicCell(Cell):
	

class Cell
	__unselectedColor = 0xFFFFFF
	__colorValues = {'pink': 0xFFFFFF, 'blue': 0xFFFFFF, 'green': 0xFFFFFF, 'yellow': 0xFFFFFF, 'orange': 0xFFFFFF, 'red': 0xFFFFFF}
	__colorScores = {'pink': 5, 'blue': 4, 'green': 3, 'yellow': 2, 'orange': 1, 'red': 0}

	def __init__(self, pixelMap, coordinates, size)
		self.pixelMap    = pixelMap
		self.coordinates = coordinates
		self.size        = size
		self.color       = self.__setColor()
	
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
		
class Checkbox
	def __init__(self, pixelMap, coordinates, size, label)
		self.cell  = Cell(pixelMap, coordinates, size)
		self.label = label
		
class CheckboxSet
	def __init__(self, checkboxes, category, label)
		self.checkboxes = checkboxes
		self.category   = category
		self.label      = label

class BooleanBar
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

class NumericalRangeBar
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

class FuzzyRangeBar
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
		
class Chart
	def __init__(self, filename, categoryWeightings)
		#pixelMap = #TODO: generate the pixel map
		self.you  = Target(pixelMap,youCheckboxSets,youNumericalRangeBars,youFuzzyRangeBars)
		self.them = Target(pixelMap,themCheckboxSets,themNumericalRangeBars,themFuzzyRangeBars)
		self.categoryWeightings = categoryWeightings
		
	def scoreAllCategories(otherChart)
		totalScore = 0.0
		for category, weighting in self.categoryWeightings
			totalScore += scoreCategory(category,otherChart)*weighting
			
		return totalScore	

	#TODO: very ugly, fix the checkbox and bar classes
	def scoreCategory(category, otherChart)
		#whatever.compare should do the weighting
		for checkboxSet in you.checkboxSetsFromCategory(category)
			checkboxSetScore = checkboxSet.compare(otherChart.them.checkboxSetFromLabel(checkboxSet.label))
		
		for numericalRangeBar in you.numericalRangeBarsFromCategory(category)
			numericalRangeBarScore = numericalRangeBar.compare(otherChart.them.numericalRangeBarFromLabel(numericalRangeBar.label))		
			
		for fuzzyRangeBar in you.fuzzyRangeBarsFromCategory(category)
			fuzzyRangeBar.compare(otherChart.them.fuzzyRangeBarFromLabel(fuzzyRangeBar.label))

		return checkboxSetScore + numericalRangeBarScore + fuzzyRangeBar

class Target
	
