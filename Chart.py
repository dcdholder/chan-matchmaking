#TODO: I should only have to load config.yaml ONCE -- fix this
class Chart:
	__filename = None
	__pixelMap = None

	def __init__(self, categoryRelativeWeightings)
		self.categoryWeightings = self.weightingsFromRelativeWeightings(categoryRelativeWeightings)
		self.categories         = self.__getCategories() #indexed by category name
	
	def getChartData():
		categoryDataDict = {}
		for name,category in category:
			categoryDataDict[name] = category.getCategoryData()
			
		return CategoryData(self.name,categoryDataDict)
	
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
	
	def getWeightingTree():
		weightingsTree = {}
		for categoryName,category in category
			weightingsTree[categoryName]             = {}
			weightingsTree[categoryName]['elements'] = {}
			weightingsTree[categoryName]['weight']   = category.weight
			
			for elementName,element in category.elements
				weightingsTree[categoryName]['elements']['elementName'] = element.weighting
				
		return weightingsTree
	
	def loadInImage(filename):
		__filename = filename
		__pixelMap = self.__getPixelMap(filename)
		
	def saveAsImage(filename):
		__filename = filename
	
	def loadInChartData():
		pass
