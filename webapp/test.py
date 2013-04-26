#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

##########################################################################
#                     Hackers of Catron Web Interface
#=========================================================================
#
# Written Spring 2013
# Last update: April 22, 2013
# Purdue University ECE 477: Senior Design Team 3
# Team Hex Me Baby
# Spencer Julian, Robert Harris, Ryan Pawling, Josh Hunsberger
#
# This is the web interface for the Hackers of Catron. It runs on any
# WSGI-compliant web server on a Raspberry Pi. Python 3, Python-Bottle,
# and the quick2wire i2c libraries are required. Everything else should
# come installed with python.
#########################################################################
import bottle
from bottle import get, post, request, response, static_file, template, TEMPLATE_PATH

##########################USEFUL FUNCTIONS################################
def readJson(jfile):
#This function reads the json from a given file and
#returns a dictionary of the file's output.
	from json import load
	jsonInfo = open(jfile)
	#Because there's a possibility that two devices try to read the file
	#at the same time, try up to 3 times at different intervals before
	#giving up.
	try:
		info = load(jsonInfo)
	except ValueError:
		from time import sleep
		sleep(.5)
		try:
			info = load(jsonInfo)
		except:
			sleep(.25)
			try:
				info = load(jsonInfo)
			except:
				sleep(.125)
				try:
					info = load(jsonInfo)
				except:
					raise ValueError('JSON Could not be read.')
	jsonInfo.close()
	return info

def writeJson(jfile, info):
#This function writes the dictionary to a given file
#in the form of json.
	from json import dump
	with open(jfile, 'w') as f:
	  #Do the same as readJson for writing files.
		try:
			dump(info, f, ensure_ascii=False)
		except ValueError:
			from time import sleep
			sleep(.5)
			try:
				dump(info, f, ensure_ascii=False)
			except:
				sleep(.25)
				try:
					dump(info, f, ensure_ascii=False)
				except:
					sleep(.125)
					try:
						dump(info, f, ensure_ascii=False)
					except:
						raise ValueError("JSON Could not be written.")
		f.close()
	return info

def writei2c(reg, val):
#Write the value val to the microcontroller in the register reg.
	import quick2wire.i2c as i2c
	registers = {'pi':0, 'currentPlayer':1, 'playerCount':2, 'debug1':30, 'debug2':31, 'debug3':32, 'debug4':33, 'debug5':34}
	flags = {'turnOn':1, 'newGame':2, 'diceRolled':3, 'endTurn':4, 'roadDevCard':5, 'knightDevCard': 6, 'confirm':7, 'reject':8, 'clearFlag':9, 'purchaseRoad':10, 'purchaseSettlement':11, 'purchaseCity':12, 'endGame':13, 'shutdown':14, 'stopBuild':15, 'readResources':16}
	if reg == 'pi':
		#If we're writing to the pi's flags register, then we'll be getting an id of what to write instead of
		#a number. Map it appropriately here.
		val = flags[val]
	with i2c.I2CMaster() as bus:
		bus.transaction(i2c.writing_bytes(0x50, registers[reg], val))

def checkIfNextPlayer(playerID):
#This function checks to see if we need to move to the next player's
#turn during initial setup. This function should only run during initial setup.
	if getGameStatus()['setupComplete'] == 1:
		return False
	playerInfo = getPlayerInfo(playerID)
	initPlacements = playerInfo['initialPlacements']
	if initPlacements['settlement'] == initPlacements['road'] and initPlacements['settlement'] < 2:
		#If the number of settlments is equal to the number of roads, and we have less than two settlements,
		#that means we've placed a settlement.
		playerInfo['initialPlacements']['settlement'] += 1
		playerInfo['points'] += 1
		writePlayerInfo(playerID, playerInfo)
	elif initPlacements['settlement'] > initPlacements['road'] and initPlacements['road'] < 2:
		#Likewise, if the number of settlements is greater than the number of roads, then we've placed a road.
		playerInfo['initialPlacements']['road'] += 1
		writePlayerInfo(playerID, playerInfo)
		endTurn(playerID)

def readi2c(reg, playerID=-1):
#This function reads from the i2c register reg. It does some fancy formatting with the output as well.
	import quick2wire.i2c as i2c
	registers = {'micro':3, 'thieved':4, 'pieceType':6, 'port':7, 'longestRoad':8, 'dice':9, 'resources':10}
	flags = {'newPiece':5, 'newThief':4, 'error':6, 'diceReady':9, 'newRoad':8, 'allClear':11}
	readNum = 1
	startReg = registers[reg]
	if reg == 'resources' and playerID >= 0 and playerID <= 3:
		#If we're reading resources, then we need to start at the right register, which is 10 for player 1, 15 for player 2, 20 for player 3, and 25 for player 4. We also need to read 5 values instead of just 1.
		startReg = (playerID * 5) + registers['resources']
		readNum = 5
	with i2c.I2CMaster() as bus:
		#When we read from the micro, we need to first write which register we want to read,
		#then read the register.
		microResponse = bus.transaction(i2c.writing_bytes(0x50, startReg), i2c.reading(0x50, readNum))
	#Now we need to format the response.
	if reg == 'resources':
		#If we've read resources, then we have 5 values, so map them to their appropriate resource and
		#return that dictionary.
		response = {'ore':microResponse[0][0], 'wheat':microResponse[0][1], 'sheep':microResponse[0][2], 'clay':microResponse[0][3], 'wood':microResponse[0][4]}
		return response
	elif reg == 'pieceType':
		#If we've read the pieceType register, then we need to do some math to determine if we're confirming,
		#removing, or replacing, and what the piece type is.
		#These values come from the i2c.h file in the micro directory.
		microResponse = microResponse[0][0]
		if microResponse >= 10 and microResponse < 20:
			toDo = 'confirm'
			modVal = 10
		elif microResponse >= 20 and microResponse < 30:
			toDo = 'remove'
			modVal = 20
		elif microResponse >= 30:
			toDo = 'replace'
			modVal = 30
		else:
			toDo = 'error'
			modVal = 10
		if microResponse % modVal == 0:
			pieceType = 'thief'
		elif microResponse % modVal == 1:
			pieceType = 'road'
		elif microResponse % modVal == 2:
			pieceType = 'settlement'
		elif microResponse % modVal == 3:
			pieceType = 'city'
		else:
			pieceType = 'error'
		return toDo, pieceType
	else:
		response = microResponse[0][0]
		return response

def getResources(playerID):
#This function assigns the resources to the given player based on the response from the board.
	resources = readi2c('resources', playerID)
	playerInfo = getPlayerInfo(playerID)
	for resource in resources:
		playerInfo['resources'][resource] += int(resources[resource])
	writePlayerInfo(playerID, playerInfo)

def displayResources(playerID):
#This function builds a json string to send back to the client, which will allow it to update it's
#interface.
	playerInfo = getPlayerInfo(playerID)
	gameStatus = getGameStatus()
	from json import dumps
	#Here we send it the player's resources, the number of development cards available, and a refresh flag.
	#The flag's values are defined in the js/functions.js file.
	output = playerInfo['resources'].copy()
	output['dev'] = sum(playerInfo['cards'].values()) + sum(playerInfo['onHold'].values())
	#If we're reading stuff for the current player, then we need to check a few other things as well.
	if(gameStatus['currentPlayer'] == playerID):
		response = readi2c('micro', playerID)
		#First we need to see if there's a new piece on the board, and if so, set the flag.
		if (response == 5 or response == 6 or response == 4):
			output['flag'] = "5"
		#We also need to see if we're currently in the middle of a road building card, and set the flag if so.
		elif (gameStatus['buildingRoads'] > -1 and gameStatus['buildingRoads'] <= 2):
			output['flag'] = "7"
		#And finally we need to see if we're in the middle of a knight card, and if so set the flag.
		elif (gameStatus['playingKnight'] == 1):
			output['flag'] = "8"
		elif playerInfo['flag'] != "15":
			if(gameStatus['runningPurchase'] == 1):
				gameStatus['runningPurchase'] = 0
				writeGameInfo("gameState", gameStatus)
			output['flag'] = playerInfo['flag']
		elif playerInfo['flag'] == "15":
			if(gameStatus['runningPurchase'] == 0):
				gameStatus['runningPurchase'] = 1
				writeGameInfo("gameState", gameStatus)
			output['flag'] = playerInfo['flag']
		else:
			output['flag'] = playerInfo['flag']
	else:
		output['flag'] = playerInfo['flag']
	#We also need to send the player's current points - all of them, not just the public ones.
	output['points'] = playerInfo['points'] + playerInfo['cards']['victory'] + playerInfo['onHold']['victory']
	#But if they're at or above 10 points, they've won the game, so skip to that function to do things.
	if output['points'] >= 10:
		endGame(playerID)
	#We also need to let the client know if the initial setup is done.
	output['initSetup'] = 0
	if gameStatus['setupComplete'] == 0:
		output['initSetup'] = 1
	#And finally, give the client the dice number.
	output['dice'] = gameStatus['diceRolled']
	return dumps(output)

def endGame(playerID):
#This function ends the game when a player has reached 10 or more points.
	gameState = getGameStatus()
	#Set the winning player ID
	for i in range(0, gameState['numPlayers']):
		#Notify everyone of game over
		playerInfo = getPlayerInfo(i)
		playerInfo['flag'] = "9"
		writePlayerInfo(i, playerInfo)
	gameState['gameEnd'] = int(playerID)
	writeGameInfo("gameState", gameState)
	#Notify micro of game over.
	writei2c('pi', 'endGame')
	

def updatePlayerName(playerID, newName):
#This function simply updates the playerName for a given player.
	playerInfo = getPlayerInfo(playerID)
	playerInfo['playerName'] = newName
	writePlayerInfo(playerID, playerInfo)
	return newName

def getPlayerInfo(playerID):
	#This function return's a player's info dictionary.
	return getGameInfo()['playerInfo'][str(playerID)]

def getGameStatus():
	#This function returns the gamestate dictionary.
	return getGameInfo()['gameState']

def getDevDeck():
	#This function returns the development card deck dictionary.
	return getGameInfo()['dev']

def getTradeStatus():
	#This function returns the current trade status dictionary.
	return getGameInfo()['trade']

def writePlayerInfo(playerID, playerInfo):
	#This function writes a specific player's information back to the game info file.
	allPlayerInfo = getGameInfo()['playerInfo']
	allPlayerInfo[str(playerID)] = playerInfo
	return writeGameInfo("playerInfo", allPlayerInfo)

def writeGameInfo(key, value):
	#This function checks to see if the game info file is still valid, and if so, writes to it.
	from time import time
	from os import path
	filename="/var/www/gameStatus.json"
	#If the game info file doesn't exist, create it.
	if not path.isfile(filename):
		gameStatus = createGameInfo(filename)
	else:
		gameStatus = readJson(filename)
		#If the game info file is more than 10 hours old, replace it.
		if float(gameStatus['gameTime']) + 36000 < time():
			gameStatus = createGameInfo(filename)
	#Only write to the file if the game has not ended.
	if gameStatus['gameState']['gameEnd'] == -1:
		gameStatus[key] = value
		gameStatus = writeJson(filename, gameStatus)
	return gameStatus

def getGameInfo():
	#This function checks to see if the game info file is still valid, and if so, reads from it.
	from time import time
	from os import path
	filename="/var/www/gameStatus.json"
	#If the game info file doesn't exist, create it.
	if not path.isfile(filename):
		gameStatus = createGameInfo(filename)
	else:
		gameStatus = readJson(filename)
		#If the game info file is more than 10 hours old, replace it.
		if float(gameStatus['gameTime']) + 36000 < time():
			gameStatus = createGameInfo(filename)
	return gameStatus

def createGameInfo(filename):	
	#This function will create a new game info file.
	from time import time
	#Careful when editing this - it's a mess, but contains everything possible for the game.
	gameStatus = {'gameTime':time(), 'trade':{'from':-1, 'to':-1, 'give':{'ore':0, 'wheat':0, 'clay':0, 'sheep':0, 'wood':0}, 'get':{'ore':0, 'wheat':0, 'clay':0, 'sheep':0, 'wood':0}}, 'dev':{'knight':14, 'monopoly':2, 'road':2, 'plenty':2, 'victory':5}, 'gameState':{'gameStart':0, 'gameEnd':-1, 'ready':{'0':0, '1':0, '2':0, '3':0}, 'numPlayers':0, 'diceRolled':0, 'setupComplete':0, 'firstPlayer':-1, 'reverse':0, 'longestRoad':-1, 'largestArmy':-1, 'currentPlayer':-1, 'devCardPlayed':0, 'runningPurchase':0, 'buildingRoads':-1, 'playingKnight':0}, 'playerInfo':{'0':{'playerName': "Player 1", 'resources':{'ore':0, 'wheat':0, 'sheep':0, 'clay':0, 'wood':0}, 'cards':{'victory':0, 'monopoly':0, 'road':0, 'knight':0, 'plenty':0}, 'onHold':{'victory':0, 'monopoly':0, 'road':0, 'knight':0, 'plenty':0}, 'playedKnights':0, 'points':0, 'flag':"0", 'initialPlacements':{'settlement':0, 'road':0}, 'portsOwned':{'5':'4 to 1'}, 'quickConfirm':0},'1':{'playerName': "Player 2", 'resources':{'ore':0, 'wheat':0, 'sheep':0, 'clay':0, 'wood':0}, 'cards':{'victory':0, 'monopoly':0, 'road':0, 'knight':0, 'plenty':0}, 'onHold':{'victory':0, 'monopoly':0, 'road':0, 'knight':0, 'plenty':0}, 'playedKnights':0, 'points':0, 'flag':"0", 'initialPlacements':{'settlement':0, 'road':0}, 'portsOwned':{'5':'4 to 1'}, 'quickConfirm':0},'2':{'playerName': "Player 3", 'resources':{'ore':0, 'wheat':0, 'sheep':0, 'clay':0, 'wood':0}, 'cards':{'victory':0, 'monopoly':0, 'road':0, 'knight':0, 'plenty':0}, 'onHold':{'victory':0, 'monopoly':0, 'road':0, 'knight':0, 'plenty':0}, 'playedKnights':0, 'points':0, 'flag':"0", 'initialPlacements':{'settlement':0, 'road':0}, 'portsOwned':{'5':'4 to 1'}, 'quickConfirm':0},'3':{'playerName': "Player 4", 'resources':{'ore':0, 'wheat':0, 'sheep':0, 'clay':0, 'wood':0}, 'cards':{'victory':0, 'monopoly':0, 'road':0, 'knight':0, 'plenty':0}, 'onHold':{'victory':0, 'monopoly':0, 'road':0, 'knight':0, 'plenty':0}, 'playedKnights':0, 'points':0, 'flag':"0", 'initialPlacements':{'settlement':0, 'road':0}, 'portsOwned':{'5':'4 to 1'}, 'quickConfirm':0}}}
	gameStatus = writeJson(filename, gameStatus)
	return gameStatus

def addPlayer():
	#This function runs during the "Join game" state. Each player that joins will call this function,
	#which will add them as a player and return their player ID to be stored as a cookie.
	#It also returns the number of players, so we know if we can start the game or not.
	gameStatus = getGameStatus()
	gameStatus['numPlayers'] += 1
	playerID = gameStatus['numPlayers'] - 1
	gameStatus['ready'][str(playerID)] = 1
	writeGameInfo("gameState", gameStatus)
	return playerID, gameStatus['numPlayers']

def removePlayer(playerID):
	#This function runs during the "Join game" state. It's the antithesis of the above function, removing
	#a player if they decide they are not ready.
	gameStatus = getGameStatus()
	gameStatus['numPlayers'] -= 1
	gameStatus['ready'][str(playerID)] = 0
	writeGameInfo("gameState", gameStatus)
	return gameStatus['numPlayers']

def startGame():
	#After everyone has joined, this function starts the game by choosing a random first player and
	#notifying the microcontroller.
	from random import randint
	gameState = getGameStatus()
	gameState['gameStart'] = 1
	gameState['firstPlayer'] = randint(0, int(gameState['numPlayers'])-1)
	gameState['currentPlayer'] = gameState['firstPlayer']
	playerInfo = getPlayerInfo(gameState['firstPlayer'])
	playerInfo['flag'] = "1"
	writePlayerInfo(gameState['firstPlayer'], playerInfo)
	writeGameInfo("gameState", gameState)
	for i in range(0, gameState['numPlayers']):
		if i != gameState['firstPlayer']:
			playerInfo = getPlayerInfo(i)
			playerInfo['flag'] = "0"
			writePlayerInfo(i, playerInfo)
	writei2c('playerCount', int(gameState['numPlayers']))
	writei2c('currentPlayer', int(gameState['currentPlayer']+1))
	writei2c('pi','newGame')

def rollDice(playerID):
	#This function rolls the dice and assigns resources for all players.
	#It also takes care of 7 rolls, which are handled differently.
	diceRoll = readi2c('dice')
	writei2c('pi', 'diceRolled')
	gameState = getGameStatus()
	gameState['diceRolled'] = diceRoll
	if diceRoll != 7:
		for i in range(0, gameState['numPlayers']):
			getResources(i)
			playerInfo = getPlayerInfo(i)
			playerInfo['flag'] = "11"
			writePlayerInfo(i, playerInfo)
		writei2c('pi', 'readResources')
	else:
		doASevenRoll(int(playerID))
		writei2c('pi', 'knightDevCard')
	writeGameInfo("gameState", gameState)
	return diceRoll

def doASevenRoll(playerID):
	#Does a barrel roll! Also sets flag to discard half your resources where necessary.
	numPlayers = getGameStatus()['numPlayers']
	for i in range(0, numPlayers):
		playerInfo = getPlayerInfo(i)
		if i == playerID:
			playerInfo['flag'] = "8"
		if sum(playerInfo['resources'].values()) > 7:
			playerInfo['flag'] = "10"
		elif i != playerID:
			playerInfo['flag'] = "11"
		writePlayerInfo(i, playerInfo)

def discardResources(playerID, resourceDict):
	playerInfo = getPlayerInfo(playerID)
	from math import floor
	resourceDict = dict((key, int(val)) for key, val in resourceDict.items() if int(val) != 0)
	for item in resourceDict:
		resourceDict[item] = int(resourceDict[item])
	if sum(resourceDict.values()) != floor(sum(playerInfo['resources'].values())/2):
		return False
	for resource in resourceDict:
		if playerInfo['resources'][resource] <= 0:
			return False
	for resource in resourceDict:
		playerInfo['resources'][resource] -= resourceDict[resource]
	if int(playerID) != int(getGameStatus()['currentPlayer']):
		playerInfo['flag'] = "0"
	else:
		playerInfo['flag'] = "8"
	writePlayerInfo(playerID, playerInfo)

def endTurn(playerID):
	#This function ends the player's turn. It also cycles the turn on initial setup.
	gameState = getGameStatus()
	if gameState['currentPlayer'] == playerID:
		playerInfo = getPlayerInfo(playerID)
		#Move any development cards they've drawn this turn to their playable cards,
		#and reset their unplayable cards.
		for resource in playerInfo['cards']:
			playerInfo['cards'][resource] += playerInfo['onHold'][resource]
			playerInfo['onHold'][resource] = 0
		#Reset game state variables
		gameState['devCardPlayed'] = 0
		gameState['diceRolled'] = 0
		#Set the next player id
		if gameState['currentPlayer'] + 1 == gameState['numPlayers']:
			nextPlayerId = 0
		else:
			nextPlayerId = gameState['currentPlayer'] + 1
		if gameState['setupComplete'] == 0:
			#If we're in initial setup, set the next player and reverse the order once everyone
			#has placed their first settlement and road.
			if gameState['reverse'] == 0 and nextPlayerId == gameState['firstPlayer']:
				nextPlayerId = gameState['currentPlayer']
				gameState['reverse'] = 1
			elif gameState['reverse'] == 1 and gameState['currentPlayer'] == gameState['firstPlayer']:
				nextPlayerId = gameState['currentPlayer']
				gameState['setupComplete'] = 1
				getResources(playerID)
				writei2c('pi', 'readResources')
				#Need to retreive player info again, it's been updated.
				playerInfo  = getPlayerInfo(playerID)
			elif gameState['reverse'] == 1:
				if gameState['currentPlayer'] == 0:
					nextPlayerId = gameState['numPlayers'] - 1
				else:
					nextPlayerId = gameState['currentPlayer'] - 1
				getResources(playerID)
				writei2c('pi', 'readResources')
				#Need to retreive player info again, it's been updated.
				playerInfo  = getPlayerInfo(playerID)
		gameState['currentPlayer'] = nextPlayerId
		newPlayerInfo = getPlayerInfo(nextPlayerId)
		#New turn flag.
		newPlayerInfo['flag'] = "1"
		#End turn flag.
		playerInfo['flag'] = "6"
		writeGameInfo("gameState", gameState)
		#Update current player on micro, notify that we've ended turn
		writei2c('currentPlayer', nextPlayerId+1)
		writei2c('pi', 'endTurn')
		writePlayerInfo(playerID, playerInfo)
		writePlayerInfo(nextPlayerId, newPlayerInfo)

def generateReadyLinks(joined, numPlayers):
#This function generates the ready links during game startup.
	if joined == False:
		return "<a href=\"javascript:setReady();\" class=\"readyLink\">I'm ready!</a>"
	else:
		if numPlayers <= 2:
			return "<span class=\"waitLink\">Waiting...</span><a href=\"javascript:unsetReady();\" class=\"notReadyLink\">I'm not ready!</a>"
		else:
			return "<a href=\"javascript:startGame();\" class=\"halfReadyLink\">Start game!</a><a href=\"javascript:unsetReady();\" class=\"notReadyLink\">I'm not ready!</a>"
def chkResources(playerID, resourceDict):
#This function checks if the given player has the resources (both type and number) given in resourceDict.
	playerInfo = getPlayerInfo(playerID)
	for resource in resourceDict:
		if playerInfo['resources'][resource] < resourceDict[resource]:
			return False
	return True

def trade(playerID, tradeInfo, option):
#This function deals with trading. option determines if it's submitting a request, accepting a request,
#or denying a request. PlayerID could be the trader or the tradee, and tradeInfo is the dictionary of
#trade information.
	if option == "submit":
		if int(tradeInfo['to']) < 4:
			#If we're submitting a new trade, write the new tradeInfo dictionary.
			#This fun line removes all entries with 0 resources and turns all the numbers into ints.
			tradeInfo['give'] = dict((key, int(val)) for key, val in tradeInfo['give'].items() if int(val) != 0)
			tradeInfo['get'] = dict((key, int(val)) for key, val in tradeInfo['get'].items() if int(val) != 0)
			tradeInfo['from'] = playerID
			tradeInfo['to'] = int(tradeInfo['to'])
			#If the player doesn't have the resources available or gives nothing or gets nothing,
			#then stop the trade.
			if(chkResources(playerID, tradeInfo['give']) == False) or (len(tradeInfo['give']) == 0) or (len(tradeInfo['get']) == 0):
				playerInfo = getPlayerInfo(playerID)
				playerInfo['flag'] = 2
				writePlayerInfo(playerID, playerInfo)
			else:
				tradePlayerInfo = getPlayerInfo(tradeInfo['to'])
				tradePlayerInfo['flag'] = 3
				writePlayerInfo(tradeInfo['to'], tradePlayerInfo)
			writeGameInfo("trade", tradeInfo)
		else:
			#Now we're doing meritime trading. So...
			tradeInfo['get'] = dict((key, int(val)) for key, val in tradeInfo['get'].items() if int(val) != 0)
			tradeInfo['give'] = dict((key, int(val)) for key, val in tradeInfo['give'].items() if int(val) != 0)
			playerInfo = getPlayerInfo(playerID)
			tradeInfo['accepted'] = 0
			if(chkResources(playerID, tradeInfo['give']) == False) or len(tradeInfo['get']) != 1 or len(tradeInfo['give']) != 1:
				playerInfo['flag'] = 2
			else:
				playerInfo['flag'] = 4
				if(int(tradeInfo['to']) == 5):
					resource = list(tradeInfo['give'])[0]
					if tradeInfo['give'][resource] == 4:
						playerInfo['resources'][resource] -= tradeInfo['give'][resource]
						playerInfo['resources'][list(tradeInfo['get'])[0]] += list(tradeInfo['get'].values())[0]
						tradeInfo['accepted'] = 1
				elif int(tradeInfo['to']) == 6 and 'ore' in tradeInfo['give'] and tradeInfo['give']['ore'] == 2:
						playerInfo['resources']['ore'] -= tradeInfo['give']['ore']
						playerInfo['resources'][list(tradeInfo['get'])[0]] += list(tradeInfo['get'].values())[0]
						tradeInfo['accepted'] = 1
				elif int(tradeInfo['to']) == 7 and 'wheat' in tradeInfo['give'] and tradeInfo['give']['wheat'] == 2:
						playerInfo['resources']['wheat'] -= tradeInfo['give']['wheat']
						playerInfo['resources'][list(tradeInfo['get'])[0]] += list(tradeInfo['get'].values())[0]
						tradeInfo['accepted'] = 1
				elif int(tradeInfo['to']) == 8 and 'sheep' in tradeInfo['give'] and tradeInfo['give']['sheep'] == 2:
						playerInfo['resources']['sheep'] -= tradeInfo['give']['sheep']
						playerInfo['resources'][list(tradeInfo['get'])[0]] += list(tradeInfo['get'].values())[0]
						tradeInfo['accepted'] = 1
				elif int(tradeInfo['to']) == 9 and 'clay' in tradeInfo['give'] and tradeInfo['give']['clay'] == 2:
						playerInfo['resources']['clay'] -= tradeInfo['give']['clay']
						playerInfo['resources'][list(tradeInfo['get'])[0]] += list(tradeInfo['get'].values())[0]
						tradeInfo['accepted'] = 1
				elif int(tradeInfo['to']) == 10 and 'wood' in tradeInfo['give'] and tradeInfo['give']['wood'] == 2:
						playerInfo['resources']['wood'] -= tradeInfo['give']['wood']
						playerInfo['resources'][list(tradeInfo['get'])[0]] += list(tradeInfo['get'].values())[0]
						tradeInfo['accepted'] = 1
				elif(int(tradeInfo['to']) == 11):
					resource = list(tradeInfo['give'])[0]
					if tradeInfo['give'][resource] == 3:
						playerInfo['resources'][resource] -= tradeInfo['give'][resource]
						playerInfo['resources'][list(tradeInfo['get'])[0]] += list(tradeInfo['get'].values())[0]
						tradeInfo['accepted'] = 1
			writeGameInfo("trade", tradeInfo)
			writePlayerInfo(playerID, playerInfo)
	elif option == "accept":
		#If we're accepting, then swap resources and complete the trade.
		tradeInfo = getTradeStatus()
		tradePlayerInfo = getPlayerInfo(tradeInfo['from'])
		tradePlayerInfo['flag'] = 4
		playerInfo = getPlayerInfo(playerID)
		playerInfo['flag'] = 0
		for resource in tradeInfo['get']:
			tradePlayerInfo['resources'][resource] += tradeInfo['get'][resource]
			playerInfo['resources'][resource] -= tradeInfo['get'][resource]
		for resource in tradeInfo['give']:
			tradePlayerInfo['resources'][resource] -= tradeInfo['give'][resource]
			playerInfo['resources'][resource] += tradeInfo['give'][resource]
		writePlayerInfo(playerID, playerInfo)
		writePlayerInfo(tradeInfo['from'], tradePlayerInfo)
		tradeInfo['accepted'] = 1
		writeGameInfo("trade", tradeInfo)
	elif option == "deny":
		#If we're denying, then notify the player.
		tradeInfo = getTradeStatus()
		tradePlayerInfo = getPlayerInfo(tradeInfo['from'])
		tradePlayerInfo['flag'] = 4
		writePlayerInfo(tradeInfo['from'], tradePlayerInfo)
		tradeInfo = getTradeStatus()
		tradeInfo['accepted'] = 0
		writeGameInfo("trade", tradeInfo)
		playerInfo = getPlayerInfo(playerID)
		playerInfo['flag'] = 0
		writePlayerInfo(playerID, playerInfo)

def checkLongestRoad():
	#This function gets the owner of the longest road from the microcontroller and
	#sets points and the like approrpiately.
	longestRoadPlayer = readi2c('longestRoad') - 1
	gameState = getGameStatus()
	if gameState['longestRoad'] != longestRoadPlayer:
		if gameState['longestRoad'] != -1:
			playerInfo = getPlayerInfo(gameState['longestRoad'])
			playerInfo['points'] -= 2
			writePlayerInfo(gameState['longestRoad'], playerInfo)
		gameState['longestRoad'] = longestRoadPlayer
		if longestRoadPlayer != -1:
			playerInfo = getPlayerInfo(longestRoadPlayer)
			playerInfo['points'] += 2
			writePlayerInfo(longestRoadPlayer, playerInfo)
		writeGameInfo("gameState", gameState)

def checkLargestArmy():
	#This function checks for largest army and sets player info appropriately.
	gameState = getGameStatus()
	largestArmyPlayer = gameState['largestArmy']
	if largestArmyPlayer != -1:
		largestArmyInfo = getPlayerInfo(largestArmyPlayer)
		largestArmy = largestArmyInfo['playedKnights']
	else:
		largestArmy = 5
	for player in range(0, gameState['numPlayers']):
		playerInfo = getPlayerInfo(player)
		if playerInfo['playedKnights'] > largestArmy:
			if largestArmyPlayer != -1:
				largestArmyInfo['points'] -= 2
				writePlayerInfo(largestArmyPlayer, largestArmyInfo)
			playerInfo['points'] += 2
			gameState['largestArmy'] = player
			writePlayerInfo(player, playerInfo)
			writeGameInfo("gameState", gameState)
				
		
def getCosts(purchase):
	#This function returns a value from the following map, for displaying a string in the purchase dialog.
	costs = {'development card':'1 wheat, 1 sheep, and 1 ore', 'road':'1 wood and 1 clay', 'city':'2 wheat and 3 ore', 'settlement':'1 wood, 1 wheat, 1 sheep, and 1 clay'}
	return {purchase:costs[purchase]}

def payForPurchase(playerID, resourceDict):
	#This function pays for a purchase by removing the resources given in the resource dictionary.
	playerInfo = getPlayerInfo(playerID)
	for resource in resourceDict:
		playerInfo['resources'][resource] -= resourceDict[resource]
	writePlayerInfo(playerID, playerInfo)

def performPurchase(playerID, purchase):
	#This function performs a purchase for the given player and the give piece.
	playerInfo = getPlayerInfo(playerID)
	#First we read i2c to see if we need to tell the player to place a peice after this or not.
	#This basically determines if the player placed a piece to purchase or purchased and is now
	#placing a piece.
	todo, pieceType = readi2c('pieceType')
	if todo == 'confirm':
		placePiece = False
	else:
		placePiece = True
	if purchase == 'settlement':
		if chkResources(playerID, {'wood':1, 'clay':1, 'sheep':1, 'wheat':1}) == True:
			playerInfo['points'] += 1
			writePlayerInfo(playerID, playerInfo)
			payForPurchase(playerID, {'wood':1, 'clay':1, 'sheep':1, 'wheat':1})
			if placePiece == False:
				getPorts(playerID)
				writei2c('pi', 'confirm')
			return True, placePiece
		else:
			if placePiece == False:
				writei2c('pi', 'reject')
			return False, placePiece
	elif purchase == 'city':
		if chkResources(playerID, {'wheat':2, 'ore':3}) == True:
			playerInfo['points'] += 1
			writePlayerInfo(playerID, playerInfo)
			payForPurchase(playerID, {'wheat':2, 'ore':3})
			if placePiece == False:
				writei2c('pi', 'confirm')
			return True, placePiece
		else:
			if placePiece == False:
				writei2c('pi', 'reject')
			return False, placePiece
	elif purchase == 'road':
		if chkResources(playerID, {'wood':1, 'clay':1}) == True:
			payForPurchase(playerID, {'wood':1, 'clay':1})
			if placePiece == False:
				writei2c('pi', 'confirm')
			checkLongestRoad()
			return True, placePiece
		else:
			if placePiece == False:
				writei2c('pi', 'reject')
			return False, placePiece
	elif purchase == 'development card':
		if chkResources(playerID, {'wheat':1, 'sheep':1, 'ore':1}) == True:
			devCards = getDevDeck()
			if sum(devCards.values()) == 0:
				return 'none', False
			else:
				#Here we need to get a random card from the cards available.
				weights = []
				cardList = []
				for key, val in devCards.items():
					weights.append(val)
					cardList.append(key)
				randNum = weighted_choice_sub(weights)
				playerInfo['onHold'][cardList[randNum]] += 1
				writePlayerInfo(playerID, playerInfo)
				payForPurchase(playerID, {'wheat':1, 'sheep':1, 'ore':1})
				devCards[cardList[randNum]] -= 1
				writeGameInfo("dev", devCards)
				return cardList[randNum], False
		else:
			return False, False
	else:
		return False, False

def yearOfPlenty(playerID, resources):
	#This function gives the given player the resources of their choice.
	playerInfo = getPlayerInfo(playerID)
	for item in resources:
		playerInfo['resources'][resources[item]] += 1
	writePlayerInfo(playerID, playerInfo)
	gameStatus = getGameStatus()
	writeGameInfo("gameState", gameStatus)
	return True

def monopoly(playerID, resource):
	#This function takes all of a given resource from all other players and gives them to the given player.
	playerInfo = getPlayerInfo(playerID)
	allPlayers = getGameInfo()["playerInfo"]
	numReceived = 0
	for player in allPlayers:
		if int(player) != int(playerID):
			playerInfo['resources'][resource] += allPlayers[player]['resources'][resource]
			numReceived += allPlayers[player]['resources'][resource]
			allPlayers[player]['resources'][resource] = 0
	writeGameInfo("playerInfo", allPlayers)
	writePlayerInfo(playerID, playerInfo)
	gameStatus = getGameStatus()
	writeGameInfo("gameState", gameStatus)
	return({resource:numReceived})

def knight(playerID, playerSteal):
	#This function steals a random resource from the given playerSteal 
	#player and gives it to the given player.
	playerInfo = getPlayerInfo(playerID)
	playerStealInfo = getPlayerInfo(playerSteal)
	if int(playerStealInfo['flag']) == 10:
		playerInfo['flag'] = "12"
		return {'wait':'0'}
	playerInfo['flag'] = "8"
	from random import randint
	availableResources = dict((key, int(val)) for key, val in playerStealInfo['resources'].items() if int(val) != 0)
	if len(availableResources) > 0:
		stolenResource = list(availableResources)[randint(0, len(availableResources)-1)]
		playerInfo['resources'][stolenResource] += 1
		playerStealInfo['resources'][stolenResource] -= 1
		writePlayerInfo(playerID, playerInfo)
		writePlayerInfo(playerSteal, playerStealInfo)
		return {stolenResource:'1'}
	else:
		writePlayerInfo(playerID, playerInfo)
		return {'none':'0'}

def getStealPlayers(playerID):
	#This function reads the thieved register from the micro and checks to see what players
	#can be stolen from. This is based on bits from the micro, so we have to play with it a bit 
	#and do things generally non-pythonic.
	playerBits = readi2c('thieved')
	thieved = {}
	if playerBits & 0x01 == 0x01:
		if playerID != 0:
			thieved['0'] = getPlayerInfo('0')['playerName']
	if playerBits & 0x02 == 0x02:
		if playerID != 1:
			thieved['1'] = getPlayerInfo('1')['playerName']
	if playerBits & 0x04 == 0x04:
		if playerID != 2:
			thieved['2'] = getPlayerInfo('2')['playerName']
	if playerBits & 0x08 == 0x08:
		if playerID != 3:
			thieved['3'] = getPlayerInfo('3')['playerName']
	return thieved

def roadBuilding(playerID):
	#This function tells the micro we're building roads and sets the number of roads built to 0
	#for the road building card.
	writei2c('pi', 'roadDevCard')
	gameStatus = getGameStatus()
	gameStatus['buildingRoads'] = 0
	writeGameInfo("gameState", gameStatus)

def weighted_choice_sub(weights):
	#This function came from http://eli.thegreenplace.net/2010/01/22/weighted-random-generation-in-python/
	#It's a weighted random number generator that will pick a number based on given weights instead of
	#completely randomly.
	from random import random
	rnd = random() * sum(weights)
	for i, w in enumerate(weights):
		rnd -= w
		if rnd < 0:
			return i

def getPorts(playerID):
	portType = readi2c('port')
	if portType == 255:
		return False
	else:
		playerInfo = getPlayerInfo(playerID)
		if portType == 0:
			playerInfo['portsOwned']['6'] = '2 to 1 Ore'
		elif portType == 1:
			playerInfo['portsOwned']['7'] = '2 to 1 Wheat'
		elif portType == 2:
			playerInfo['portsOwned']['8'] = '2 to 1 Sheep'
		elif portType == 3:
			playerInfo['portsOwned']['9'] = '2 to 1 Clay'
		elif portType == 4:
			playerInfo['portsOwned']['10'] = '2 to 1 Wood'
		elif portType == 5:
			playerInfo['portsOwned']['11'] = '3 to 1'
		writePlayerInfo(playerID, playerInfo)
		return True

def restartGame():
	from sys import path
	from time import sleep
	path.insert(0, '/home/pi/477grp3/rpi')
	sleep(2)
	writei2c('pi', 'newGame')
	sleep(2)
	from catronBootup import startBoard
	startBoard()
	for i in range(0, 4):
		playerInfo = getPlayerInfo(i)
		playerInfo['flag'] = "13"
		writePlayerInfo(i, playerInfo)

def shutdown():
	writei2c('pi', 'shutdown')
	from subprocess import call
	call(["/usr/bin/sudo", "/sbin/halt"])

#########################BOTTLE OUTPUT###################################
#Add the template path if it's not there.
if '/home/pi/477grp3/webapp/layouts/' not in TEMPLATE_PATH:
	TEMPLATE_PATH.insert(0,'/home/pi/477grp3/webapp/layouts/')

#Serve images
@get('/images/<filename>')
def serve_image(filename):
	return static_file(filename, root='/home/pi/477grp3/webapp/images/')

#Serve styles
@get('/styles/style.css')
def serve_stylesheet():
	return static_file("style.css", root='/home/pi/477grp3/webapp/styles/')

#Serve javascript
@get('/js/functions.js')
def serve_javascript():
	return static_file("functions.js", root='/home/pi/477grp3/webapp/js/')

#Serve more styles. ALL THE STYLES!
@get('/styles/<filename>')
def serve_image(filename):
	return static_file(filename, root='/home/pi/477grp3/webapp/styles')

# This request happens every X seconds in case anything needs to be updated in the webapp
@get('/refreshContent')
def handle_ajax():
	rid = request.query.id
	if rid == "resources":
		return displayResources(int(request.get_cookie("playerID")))
	elif rid == "readyState":
		from json import dumps
		from time import time
		gameStatus = getGameStatus()
		numPlayers = gameStatus['numPlayers']
		gameStart = gameStatus['gameStart']
		if request.get_cookie("joinTime") is not None and float(request.get_cookie("joinTime")) + 120 > time():
			joined = True
		else:
			joined = False
		readyLinks = generateReadyLinks(joined, numPlayers)
		return dumps({"readyLink":readyLinks, "players":numPlayers, "gameStart":int(gameStart)})
	elif rid == "clearFlag":
		playerID = request.get_cookie("playerID")
		playerInfo = getPlayerInfo(str(playerID))
		playerInfo['flag'] = "0"
		writePlayerInfo(playerID, playerInfo)
		return "done"
	elif rid == "ModalBox":
		#If we need to update the ModalBox, then we need to see what we need to update in the Modal box.
		mid = request.query.modal
		playerID = request.get_cookie("playerID")
		if playerID is not None:
			playerInfo = getPlayerInfo(playerID)
		if mid == "name":
			return template('nameBox', name=playerInfo['playerName'])
		elif mid == "status":
			gameStatus = getGameStatus()
			return template('statusBox', playerInfo=getGameInfo()['playerInfo'], longestRoad=gameStatus['longestRoad'], largestArmy=gameStatus['largestArmy'], numPlayers=gameStatus['numPlayers'])
		elif mid == "endTurn":
			return template('endTurn')
		elif mid == "trade":
			#Current player wishes to trade
			gameStatus = getGameStatus()
			if gameStatus['diceRolled'] != 0:
				portsOwned = getPlayerInfo(int(request.get_cookie("playerID")))['portsOwned']
				tradePlayers = getGameInfo()['playerInfo']
				tradePlayers.update(dict((key, {"playerName":portsOwned[key]}) for key in portsOwned))
				return template('trade', players=tradePlayers, newTrade=True, numPlayers=gameStatus['numPlayers'], currentPlayer=request.get_cookie('playerID'))
			else:
				return template('trade', needRollDice=True)
		elif mid == "invalidTrade":
			#Current player cannot trade with given values
			writePlayerInfo(playerID, playerInfo)
			return template('trade', invalidTrade=True)
		elif mid == "remoteTrade":
			#Remote player needs to confirm or deny trade
			writePlayerInfo(playerID, playerInfo)
			tradeInfo = getTradeStatus()
			if chkResources(playerID, tradeInfo['get']) == False:
				#if the player doesn't have the resources available that are asked for,
				#Then just tell them this and make them click "Deny".
				return template('trade', cannotTrade=True)
			else:
				#Build the string for giving and getting. The logic here needs improved.
				getString = ""
				giveString = ""
				if len(tradeInfo['get']) == 1:
					for resource in tradeInfo['get']:
						getString = str(tradeInfo['get'][resource]) + " " + resource
				else:
					for resource in tradeInfo['get']:
						getString = getString + str(tradeInfo['get'][resource]) + " " + resource + ", "
				if len(tradeInfo['give']) == 1:
					for resource in tradeInfo['give']:
						giveString = str(tradeInfo['give'][resource]) + " " + resource
				else:
					for resource in tradeInfo['give']:
						giveString = giveString + str(tradeInfo['give'][resource]) + " " + resource + ", "
				return template('trade', confirm=True, getStuff=getString, giveStuff=giveString)
		elif mid == "returnTrade":
			#Current player sees remote player's response
			writePlayerInfo(playerID, playerInfo)
			tradeInfo = getTradeStatus()
			if tradeInfo['accepted'] == 1:
				return template('trade', success=True)
			elif tradeInfo['accepted'] == 0:
				return template('trade', denied=True)
			else:
				return template('trade')
		elif mid == "purchase":
			if (getGameStatus()['diceRolled'] == 0):
				diceRolled = False
			else:
				diceRolled = True
			return template('purchase', newPurchase=True, diceRolled=diceRolled)
		elif mid == "devCards":
			playerInfo = getPlayerInfo(playerID)
			output = playerInfo['cards'].copy()
			output['knightsPlayed'] = playerInfo['playedKnights']
			return template('devCards', showCards=True, devCards=output)
		elif mid == "pieceInfo":
			#Confirm piece placement, purchase placed piece, remove invalid piece, replace invalid removed piece
			gameStatus = getGameStatus()
			playerInfo = getPlayerInfo(int(request.get_cookie('playerID')))
			errorType, piece = readi2c('pieceType', playerID)
			if errorType == 'confirm' and gameStatus['setupComplete'] == 1 and gameStatus['buildingRoads'] == -1 and piece != 'thief' and gameStatus['runningPurchase'] == 0:
				if playerInfo['quickConfirm'] == 0:
					if piece != 'city':
						gameState = getGameStatus();
						gameState['runningPurchase'] = 1
						writeGameInfo("gameState", gameState)
					return template('purchase', confirmPurchase=True, purchaseItem=getCosts(piece))
				else:
					#Accept the purchase.
					purchaseResult, placePiece = performPurchase(request.get_cookie("playerID"), piece)
					if purchaseResult == False:
						#If purchaseResult is false, then they didn't have the resources available.
						gameState = getGameStatus();
						if gameState['runningPurchase'] == 1:
							gameState['runningPurchase'] = 0
							writeGameInfo("gameState", gameState)
							return template('purchase', invalidPurchase=True, purchaseItem=getCosts(piece))
					else:
						if gameState['runningPurchase'] == 1:
							if piece != 'development card' and placePiece == True:
								#If they didn't purchase a development card, have them place their piece, if they need to.
								return template('purchase', placePiece=True)
						elif piece == 'city':
							#Cities are weird, because they can be purchased by removing a settlement.
							return template('purchase', placePiece=True)
						else:
							return
			else:
				if (errorType == 'confirm' and playerInfo['quickConfirm'] == 0) or gameStatus['setupComplete'] == 0 or errorType != 'confirm' or piece == 'thief':
					return template('pieceStuff', errorType=errorType, piece=piece)
				elif (errorType == 'confirm' and playerInfo['quickConfirm'] == 1):
					getPorts(playerID)
					writei2c('pi', 'confirm')
					return "close"
		elif mid == "initSetup":
			#"Please place your initial __________ now"
			initPlace = getPlayerInfo(playerID)['initialPlacements']
			if(initPlace['settlement'] == initPlace['road'] and initPlace['settlement'] < 2):
				return template('initSetup', piece='settlement')
			elif(initPlace['settlement'] > initPlace['road'] and initPlace['road'] < 2):
				return template('initSetup', piece='road')
			else:
				endTurn(int(playerID))
				return
		elif mid == "buildRoads":
			#If we're currently building roads, show this.
			gameState = getGameStatus()
			if gameState['buildingRoads'] >= 2:
				#If we've built roads, then unset building roads and show complete.
				gameState['buildingRoads'] = -1
				writeGameInfo("gameState", gameState)
				checkLongestRoad()
				return template('devCards', success='road')
			else:
				return template('devCards', playCard='road')
		elif mid == "knight":
			if "player" in request.query:
				resources = knight(int(request.get_cookie("playerID")), int(request.query.player))
				if list(resources.keys())[0] == 'wait':
					playerInfo = getPlayerInfo(int(request.get_cookie("playerID")))
					playerInfo['flag'] = "12"
					writePlayerInfo(int(request.get_cookie("playerID")), playerInfo)
					return template('devCards', resources=resources, wait='knight', stealPlayer=request.query.player)
				gameState = getGameStatus()
				gameState['playingKnight'] = 0
				writeGameInfo("gameState", gameState)
				return template('devCards', resources=resources, success='knight')
			else:
				#Show the "Steal from this player" box for the knight
				playerInfo = getPlayerInfo(int(playerID))
				checkLargestArmy()
				return template('devCards', playCard='knight', steal=getStealPlayers(int(playerID)))
		elif mid == "endGame":
			#Show the "Game is over! Whoo! Congrats player X!" screen.
			gameStatus = getGameStatus()
			if(gameStatus['gameEnd'] != -1):
				return template('gameOver', winner=getPlayerInfo(getGameStatus()['gameEnd'])['playerName'])
			else:
				return template('gameOver', winner=False)
		elif mid == "discardHand":
			#Force the player to discard half of their hand. A 7 was rolled and they have more then 7 resources.
			from math import floor
			numDiscard = floor(sum(getPlayerInfo(int(request.get_cookie("playerID")))['resources'].values())/2)
			return template('sevenRoll', error=False, complete=False, numDiscard=numDiscard)
		elif mid == "rollBox":
			return template('rollBox', numberRolled=str(getGameStatus()['diceRolled']))
		elif mid == "settings":
			if request.get_cookie("playerID") is not None:
				return template('settings', quickConfirm=int(getPlayerInfo(int(request.get_cookie("playerID")))['quickConfirm']))
			else:
				return template('settings', quickConfirm=0)
		
	return "<p>Please wait...(if this does not go away in at most a minute, please try again.)</p>"

#This request happens whenever a form is submitted from the webapp.
@get('/submitForm')
def handle_form():
	fid = request.params.id
	if fid == "name":
		return updatePlayerName(request.get_cookie("playerID"), request.params.value)
	elif fid == "endTurn":
		endTurn(int(request.get_cookie("playerID")))
		return "done"
	elif fid == "trade":
		if request.params.value != "accept" and request.params.value != "deny":
			from json import loads
			trade(request.get_cookie("playerID"), loads(request.params.value), "submit")
			return "done"
		elif request.params.value == "accept":
			trade(request.get_cookie("playerID"), None, "accept")
			return "done"
		elif request.params.value == "deny":
			trade(request.get_cookie("playerID"), None, "deny")
			return "done"
		return "error."
	elif fid == "discard":
		from json import loads
		if discardResources(request.get_cookie("playerID"), loads(request.params.value)) != False:
			return template('sevenRoll', error=False, complete=True, numDiscard=0)
		else:
			from math import floor
			numDiscard = floor(sum(getPlayerInfo(int(request.get_cookie("playerID")))['resources'].values())/2)
			return template('sevenRoll', error=True, complete=False, numDiscard=numDiscard)
	elif fid == "purchase":
		from json import loads
		value = loads(request.params.value)
		if value['action'] == 'get':
			#Selected item to purchase, start the runningPurchase to prevent other things.
			gameState = getGameStatus();
			gameState['runningPurchase'] = 1
			writeGameInfo("gameState", gameState)
			return template('purchase', confirmPurchase=True, purchaseItem=getCosts(value['type']))
		elif value['action'] == 'deny':
			#Cancel the purchase.
			gameState = getGameStatus();
			gameState['runningPurchase'] = 0
			writeGameInfo("gameState", gameState)
		elif value['action'] == 'accept':
			#Accept the purchase.
			purchaseResult, placePiece = performPurchase(request.get_cookie("playerID"), value['type'])
			if purchaseResult == False:
				#If purchaseResult is false, then they didn't have the resources available.
				gameState = getGameStatus();
				if gameState['runningPurchase'] == 1:
					gameState['runningPurchase'] = 0
					writeGameInfo("gameState", gameState)
				return template('purchase', invalidPurchase=True, purchaseItem=getCosts(value['type']))
			else:
				gameState = getGameStatus()
				if value['type'] != 'development card' and placePiece == True:
					#If they didn't purchase a development card, have them place their piece, if they need to.
					playerInfo = getPlayerInfo(int(request.get_cookie("playerID")))
					playerInfo['flag'] = "15"
					writePlayerInfo(int(request.get_cookie("playerID")), playerInfo)
					return template('purchase', placePiece=True)
				elif value['type'] == 'development card':
					if purchaseResult == 'plenty':
						output = 'Year of Plenty'
					elif purchaseResult == 'knight':
						output = 'Knight'
					elif purchaseResult == 'monopoly':
						output = 'Monopoly'
					elif purchaseResult == 'road':
						output = 'Road Building'
					else:
						output = purchaseResult
					return template('purchase', devCard=output)
				elif value['type'] == 'city':
					#Cities are weird, because they can be purchased by removing a settlement.
					return template('purchase', placePiece=True)
				else:
					return
	elif fid == "playDevCard":
		from json import loads
		playerInfo = getPlayerInfo(request.get_cookie("playerID"))
		output = playerInfo['cards'].copy()
		output['knightsPlayed'] = playerInfo['playedKnights']
		gameStatus = getGameStatus()
		value = loads(request.params.value)
		if value['play'] == 'playing':
			#playing indicates the player has decided to play a card so we are mid-play.
			if value['type'] == 'road':
				roadBuilding(int(request.get_cookie("playerID")))
			elif value['type'] == 'knight':
				writei2c('pi', 'knightDevCard')
				playerInfo['playedKnights'] += 1
				gameStatus['playingKnight'] = 1
			gameStatus['devCardPlayed'] = 1
			playerInfo['cards'][value['type']] -= 1
			writePlayerInfo(int(request.get_cookie("playerID")), playerInfo)
			writeGameInfo("gameState", gameStatus)
			return template('devCards', devCards=output, playCard=value['type'])
		else:
			if gameStatus['currentPlayer'] == int(request.get_cookie("playerID")):
				currentTurn = True
			else:
				currentTurn = False
			return template('devCards', devCards=output, playedDevCard=gameStatus['devCardPlayed'], showCard=value['type'], currentTurn=currentTurn)
	elif fid == "yearofplenty":
		#If a year of plenty form was submitted
		from json import loads
		value = loads(request.params.value)
		yearOfPlenty(int(request.get_cookie("playerID")), value['resources'])
		return template('devCards', success='plenty')
	elif fid == "monopoly":
		#If a monopoly form was submitted
		resources = monopoly(request.get_cookie("playerID"), request.params.value)
		return template('devCards', resources=resources, success='monopoly')
	elif fid == "knight":
		#If a knight form was submitted
		resources = knight(int(request.get_cookie("playerID")), int(request.params.value))
		if list(resources.keys())[0] == 'wait':
			playerInfo = getPlayerInfo(int(request.get_cookie("playerID")))
			playerInfo['flag'] = "12"
			writePlayerInfo(int(request.get_cookie("playerID")), playerInfo)
			return template('devCards', resources=resources, wait='knight', stealPlayer=request.params.value)
		gameState = getGameStatus()
		gameState['playingKnight'] = 0
		writeGameInfo("gameState", gameState)
		return template('devCards', resources=resources, success='knight')

@get('/ready')
def handle_players():
	if "start" in request.params:
		startGame()
	else:
		set = request.params.set
		if set == "true":
			#Joining a new player, set the cookies and write stuff as necessary.
			from time import time
			playerID, numPlayers = addPlayer()
			gameTime = getGameInfo()['gameTime']
			response.set_cookie("gameTime", str(gameTime))	#Game start time, like an ID
			#Player join time prevents multiple players from having the same ID and times out if it takes too
			#long to start the game (so they have to re-join)
			response.set_cookie("joinTime", str(time()))		
			response.set_cookie("playerID", str(playerID))	#Player ID
			return str(numPlayers)
		elif set == "false":
			#Unjoining a player, unset cookies and remove as necessary.
			numPlayers = removePlayer(request.get_cookie("playerID"))
			response.set_cookie("gameTime", "-1")
			response.set_cookie("joinTime", "-1")
			response.set_cookie("playerID", "-1")
			return str(numPlayers)

@get('/i2c')
def handle_i2c():
	#Basically handles confirm/deny directly from the web interface.
	todo = request.params.todo
	if todo == "confirm":
		getPorts(int(request.get_cookie("playerID")))
		writei2c('pi', 'confirm')
		#Every time we confirm, check if we're in initial setup and if so auto inc to next player.
		checkIfNextPlayer(int(request.get_cookie("playerID")))
		gameState = getGameStatus();
		playerInfo = getPlayerInfo(int(request.get_cookie("playerID")))
		if playerInfo['flag'] == "15":
			playerInfo['flag'] = "0"
			writePlayerInfo(int(request.get_cookie("playerID")), playerInfo)
			if gameState['runningPurchase'] == 1:
				#If we're confirming a purchase, we've completed it.
				gameState['runningPurchase'] = 0
				writeGameInfo("gameState", gameState)
		if gameState['buildingRoads'] > -1 and gameState['buildingRoads'] < 2:
			#Increment number of roads built if we're buliding roads.
			gameState['buildingRoads'] += 1
			writeGameInfo("gameState", gameState)

@get('/rollDice')
def handle_dice_roll():
	if "seen" in request.params:
		playerInfo = getPlayerInfo(int(request.get_cookie("playerID")))
		playerInfo['flag'] = "0"
		writePlayerInfo(int(request.get_cookie("playerID")), playerInfo)
	else:
		#Handle a dice roll.
		diceNumber = rollDice(int(request.get_cookie("playerID")))

@get('/settings')
def handle_settings():
	todo = request.params.todo
	if todo == "quickConfirm":
		playerInfo = getPlayerInfo(int(request.get_cookie("playerID")))
		if playerInfo['quickConfirm'] == 1:
			playerInfo['quickConfirm'] = 0
		else:
			playerInfo['quickConfirm'] = 1
		writePlayerInfo(int(request.get_cookie("playerID")), playerInfo)
	elif todo == "shutdown":
		if request.get_cookie("playerID") is not None:
			playerInfo = getPlayerInfo(int(request.get_cookie("playerID")))
			if playerInfo['flag'] == "9":
				playerInfo['flag'] = "14"
				writePlayerInfo(int(request.get_cookie("playerID")), playerInfo)
		return template('settings', confirmShutdown=True)
	elif todo == "reallyShutdown":
		shutdown()
		return "<h2>Shutdown</h2><p>Shutting down.</p>"
	elif todo == "endGame":
		return template('settings', endGame=True)
	elif todo == "reallyEndGame":
		endGame(-1)
	elif todo == "restartGame":
		playerInfo = getPlayerInfo(int(request.get_cookie("playerID")))
		if playerInfo['flag'] == "9":
			playerInfo['flag'] = "14"
			writePlayerInfo(int(request.get_cookie("playerID")), playerInfo)
		return template('settings', restartGame=True)
	elif todo == 'reallyRestartGame':
		from time import sleep
		winner = getGameStatus()['gameEnd']
		if int(winner) == -1:
			endGame(-1)
			sleep(2)
		restartGame()
	elif todo == 'cancel':
		playerInfo = getPlayerInfo(int(request.get_cookie("playerID")))
		if playerInfo['flag'] == "14":
			playerInfo['flag'] = "9"
			writePlayerInfo(int(request.get_cookie("playerID")), playerInfo)
		return

# This request handles initial loading of the page.
@get('/')
def show_webapp():
	gameTime = getGameInfo()['gameTime'] #Check the game time (it's sort of our ID)
	gameStatus = getGameStatus()
	if gameStatus['gameStart'] == 0:
		#Display the pregame stuff if the game hasn't started.
		from time import time
		if request.get_cookie("joinTime") is not None and float(request.get_cookie("joinTime")) + 120 > time():
			#Check if their joinTime cookie has expired.
			return template('preGame', joined=True, numPlayers=gameStatus['numPlayers'])
		else:
			#If it has expired, then allow them to re-join if there aren't 4 players already.
			if gameStatus['numPlayers'] >= 4:
				return template('error', maxPlayers=True)
			else:
				return template('preGame', joined=False, numPlayers=gameStatus['numPlayers']) 
	else:
		if request.get_cookie("gameTime") is not None and request.get_cookie("gameTime") == str(gameTime):
			#Normal game stuff, check if there is a gameTime cookie and it matches the current gameTime
			playerID = int(request.get_cookie("playerID"))
			playerInfo = getPlayerInfo(playerID)
			#Uncomment this for turn-based gameplay.
			return template('layout', name=playerInfo['playerName'], points=str(playerInfo['points'] + playerInfo['cards']['victory'] + playerInfo['onHold']['victory']), devCards=str(sum(playerInfo['cards'].values())), resources=dict((key, str(val)) for key, val in playerInfo['resources'].items()), currentTurn=True if playerID == gameStatus['currentPlayer'] else False, diceRolled=False if gameStatus['diceRolled'] == 0 else True)
			#Uncomment this for debug mode - it's everybody's turn always!
			#return template('layout', name=playerInfo['playerName'], points=str(playerInfo['points'] + playerInfo['cards']['victory'] + playerInfo['onHold']['victory']), devCards=str(sum(playerInfo['cards'].values())), resources=dict((key, str(val)) for key, val in playerInfo['resources'].items()), currentTurn=True, diceRolled=False is gameStatus['diceRolled'] == 0 else True)
		else:
			#If they don't have the correct gametime cookie, then the game has started and they can't join.
			return template('error', gameStarted=True)

bottle.debug(True)													#Turn on debug mode
bottle.app().catchall = False								#Let errors pass through to the server (apache)
application=bottle.default_app()						#Run in a WSGI server
#bottle.run(host='localhost', port=8080)		#Run in a local test server
