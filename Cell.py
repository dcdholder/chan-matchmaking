#a cell may have the color 'unselected', 'invalid', or one of six others

#TODO: determine whether color testing needs some "fuzziness" by testing with multiple jpeg qualities

from ChartData import ColorFieldData
from PIL import Image,ImageDraw,ImageColor
import yaml

class Cell: #an indivisble component of an image element
    STANDARD_DIMENSIONS = (3828, 4587)

    def __init__(self,label,coordinates):
        #print("Cell creation label: " + label)
        self.label       = label
        self.pixelMap    = None
        self.coordinates = coordinates
    
    def getColorFieldData(self,isYou,isMulticolor):
        return ColorFieldData(self.getColor(),isYou,isMulticolor)
    
    def getColor(self): #just select color from the given coordinates -- is different for square cell
        #TODO: figure out how to handle invalid cell colors
        centerPixelCoordinates = self.getCenterPixel()
        
        if self.pixelMap!=None:
            rgb          = self.pixelMap.getpixel(centerPixelCoordinates)
            hexColorCode = '#{:02x}{:02x}{:02x}'.format(rgb[0],rgb[1],rgb[2])
        else:
            raise ValueError('No pixel map has been propagated down to the cells.')
        
        return hexColorCode
    
    def getCenterPixel(self):
        raise ValueError('Should not reach parent version of method.')
    
    def getExpansionRatio(self):
        x,y = self.pixelMap.size
        xExpansion = x / self.STANDARD_DIMENSIONS[0]
        yExpansion = y / self.STANDARD_DIMENSIONS[1]
        
        expansionRatio = xExpansion
        xYRatio        = xExpansion / yExpansion
        if xYRatio < 0.99 or xYRatio > 1.01: #check that aspect ratio is very close to the original chart's (currently within 1 percent)
            raise ValueError('Image has invalid aspect ratio.')
            
        return expansionRatio
    
    def fillCell(self,colorCode): #WARNING: Pillow does not support fuzzy floodfill, so use a losslessly compressed image
        fillCoordinates = self.getCenterPixel()
        ImageDraw.floodfill(self.pixelMap,fillCoordinates,ImageColor.getrgb(colorCode))
        
    def fillCellByColorFieldData(self,colorFieldData):
        colorCode = colorFieldData.getColorCode()
        self.fillCell(colorCode)

#TODO: allow for multiple color sampling points, since users don't fill in pictographic cells all the same way
class PictographicCell(Cell): #subclass is really just for readability right now
    def __init__(self,label,coordinates):
        super().__init__(label,coordinates)
        
    def getCenterPixel(self): #the default is just to return the 'coordinates' -- overriden in SquareCell, but not PictographicCell
        return (int(self.coordinates[0]*self.getExpansionRatio()), int(self.coordinates[1]*self.getExpansionRatio()))

class SquareCell(Cell):
    def __init__(self,label,coordinates,size):
        self.size = size
        super().__init__(label,coordinates)
    
    @staticmethod
    def genRow(baseCoordinates,cellSize,numCells): #create a horizontal row of cells
        cells = {}
        for i in range(0,numCells):
            cellCoordinates = ((baseCoordinates[0] + cellSize[0] * i), baseCoordinates[1])
            cells[str(i)]   = SquareCell(str(i),cellCoordinates,cellSize)
            
        return cells
    
    @staticmethod
    def genSquare(baseCoordinates,cellSize,cellDimensions):
        cells = {}
        for j in range(0,cellDimensions): #assume all 2D cell arrays are square
            for i in range(0,cellDimensions):
                cellCoordinates              = ((baseCoordinates[0] + cellSize[0] * i), (baseCoordinates[1] - cellSize[1] * j))
                cells[(str(i) + "," + str(j))] = SquareCell((str(i) + "," + str(j)),cellCoordinates,cellSize)
                
        return cells
    
    def getCenterPixel(self):
        middleXBase = self.coordinates[0] + self.size[0] / 2
        middleYBase = self.coordinates[1] - self.size[1] / 2

        return (int(middleXBase*self.getExpansionRatio()), int(middleYBase*self.getExpansionRatio()))
