import os
import sys
import urllib.parse
import json
import string
import random
import hashlib
from datetime import datetime

from flask import Flask, send_from_directory, request, send_file
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy

from common.Chart import Chart

chartApp = Flask(__name__)
chartApp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath(os.path.dirname(os.path.realpath(__file__))) + '/charts.db'
db = SQLAlchemy(chartApp)

#basically, this prevents the generated image "cache" from growing out of control
class ChartImageModel(db.Model):
    MAX_IMAGES = 100 #as long as 100 users don't try to generate images at the exact same time, we should be alright

    chartDataHash = db.Column(db.String(100), primary_key=True)
    filename      = db.Column(db.String(100), unique=True) #for simplicity's sake, this is the full path
    creationDate  = db.Column(db.DateTime, unique=False)

    def __init__(self,chartDataString,filename):
        self.chartDataHash = self.hashingFunction(chartDataString)
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
        #raise ValueError(ChartImageModel.query.count())
        if (ChartImageModel.query.count() > self.MAX_IMAGES):
            #raise ValueError(ChartImageModel.query.count())
            entries = ChartImageModel.query.order_by(ChartImageModel.creationDate.asc())
            for i in range(0,len(entries.all())-self.MAX_IMAGES):
                os.remove(entries.all()[i].filename)
                db.session.delete(entries[i])

            db.session.commit()

    @classmethod
    def alreadyExists(self,chartDataString): #filename string will evaluate to true
        try:
            existingChart = ChartImageModel.query.filter_by(chartDataHash=self.hashingFunction(chartDataString)).first()
            return existingChart.filename
        except:
            return False

class ChartImageResource(Resource):
    filenameNumLetters = 20
    imageDirectory     = './media/charts/generated/'

    def get(self):
        return self.imageFromChartDataUri(request.form['chartdata'].lower()) #the 'lower()' is important, here

    @classmethod
    def imageFromChartDataUri(self,chartDataUri):
        path     = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + '/' + self.imageDirectory)
        fullPath = ''
        if (ChartImageModel.alreadyExists(chartDataUri)):
            fullPath = ChartImageModel.alreadyExists(chartDataUri)
        else:
            filename            = self.randomAlphabeticalFilename() + '.png'
            fullPath            = os.path.abspath(path + '/' + filename)
            chartDataStringDict = self.jsonUri2Dict(chartDataUri)
            Chart.chartImageFromStringDict(chartDataStringDict,fullPath)
            ChartImageModel.addNew(chartDataUri,fullPath)

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

#TODO: spend a few dozen more hours trying to break this into multiple files without descending into circular import hell
chartApi = Api(chartApp)
chartApi.add_resource(ChartImageResource, '/new')

if __name__ == '__main__':
    db.create_all()
    chartApp.run(debug=True)
