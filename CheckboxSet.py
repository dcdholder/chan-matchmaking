#TODO: figure out how abstract classes work in Python
class CheckboxSet(Element):
	def __init__(self, elementYaml, pixelMap, isYou)
		super().__init__(self,elementYaml,pixelMap,isYou)

class PictographicCheckboxSet(CheckboxSet):
	def __init__(self, elementYaml, pixelMap, isYou)
		super().__init__(self,elementYaml,pixelMap,isYou)
	
	def __getCells():
		cells = {}
		for cellYaml in elementYaml['checkboxes']
			label           = cellYaml['label']
			cellCoordinates = cellYaml['coordinates'][__youOrThemString()]
			cells[cellYaml['label']] = PictographicCell(self,label,pixelMap,cellCoordinates)

class SquareCheckboxSet(CheckboxSet):
	def __init__(self, elementYaml, pixelMap, isYou)
		super().__init__(self,elementYaml,pixelMap,isYou)
		self.isMulticolor = self.elementYaml['isMulticolor']
		self.checkboxSize = self.elementYaml['size']
	
	#TODO: DRY
	def __getCells():
		cells = {}
		for cellYaml in elementYaml['checkboxes']
			label           = cellYaml['label']
			cellCoordinates = cellYaml['coordinates'][__youOrThemString()]
			cells[cellYaml['label']] = SquareCell(self,label,pixelMap,cellCoordinates,checkboxSize)
			
		return cells
