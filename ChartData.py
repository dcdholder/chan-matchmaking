import re
from PIL import Image

class ChartData:
    def __init__(self, name, categoryDataDict):
        self.name             = name
        self.categoryDataDict = categoryDataDict

    def __str__(self):
        chartString = "Chart name: " + self.name + '\n'
        for name,categoryData in self.categoryDataDict.items():
            chartString += self.tabTextBlock(str(categoryData)) + '\n' #add an indentation level to the category data output, then add a newline

        return chartString

    @staticmethod
    def tabTextBlock(textBlock):
        newTextBlock = textBlock.replace('\n','\n\t')
        newTextBlock = '\t' + newTextBlock

        return newTextBlock

    def scoreChartData(self,theirChartData,weightingsTree):
        totalChartScore = 0.0
        for categoryName,categoryData in self.categoryDataDict.items():
            totalChartScore += categoryData.scoreCategoryData(theirChartData.categoryDataDict[categoryName],weightingsTree[categoryName]['weight'],weightingsTree[categoryName]['elements']) #each category takes care of its weighting

        return totalChartScore

    #TODO: improve this so that fewer 'one-sided' high compatibility scores occur -- should not be simply an average of two compatibility scores
    def compare(self,chartDataB,weightingsTree):
        chartAScore = self.scoreChartData(chartDataB,weightingsTree)
        chartBScore = chartDataB.scoreChartData(self,weightingsTree)

        return (chartAScore + chartBScore) / 2.0

    @staticmethod
    def compareAll(chartDataList,weightingsTree):
        scores = {}
        for j in range(0,len(chartDataList)):
            scores[chartDataList[j].name] = {}
            for i in range(j,len(chartDataList)): #two dict elements for every pair (indexed both by chart A first, and by chart B first)
                scores[chartDataList[j].name][chartDataList[i].name] = chartDataList[j].compare(chartDataList[i],weightingsTree)
                scores[chartDataList[i].name][chartDataList[j].name] = scores[chartDataList[j].name][chartDataList[i].name]

        return scores

    @staticmethod
    def bestMatchesAll(chartDataList,weightingsTree):
        scores = compareAll(chartDataList,weightingsTree)

        highestScores = {}
        for nameA,chartDataScoreDict in chartDataList:
            highestScore         = 0.0
            highestScores[nameA] = {}
            for nameB,chartDataScore in chartDataScoreDict:
                if chartDataScore > highestScore:
                    highestScore     = chartDataScore
                    highestScoreName = nameB

            highestScores[nameA]['name']  = highestScoreName
            highestScores[nameA]['score'] = highestScore

        return highestScores

class CategoryData:
    def __init__(self, name, elementDataDict):
        self.name            = name
        self.elementDataDict = elementDataDict
        self.postProcessCategory()

    #TODO: DRY
    def __str__(self):
        youElements  = []
        themElements = []
        for name,elementDataPair in self.elementDataDict.items():
            youElements.append(elementDataPair['you'])
            themElements.append(elementDataPair['them'])

        categoryString = "Category: " + self.name
        categoryString += '\n\tYou: '
        for youElement in youElements:
            categoryString += '\n' + ChartData.tabTextBlock(ChartData.tabTextBlock(str(youElement))) #TODO: number of extra tabs should be an optional argument to tabTextBlock

        categoryString += '\n\tThem: '
        for themElement in themElements:
            categoryString += '\n' + ChartData.tabTextBlock(ChartData.tabTextBlock(str(themElement)))

        return categoryString

    def postProcessCategory(self):
        if self.name.lower()=='physical':
            self.postProcessGender()

    def postProcessGender(self):
        if self.name.lower()!='physical':
            raise ValueError('Category must be physical to post-process genders.')

        acceptsMale   = not self.elementDataDict['gender']['them'].colorFieldDataDict['male'].isWorst()
        acceptsFemale = not self.elementDataDict['gender']['them'].colorFieldDataDict['female'].isWorst()
        acceptsMtf    = not self.elementDataDict['gender']['them'].colorFieldDataDict['mtf'].isWorst()
        acceptsFtm    = not self.elementDataDict['gender']['them'].colorFieldDataDict['ftm'].isWorst()

        if (acceptsMale or acceptsFtm) and not acceptsFemale and not acceptsMtf:    #allow facial hair, do not allow female body types
            for bodyTypeName,bodyTypeData in self.elementDataDict['bodyType']['them'].colorFieldDataDict.items():
                if 'Female' in bodyTypeName:
                    bodyTypeData.resetToWorst()

        elif not acceptsMale and not acceptsFtm and (acceptsFemale or acceptsMtf): #do not allow facial hair (except for 'None'), do not allow male body types
            for bodyTypeName,bodyTypeData in self.elementDataDict['bodyType']['them'].colorFieldDataDict.items():
                if 'Male' in bodyTypeName:
                    bodyTypeData.resetToWorst()

            for facialHairName,facialHairData in self.elementDataDict['facialHair']['them'].colorFieldDataDict.items():
                if facialHairName.lower()=='none':
                    facialHairData.resetToBest()
                else:
                    facialHairData.resetToWorst()

    def scoreCategoryData(self,theirCategory,weighting,elementWeightings):
        totalCategoryScore = 0.0
        for elementName,elementPair in self.elementDataDict.items():
            totalCategoryScore += elementPair['them'].scoreElementData(theirCategory.elementDataDict[elementName]['you'],elementWeightings[elementName]) #'You' scores 'Them'

        totalCategoryScore *= weighting

        return totalCategoryScore

class ElementData:
    def __init__(self, name, colorFieldDataDict):
        self.name               = name
        self.colorFieldDataDict = colorFieldDataDict

    def __str__(self):
        elementString = "Element: " + self.name
        for label,colorFieldData in self.colorFieldDataDict.items():
            elementString += '\n\t' + label + ": " + str(colorFieldData)

        return elementString

    def scoreElementData(self,theirElement,weighting):
        totalElementScore = 0.0
        for colorFieldName,colorFieldData in self.colorFieldDataDict.items():
            totalElementScore += colorFieldDataDict[colorFieldName].scoreColorFieldData(theirElement.colorFieldDataDict[colorFieldName])

        totalElementScore *= weighting

        return totalElementScore

class ColorFieldData:
    __unselectedColors  = ['#ebebeb','#c3c3c3','#c0c0c0','#ffffff'] #almost everything uses 'ebebeb'; 'facial hair' and 'body type' use the others
    __defaultEmptyIndex = 0
    __singleSelectIndex = 2
    __neutralIndex      = 3
    __bestIndex         = 0
    __worstIndex        = 5
    #TODO: endianness should be the same in the frontend and the backend
    __colorNames = ['pink', 'blue', 'green', 'yellow', 'orange', 'red']
    __colorCodes = ['#ff00ff', '#0000ff', '#00ff00', '#ffff00', '#ff7200', '#ff0000'] #these should be FF for at least one RGB component
    __importanceScoreMapping = [1.0, 0.33, 0.67, 0, -0.5, -1.0]
    __traitScoreMapping      = [1.0, 0.5, 0.0, -0.5, -1.0]

    def __init__(self, colorCode, isYou, isMulticolor):
        self.isYou        = isYou #tells us whether this is a trait or importance score
        self.isMulticolor = isMulticolor

        if not self.isYou:
            self.isMulticolor = True

        self.isSelected   = False
        self.colorScore   = self.colorScoreFromCode(colorCode) #TODO: would be nice to have an alternate constructor for colorIndex rather than colorCode...

        if not self.isYou and not self.isMulticolor:
            raise ValueError('Them cells are always multicolor.')

    def __str__(self):
        return str(self.__colorNames[self.colorScore])

    def isWorst(self):
        return self.colorScore==self.__worstIndex

    def isBest(self):
        return self.colorScore==self.__bestIndex

    def isPositive(self):
        return self.colorScore in range(self.__bestIndex,self.__neutralIndex+1) #will need to be changed if we decide to flip the color arrays

    def resetToWorst(self):
        self.colorScore = self.__worstIndex

    def resetToBest(self):
        self.colorScore = self.__bestIndex

    def colorScoreFromCode(self,colorCode):
        for i in range(0,len(self.__colorCodes)):
            if self.closeEnoughColor(self.__colorCodes[i],colorCode):
                self.isSelected = True
                return i

        for unselectedColorCode in self.__unselectedColors:
            if self.closeEnoughColor(unselectedColorCode,colorCode):
                if self.isMulticolor:
                    self.isSelected = True
                    return self.__neutralIndex #for multicolor cells, an unfilled cell can be assumed yellow
                else:
                    self.isSelected = False
                    return self.__worstIndex

        return self.__neutralIndex #TODO: For now, we handle colors we can't identify using the 'neutral' color. Find a better way.

        raise ValueError('Could not map color code ' + colorCode + ' to a valid color score.')

    @staticmethod
    def colorCodeFromExternalScore(colorScore):
        return ColorFieldData.__colorCodes[colorScore]

    def getColorCode(self):
        if self.isYou and not self.isMulticolor:
            if self.colorScore==self.__worstIndex:
                return self.__unselectedColors[self.__defaultEmptyIndex]
            else:
                return self.__colorCodes[self.colorScore]
        else:
            return self.__colorCodes[self.colorScore]

    @staticmethod
    def htmlCodeToRgb(htmlCode):
        pattern = re.compile('^#[a-f0-9]{6}$') #check that the format is correct
        if not pattern.match(htmlCode):
            raise ValueError('Improperly-formatted html color code.')

        stringTuple = ((htmlCode[1] + htmlCode[2]), (htmlCode[3] + htmlCode[4]), (htmlCode[5] + htmlCode[6]))
        intTuple    = (int(stringTuple[0], 16), int(stringTuple[1], 16), int(stringTuple[2], 16))

        return intTuple

    #TODO: add a method which takes a list of possible canonical colors, and outputs the most likely one if it's "close enough"

    @staticmethod
    def closeEnoughColor(htmlCanonicalColor,htmlTestColor):
        PRIMARY_FUZZINESS     = 32
        NON_PRIMARY_FUZZINESS = 32

        COMPOUND_PRIMARY_ZERO_FUZZINESS          = 128
        COMPOUND_PRIMARY_INTER_ELEMENT_FUZZINESS = 16

        canonicalColor = ColorFieldData.htmlCodeToRgb(htmlCanonicalColor)
        testColor      = ColorFieldData.htmlCodeToRgb(htmlTestColor)

        closeEnoughPrimaries    = True
        closeEnoughNonPrimaries = True
        for i in range(0,3):
            if canonicalColor[i]==255: #primary color
                if testColor[i] < (canonicalColor[i] - PRIMARY_FUZZINESS):
                    closeEnoughPrimaries = False
            else:
                if testColor[i] < (canonicalColor[i] - NON_PRIMARY_FUZZINESS) or testColor[i] > (canonicalColor[i] + NON_PRIMARY_FUZZINESS):
                    closeEnoughNonPrimaries = False

        if not closeEnoughNonPrimaries: #give extra allowance when the subpixels are exclusively either FF or 00
            numZeros = 0
            for i in range(0,3):
                if canonicalColor[i]==0:
                    numZeros+=1

            compoundPrimary = True
            for i in range(0,3):
                if canonicalColor[i]!=255 and canonicalColor[i]!=0:
                    compoundPrimary=False

            if compoundPrimary:
                if numZeros==1:
                    for i in range(0,3):
                        if canonicalColor[i]==0:
                            closeEnoughNonPrimaries = testColor[i]<COMPOUND_PRIMARY_ZERO_FUZZINESS

                #TODO: make this a little less clunky
                if numZeros==2: #as long as the difference between elements which are supposed to be 0 is small, the distance from zero can be fairly large (affects brightness)
                    if canonicalColor[0]==0 and canonicalColor[1]==0 and abs(testColor[0] - testColor[1]) < COMPOUND_PRIMARY_INTER_ELEMENT_FUZZINESS:
                        if testColor[0]<COMPOUND_PRIMARY_ZERO_FUZZINESS and testColor[1]<COMPOUND_PRIMARY_ZERO_FUZZINESS:
                            closeEnoughNonPrimaries = True
                    elif canonicalColor[0]==0 and canonicalColor[2]==0 and abs(testColor[0] - testColor[2]) < COMPOUND_PRIMARY_INTER_ELEMENT_FUZZINESS:
                        if testColor[0]<COMPOUND_PRIMARY_ZERO_FUZZINESS and testColor[2]<COMPOUND_PRIMARY_ZERO_FUZZINESS:
                            closeEnoughNonPrimaries = True
                    elif canonicalColor[1]==0 and canonicalColor[2]==0 and abs(testColor[1] - testColor[2]) < COMPOUND_PRIMARY_INTER_ELEMENT_FUZZINESS:
                        if testColor[1]<COMPOUND_PRIMARY_ZERO_FUZZINESS and testColor[2]<COMPOUND_PRIMARY_ZERO_FUZZINESS:
                            closeEnoughNonPrimaries = True

        return closeEnoughPrimaries and closeEnoughNonPrimaries

    def singleColorTraitSelected(self):
        return self.__colorNames[self.colorScore]=='green'

    def scoreColorFieldData(self,theirImportanceData):
        if not isYou:
            raise ValueError('Must be executed on a You color data field.')

        if isMulticolor:
            return multiColorYouScoring(theirImportanceData.colorScore)
        else:
            return singleColorYouScoring(singleColorTraitSelected(),theirImportanceData.colorScore)

    def multiColorYouScoring(self,importanceScoreIndex): #min possible score is 0, max possible score is 1.0
        importanceScore = self.__importanceScoreMapping[importanceScoreIndex]
        traitScore      = self.__traitScoreMapping[self.colorScore]

        scoreDelta = importanceScore - traitScore
        if importanceScore*traitScore > 0: #true if they're the same sign
            scoreDelta=abs(scoreDelta)
        else:
            scoreDelta=-abs(scoreDelta)

        finalScore = scoreDelta * importanceScore #increases importance of delta for extreme scores, makes score 0 if importance is neutral
        finalScore = (finalScore+1.0) / 2.0       #normalize final answer to a range between 0 and 1.0

        return finalScore

    def singleColorYouScoring(self,traitIsSelected,importanceScoreIndex): #trait score is either 1.0 or 0.0, no in-betweens
        if traitIsSelected:
            traitScoreIndex = self.__bestIndex #just set to either extreme trait score
        else:
            traitScoreIndex = self.__worstIndex

        return self.multiColorYouScoring(traitScoreIndex,importanceScoreIndex)
