from flask import Flask
from flask_restful import Api

from resources.chartImageResource import ChartImageResource

chartApp = Flask(__name__)
chartApi = Api(chartApp)

chartApi.add_resource(ChartImageResource, '/new')

if __name__ == '__main__':
    chartApp.run(debug=True)
