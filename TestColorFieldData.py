import pytest

from ChartData import ColorFieldData

def test_closeEnoughCompoundPrimaryFarFromZero(): #should fail when you get too far from zero, despite non-primaries being close to each other
    assert not ColorFieldData.closeEnoughColor('#ff0000','#feaaaa')

def test_closeEnoughCompoundPrimaryFarNonPrimary(): #should fail when subpixels which are supposed to be 0 are far from each other
    assert not ColorFieldData.closeEnoughColor('#ff0000','#fe4400')

def test_closeEnoughCompoundPrimaryCloseNonprimary(): #should succeed when subpixels which are supposed to be 0 are close to each other
    assert ColorFieldData.closeEnoughColor('#ff0000','#fe2220')

def test_closeEnoughNonCompoundPrimaryClose(): #should succeed when subpixels are close to canonical values
    assert ColorFieldData.closeEnoughColor('#ff7200','#fe6511')

def test_closeEnoughNonCompoundPrimaryFar(): #should fail when subpixels are far from canonical values
    assert not ColorFieldData.closeEnoughColor('#ff7200','#ee9943')
    
def test_htmlCodeToRgbPositive():
    assert ColorFieldData.htmlCodeToRgb('#ff00ff') == (255,0,255)
    
def test_htmlCodeToRgbInvalidChars():
    with pytest.raises(ValueError):
        ColorFieldData.htmlCodeToRgb('#gg00ff')
        
def test_htmlCodeToRgbMissingPoundSign():
    with pytest.raises(ValueError):
        ColorFieldData.htmlCodeToRgb('ff00ff')
        
def test_htmlCodeToRgbTooLong():
    with pytest.raises(ValueError):
        ColorFieldData.htmlCodeToRgb('#ff00ff00')

def test_htmlCodeToRgbTooShort():
    with pytest.raises(ValueError):
        ColorFieldData.htmlCodeToRgb('#ff00')
