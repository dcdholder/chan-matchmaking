from PIL import Image

class ChartData:
    def __init__(self, name, categoryDataDict):
        self.name             = name
        self.categoryDataDict = categoryDataDict
    
    def __str__(self):
        chartString = "Chart name: " + self.name + '\n'
        for name,categoryData in self.categoryDataDict: 
            chartString += str(categoryData).replace('\n','\n\t') + '\n' #add an indentation level to the category data output, then add a newline
        
        return chartString
    
    def scoreChartData(self,theirChartData,weightingsTree):
        totalChartScore = 0.0
        for categoryName,categoryData in self.categoryDataDict:
            totalChartScore += category.scoreCategoryData(weightingsTree[categoryName]['weight'],weightingsTree[categoryName]['elements']) #each category takes care of its weighting
            
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
    
    #TODO: DRY
    def __str__(self):
        categoryString = "Category: " + self.name + '\n'
        for name,elementDataPair in self.elementDataDict: 
            categoryString += str(elementDataPair['you']).replace('\n','\n\t') #add an indentation level to the category data output, then add a newline
            categoryString += str(elementDataPair['them']).replace('\n','\n\t')
            categoryString += '\n'
        
        return categoryString
    
    def scoreCategoryData(self,theirCategory,weighting,elementWeightings):
        totalCategoryScore = 0.0
        for elementName,elementPair in self.elementDataDict:
            totalCategoryScore += elementPair['you'].scoreElementData(elementPair['them'],elementWeightings[elementName]) #'You' scores 'Them'
        
        totalCategoryScore *= weighting
        
        return totalCategoryScore

class ElementData:
    def __init__(self, name, colorFieldDataDict):
        self.name               = name
        self.colorFieldDataDict = colorFieldDataDict
    
    def __str__(self):
        elementString = "Element: " + self.name + '\n'
        for label,colorFieldData in self.colorFieldDataDict:
            elementString += label + ": " + str(colorFieldData).replace('\n','\n\t') + '\n'
            
        return elementString
    
    def scoreElementData(self,theirElement,weighting):    
        totalElementScore = 0.0
        for colorFieldName,colorFieldData in self.colorFieldDataDict:
            totalElementScore += colorFieldDataDict[colorFieldName].scoreColorFieldData(theirElement.colorFieldDataDict[colorFieldName])
            
        totalElementScore *= weighting
        
        return totalElementScore

class ColorFieldData:
    __unselectedColor   = '#ebebeb'
    __singleSelectIndex = 2
    __neutralIndex      = 3
    __colorNames = ['pink', 'blue', 'green', 'yellow', 'orange', 'red']
    __colorCodes = ['#ff00ff', '#0000ff', '#00ff00', '#ffff00', '#ff7200', '#ff0000']
    __importanceScoreMapping = [-1.0, -0.5, 0.0, 0.33, 0.67, 1.0]
    __traitScoreMapping      = [-1.0, -0.5, 0.0, 0.5, 1.0]
    
    def __init__(self, colorCode, isYou, isMulticolor):
        self.isYou        = isYou #tells us whether this is a trait or importance score
        self.isMulticolor = isMulticolor
        self.isSelected   = False
        self.colorScore   = colorScoreFromCode(colorCode) #TODO: would be nice to have an alternate constructor for colorIndex rather than colorCode...
        
        if not isYou and not isMulticolor:
            raise ValueError('Them cells are always multicolor.')
    
    def __str__(self):
        return colorCode
    
    def colorScoreFromCode(self,colorCode):
        for i in range(0,len(colorValues)):
            if __colorCodes[i]==colorCode:
                self.isSelected = True
                return i
        
        if colorCode==__unselectedColor:
            if isMulticolor:
                self.isSelected = True
                return __neutralIndex #for multicolor cells, an unfilled cell can be assumed yellow
            else:
                self.isSelected = False
                return 0
        
        raise ValueError('Could not map color code ' + colorCode + 'to a valid color score.')
    
    def getColorCode(self):
        return __colorCodes[self.colorScore]
    
    def singleColorTraitSelected(self):
        return __colorNames[self.colorScore]=='green'
    
    def scoreColorFieldData(self,theirImportanceData):
        if not isYou:
            raise ValueError('Must be executed on a You color data field.')
        
        if isMulticolor:
            return multiColorYouScoring(theirImportanceData.colorScore)
        else:
            return singleColorYouScoring(singleColorTraitSelected(),theirImportanceData.colorScore)
        
    def multiColorYouScoring(self,importanceScoreIndex): #min possible score is 0, max possible score is 1.0    
        importanceScore = __importanceScoreMapping[importanceScoreIndex]
        traitScore      = __traitScoreMapping[self.colorScore]

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
            traitScoreIndex = len(__traitScoreMapping)-1 #just set to either extreme trait score
        else:
            traitScoreIndex = 0
        
        return multiColorYouScoring(traitScoreIndex,importanceScoreIndex)
