#a cell may have the color 'unselected', 'invalid', or one of six others

#TODO: determine whether color testing needs some "fuzziness" by testing with multiple jpeg qualities

import yaml

#Cells
class Cell: #an indivisble component of an image element
	def __init__(self,label,pixelMap,coordinates)
		self.pixelMap       = pixelMap
		self.coordinates    = coordinates
		self.colorDataField = self.__setColor()
	
	def __setColor() #just select color from the given coordinates -- is different for square cell
		#TODO: figure out how to handle invalid cell colors
		centerPixelCoordinates = self.__getCenterPixel()
		
		rgb          = self.pixelMap.getPixel(centerPixelCoordinates)
		hexColorCode = '#{:02x}{:02x}{:02x}'.format(rgb[0],rgb[1],rgb[2])
		
		return ColorDataField(hexColorCode)
	
	def __getCenterPixel(): #the default is just to return the 'coordinates' -- overriden in SquareCell, but not PictographicCell
		return coordinates
	
	def fillCell(coordinates, colorCode):
		pass	

#TODO: allow for multiple color sampling points, since users don't fill in pictographic cells all the same way
class PictographicCell(Cell): #subclass is really just for readability right now
	def __init__(self,label,pixelMap,coordinates)
		super().__init__(self,label,pixelMap,coordinates)

class SquareCell(Cell):
	def __init__(self,label,pixelMap,coordinates,size)
		self.size = size
		super().__init__(self,label,pixelMap,coordinates)
	
	def genRow(pixelMap,baseCoordinates,cellSize,numCells) #create a horizontal row of cells
		cells = []
		for i in range(0,numCells)
			cellCoordinates[0] = baseCoordinates[0] + cellSize[0] * i
			cellCoordinates[1] = baseCoordinates[1]
			cells[i] = SquareCell(pixelMap,cellCoordinates,cellSize)
			
		return cells
	
	def genSquare(pixelMap,coordinates,cellSize,cellDimensions)
		for j in range(0,cellDimensions) #assume all 2D cell arrays are square
			for i in range(0,cellDimensions)
				cells[j][i] = SquareCells(pixelMap,cellCoordinates,cellSize)
	
	def __getCenterPixel()
		middleX = self.coordinates[0] + self.size[0] / 2
		middleY = self.coordinates[1] + self.size[1] / 2

		return (middleX, middleY)
