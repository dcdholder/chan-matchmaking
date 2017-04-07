from qtrest.common.Element import Element
from qtrest.common.Bar import Bar, BooleanBar, NumericalRangeBar, FuzzyRangeBar, TwoDFuzzyRangeBar
from qtrest.common.CheckboxSet import CheckboxSet, PictographicCheckboxSet, SquareCheckboxSet
from qtrest.common.ChartData import CategoryData

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
        for name,elementDict in self.elements.items():
            elementDataDict[name]         = {}
            elementDataDict[name]['you']  = elementDict['you'].getElementData()
            elementDataDict[name]['them'] = elementDict['them'].getElementData()

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

        if 'booleanBars' in self.categoryYaml.keys():
            booleanBarsYaml = self.categoryYaml['booleanBars']
            for booleanBarYaml in booleanBarsYaml:
                elements[booleanBarYaml['name']] = BooleanBar.getYouAndThemElementsFromYaml(booleanBarYaml)

        if 'numericalRangeBars' in self.categoryYaml.keys():
            numericalRangeBarsYaml = self.categoryYaml['numericalRangeBars']
            for numericalRangeBarYaml in numericalRangeBarsYaml:
                elements[numericalRangeBarYaml['name']] = NumericalRangeBar.getYouAndThemElementsFromYaml(numericalRangeBarYaml)

        if 'fuzzyRangeBars' in self.categoryYaml.keys():
            fuzzyRangeBarsYaml = self.categoryYaml['fuzzyRangeBars']
            for fuzzyRangeBarYaml in fuzzyRangeBarsYaml:
                elements[fuzzyRangeBarYaml['name']] = FuzzyRangeBar.getYouAndThemElementsFromYaml(fuzzyRangeBarYaml)

        if 'twoDFuzzyRangeBars' in self.categoryYaml.keys():
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

        return Category.weightingsFromRelativeWeightings(elementRelativeWeightings)

    #relativeWeightings are integers -- the fractional weightings are relative to the sum of the relativeWeightings
    @staticmethod
    def weightingsFromRelativeWeightings(relativeWeightings):
        totalRelative = 0
        for weightingName,relativeWeighting in relativeWeightings.items():
            totalRelative += relativeWeighting

        weightings = {}
        for weightingName,relativeWeighting in relativeWeightings.items():
            weightings[weightingName] = float(relativeWeighting) / float(totalRelative)

        return weightings

    def colorCategory(self,categoryData):
        for elementName,elementDict in self.elements.items():
            for elementOwner,element in elementDict.items():
                element.colorElement(categoryData.elementDataDict[elementName][elementOwner])

    #TODO: DRY
    #TODO: for the moment, we won't require all elements in a category to be present
    def colorCategoryFromStringDict(self,categoryName,categoryDataStringDict):
        if categoryName=='physical':
            self.preprocessBodyType(categoryDataStringDict)

        for elementName,elementPairStringDict in categoryDataStringDict.items():
            for elementOwner,elementStringDict in elementPairStringDict.items():
                self.elements[elementName][elementOwner].colorElementFromStringDict(elementStringDict)

    def preprocessBodyType(self,categoryDataStringDict):
        defaultGender = 'male'
        for gender,score in categoryDataStringDict['gender']['you'].items():
            if score!='none':
                if gender=='male' or gender=='ftm':
                    defaultGender = 'male'
                else:
                    defaultGender = 'female'

        #pick the correct body type image for you
        for label in list(categoryDataStringDict['body type']['you'].keys()):
            categoryDataStringDict['body type']['you'][label + ' ' + defaultGender] = categoryDataStringDict['body type']['you'][label]
            del categoryDataStringDict['body type']['you'][label]

        acceptsMale   = False
        acceptsFemale = False
        for gender,score in categoryDataStringDict['gender']['them'].items():
            if score!=0 and score!='none':
                if gender=="mtf" or gender=="female":
                    acceptsFemale = True
                else:
                    acceptsMale = True

        #pick the correct body type image for them
        for label in list(categoryDataStringDict['body type']['them'].keys()):
            if acceptsMale or (not acceptsMale and not acceptsFemale): #if the target accepts neither, give them both (and see how they like it)
                categoryDataStringDict['body type']['them'][label + ' male'] = categoryDataStringDict['body type']['them'][label]
            if acceptsFemale or (not acceptsMale and not acceptsFemale):
                categoryDataStringDict['body type']['them'][label + ' female'] = categoryDataStringDict['body type']['them'][label]

            del categoryDataStringDict['body type']['them'][label]

    def propagatePixelMap(self,pixelMap):
        for elementName,elementDict in self.elements.items():
            for elementOwner,element in elementDict.items():
                element.propagatePixelMap(pixelMap)
