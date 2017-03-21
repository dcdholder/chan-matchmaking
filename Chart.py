import ChartData
import Category

from PIL import Image
import os

#TODO: I should only have to load config.yaml ONCE -- fix this
class Chart:
    CLEAN_CHART_FILENAME             = "clean.png"
    DEF_CATEGORY_RELATIVE_WEIGHTINGS = {'physical': 1, 'emotional': 1, 'beliefs': 1, 'other': 1}

    def __init__(self, categoryRelativeWeightings):
        self.filename  = None
        self.pixelMap  = None
        self.chartData = None
    
        self.categoryWeightings = self.weightingsFromRelativeWeightings(categoryRelativeWeightings)
        self.categories         = self.__getCategories() #indexed by category name
    
    def getChartData():
        categoryDataDict = {}
        for name,category in category:
            categoryDataDict[name] = category.getCategoryData()
            
        return ChartData(self.name,categoryDataDict)
    
    def __getCategories():
        with open('config.yaml', 'r') as f:
            try:
                categories = {}
                categoriesYaml = yaml.load(f)
                for categoryYaml in categoriesYaml:
                    categories[categoryYaml['category']] = Category(categoryYaml,categoryWeighting[categoryYaml['category']],self.pixelMap)
                    
            except yaml.YAMLError:
                print('Could not open config file.')
    
    def __getPixelMap():
        im = Image.open(self.filename)
        im.convert('RGB')
        
        for category in self.categories: #we need to propagate the new pixelMap down the tree to the Cells
            category.propagatePixelMap(pixelMap)
    
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
        for categoryName,category in category:
            weightingsTree[categoryName]             = {}
            weightingsTree[categoryName]['elements'] = {}
            weightingsTree[categoryName]['weight']   = category.weight
            
            for elementName,element in category.elements:
                weightingsTree[categoryName]['elements']['elementName'] = element.weighting
                
        return weightingsTree
    
    def loadInImage(filename): #loadInImage loads chart data automatically
        self.filename  = filename
        self.pixelMap  = self.__getPixelMap(filename)
        self.chartData = self.getChartData()
    
    def saveAsImage(filename):
        self.filename = filename
        
        for categoryName,category in categories:
            category.colorCategory(self.chartData[categoryName])
    
    def loadInChartData(chartData):
        self.chartData = chartData
        
    def convertImageToCleanImage(filenameA,filenameB):
        chart = Chart()
        chart.loadInImage(filenameA)
        chartData = chart.chartData
        chart.loadInImage(CLEAN_CHART_FILENAME)
        chart.loadInChartData(chartData)
        chart.saveAsImage(filenameB)
        
    def getChartDataFromImage(filename,categoryRelativeWeightings=None):
        if categoryRelativeWeightings==None:
            categoryRelativeWeightings = self.DEF_CATEGORY_RELATIVE_WEIGHTINGS
    
        chart = Chart(categoryRelativeWeightings)
        chart.loadInImage(filename)
        
        return self.chartData
    
    def printChartDataFromImage(filename):
        print(getChartDataFromImage(filename))
    
    def getChartDataFromAllImages(path):
        imageExtensions = [".jpg",".gif",".png"]
    
        for filename in os.listdir(path):
            if filename.endswith(imageExtensions):
                filenames.append(filename)
    
        chartDataDict = {}
        for filename in filenames:
            chartDataDict[filename] = getChartDataFromImage(filename)
            
        return chartDataDict
