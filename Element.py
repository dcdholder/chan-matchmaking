from Cell import Cell,PictographicCell,SquareCell
from ChartData import ChartData, CategoryData, ElementData, ColorFieldData

from PIL import Image

#TODO: figure out how abstract classes work in Python
class Element: #a chart element is a collection of individual cells, has a non-configurable weighting within a category
    def __init__(self, elementYaml, isYou):
        self.elementYaml  = elementYaml
        self.name         = elementYaml['name']
        self.weighting    = elementYaml['weighting']
        self.isYou        = isYou #specify whether to get 'You' or 'Them'
        self.isMulticolor = False
        self.cells        = self.__getCells()

    def getElementData(self):
        cellDataDict = {}
        for label,cell in cells.items():
            cellDataDict[label] = cell.getColorFieldData(self.isYou,self.isMulticolor)
            
        return ElementData(self.name,cellDataDict)

    def youOrThemString(self):
        if self.isYou:
            return 'you'
        else:
            return 'them'

    def __coordinatesFromString(self,coordinates):
        coordsAsStringArray = coordinates.split("x")
        coordsAsIntTuple    = tuple(list(map(int,coordsAsStringArray)))

    def getYouAndThemElementsFromYaml(self,elementYaml):
        pass

    def __getCells(self):
        pass
    
    def colorElement(self,elementData):
        for cellName,cell in self.cells:
            cell.fillCellByColorFieldData(elementData[cellName])
    
    def propagatePixelMap(self,pixelMap):
        for cell in self.cells.items():
            cell.pixelMap = pixelMap
