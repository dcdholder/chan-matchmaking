#a cell may have the color 'unselected', 'invalid', or one of six others

#TODO: determine whether color testing needs some "fuzziness" by testing with multiple jpeg qualities

from PIL import Image,ImageDraw
import yaml

class Cell: #an indivisble component of an image element
    def __init__(self,label,coordinates):
        self.pixelMap    = None
        self.coordinates = coordinates
    
    def getColorFieldData(self,isYou,isMulticolor):
        return ColorFieldData(__getColor(),isYou,isMulticolor)
    
    def __getColor(self): #just select color from the given coordinates -- is different for square cell
        #TODO: figure out how to handle invalid cell colors
        centerPixelCoordinates = self.__getCenterPixel()
        
        if self.pixelMap!=None:
            rgb          = self.pixelMap.getPixel(centerPixelCoordinates)
            hexColorCode = '#{:02x}{:02x}{:02x}'.format(rgb[0],rgb[1],rgb[2])
        else:
            raise ValueError('No pixel map has been propagated down to the cells.')
        
        return hexColorCode
    
    def fillCell(self,colorCode): #WARNING: Pillow does not support fuzzy floodfill, so use a losslessly compressed image
        fillCoordinates = self.__getCenterPixel()
        ImageDraw.floodfill(self.pixelMap,fillCoordinates,ImageColor.getrgb(colorCode))
        
    def fillCellByColorFieldData(self,colorFieldData):
        colorCode = colorFieldData.getColorCode()
        self.fillCell(colorCode)

#TODO: allow for multiple color sampling points, since users don't fill in pictographic cells all the same way
class PictographicCell(Cell): #subclass is really just for readability right now
    def __init__(self,label,coordinates):
        super().__init__(self,label,coordinates)
        
    def __getCenterPixel(self): #the default is just to return the 'coordinates' -- overriden in SquareCell, but not PictographicCell
        return coordinates

class SquareCell(Cell):
    def __init__(self,label,coordinates,size):
        self.size = size
        super().__init__(self,label,coordinates)
    
    def genRow(self,baseCoordinates,cellSize,numCells): #create a horizontal row of cells
        cells = []
        for i in range(0,numCells):
            cellCoordinates    = ()
            cellCoordinates[0] = baseCoordinates[0] + cellSize[0] * i
            cellCoordinates[1] = baseCoordinates[1]
            cells[i] = SquareCell(cellCoordinates,cellSize)
            
        return cells
    
    def genSquare(self,baseCoordinates,cellSize,cellDimensions):
        for j in range(0,cellDimensions): #assume all 2D cell arrays are square
            for i in range(0,cellDimensions):
                cellCoordinates    = ()
                cellCoordinates[0] = baseCoordinates[0] + cellSize[0] * i
                cellCoordinates[1] = baseCoordinates[1] - cellSize[1] * j
                cells[j][i]        = SquareCell(cellCoordinates,cellSize)
                
        return cells
    
    def __getCenterPixel(self):
        middleX = self.coordinates[0] + self.size[0] / 2
        middleY = self.coordinates[1] - self.size[1] / 2

        return (middleX, middleY)
