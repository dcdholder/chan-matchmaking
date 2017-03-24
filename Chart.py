from ChartData import ChartData, CategoryData, ElementData, ColorFieldData
from Category import Category

import yaml
from PIL import Image
import os

#TODO: I should only have to load config.yaml ONCE -- fix this
class Chart:
    CLEAN_CHART_FILENAME             = "clean.png"
    DEF_CATEGORY_RELATIVE_WEIGHTINGS = {'physical': 1, 'emotional': 1, 'beliefs': 1, 'other': 1}

    def __init__(self, categoryRelativeWeightings=None):
        self.filename  = None
        self.pixelMap  = None
        self.chartData = None

        if categoryRelativeWeightings==None:
            categoryRelativeWeightings = self.DEF_CATEGORY_RELATIVE_WEIGHTINGS
    
        self.categoryWeightings = Category.weightingsFromRelativeWeightings(categoryRelativeWeightings)
        self.categories         = self.__getCategories() #indexed by category name
    
    def getChartData(self):
        categoryDataDict = {}
        for name,category in self.categories.items():
            categoryDataDict[name] = category.getCategoryData()
            
        return ChartData(self.filename,categoryDataDict) #TODO: figure out how to make name something other than the filename
    
    def __getCategories(self):
        with open('config.yaml', 'r') as f:
            categories = {}
            try:
                categoriesYaml = yaml.load(f)
                for categoryYaml in categoriesYaml:
                    categories[categoryYaml['category']] = Category(categoryYaml,self.categoryWeightings[categoryYaml['category']])
                    
            except yaml.YAMLError:
                print('Could not open config file.')
                
        return categories
    
    def __getPixelMap(self):
        pixelMap = Image.open(self.filename)
        pixelMap.convert('RGB')
        
        for categoryName,category in self.categories.items(): #we need to propagate the new pixelMap down the tree to the Cells
            category.propagatePixelMap(pixelMap)
    
    def getWeightingTree(self):
        weightingsTree = {}
        for categoryName,category in category:
            weightingsTree[categoryName]             = {}
            weightingsTree[categoryName]['elements'] = {}
            weightingsTree[categoryName]['weight']   = category.weight
            
            for elementName,element in category.elements.items():
                weightingsTree[categoryName]['elements']['elementName'] = element.weighting
                
        return weightingsTree
    
    def loadInImage(self,filename): #loadInImage loads chart data automatically
        self.filename  = filename
        self.pixelMap  = self.__getPixelMap()
        self.chartData = self.getChartData()
    
    def saveAsImage(self,filename):
        self.filename = filename
        
        for categoryName,category in categories:
            category.colorCategory(self.chartData[categoryName])
    
    def loadInChartData(self,chartData):
        self.chartData = chartData
    
    @staticmethod    
    def convertImageToCleanImage(filenameA,filenameB):
        chart = Chart()
        chart.loadInImage(filenameA)
        chartData = chart.chartData
        chart.loadInImage(CLEAN_CHART_FILENAME)
        chart.loadInChartData(chartData)
        chart.saveAsImage(filenameB)
    
    @staticmethod
    def getChartDataFromImage(filename,categoryRelativeWeightings=None):
        if categoryRelativeWeightings==None:
            categoryRelativeWeightings = Chart.DEF_CATEGORY_RELATIVE_WEIGHTINGS
    
        chart = Chart(categoryRelativeWeightings)
        chart.loadInImage(filename)
        
        return chart.chartData
    
    @staticmethod
    def printChartDataFromImage(filename):
        print(Chart.getChartDataFromImage(filename))
    
    @staticmethod
    def getChartDataFromAllImages(path):
        imageExtensions = [".jpg",".gif",".png"]
    
        for filename in os.listdir(path):
            if filename.endswith(imageExtensions):
                filenames.append(filename)
    
        chartDataDict = {}
        for filename in filenames:
            chartDataDict[filename] = Chart.getChartDataFromImage(filename)
            
        return chartDataDict
