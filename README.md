# The Ultimate QT Infograph REST API
This thing spits out an *Ultimate QT Infograph* friendship/relationship chart when presented with a REST request in the form of a garbled JSON string containing the desired chart data.  

# API
Chart data should be of the form encodeURIComponent(JSON.stringify(chartDataObject)), where chartDataObject is a JS object indexed first by category name, image element name, 'you' or 'them', then image subelement name.
- {url}/new/?chartdata={chart data}

## Basic Development Info
The API is written in Flask with the help of flask-restful (to simplify the REST interface) and flask-sqlalchemy (to keep track of a small cache of generated images). The images are generated from the chart data using Pillow.

## Progress
Currently the API is only able to fill in the "personality quirks" section. The plan is to add support for other parts of the chart in tandem with the frontend.

## Future Challenges
- Support all non-text, non-image fields from the QT chart
- Add matchmaker functionality
