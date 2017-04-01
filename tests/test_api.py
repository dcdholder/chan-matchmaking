import pytest

from qtrest.api import ChartImageResource

def testRandomAlphabeticalFilename(): #just a really cursory check
    randomString = ChartImageResource.randomAlphabeticalFilename()

    assert len(randomString)==ChartImageResource.filenameNumLetters  #Is the string the right length?
    assert randomString.isalpha()                                      #Is it purely alphabetic?
    assert randomString!=ChartImageResource.randomAlphabeticalFilename #Is a different string reliably generated each time?

def testJsonUri2DictPositive():
    inputUri    = '%7B%22a%22%3A%22b%22%2C%22c%22%3A%5B%22d%22%2C%22e%22%5D%7D'
    decodedDict = ChartImageResource.jsonUri2Dict(inputUri)
    assert decodedDict=={'a': 'b', 'c': ['d', 'e']}

def testJsonUri2DictNegative():
    invalidJSON = 'This is invalid JSON.'

    with pytest.raises(ValueError):
        ChartImageResource.jsonUri2Dict(invalidJSON)
