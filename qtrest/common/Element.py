from qtrest.common.Cell import Cell,PictographicCell,SquareCell
from qtrest.common.ChartData import ChartData, CategoryData, ElementData, ColorFieldData

from PIL import Image, ImageFont

class Element:
    def __init__(self, elementYaml, isYou):
        self.name = elementYaml['name']

    def youOrThemString(self):
        if self.isYou:
            return 'you'
        else:
            return 'them'

    @staticmethod
    def coordinatesFromString(coordinates):
        coordsAsStringArray = coordinates.split("x")
        coordsAsIntTuple    = tuple(list(map(int,coordsAsStringArray)))

        return coordsAsIntTuple

class TextElement(Element):
    def __init__(self, elementYaml, isYou):
        if isYou: #TODO: fix this ugly hack to get around calling youOrThemString before isYou is set, without setting isYou twice
            self.coordinates = Element.coordinatesFromString(elementYaml['coordinates']['you'])
        else:
            self.coordinates = Element.coordinatesFromString(elementYaml['coordinates']['them'])

        self.elementYaml  = elementYaml
        self.textSize     = elementYaml['textSize']
        self.maxWidth     = elementYaml['maxWidth']

        super().__init__(elementYaml,isYou)

    def enterTextFromStringDict(self,elementDataFromStringDict):
        raise ValueError('The generic version of this method should not be called.')

    def propagatePixelMap(self,pixelMap):
        self.pixelMap = pixelMap

    def propagateFontFilename(self,fontFilename):
        self.font = ImageFont.truetype(fontFilename,self.textSize)

class ImageElement(Element): #a chart element is a collection of individual cells, has a non-configurable weighting within a category
    def __init__(self, elementYaml, isYou):
        self.isYou        = isYou
        self.elementYaml  = elementYaml

        self.isMulticolor = False
        self.cells        = self.getCells()
        super().__init__(elementYaml,isYou)

    def getElementData(self):
        cellDataDict = {}
        for label,cell in self.cells.items():
            cellDataDict[label] = cell.getColorFieldData(self.isYou,self.isMulticolor)

        return ElementData(self.name,cellDataDict)

    def getCells(self):
        raise ValueError('Parent version should never be called.')

    def getYouAndThemElementsFromYaml(self,elementYaml):
        pass

    #TODO: should we allow for missing cell data for cells which shouldn't be colored in?
    def colorElement(self,elementData):
        for cellName,cell in self.cells.items():
            cell.fillCellByColorFieldData(elementData.colorFieldDataDict[cellName])

    #TODO: allows for missing cell data in string dict, see above
    def colorElementFromStringDict(self,elementDataStringDict):
        for cellName,cellColorCode in elementDataStringDict.items():
            self.cells[cellName].fillCellByColorStringData(cellColorCode,self.isYou,self.isMulticolor)

    def propagatePixelMap(self,pixelMap):
        for cellName,cell in self.cells.items():
            cell.pixelMap = pixelMap
