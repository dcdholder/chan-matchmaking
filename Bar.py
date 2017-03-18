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
			cells[str(i)] = cellArray[i] #TODO: maybe there's a better way to do this than with a for loop
			
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
