import os
import sys
import urllib.parse
import json
import string
import random
import hashlib
from datetime import datetime

from flask import Flask, request, send_file
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from qtrest.common.Chart import Chart

chartApp = Flask(__name__)
chartApp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath(os.path.dirname(os.path.realpath(__file__))) + '/charts.db'
db = SQLAlchemy(chartApp)
CORS(chartApp)

#basically, this prevents the generated image "cache" from growing out of control
class ChartImageModel(db.Model):
    MAX_IMAGES = 100 #as long as 100 users don't try to generate images at the exact same time, we should be alright

    chartDataHash = db.Column(db.String(100), primary_key=True)
    filename      = db.Column(db.String(100), unique=True) #for simplicity's sake, this is the full path
    creationDate  = db.Column(db.DateTime, unique=False)

    def __init__(self,chartDataString,filename):
        self.chartDataHash = ChartImageModel.hashingFunction(chartDataString)
        self.filename      = filename
        self.creationDate  = datetime.utcnow()

    def __repr__(self):
        return self.filename

    @classmethod
    def hashingFunction(self,string): #just a dinky general-purpose string hasher
        return hashlib.sha224(string.encode("utf8")).hexdigest()

    @classmethod
    def addNew(self,chartDataString,filename):
        db.session.add(ChartImageModel(chartDataString,filename))
        db.session.commit()
        self.keepNewestN()

    @classmethod
    def keepNewestN(self):
        if (ChartImageModel.query.count() > self.MAX_IMAGES):
            entries = ChartImageModel.query.order_by(ChartImageModel.creationDate.asc())
            for i in range(0,len(entries.all())-self.MAX_IMAGES):
                os.remove(entries.all()[i].filename)
                db.session.delete(entries[i])

            db.session.commit()

    @classmethod
    def alreadyExists(self,chartDataString): #filename string will evaluate to true
        try:
            existingChart = ChartImageModel.query.filter_by(chartDataHash=ChartImageModel.hashingFunction(chartDataString)).first()
            return existingChart.filename
        except:
            return False

#TODO: get this running, then put this config data somewhere centralized ('global.yaml')
class VersionsResource(Resource):
    pass

class VersionFormatResource(Resource):
    pass

class ChartImageResource(Resource):
    filenameNumLetters = 20
    imageDirectory     = './media/charts/generated/'

    def post(self):
        return self.imageFromChartDataUri(request.get_json()) #the 'lower()' is important, here

    @classmethod
    def imageFromChartDataUri(self,chartDataStringDict):
        path     = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + '/' + self.imageDirectory)
        fullPath = ''
        if ChartImageModel.alreadyExists(json.dumps(chartDataStringDict)):
            fullPath = ChartImageModel.alreadyExists(json.dumps(chartDataStringDict))
        else:
            filename            = self.randomAlphabeticalFilename() + '.jpg'
            fullPath            = os.path.abspath(path + '/' + filename)
            ChartImageModel.addNew(json.dumps(chartDataStringDict),fullPath)
            Chart.chartImageFromStringDict(chartDataStringDict,fullPath)

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

db.create_all() #needs to be after the model is defined

#TODO: spend a few dozen more hours trying to break this into multiple files without descending into circular import hell
chartApi = Api(chartApp)
chartApi.add_resource(ChartImageResource, '/new')
#chartApi.add_resource(VersionsResource, '/versions')
#chartApi.add_resource(VersionFormatResource, '/format')

if __name__ == '__main__':
    chartApp.run(debug=True)
