def htmlCodeToRgb(htmlCode):
    #collect the digit portion
    #break into string trio of two characters each
    #convert hex string to byte for each
    #return result

def closeEnough(htmlCanonicalColor,htmlTestColor):
    PRIMARY_FUZZINESS               = 16
    NON_PRIMARY_FUZZINESS           = 32
    
    COMPOUND_PRIMARY_ZERO_FUZZINESS          = 128
    COMPOUND_PRIMARY_INTER_ELEMENT_FUZZINESS = 16

    canonicalColor = htmlCodeToRgb(htmlCanonicalColor)
    testColor      = htmlCodeToRgb(htmlTestColor)

    closeEnoughPrimaries    = True
    closeEnoughNonPrimaries = True
    for i in range(0,3):
        if canonicalColor[i]==255: #primary color
            if testColor[i] < (canonicalColor[i] - PRIMARY_FUZZINESS):
                closeEnoughPrimaries = False
        else:
            if testColor[i] < (canonicalColor[i] - NON_PRIMARY_FUZZINESS) || testColor[i] > (canonicalColor[i] + NON_PRIMARY_FUZZINESS):
                closeEnoughNonPrimaries = False
    
    if !closeEnoughNonPrimaries: #give extra allowance when the subpixels are exclusively either FF or 00
        compoundPrimary = True
        for i in range(0,3):
            if canonicalColor[i]!=0 && canonicalColor[i]!=255:
                compoundPrimary = False
                
        if compoundPrimary: #as long as the difference between elements which are supposed to be 0 is small, the distance from zero can be fairly large (affects brightness) 
            redGreenPasses  = abs(canonicalColor[0] - canonicalColor[1]) < COMPOUND_PRIMARY_INTER_ELEMENT_FUZZINESS
            redBluePasses   = abs(canonicalColor[0] - canonicalColor[2]) < COMPOUND_PRIMARY_INTER_ELEMENT_FUZZINESS
            greenBluePasses = abs(canonicalColor[1] - canonicalColor[2]) < COMPOUND_PRIMARY_INTER_ELEMENT_FUZZINESS
            
            if redGreenPasses && redBluePasses && greenBluePasses:
                for i in range(0,3):
                    if testColor[i] > (canonicalColor[i] - COMPOUND_PRIMARY_ZERO_FUZZINESS) && testColor[i] < (canonicalColor[i] + COMPOUND_PRIMARY_ZERO_FUZZINESS):
                        closeEnoughNonPrimaries = True
                        
    return closeEnoughPrimaries && closeEnoughNonPrimaries

#take some points from a sample chart
#I'm definitely going to want to unit test this one, and it should be easy since I have complete control over state
#use red and pink for compound color tests
#use orange for non-compound color tests
def testCloseEnoughCompoundPrimaryFarFromZero(): #should fail when you get too far from zero, despite non-primaries being close to each other

def testCloseEnoughCompoundPrimaryFarNonPrimary(): #should fail when elements supposed to be 0 are far from each other

def testCloseEnoughCompoundPrimaryCloseNonprimary(): #should succeed when elements supposed to be 0 are close to each other

def testCloseEnoughNonCompoundPrimaryClose():

def testCloseEnoughNonCompoundPrimaryFar():

def testHtmlCodeToRgbPositive():

def testHtmlCodeToRgbNegative():
