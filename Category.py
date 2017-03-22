from Element import Element
from Bar import Bar, BooleanBar, NumericalRangeBar, FuzzyRangeBar, TwoDFuzzyRangeBar
from CheckboxSet import CheckboxSet, PictographicCheckboxSet, SquareCheckboxSet

from PIL import Image

class Category:
    def __init__(self, categoryYaml, weighting): #category weighting must be passed in by chart, not set in stone
        self.categoryYaml      = categoryYaml
        self.name              = categoryYaml['category']
        self.weighting         = weighting
        self.elements          = self.__getElements() #dict of dicts -- each key corresponds to the 'You' and 'Them' versions of an element
        self.elementWeightings = self.__getElementWeightings()
        
    def getCategoryData(self):
        elementDataDict = {}
        for name,elementDict in elementDicts:
            elementDataDict[name]         = {}
            elementDataDict[name]['you']  = elementTuple['you'].getElementData()
            elementDataDict[name]['them'] = elementTuple['them'].getElementData()
            
        return CategoryData(self.name,elementDataDict)
    
    #TODO: pretty ugly
    def __getElements(self): #Yaml format is different for each element type
        elements = {}
    
        if 'checkboxSets' in self.categoryYaml.keys():
            checkboxSetsYaml = self.categoryYaml['checkboxSets']
            for checkboxSetYaml in checkboxSetsYaml:
                elements[checkboxSetYaml['name']] = SquareCheckboxSet.getYouAndThemElementsFromYaml(checkboxSetYaml)

        if 'pictographicCheckboxSets' in self.categoryYaml.keys():        
            pictographicCheckboxSetsYaml = self.categoryYaml['pictographicCheckboxSets']
            for pictographicCheckboxSetYaml in pictographicCheckboxSetsYaml:
                elements[pictographicCheckboxSetYaml['name']] = PictographicCheckboxSet.getYouAndThemElementsFromYaml(pictographicCheckboxSetYaml)
        
        if 'numericalRangeBars' in self.categoryYaml.keys():
            numericalRangeBarsYaml = self.categoryYaml['numericalRangeBars']
            for numericalRangeBarYaml in numericalRangeBarsYaml:
                elements[numericalRangeBarYaml['name']] = NumericalRangeBar.getYouAndThemElementsFromYaml(numericalRangeBarYaml)

        if 'fuzzyRangeBarsYaml' in self.categoryYaml.keys():        
            fuzzyRangeBarsYaml = self.categoryYaml['fuzzyRangeBars']
            for fuzzyRangeBarYaml in fuzzyRangeBarsYaml:
                elements[fuzzyRangeBarYaml['name']] = FuzzyRangeBar.getYouAndThemElementsFromYaml(fuzzyRangeBarYaml)

        if 'twoDFuzzyRangeBarsYaml' in self.categoryYaml.keys():        
            twoDFuzzyRangeBarsYaml = self.categoryYaml['twoDFuzzyRangeBars']
            for twoDFuzzyRangeBarYaml in twoDFuzzyRangeBarsYaml:
                elements[twoDFuzzyRangeBarYaml['name']] = TwoDFuzzyRangeBar.getYouAndThemElementsFromYaml(twoDFuzzyRangeBarYaml)
            
        return elements
    
    def __getElementWeightings(self):
        elementRelativeWeightings = {}
    
        for elementTypeYaml in self.categoryYaml:
            if elementTypeYaml!='category': #ignore lines in the yaml starting with 'category'
                for elementYaml in self.categoryYaml[elementTypeYaml]:
                    elementRelativeWeightings[elementYaml['name']] = elementYaml['weighting']
                
        return Chart.weightingsFromRelativeWeightings(elementRelativeWeightings)
        
    def colorCategory(self,categoryData):
        for elementName,elementDict in self.elements.items():
            for elementOwner,element in elementDict.items():
                element.colorElement(categoryData[elementName][elementOwner])    
        
    def propagatePixelMap(self):
        for elementName,elementDict in self.elements.items():
            for elementOwner,element in elementDict.items():
                element.propagatePixelMap(pixelMap)
