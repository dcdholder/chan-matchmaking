from Element import Element
from Cell import Cell,SquareCell,PictographicCell

#TODO: figure out how abstract classes work in Python
class Bar(Element):
    def __init__(self, elementYaml, isYou):
        if isYou: #TODO: fix this ugly hack to get around calling youOrThemString before isYou is set, without setting isYou twice
            self.coordinates = Element.coordinatesFromString(elementYaml['coordinates']['you'])
        else:
            self.coordinates = Element.coordinatesFromString(elementYaml['coordinates']['them'])
            
        self.size     = Element.coordinatesFromString(elementYaml['size'])
        self.cellSize = self.getCellSize()
        super().__init__(elementYaml,isYou)
        
    def getCellSize(self):
        return ((self.size[0] // self.numCells), (self.size[1]))

class BooleanBar(Bar):
    def __init__(self, elementYaml, isYou):
        self.numCells = 2
        super().__init__(elementYaml,isYou)
        self.yesPosition = elementYaml['yesPosition']
            
    def getCells(self):
        cells = {}

        cellSize = ()
        cellSize[0] = self.size[0] / 2
        cellSize[1] = self.size[1]
        
        rightCoordinates = ()
        rightCoordinates[0] = self.coordinates[0] + self.cellSize[0]
        rightCoordinates[1] = self.coordinates[1]
        
        if yesPosition=='left':
            yesCell = SquareCell(self.coordinates, self.cellSize)
            noCell  = SquareCell(rightCoordinates, self.cellSize)
        else:
            yesCell = SquareCell(rightCoordinates, self.cellSize)
            noCell  = SquareCell(self.coordinates, self.cellSize)
        
        cells['yes'] = yesCell
        cells['no']  = noCell
        
        return cells
    
    #TODO: DRY
    @staticmethod
    def getYouAndThemElementsFromYaml(elementYaml):
        youAndThemElements = {}
        youAndThemElements['you']  = BooleanBar(elementYaml,True)
        youAndThemElements['them'] = BooleanBar(elementYaml,False)
        
        return youAndThemElements

class NumericalRangeBar(Bar):
    def __init__(self, elementYaml, isYou):
        self.numCells = int(elementYaml['numCells'])
        super().__init__(elementYaml,isYou)
        self.leftQuality  = elementYaml['min']
        self.rightQuality = elementYaml['max']
    
    #TODO: DRY
    def getCells(self):            
        return SquareCell.genRow(self.coordinates,self.cellSize,self.numCells)
    
    def getNumericalValue(self):
        pass
        #TODO:
        #go through cells from left to right, find the max which has been selected
        #check if a single cell is selected, two adjacent cells only, or all cells up to a final cell (and no other cells beyond that)
        #throw an exception if any weirdness is encountered
        
    #TODO: DRY
    @staticmethod
    def getYouAndThemElementsFromYaml(elementYaml):
        youAndThemElements = {}
        youAndThemElements['you']  = NumericalRangeBar(elementYaml,True)
        youAndThemElements['them'] = NumericalRangeBar(elementYaml,False)
        
        return youAndThemElements

class FuzzyRangeBar(Bar):
    def __init__(self, elementYaml, isYou):
        self.numCells = int(elementYaml['numCells'])
        super().__init__(elementYaml,isYou)
        self.leftQuality  = elementYaml['left']
        self.rightQuality = elementYaml['right']
    
    def getCells(self):    
        return SquareCell.genRow(self.coordinates,self.cellSize,self.numCells)
    
    def getPercentScoreLeft(self):
        pass
        #TODO: generate a key-value pair corresponding to the "matching percentage" of the left attribute
    
    def getPercentScoreRight(self):
        pass
        #TODO: generate a key-value pair corresponding to the "matching percentage" of the right attribute

    #TODO: DRY
    @staticmethod
    def getYouAndThemElementsFromYaml(elementYaml):
        youAndThemElements = {}
        youAndThemElements['you']  = FuzzyRangeBar(elementYaml,True)
        youAndThemElements['them'] = FuzzyRangeBar(elementYaml,False)
        
        return youAndThemElements

class TwoDFuzzyRangeBar(Bar):
    def __init__(self, elementYaml, isYou):
        self.cellDimensions = int(elementYaml['cellDimensions'])
        self.numCells = self.cellDimensions #TODO: Hideous hack. May lead to bugs.
        super().__init__(elementYaml,isYou)
        self.leftQuality   = elementYaml['left']
        self.rightQuality  = elementYaml['right']
        self.topQuality    = elementYaml['top']
        self.bottomQuality = elementYaml['bottom']
        
    def getCells(self):        
        return SquareCell.genSquare(self.coordinates,self.cellSize,self.cellDimensions)
        
    def getCellSize(self):
        return ((self.size[0] // self.numCells), (self.size[1]) // self.numCells)
        
    #TODO: DRY
    @staticmethod
    def getYouAndThemElementsFromYaml(elementYaml):
        youAndThemElements = {}
        youAndThemElements['you']  = TwoDFuzzyRangeBar(elementYaml,True)
        youAndThemElements['them'] = TwoDFuzzyRangeBar(elementYaml,False)
        
        return youAndThemElements
