from qtrest.common.Element import TextElement

from PIL import Image, ImageFont, ImageDraw

class Bullet(TextElement):
    def __init__(self, elementYaml, isYou):
        super().__init__(elementYaml, isYou)

    #TODO: DRY
    @staticmethod
    def getYouAndThemElementsFromYaml(elementYaml):
        youAndThemElements = {}
        if 'you' in elementYaml['coordinates'].keys():
            youAndThemElements['you']  = Bullet(elementYaml,True)
        if 'them' in elementYaml['coordinates'].keys():
            youAndThemElements['them'] = Bullet(elementYaml,False)

        return youAndThemElements

    #"StringArr" here is a bit of a misnomer, since only one string is passed in (not wrapped in a list)
    def enterTextFromStringArr(self,elementDataString):
        if len(elementDataString) > self.maxWidth:
            raise ValueError('String too long for bullet.')

        draw = ImageDraw.Draw(self.pixelMap)
        draw.text((self.coordinates[0],self.coordinates[1]-self.textSize), elementDataString, fill=(0,0,0), font=self.font)
        del draw

class BulletList(TextElement):
    def __init__(self, elementYaml, isYou):
        self.numBullets  = elementYaml['numBullets']
        self.lineSpacing = elementYaml['lineSpacing']
        super().__init__(elementYaml, isYou)

    #TODO: DRY
    @staticmethod
    def getYouAndThemElementsFromYaml(elementYaml):
        youAndThemElements = {}
        if 'you' in elementYaml['coordinates'].keys():
            youAndThemElements['you']  = BulletList(elementYaml,True)
        if 'them' in elementYaml['coordinates'].keys():
            youAndThemElements['them'] = BulletList(elementYaml,False)

        return youAndThemElements

    #TODO: allows for missing cell data in string dict, see above
    def enterTextFromStringArr(self,elementDataStringArr):
        if len(elementDataStringArr) > self.numBullets:
            raise ValueError('More strings than bullets.')

        for elementDataString in elementDataStringArr:
            if len(elementDataString) > self.maxWidth:
                raise ValueError('String too long for bullet.')

        #eliminate empty bullet points
        collapsedElementDataStringArr = []
        for lineText in elementDataStringArr:
            if (not lineText.isspace()) and lineText!='':
                collapsedElementDataStringArr.append(lineText)

        concatenatedText = ''
        #if len(elementDataStringArr)!=1:
        for lineText in collapsedElementDataStringArr:
            concatenatedText += '•' + lineText + '\n'

        draw = ImageDraw.Draw(self.pixelMap)
        draw.text((self.coordinates[0],self.coordinates[1]-self.textSize), concatenatedText, fill=(0,0,0), font=self.font, spacing=self.lineSpacing)
        del draw
