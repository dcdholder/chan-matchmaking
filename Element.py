#TODO: figure out how abstract classes work in Python
class Element: #a chart element is a collection of individual cells, has a non-configurable weighting within a category
	def __init__(self, elementYaml, pixelMap, isYou)
		self.elementYaml = elementYaml
		self.name        = elementYaml['name']
		self.weighting   = elementYaml['weighting']
		self.pixelMap    = pixelMap
		self.isYou       = isYou #specify whether to get 'You' or 'Them'
		self.cells       = self.__getCells()

	def __youOrThemString():
		if self.isYou:
			return 'you'
		else:
			return 'them'

	def __coordinatesFromString(coordinates):
		coordsAsStringArray = coordinates.split("x")
		coordsAsIntTuple    = tuple(list(map(int,coordsAsStringArray)))

	def getYouAndThemElementsFromYaml(elementYaml)
		pass

	def __getCells():
		pass
