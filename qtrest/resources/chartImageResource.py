import sys
import os
import urllib.parse
import json
import string
import random

from flask import send_from_directory,request, send_file
from flask_restful import Resource

from common.Chart import Chart

class ChartImageResource(Resource):
    filenameNumLetters = 20
    imageDirectory     = '../media/charts/generated/'

    def get(self):
        return self.imageUrlFromChartDataUri(request.form['chartdata'].lower()) #the 'lower()' is important, here

    @classmethod
    def imageUrlFromChartDataUri(self,chartDataUri):
        filename            = self.randomAlphabeticalFilename() + '.png'
        path                = os.path.abspath(os.path.dirname(__file__) + '/' + self.imageDirectory)
        fullPath            = os.path.abspath(path + '/' + filename)
        chartDataStringDict = self.jsonUri2Dict(chartDataUri)
        Chart.chartImageFromStringDict(chartDataStringDict,fullPath)

        #return fullPath
        return send_file(fullPath,mimetype='image/png')

    @classmethod
    def randomAlphabeticalFilename(self): #does not generate the image extension
        numLetters   = self.filenameNumLetters
        randomString = ''
        for i in range(0,numLetters):
            randomString += random.choice(string.ascii_letters)

        return randomString

    @classmethod
    def jsonUri2Dict(self,jsonUriString):
        try:
            decodedString = urllib.parse.unquote(jsonUriString)
            decodedDict   = json.loads(decodedString)
        except json.decoder.JSONDecodeError:
            raise ValueError('Cannot retrieve JSON from URI')

        return decodedDict
