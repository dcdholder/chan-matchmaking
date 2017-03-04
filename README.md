# WORK IN PROGRESS

## General Idea
This is an application for playing matchmaker, using a database of personal data taken from QT charts.
Looks like I'll be learning/using Django, since I want to stick with one language and Python has the best Imagemagick/Tesseract support.

## Challenges
- Finish data entry for the image elements config file (image coordinates and size)
- Figure out how to combine the different chart image data representations with the models
- Write a script for generating chart images from chart data objects
- Write a form application for generating chart data objects
- Write a script to convert a batch of chart images into chart data, and save that data to the database
- Add database search functionality (user-configurable category weightings)
- Find a way to return QT data on the frontend in text and image form
- Find a way to pull text from the text sections
