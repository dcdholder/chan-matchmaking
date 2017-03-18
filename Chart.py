#TODO: I should only have to load config.yaml ONCE -- fix this
class Chart:
	def __init__(self, filename, categoryRelativeWeightings)
		self.filename           = filename
		self.categoryWeightings = self.weightingsFromRelativeWeightings(categoryRelativeWeightings)
		self.pixelMap           = self.__getPixelMap()
		self.categories         = self.__getCategories() #indexed by category name
		
	def __getCategories():
		with open('config.yaml', 'r') as f:
    		try:
    			categories = {}
    			categoriesYaml = yaml.load(f)
        		for categoryYaml in categoriesYaml
        			categories[categoryYaml['category']] = Category(categoryYaml,categoryWeighting[categoryYaml['category']],self.pixelMap)
        			
    		except yaml.YAMLError:
        		print('Could not open config file.')
	
	def __getPixelMap():
		im = Image.open(self.filename)
		im.convert('RGB')
	
	#relativeWeightings are integers -- the fractional weightings are relative to the sum of the relativeWeightings
	def weightingsFromRelativeWeightings(relativeWeightings):
		totalRelative = 0
		for weightingName,relativeWeighting in relativeWeightings:
			totalRelative += relativeWeighting
			
		weightings = {}
		for weightingName,relativeWeighting in relativeWeightings:
			weightings[weightingName] = (float)relativeWeighting / (float)totalRelative
			
		return weightings
	
	def scoreChart():
		totalChartScore = 0.0
		for categoryName,category in categories:
			totalChartScore += category.scoreCategory() #each category takes care of its weighting
			
		return totalChartScore
	
	#TODO: improve this so that fewer 'one-sided' high compatibility scores occur -- should not be simply an average of two compatibility scores
	def compareCharts(chartB):
		chartAScore = scoreChart()
		chartBScore = chartB.scoreChart()
		
		return (chartAScore + chartBScore) / 2.0
