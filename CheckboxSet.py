from Element import Element

#TODO: figure out how abstract classes work in Python
class CheckboxSet(Element):
    def __init__(self, elementYaml, isYou):
        super().__init__(elementYaml,isYou)

class PictographicCheckboxSet(CheckboxSet):
    def __init__(self, elementYaml, isYou):
        super().__init__(elementYaml,isYou)
    
    def __getCells(self):
        cells = {}
        for cellYaml in elementYaml['checkboxes']:
            label           = cellYaml['label']
            cellCoordinates = cellYaml['coordinates'][__youOrThemString()]
            cells[cellYaml['label']] = PictographicCell(self,label,pixelMap,cellCoordinates)

    #TODO: DRY
    @staticmethod
    def getYouAndThemElementsFromYaml(elementYaml):
        youAndThemElements = {}
        youAndThemElements['you']  = PictographicCheckboxSet(elementYaml,True)
        youAndThemElements['them'] = PictographicCheckboxSet(elementYaml,False)
        
        return youAndThemElements

class SquareCheckboxSet(CheckboxSet):
    def __init__(self, elementYaml, isYou):
        super().__init__(elementYaml,isYou)
        self.isMulticolor = self.elementYaml['isMulticolor']
        self.checkboxSize = self.elementYaml['size']
    
    #TODO: DRY
    def __getCells(self):
        cells = {}
        for cellYaml in elementYaml['checkboxes']:
            label           = cellYaml['label']
            cellCoordinates = cellYaml['coordinates'][__youOrThemString()]
            cells[cellYaml['label']] = SquareCell(self,label,pixelMap,cellCoordinates,checkboxSize)
            
        return cells
        
    #TODO: DRY
    @staticmethod
    def getYouAndThemElementsFromYaml(elementYaml):
        youAndThemElements = {}
        youAndThemElements['you']  = SquareCheckboxSet(elementYaml,True)
        youAndThemElements['them'] = SquareCheckboxSet(elementYaml,False)
        
        return youAndThemElements
