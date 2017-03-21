import Element
import Bar
import CheckboxSet

from PIL import Image

class Category:
    def __init__(self, categoryYaml, weighting): #category weighting must be passed in by chart, not set in stone
        self.categoryYaml      = categoryYaml
        self.name              = categoryYaml['category']
        self.weighting         = weighting
        self.elements          = self.__getElements() #dict of dicts -- each key corresponds to the 'You' and 'Them' versions of an element
        self.elementWeightings = self.__getElementWeightings()
        
    def getCategoryData():
        elementDataDict = {}
        for name,elementDict in elementDicts:
            elementDataDict[name]         = {}
            elementDataDict[name]['you']  = elementTuple['you'].getElementData()
            elementDataDict[name]['them'] = elementTuple['them'].getElementData()
            
        return CategoryData(self.name,elementDataDict)
    
    #TODO: pretty ugly
    def __getElements(): #Yaml format is different for each element type
        elements = {}
    
        checkboxSetsYaml = categoryYaml['checkboxSets']
        for checkboxSetYaml in checkboxSetsYaml:
            elements[checkboxSetYaml['name']] = CheckboxSet.getYouAndThemElementsFromYaml(checkboxSetYaml)
        
        pictographicCheckboxSetsYaml = categoryYaml['pictographicCheckboxSets']
        for pictographicCheckboxSetYaml in pictographicCheckboxSetsYaml:
            elements[pictographicCheckboxSetYaml['name']] = PictographicCheckboxSet.getYouAndThemElementsFromYaml(pictographicCheckboxSetYaml)
        
        numericalRangeBars = categoryYaml['numericalRangeBars']
        for numericalRangeBarYaml in numericalRangeBarsYaml:
            elements[numericalRangeBarYaml['name']] = NumericalRangeBar.getYouAndThemElementsFromYaml(numericalRangeBarYaml)
        
        fuzzyRangeBars = categoryYaml['fuzzyRangeBars']
        for fuzzyRangeBarYaml in fuzzyRangeBarsYaml:
            elements[fuzzyRangeBarYaml['name']] = FuzzyRangeBar.getYouAndThemElementsFromYaml(fuzzyRangeBarYaml)
        
        twoDFuzzyRangeBars = categoryYaml['twoDFuzzyRangeBars']
        for twoDFuzzyRangeBarYaml in twoDFuzzyRangeBarsYaml:
            elements[twoDFuzzyRangeBarYaml['name']] = TwoDFuzzyRangeBar.getYouAndThemElementsFromYaml(twoDFuzzyRangeBarYaml)
            
        return elements
    
    def __getElementWeightings():
        for elementTypeYaml in categoryYaml:
            for elementYaml in elementTypeYaml:
                elementRelativeWeightings[elementYaml['name']] = elementYaml['weighting']
                
        return Chart.weightingsFromRelativeWeightings(elementRelativeWeightings)
        
    def colorCategory(categoryData):
        for elementName,elementDict in self.elements:
            for elementOwner,element in elementDict:
                element.colorElement(categoryData[elementName][elementOwner])    
        
    def propagatePixelMap()
        for elementName,elementDict in self.elements:
            for elementOwner,element in elementDict:
                element.propagatePixelMap(pixelMap)
