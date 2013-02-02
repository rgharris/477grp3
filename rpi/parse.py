#!/usr/bin/env python
#This just has a few functions to
#parse the json coming from the microcontroller.
import json, string

numPlayers = 4 #Need to make this change based on webapp
currentPlayer = 1

#Set basic resources for players
baseResources = {'wheat':0, 'ore':0, 'wood':0, 'brick':0, 'sheep':0}
playerResources = []
for i in range(0,numPlayers-1):
	playerResources[i] = baseResources

#Set basic developments for players
baseDev = {'knight':0, 'monopoly':0, 'yearOfPlenty':0, 'roadBuilding':0, 'victoryPoint':0}
playerDev = []
for i in range(0,numPlayers-1):
	playerDev[i] = baseDev

#Set victory cards for players
baseVic = {'longestRoad':False, 'largestArmy':False}
playerVic = []
for i in range(0, numPlayers-1):
	playerVic[i] = baseVic

placedRoads = []
placedSettlements = []
placedCities = []
placedThief = ""

dice = [0,0]

def parse (stringToParse):
	parsedDict = json.loads(stringToParse)
	if(parsedDict[u'command'] == u'piece'):
		if(parsedDict[u'piece'] == u'new'):
			newPiece(parsedDict)
		elif(parsedDict[u'piece'] == u'replace'):
			replacePiece(parsedDict)
		elif(parsedDict[u'piece'] == u'removed'):
			removePiece(parsedDict)
	elif(parsedDict[u'command'] == u'turn'):
		turnChange(parsedDict)

def sendCommand (command, cmdType, result=None, piece=None):
	toSend = {"command":command, "type":cmdType}
	if (result != None):
		toSend["result"] = result
	if (piece != None):
		toSend["piece"] = piece
	toSend = json.dumps(toSend)

def newPiece(parsedDict):
	if(parsedDict[u'piecetype'] == u'road'):
		if(parsedDict[u'isvalid'] == True):
			if(chkroad(parsedDict[u'pieceloc']) == True):
				setRoad(parsedDict[u'pieceloc'])
			else:
				invalidRoad(parsedDict[u'pieceloc'])
		elif(parsedDict[u'isvalid'] == False):
			invalidRoad(parsedDict[u'pieceloc']) #On first call with a location, it will wait for a second call at the same location.
	elif(parsedDict[u'piecetype'] == u'town'):
		if(parsedDict[u'isvalid'] == False):
			invalidTown(parsedDict[u'pieceloc'])
		elif(parsedDict[u'isvalid'] == True):
			if (chkTown(parsedDict[u'pieceloc']) == False): #location, 0 for settlement, 1 for city
				invalidTown(parsedDict[u'pieceloc'])
			else:
				setTown(parsedDict[u'pieceloc'], parsedDict[u'locResources'], 0)
	elif(parsedDict[u'piecetype'] == u'thief'):
		if(parsedDict[u'isvalid'] == True):
			setThief(parsedDict[u'pieceloc']) 
		else:
			invalidThief(parsedDict[u'pieceloc'])

def removePiece(parsedDict):
	if(parsedDict[u'piecetype'] == u'road'):
		invalidRoad(parsedDict[u'pieceloc'])
	elif(parsedDict[u'piecetype'] == u'town'):
		if (chkTown(parsedDict[u'pieceloc'], False, True) == False || parsedDict[u'isvalid'] == False):
			invalidTown(parsedDict[u'pieceloc'])
		else:
			markForCity(parsedDict[u'pieceloc']) #As the city isn't placed yet, it will wait for it to be replaced before showing stuff.
	elif(parsedDict[u'piecetype'] == u'thief'):
		if(chkThief(parsedDict[u'pieceloc'], True) == False || parsedDict[u'isvalid'] == False):
			invalidThief(parsedDict[u'pieceloc'])

def replacePiece(parsedDict):
	if(parsedDict[u'piecetype'] == u'road'):
		invalidRoad(parsedDict[u'pieceloc'])
	elif(parsedDict[u'piecetype'] == u'town'):
		if (chkTown(parsedDict[u'pieceloc'], True) == False || parsedDict[u'isvalid'] == False):
			invalidTown(parsedDict[u'pieceloc']) #Really, this should never be hit, as the check in remove piece should deal with it.
		else:
			setTown(parsedDict[u'pieceloc'], parsedDict[u'locResources'], 0)
	elif(parsedDict[u'piecetype'] == u'thief'):
		if(chkThief(parsedDict[u'pieceloc']) == False || parsedDict[u'isvalid'] == False):
			invalidThief(parsedDict[u'pieceloc'])
		else:
			setThief(parsedDict[u'pieceloc'])

def turnChange(parsedDict):
	for player in parsedDict[u'resources']:
		giveResources(player[u'player'], player[u'received'])
	if currentPlayer == 4:
		currentPlayer = 1
	else:
		currentPlayer = currentPlayer + 1

def giveResources(player, resources):
	player = player - 1
	for resource in resources:
		playerResources[player][resource['resource']] = playerResources[player][resource['resource']] + resource['amount']
	
def chkRoad(loc):
	if loc in placedRoads:
		return False
	else:
		if playerResources[currentPlayer - 1]['brick'] < 1 or playerResources[currentPlayer - 1]['wood'] < 1:
			return False
		else:
			return True

def chkThief(loc, removed=False):
	if(dice[0] + dice[1] != 7):
		if (askKnight() == False): #Ask if the player wishes to use a knight - if none are available, show an empty dialog box "You have no knights. Press OK to continue." type deal
			return False
		elif(removed == False and loc == placedThief):
			return False
		else:
			return True

def chkTown(loc, city=False, removed=False):
	if(city == False):
		if loc in placedCities: #This means we were called by remove, but the thing removed was a city. Whoops!
			return False
		if removed == False:
			if loc in placedSettlements:
				return False
			elif (playerResources[currentPlayer - 1]['brick'] < 1 or playerResources[currentPlayer - 1]['wood'] < 1 or playerResources[currentPlayer - 1]['wheat'] < 1 or playerResrouces[currentPlayer - 1]['sheep'] < 1):
				return False
			elif(askSettlement() == False):
				return False
			else:
				return True
		else:
			if (playerResources[currentPlayer - 1]['wheat'] < 2 or playerResources[currentPlayer - 1]['ore'] < 3):
				return False
			elif(askCity() == False):
				return False
			else:
				return True
	elif(city == True):
		if removed == True:
			return False
		elif loc in placedCities: #Settown should move into placed cities, so if it's in here then it was placed in the wrong spot.
			return False
		else:
			return True

