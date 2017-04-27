# The Ultimate QT Infograph REST API
This API spits out a modified *Ultimate QT Infograph* friendship/relationship chart.  

# API
The API accepts a POST request to /new with a JSON payload. Chart image data is returned as a binary blob once the image has been generated.

## Basic Development Info
The API is written in Flask with the help of flask-restful and flask-sqlalchemy (to keep track of a small cache of generated images). The images are generated from the chart data using Pillow.

## Progress
The API can fill in every element in the modified version of the chart it uses (where the sub-image fields have been replaced with bullet lists).

## The Future
- Box in the selected 'Facial Hair' sub-element instead of trying to color it in(no built-in 'fuzziness' support for Pillow floodfill).
- Consider turning off auto-coloring of some empty image elements.
- Extra bullet characters sometimes get drawn in bullet lists.
- Change the font used for the text components.
