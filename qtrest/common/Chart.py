from qtrest.common.ChartData import ChartData, CategoryData, ElementData, ColorFieldData
from qtrest.common.Category import Category

import time
import yaml
from PIL import Image
import os

#TODO: I should only have to load config.yaml ONCE -- fix this
class Chart:
    CHART_CONFIG_FILENAME            = "chart-configs/v3.yaml"
    CLEAN_CHART_FILENAME             = "../media/charts/blank/v3.png"
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
        with open(os.path.dirname(__file__) + '/' + self.CHART_CONFIG_FILENAME, 'r') as f:
            categories = {}
            try:
                categoriesYaml = yaml.load(f)
                for categoryYaml in categoriesYaml:
                    categories[categoryYaml['category']] = Category(categoryYaml,self.categoryWeightings[categoryYaml['category']])

            except yaml.YAMLError:
                raise ValueError('Could not open config file.')

        return categories

    #TODO: change this to a setter, and update references to it
    def __getPixelMap(self):
        pixelMap = Image.open(os.path.dirname(__file__) + '/' + self.filename)
        pixelMap.load()
        pixelMap.convert('RGB')

        for categoryName,category in self.categories.items(): #we need to propagate the new pixelMap down the tree to the Cells
            category.propagatePixelMap(pixelMap)

        return pixelMap

    def getWeightingTree(self):
        weightingsTree = {}
        for categoryName,category in self.categories.items():
            weightingsTree[categoryName]             = {}
            weightingsTree[categoryName]['elements'] = {}
            weightingsTree[categoryName]['weight']   = category.weighting

            for elementName,elementDict in category.elements.items():
                weightingsTree[categoryName]['elements']['elementName'] = elementDict['you'].weighting

        return weightingsTree

    def loadInImage(self,filename): #loadInImage loads chart data automatically
        self.filename  = filename
        self.pixelMap  = self.__getPixelMap()
        self.chartData = self.getChartData()

    def saveAsImage(self,filename):
        self.filename = filename

        initial = time.time() * 1000
        for categoryName,category in self.categories.items():
            category.colorCategory(self.chartData.categoryDataDict[categoryName])
        final = time.time() * 1000 - initial
        print(final)

        initial = time.time() * 1000
        self.pixelMap.save(filename)
        final = time.time() * 1000 - initial
        print(final)

    def loadInChartData(self,chartData):
        self.chartData = chartData

    #TODO: currently does not check if all category data is present, include this once frontend is done
    def colorWithChartDataStringDict(self,chartDataStringDict):
        for categoryName,categoryStringDict in chartDataStringDict.items():
            self.categories[categoryName].colorCategoryFromStringDict(categoryName,categoryStringDict)

    @staticmethod
    def chartImageFromStringDict(stringDict,filename):
        chart = Chart()
        chart.loadInImage(Chart.CLEAN_CHART_FILENAME)
        chart.colorWithChartDataStringDict(stringDict)

        chart.pixelMap.save(filename)

    @staticmethod
    def convertImageToCleanImage(filenameA,filenameB):
        chart = Chart()
        #initial = time.time() * 1000
        chart.loadInImage(filenameA)
        #final = time.time() * 1000 - initial
        #print(final)
        chartData = chart.chartData
        chart.loadInImage(Chart.CLEAN_CHART_FILENAME)
        chart.loadInChartData(chartData)
        #initial = time.time() * 1000
        chart.saveAsImage(filenameB)
        #final = time.time() * 1000 - initial
        #print(final)

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

    @staticmethod
    def compareImages(filenameA,filenameB):
        chart      = Chart(Chart.DEF_CATEGORY_RELATIVE_WEIGHTINGS)
        weightings = chart.getWeightingTree()

        chartDataA = Chart.getChartDataFromImage(filenameA)
        chartDataB = Chart.getChartDataFromImage(filenameB)

        compatibilityScore = chartDataA.compare(chartDataB,weightings)

        return compatibilityScore
