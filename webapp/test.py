import bottle
from bottle import get, post, request, response, static_file, template, TEMPLATE_PATH

##########################USEFUL FUNCTIONS################################
def readJson(jfile):
	from json import load
	jsonInfo = open(jfile)
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
	from json import dump
	with open(jfile, 'w') as f:
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

def writei2c(reg, val, playerID=-1):
	import quick2wire.i2c as i2c
	registers = {'pi':0, 'currentPlayer':1, 'playerCount':2, 'debug1':30, 'debug2':31, 'debug3':32, 'debug4':33, 'debug5':34}
	flags = {'turnOn':1, 'newGame':2, 'diceRolled':3, 'endTurn':4, 'roadDevCard':5, 'knightDevCard': 6, 'confirm':7, 'reject':8, 'clearFlag':9, 'purchaseRoad':10, 'purchaseSettlement':11, 'purchaseCity':12, 'endGame':13, 'shutdown':14}
	if reg == 'pi':
		val = flags[val]
	with i2c.I2CMaster() as bus:
		bus.transaction(i2c.writing_bytes(0x50, registers[reg], val))

def checkIfNextPlayer(playerID):
	if getGameStatus()['setupComplete'] == 1:
		return False
	playerInfo = getPlayerInfo(playerID)
	initPlacements = playerInfo['initialPlacements']
	if initPlacements['settlement'] == initPlacements['road'] and initPlacements['settlement'] < 2:
		playerInfo['initialPlacements']['settlement'] += 1
		playerInfo['points'] += 1
		writePlayerInfo(playerID, playerInfo)
	elif initPlacements['settlement'] > initPlacements['road'] and initPlacements['road'] < 2:
		playerInfo['initialPlacements']['road'] += 1
		writePlayerInfo(playerID, playerInfo)
		endTurn(playerID)

def readi2c(reg, playerID=-1):
	import quick2wire.i2c as i2c
	registers = {'micro':3, 'thieved':4, 'pieceType':6, 'port':7, 'longestRoad':8, 'dice':9, 'resources':10}
	flags = {'newPiece':5, 'newThief':4, 'error':6, 'diceReady':9, 'newRoad':8, 'allClear':11}
	readNum = 1
	startReg = registers[reg]
	if reg == 'resources' and playerID >= 0 and playerID <= 3:
		startReg = (playerID * 5) + registers['resources']
		readNum = 5
	with i2c.I2CMaster() as bus:
		microResponse = bus.transaction(i2c.writing_bytes(0x50, startReg), i2c.reading(0x50, readNum))
	if reg == 'resources':
		response = {'ore':microResponse[0][0], 'wheat':microResponse[0][1], 'sheep':microResponse[0][2], 'clay':microResponse[0][3], 'wood':microResponse[0][4]}
		return response
	elif reg == 'pieceType':
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
	resources = readi2c('resources', playerID)
	playerInfo = getPlayerInfo(playerID)
	for resource in resources:
		playerInfo['resources'][resource] += int(resources[resource])
	writePlayerInfo(playerID, playerInfo)

def displayResources(playerID):
	playerInfo = getPlayerInfo(playerID)
	gameStatus = getGameStatus()
	from json import dumps
	output = playerInfo['resources'].copy()
	output['dev'] = sum(playerInfo['cards'].values()) + sum(playerInfo['onHold'].values())
	output['flag'] = playerInfo['flag']
	if(gameStatus['currentPlayer'] == playerID):
		response = readi2c('micro', playerID)
		if (response == 5 or response == 6 or response == 4):
			output['flag'] = "5"
		elif (gameStatus['buildingRoads'] > -1 and gameStatus['buildingRoads'] <= 2):
			output['flag'] = "7"
		elif (gameStatus['playingKnight'] == 1):
			output['flag'] = "8"
	output['points'] = playerInfo['points'] + playerInfo['cards']['victory'] + playerInfo['onHold']['victory']
	if output['points'] >= 10:
		endGame(playerID)
	output['initSetup'] = 0
	if gameStatus['setupComplete'] == 0:
		output['initSetup'] = 1
	output['dice'] = gameStatus['diceRolled']
	return dumps(output)

def endGame(playerID):
	gameState = getGameStatus()
	gameState['gameEnd'] == playerID
	for i in range(0, gameState['numPlayers']):
		playerInfo = getPlayerInfo(i)
		playerInfo['flag'] = "9"
		writePlayerInfo(i, playerInfo)
	writei2c('pi', 'endGame')
	

def updatePlayerName(playerID, newName):
	playerInfo = getPlayerInfo(playerID)
	playerInfo['playerName'] = newName
	writePlayerInfo(playerID, playerInfo)
	return newName

def getPlayerInfo(playerID):
	return getGameInfo()['playerInfo'][str(playerID)]

def getGameStatus():
	return getGameInfo()['gameState']

def getDevDeck():
	return getGameInfo()['dev']

def getTradeStatus():
	return getGameInfo()['trade']

def writePlayerInfo(playerID, playerInfo):
	allPlayerInfo = getGameInfo()['playerInfo']
	allPlayerInfo[str(playerID)] = playerInfo
	return writeGameInfo("playerInfo", allPlayerInfo)

def writeGameInfo(key, value):
	from time import time
	from os import path
	filename="/var/www/gameStatus.json"
	if not path.isfile(filename):
		gameStatus = createGameInfo(filename)
	else:
		gameStatus = readJson(filename)
		if float(gameStatus['gameTime']) + 36000 < time():
			gameStatus = createGameInfo(filename)
	gameStatus[key] = value
	if gameStatus['gameState']['gameEnd'] == -1:
		gameStatus = writeJson(filename, gameStatus)
	return gameStatus

def getGameInfo():
	from time import time
	from os import path
	filename="/var/www/gameStatus.json"
	if not path.isfile(filename):
		gameStatus = createGameInfo(filename)
	else:
		gameStatus = readJson(filename)
		if float(gameStatus['gameTime']) + 36000 < time():
			gameStatus = createGameInfo(filename)
	return gameStatus

def createGameInfo(filename):	
	from time import time
	#Careful when editing this - it's a mess, but contains everything possible for the game.
	gameStatus = {'gameTime':time(), 'trade':{'from':-1, 'to':-1, 'give':{'ore':0, 'wheat':0, 'clay':0, 'sheep':0, 'wood':0}, 'get':{'ore':0, 'wheat':0, 'clay':0, 'sheep':0, 'wood':0}}, 'dev':{'knight':14, 'monopoly':2, 'road':2, 'plenty':2, 'victory':5}, 'gameState':{'gameStart':0, 'gameEnd':-1, 'ready':{'0':0, '1':0, '2':0, '3':0}, 'numPlayers':0, 'diceRolled':0, 'setupComplete':0, 'firstPlayer':-1, 'reverse':0, 'longestRoad':-1, 'largestArmy':-1, 'currentPlayer':-1, 'devCardPlayed':0, 'runningPurchase':0, 'buildingRoads':-1, 'playingKnight':0}, 'playerInfo':{'0':{'playerName': "Player 1", 'resources':{'ore':0, 'wheat':0, 'sheep':0, 'clay':0, 'wood':0}, 'cards':{'victory':0, 'monopoly':0, 'road':0, 'knight':0, 'plenty':0}, 'onHold':{'victory':0, 'monopoly':0, 'road':0, 'knight':0, 'plenty':0}, 'playedKnights':0, 'points':0, 'flag':"0", 'initialPlacements':{'settlement':0, 'road':0}},'1':{'playerName': "Player 2", 'resources':{'ore':0, 'wheat':0, 'sheep':0, 'clay':0, 'wood':0}, 'cards':{'victory':0, 'monopoly':0, 'road':0, 'knight':0, 'plenty':0}, 'onHold':{'victory':0, 'monopoly':0, 'road':0, 'knight':0, 'plenty':0}, 'playedKnights':0, 'points':0, 'flag':"0", 'initialPlacements':{'settlement':0, 'road':0}},'2':{'playerName': "Player 3", 'resources':{'ore':0, 'wheat':0, 'sheep':0, 'clay':0, 'wood':0}, 'cards':{'victory':0, 'monopoly':0, 'road':0, 'knight':0, 'plenty':0}, 'onHold':{'victory':0, 'monopoly':0, 'road':0, 'knight':0, 'plenty':0}, 'playedKnights':0, 'points':0, 'flag':"0", 'initialPlacements':{'settlement':0, 'road':0}},'3':{'playerName': "Player 4", 'resources':{'ore':0, 'wheat':0, 'sheep':0, 'clay':0, 'wood':0}, 'cards':{'victory':0, 'monopoly':0, 'road':0, 'knight':0, 'plenty':0}, 'onHold':{'victory':0, 'monopoly':0, 'road':0, 'knight':0, 'plenty':0}, 'playedKnights':0, 'points':0, 'flag':"0", 'initialPlacements':{'settlement':0, 'road':0}}}}
	gameStatus = writeJson(filename, gameStatus)
	return gameStatus

def addPlayer():
	gameStatus = getGameStatus()
	gameStatus['numPlayers'] += 1
	playerID = gameStatus['numPlayers'] - 1
	gameStatus['ready'][str(playerID)] = 1
	writeGameInfo("gameState", gameStatus)
	return playerID, gameStatus['numPlayers']

def removePlayer(playerID):
	gameStatus = getGameStatus()
	gameStatus['numPlayers'] -= 1
	gameStatus['ready'][str(playerID)] = 0
	writeGameInfo("gameState", gameStatus)
	return gameStatus['numPlayers']

def startGame():
	from random import randint
	gameState = getGameStatus()
	gameState['gameStart'] = 1
	gameState['firstPlayer'] = randint(0, int(gameState['numPlayers'])-1)
	gameState['currentPlayer'] = gameState['firstPlayer']
	playerInfo = getPlayerInfo(gameState['firstPlayer'])
	playerInfo['flag'] = "1"
	writePlayerInfo(gameState['firstPlayer'], playerInfo)
	writeGameInfo("gameState", gameState)
	writei2c('playerCount', int(gameState['numPlayers']))
	writei2c('currentPlayer', int(gameState['currentPlayer']+1))
	writei2c('pi','newGame')

def rollDice(playerID):
	diceRoll = readi2c('dice')
	writei2c('pi', 'diceRolled')
	gameState = getGameStatus()
	gameState['diceRolled'] = diceRoll
	if diceRoll != 7:
		for i in range(0, gameState['numPlayers']):
			getResources(i)
	else:
		writei2c('pi', 'knightDevCard')
	writeGameInfo("gameState", gameState)

def endTurn(playerID):
	gameState = getGameStatus()
	playerInfo = getPlayerInfo(playerID)
	for resource in playerInfo['cards']:
		playerInfo['cards'][resource] += playerInfo['onHold'][resource]
		playerInfo['onHold'][resource] = 0
	gameState['devCardPlayed'] = 0
	gameState['diceRolled'] = 0
	if gameState['currentPlayer'] + 1 == gameState['numPlayers']:
		nextPlayerId = 0
	else:
		nextPlayerId = gameState['currentPlayer'] + 1
	if gameState['setupComplete'] == 0:
		if gameState['reverse'] == 0 and nextPlayerId == gameState['firstPlayer']:
			nextPlayerId = gameState['currentPlayer']
			gameState['reverse'] = 1
		elif gameState['reverse'] == 1 and gameState['currentPlayer'] == gameState['firstPlayer']:
			nextPlayerId = gameState['currentPlayer']
			gameState['setupComplete'] = 1
			getResources(playerID)
			#Need to retreive player info again, it's been updated.
			playerInfo  = getPlayerInfo(playerID)
		elif gameState['reverse'] == 1:
			if gameState['currentPlayer'] == 0:
				nextPlayerId = gameState['numPlayers'] - 1
			else:
				nextPlayerId = gameState['currentPlayer'] - 1
			getResources(playerID)
			#Need to retreive player info again, it's been updated.
			playerInfo  = getPlayerInfo(playerID)
	gameState['currentPlayer'] = nextPlayerId
	newPlayerInfo = getPlayerInfo(nextPlayerId)
	newPlayerInfo['flag'] = "1"
	playerInfo['flag'] = "6"
	writeGameInfo("gameState", gameState)
	writei2c('currentPlayer', nextPlayerId+1)
	writei2c('pi', 'endTurn')
	writePlayerInfo(playerID, playerInfo)
	writePlayerInfo(nextPlayerId, newPlayerInfo)

def generateReadyLinks(joined, numPlayers):
	if joined == False:
		return "<a href=\"javascript:setReady();\" class=\"readyLink\">I'm ready!</a>"
	else:
		if numPlayers <= 2:
			return "<span class=\"waitLink\">Waiting...</span><a href=\"javascript:unsetReady();\" class=\"notReadyLink\">I'm not ready!</a>"
		else:
			return "<a href=\"/?start=true\" class=\"halfReadyLink\">Start game!</a><a href=\"javascript:unsetReady();\" class=\"notReadyLink\">I'm not ready!</a>"

def chkResources(playerID, resourceDict):
	playerInfo = getPlayerInfo(playerID)
	for resource in resourceDict:
		if playerInfo['resources'][resource] < resourceDict[resource]:
			return False
	return True

def trade(playerID, tradeInfo, option):
	if option == "submit":
		tradeInfo['give'] = dict((key, int(val)) for key, val in tradeInfo['give'].items() if int(val) != 0)
		tradeInfo['get'] = dict((key, int(val)) for key, val in tradeInfo['get'].items() if int(val) != 0)
		tradeInfo['from'] = playerID
		tradeInfo['to'] = int(tradeInfo['to'])
		if(chkResources(playerID, tradeInfo['give']) == False) or (len(tradeInfo['give']) == 0) or (len(tradeInfo['get']) == 0):
			playerInfo = getPlayerInfo(playerID)
			playerInfo['flag'] = 2
			writePlayerInfo(playerID, playerInfo)
		else:
			tradePlayerInfo = getPlayerInfo(tradeInfo['to'])
			tradePlayerInfo['flag'] = 3
			writePlayerInfo(tradeInfo['to'], tradePlayerInfo)
		writeGameInfo("trade", tradeInfo)
	elif option == "accept":
		tradeInfo = getTradeStatus()
		tradePlayerInfo = getPlayerInfo(tradeInfo['from'])
		tradePlayerInfo['flag'] = 4
		playerInfo = getPlayerInfo(playerID)
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
		tradeInfo = getTradeStatus()
		tradePlayerInfo = getPlayerInfo(tradeInfo['from'])
		tradePlayerInfo['flag'] = 4
		writePlayerInfo(tradeInfo['from'], tradePlayerInfo)
		tradeInfo = getTradeStatus()
		tradeInfo['accepted'] = 0
		writeGameInfo("trade", tradeInfo)

def checkLongestRoad():
	longestRoadPlayer = readi2c('longestRoad') - 1
	gameState = getGameStatus()
	if gameState['longestRoad'] != longestRoadPlayer:
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
	gameState = getGameStatus()
	largestArmyPlayer = gameState['largestArmy']
	if largestArmyPlayer != -1:
		largestArmyInfo = getPlayerInfo(largestArmyPlayer)
		largestArmy = largestArmyInfo['playedKnights']
	else:
		largestArmy = 0
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
	costs = {'development card':'1 wheat, 1 sheep, and 1 ore', 'road':'1 wood and 1 clay', 'city':'2 wheat and 3 ore', 'settlement':'1 wood, 1 wheat, 1 sheep, and 1 clay'}
	return {purchase:costs[purchase]}

def payForPurchase(playerID, resourceDict):
	playerInfo = getPlayerInfo(playerID)
	for resource in resourceDict:
		playerInfo['resources'][resource] -= resourceDict[resource]
	writePlayerInfo(playerID, playerInfo)

def performPurchase(playerID, purchase):
	playerInfo = getPlayerInfo(playerID)
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
	playerInfo = getPlayerInfo(playerID)
	for item in resources:
		playerInfo['resources'][resources[item]] += 1
	playerInfo['cards']['plenty'] -= 1
	writePlayerInfo(playerID, playerInfo)
	gameStatus = getGameStatus()
	writeGameInfo("gameState", gameStatus)
	return True

def monopoly(playerID, resource):
	playerInfo = getPlayerInfo(playerID)
	allPlayers = getGameInfo()["playerInfo"]
	numReceived = 0
	for player in allPlayers:
		if int(player) != int(playerID):
			playerInfo['resources'][resource] += allPlayers[player]['resources'][resource]
			numReceived += allPlayers[player]['resources'][resource]
			allPlayers[player]['resources'][resource] = 0
	writeGameInfo("playerInfo", allPlayers)
	playerInfo['cards']['monopoly'] -= 1
	writePlayerInfo(playerID, playerInfo)
	gameStatus = getGameStatus()
	writeGameInfo("gameState", gameStatus)
	return({resource:numReceived})

def knight(playerID, playerSteal):
	playerInfo = getPlayerInfo(playerID)
	playerStealInfo = getPlayerInfo(playerSteal)
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
		return {'none':'0'}

def getStealPlayers():
	playerBits = readi2c('thieved')
	thieved = {}
	if playerBits & 0x01 == 0x01:
		thieved.append('0', getPlayerInfo('0')['playerName'])
	if playerBits & 0x02 == 0x02:
		thieved.append('1', getPlayerInfo('0')['playerName'])
	if playerBits & 0x04 == 0x04:
		thieved.append('2', getPlayerInfo('0')['playerName'])
	if playerBits & 0x08 == 0x08:
		thieved.append('3', getPlayerInfo('0')['playerName'])
	return thieved

def roadBuilding(playerID):
	writei2c('pi', 'roadDevCard')
	gameStatus = getGameStatus()
	gameStatus['buildingRoads'] = 0
	writeGameInfo("gameState", gameStatus)

def weighted_choice_sub(weights):
	from random import random
	#http://eli.thegreenplace.net/2010/01/22/weighted-random-generation-in-python/
	rnd = random() * sum(weights)
	for i, w in enumerate(weights):
		rnd -= w
		if rnd < 0:
			return i
#########################BOTTLE OUTPUT###################################
if '/home/pi/477grp3/webapp/layouts/' not in TEMPLATE_PATH:
	TEMPLATE_PATH.insert(0,'/home/pi/477grp3/webapp/layouts/')

@get('/images/<filename>')
def serve_image(filename):
	return static_file(filename, root='/home/pi/477grp3/webapp/images/')

@get('/styles/style.css')
def serve_stylesheet():
	return static_file("style.css", root='/home/pi/477grp3/webapp/styles/')

@get('/js/functions.js')
def serve_javascript():
	return static_file("functions.js", root='/home/pi/477grp3/webapp/js/')

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
	elif rid == "ModalBox":
		mid = request.query.modal
		playerID = request.get_cookie("playerID")
		playerInfo = getPlayerInfo(playerID)
		if mid == "name":
			return template('nameBox', name=playerInfo['playerName'])
		elif mid == "status":
			gameStatus = getGameStatus()
			return template('statusBox', playerInfo=getGameInfo()['playerInfo'], longestRoad=gameStatus['longestRoad'], largestArmy=gameStatus['largestArmy'])
		elif mid == "endTurn":
			return template('endTurn')
		elif mid == "trade":
			gameStatus = getGameStatus()
			return template('trade', players=getGameInfo()['playerInfo'], newTrade=True, numPlayers=gameStatus['numPlayers'])
		elif mid == "invalidTrade":
			playerInfo['flag'] = "0"
			writePlayerInfo(playerID, playerInfo)
			return template('trade', invalidTrade=True)
		elif mid == "remoteTrade":
			playerInfo['flag'] = "0"
			writePlayerInfo(playerID, playerInfo)
			tradeInfo = getTradeStatus()
			if chkResources(playerID, tradeInfo['get']) == False:
				return template('trade', cannotTrade=True)
			else:
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
			playerInfo['flag'] = "0"
			writePlayerInfo(playerID, playerInfo)
			tradeInfo = getTradeStatus()
			if tradeInfo['accepted'] == 1:
				return template('trade', success=True)
			elif tradeInfo['accepted'] == 0:
				return template('trade', denied=True)
			else:
				return template('trade')
		elif mid == "purchase":
			return template('purchase', newPurchase=True)
		elif mid == "devCards":
			playerInfo = getPlayerInfo(playerID)
			output = playerInfo['cards'].copy()
			output['knightsPlayed'] = playerInfo['playedKnights']
			return template('devCards', showCards=True, devCards=output)
		elif mid == "pieceInfo":
			gameStatus = getGameStatus()
			errorType, piece = readi2c('pieceType', playerID)
			if errorType == 'confirm' and gameStatus['setupComplete'] == 1 and gameStatus['runningPurchase'] == 0 and gameStatus['buildingRoads'] == -1 and piece != 'thief':
				if piece != 'city':
					gameState = getGameStatus();
					gameState['runningPurchase'] = 1
					writeGameInfo("gameState", gameState)
				return template('purchase', confirmPurchase=True, purchaseItem=getCosts(piece))
			else:
				return template('pieceStuff', errorType=errorType, piece=piece)
		elif mid == "initSetup":
			initPlace = getPlayerInfo(playerID)['initialPlacements']
			if(initPlace['settlement'] == initPlace['road'] and initPlace['settlement'] < 2):
				return template('initSetup', piece='settlement')
			elif(initPlace['settlement'] > initPlace['road'] and initPlace['road'] < 2):
				return template('initSetup', piece='road')
			else:
				endTurn(int(playerID))
				return
		elif mid == "buildRoads":
			gameState = getGameStatus()
			if gameState['buildingRoads'] >= 2:
				gameState['buildingRoads'] = -1
				writeGameInfo("gameState", gameState)
				checkLongestRoad()
				return template('devCards', success='road')
			else:
				return template('devCards', playCard='road')
		elif mid == "knight":
			playerInfo = getPlayerInfo(int(playerID))
			checkLargestArmy()
			return template('devCards', playCard='knight', steal=getStealPlayers())
		elif mid == "endGame":
			return template('gameOver', winner=getPlayerInfo(getGameStatus()['gameEnd'])['playerName'])
		
	return "<p>Your request was invalid. Please try again.</p>"

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
	elif fid == "purchase":
		from json import loads
		value = loads(request.params.value)
		if value['action'] == 'get':
			gameState = getGameStatus();
			gameState['runningPurchase'] = 1
			writeGameInfo("gameState", gameState)
			return template('purchase', confirmPurchase=True, purchaseItem=getCosts(value['type']))
		elif value['action'] == 'deny':
			gameState = getGameStatus();
			gameState['runningPurchase'] = 0
			writeGameInfo("gameState", gameState)
		elif value['action'] == 'accept':
			purchaseResult, placePiece = performPurchase(request.get_cookie("playerID"), value['type'])
			if purchaseResult == False:
				gameState = getGameStatus();
				if gameState['runningPurchase'] == 1:
					gameState['runningPurchase'] = 0
					writeGameInfo("gameState", gameState)
				return template('purchase', invalidPurchase=True, purchaseItem=getCosts(value['type']))
			else:
				if value['type'] != 'development card' and placePiece == True:
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
					gameState = getGameStatus();
					gameState['runningPurchase'] = 0
					writeGameInfo("gameState", gameState)
					return template('purchase', placePiece=True)
				elif placePiece != True:
					gameState = getGameStatus();
					gameState['runningPurchase'] = 0
					writeGameInfo("gameState", gameState)
					return
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
			return template('devCards', devCards=output, playedDevCard=gameStatus['devCardPlayed'], showCard=value['type'])
	elif fid == "yearofplenty":
		from json import loads
		value = loads(request.params.value)
		yearOfPlenty(int(request.get_cookie("playerID")), value['resources'])
		return template('devCards', success='plenty')
	elif fid == "monopoly":
		resources = monopoly(request.get_cookie("playerID"), request.params.value)
		return template('devCards', resources=resources, success='monopoly')
	elif fid == "knight":
		resources = knight(request.get_cookie("playerID"), request.params.value)
		gameState = getGameStatus()
		gameState['playingKnight'] = 0
		writeGameInfo("gameState", gameState)
		return template('devCards', resources=resources, success='knight')

@get('/ready')
def handle_players():
	set = request.params.set
	if set == "true":
		from time import time
		playerID, numPlayers = addPlayer()
		gameTime = getGameInfo()['gameTime']
		response.set_cookie("gameTime", str(gameTime))
		response.set_cookie("joinTime", str(time()))
		response.set_cookie("playerID", str(playerID))
		return str(numPlayers)
	elif set == "false":
		numPlayers = removePlayer(request.get_cookie("playerID"))
		response.set_cookie("gameTime", "-1")
		response.set_cookie("joinTime", "-1")
		response.set_cookie("playerID", "-1")
		return str(numPlayers)

@get('/i2c')
def handle_i2c():
	todo = request.params.todo
	if todo == "confirm":
		writei2c('pi', 'confirm', int(request.get_cookie("playerID")))
		checkIfNextPlayer(int(request.get_cookie("playerID")))
		gameState = getGameStatus();
		if gameState['runningPurchase'] == 1:
			gameState['runningPurchase'] = 0
			writeGameInfo("gameState", gameState)
		if gameState['buildingRoads'] > -1 and gameState['buildingRoads'] < 2:
			gameState['buildingRoads'] += 1
			writeGameInfo("gameState", gameState)
@get('/rollDice')
def handle_dice_roll():
	rollDice(int(request.get_cookie("playerID")))

# This request handles a 
@get('/')
def show_webapp():
	if "start" in request.params:
		startGame()
	gameTime = getGameInfo()['gameTime']
	gameStatus = getGameStatus()
	if gameStatus['gameStart'] == 0:
		from time import time
		if request.get_cookie("joinTime") is not None and float(request.get_cookie("joinTime")) + 120 > time():
			return template('preGame', joined=True, numPlayers=gameStatus['numPlayers'])
		else:
			if gameStatus['numPlayers'] >= 4:
				return template('error', maxPlayers=True)
			else:
				return template('preGame', joined=False, numPlayers=gameStatus['numPlayers']) 
	else:
		if request.get_cookie("gameTime") is not None and request.get_cookie("gameTime") == str(gameTime):
			playerID = int(request.get_cookie("playerID"))
			playerInfo = getPlayerInfo(playerID)
			#Uncomment this for turn-based gameplay.
			return template('layout', name=playerInfo['playerName'], points=str(playerInfo['points'] + playerInfo['cards']['victory'] + playerInfo['onHold']['victory']), devCards=str(sum(playerInfo['cards'].values())), resources=dict((key, str(val)) for key, val in playerInfo['resources'].items()), currentTurn=True if playerID == gameStatus['currentPlayer'] else False, diceRolled=False if gameStatus['diceRolled'] == 0 else True)
			#Uncomment this for debug mode - it's everybody's turn always!
			#return template('layout', name=playerInfo['playerName'], points=str(playerInfo['points'] + playerInfo['cards']['victory'] + playerInfo['onHold']['victory']), devCards=str(sum(playerInfo['cards'].values())), resources=dict((key, str(val)) for key, val in playerInfo['resources'].items()), currentTurn=True, diceRolled=False is gameStatus['diceRolled'] == 0 else True)
		else:
			return template('error', gameStarted=True)

bottle.debug(True)
bottle.app().catchall = False
application=bottle.default_app()       # run in a WSGI server
#bottle.run(host='localhost', port=8080) # run in a local test server
