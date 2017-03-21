# can I have the objects INCLUDE a model? 
from django.db import models

class Chart(models.Model):
	filename = models.CharField(max_length=30)
	fileHash = models.CharField(max_length=30)

class Field(models.Model):
	subCategory   = models.CharField(max_length=30)
	selection     = models.CharField(max_length=30) #selection is in some cases a string representing a numerical index
	multivalueYou = models.BooleanField() #do we support values other than green for this field in the (You) section?
	weighting     = FloatField()

#compound key should be fieldId, chartId, isYou
class FieldData(models.Model):
	chart     = models.ForeignKey(ChartData)
	isYou     = models.BooleanField() #obviously, if the field doesn't apply to you it must apply to them
	field     = models.ForeignKey(Field)
	score     = models.FloatField()
	weighting = FloatField() #weighting is here and not in Field to account for 
	
	def compatibilityScoreYourPerspective(theirYouField)
		if !isYou
			
		else
			#throw an exception - must compare your Them to their You
	
	def compatibilityScoreTheirPerspective(theirThemField)
		if isYou
			
		else
			#throw an exception - must compare your You to their Them

	#just take the average of the unidirectional compatibility scores -- unless either score is zero
	def compatibilityScore(yourYou,yourThem,theirYou,theirThem)
		total =  yourYou.compatibilityScoreTheirPerspective(theirThem)
		if total==0.0
			return 0.0
		
		total += yourThem.compatibilityScoreYourPerspective(theirYou)
		
		return total/2.0 #will return 0.0 if both are zero
	
#first we order fields by weighting, given an input category weighting
#returns a list of Fields sorted by "true weighting"
def fieldWeightingOrder(categoryWeightings)
	trueWeighting = {}
	for field in Field.objects.all()
		if field in categoryWeightings
			trueWeighting[field] = field.weighting * categoryWeightings[field.category]
	
	return sorted(trueWeighting, key=trueWeighting.get())

#search through charts for best match within time limit
#if time limit exceeded, take a small selection from the remaining chart list and return the best one
def searchForBestMatches(yourChart,categoryWeightings,dealBreakers,timeLimit)
	currentScores = {}
	chartsInRunning = set(ChartData.objects.all()) #set allows for fast removes
	fieldsInWeightingOrder = fieldWeightingOrder(categoryWeightings)
	
	#immediately filter out any dealBreaker fields (to save a massive amount of processing time)
	#gender, height, age, race likely on the chopping block -- set using "looking for waifu"
	for field in dealBreakers
		yourYou  = FieldData.objects.get(field=field, chart=yourChart, isYou=True)
		yourThem = FieldData.objects.get(field=field, chart=yourChart, isYou=False)
	
		markForDeletion = []
		for chart in chartsInRunning
			theirYou  = FieldData.objects.get(field=field, chart=chart, isYou=True)
			theirThem = FieldData.objects.get(field=field, chart=chart, isYou=False)
			
			if compatibilityScore(yourYou,yourThem,theirYou,theirThem)==0.0
				markForDeletion.append(chart) #can't change size of set while iterating over it
	
	for chart in markForDeletion
		chartsInRunning.remove(chart)
	
	#now create a filtered list of fields to search without breaking order
	filteredFields = {}
	for field in fieldsInWeightingOrder
		if field not in dealBreakers
			filteredFields.append(field)
	
	#TODO: add a way to remove almost all charts from scoring system on timeout
	#find the remaining chart with the best score
	bestScore = 0.0
	bestScoreChart = ChartData.objects.get() #just get a random chart, doesn't matter which
	for field in fieldsInWeightingOrder
		trueWeighting = field.weighting * categoryWeightings[field.category]
	
		yourYou  = FieldData.objects.get(field=field, chart=yourChart, isYou=True)
		yourThem = FieldData.objects.get(field=field, chart=yourChart, isYou=False)
	
		markForDeletion = []
		for chart in chartsInRunning
			maxPossibleScoreForChart = currentScores[chart] + (1.0-weightingAccountedFor)
		
			if bestScore > maxPossibleScoreForChart
				markForDeletion.append(chart) #remove charts which couldn't possibly win
				break
		
			theirYou  = FieldData.objects.get(field=field, chart=chart, isYou=True)
			theirThem = FieldData.objects.get(field=field, chart=chart, isYou=False)
			
			currentScores[chart] += compatibilityScore(yourYou,yourThem,theirYou,theirThem) * weight
			if currentScores[chart] > bestScore
				bestScore      = currentScores[chart]
				bestScoreChart = chart
		
		for chart in markForDeletion
			chartsInRunning.remove(chart)
				
		weightingAccountedFor += trueWeighting
		
	#take into account missing dealBreaker weightings
	missingWeight = 0.0
	for field in dealBreakers
		missingWeight += field.weighting
		
	for chart in currentScores
		currentScores[chart] /= 1.0-missingWeight
		
	#sort the charts still in the running by highest first
	sortedCharts = reverse(sorted(currentScores, key=currentScores.get()))
	
	return sortedCharts
