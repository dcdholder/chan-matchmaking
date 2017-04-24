from qtrest.common.Element import Element, ImageElement
from qtrest.common.Cell import Cell,SquareCell,PictographicCell

#TODO: figure out how abstract classes work in Python
class CheckboxSet(ImageElement):
    def __init__(self, elementYaml, isYou):
        super().__init__(elementYaml,isYou)

class PictographicCheckboxSet(CheckboxSet):
    def __init__(self, elementYaml, isYou):
        super().__init__(elementYaml,isYou)

    def getCells(self):
        cells = {}
        for cellYaml in self.elementYaml['checkboxes']:
            label           = cellYaml['label']
            cellCoordinates = Element.coordinatesFromString(cellYaml['coordinates'][self.youOrThemString()])
            cells[cellYaml['label']] = PictographicCell(label,cellCoordinates)

        return cells

    #TODO: DRY
    @staticmethod
    def getYouAndThemElementsFromYaml(elementYaml):
        youAndThemElements = {}
        youAndThemElements['you']  = PictographicCheckboxSet(elementYaml,True)
        youAndThemElements['them'] = PictographicCheckboxSet(elementYaml,False)

        return youAndThemElements

class SquareCheckboxSet(CheckboxSet):
    def __init__(self, elementYaml, isYou):
        self.checkboxSize = Element.coordinatesFromString(elementYaml['size'])
        super().__init__(elementYaml,isYou)
        self.isMulticolor = self.elementYaml['isMulticolor']

    #TODO: DRY
    def getCells(self):
        cells = {}
        for cellYaml in self.elementYaml['checkboxes']:
            label           = cellYaml['label']
            cellCoordinates = Element.coordinatesFromString(cellYaml['coordinates'][self.youOrThemString()])
            cells[cellYaml['label']] = SquareCell(label,cellCoordinates,self.checkboxSize)

        return cells

    #TODO: DRY
    @staticmethod
    def getYouAndThemElementsFromYaml(elementYaml):
        youAndThemElements = {}
        youAndThemElements['you']  = SquareCheckboxSet(elementYaml,True)
        youAndThemElements['them'] = SquareCheckboxSet(elementYaml,False)

        return youAndThemElements
