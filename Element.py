import Cell
import Bar
import CheckboxSet
import ElementData

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

    def getElementData():
        cellDataDict = {}
        for label,cell in cells:
            cellDataDict[label] = cell.getColorFieldData(self.isYou,self.isMulticolor)
            
        return ElementData(self.name,cellDataDict)

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
    
    def colorElement(elementData):
        for cellName,cell in self.cells
            cell.fillCellByColorFieldData(elementData[cellName])
    
    def propagatePixelMap(pixelMap):
        for cell in self.cells:
            cell.pixelMap = pixelMap
