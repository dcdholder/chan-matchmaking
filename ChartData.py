class ChartData:
	def __init__(self, name, categoryDataDict)
		self.name             = name
		self.categoryDataDict = categoryDataDict
		
	def __scoreChartData():
		totalChartScore = 0.0
		for categoryName,category in categories:
			totalChartScore += category.scoreCategory() #each category takes care of its weighting
			
		return totalChartScore
	
	#TODO: improve this so that fewer 'one-sided' high compatibility scores occur -- should not be simply an average of two compatibility scores
	def compare(chartDataB):
		chartAScore = self.__scoreChartData()
		chartBScore = chartB.__scoreChartData()
		
		return (chartAScore + chartBScore) / 2.0

class CategoryData:

class ElementData:
	def __init__

class ColorFieldData:
	__unselectedColor   = 0xFFFFFF
	__singleSelectIndex = 2
	__neutralIndex      = 3
	__colorNames = ['pink', 'blue', 'green', 'yellow', 'orange', 'red']
	__colorCodes = [0xFF00FF, 0x0000FF, 0x00FF00, 0xFFFF00, 0xFF7200, 0xFF0000]
	__importanceScoreMapping = [-1.0, -0.5, 0.0, 0.33, 0.67, 1.0]
	__traitScoreMapping      = [-1.0, -0.5, 0.0, 0.5, 1.0]
	
	def __init__(self, colorCode, isYou, isMulticolor)
		self.isYou        = isYou #tells us whether this is a trait or importance score
		self.isMulticolor = isMulticolor
		self.isSelected   = False
		self.colorScore   = colorScoreFromCode(colorCode) #TODO: would be nice to have an alternate constructor for colorIndex rather than colorCode...
		
		if !isYou and !isMulticolor
			raise ValueError('Them cells are always multicolor.')
		
	def colorScoreFromCode(colorCode)
		for i in range(0,len(colorValues))
			if __colorCodes[i]==colorCode
				self.isSelected = True
				return i
		
		if colorCode==__unselectedColor
			if isMulticolor
				self.isSelected = True
				return __neutralIndex #for multicolor cells, an unfilled cell can be assumed yellow
			else
				self.isSelected = False
				return 0
		
		raise ValueError('Could not map color code ' + colorCode + 'to a valid color score.')
		
	def singleColorTraitSelected()
		return __colorNames[self.colorScore]=='green'
		
	def yourTraitVsTheirImportance(theirImportance)
		if !isYou
			raise ValueError('Must be executed on a You color data field.')
		
		if isMulticolor
			return multiColorYouScoring(theirImportance.colorScore)
		else
			return singleColorYouScoring(singleColorTraitSelected(),theirImportance.colorScore)
		
	def multiColorYouScoring(importanceScoreIndex) #min possible score is 0, max possible score is 1.0	
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
	
	def singleColorYouScoring(traitIsSelected,importanceScoreIndex) #trait score is either 1.0 or 0.0, no in-betweens
		if traitIsSelected:
			traitScoreIndex = len(__traitScoreMapping)-1 #just set to either extreme trait score
		else:
			traitScoreIndex = 0
		
		return multiColorYouScoring(traitScoreIndex,importanceScoreIndex)
