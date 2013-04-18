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

def displayResources(playerID):
	playerInfo = getPlayerInfo(playerID)
	from json import dumps
	output = playerInfo['resources'].copy()
	output['dev'] = sum(playerInfo['cards'].values())
	output['flag'] = playerInfo['flag']
	return dumps(output)

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
	gameStatus = writeJson(filename, gameStatus)
	return gameStatus

def getGameInfo():
	from time import time
	from os import path
	filename="/var/www/gameStatus.json"
	#Careful when editing this - it's a mess, but contains everything possible for the game.
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
	gameStatus = {'gameTime':time(), 'trade':{'from':-1, 'to':-1, 'give':{'ore':0, 'wheat':0, 'clay':0, 'sheep':0, 'wood':0}, 'get':{'ore':0, 'wheat':0, 'clay':0, 'sheep':0, 'wood':0}}, 'dev':{'knights':14, 'monopoly':2, 'road':2, 'plenty':2, 'victory':5}, 'gameState':{'gameStart':0, 'gameEnd':0, 'ready':{'0':0, '1':0, '2':0, '3':0}, 'numPlayers':0, 'diceRolled':0, 'setupComplete':0, 'firstPlayer':-1, 'reverse':0, 'longestRoad':-1, 'largestArmy':-1, 'currentPlayer':-1, 'devCardPlayed':0}, 'playerInfo':{'0':{'playerName': "Player 1", 'resources':{'ore':0, 'wheat':0, 'sheep':0, 'clay':0, 'wood':0}, 'cards':{'victory':0, 'monopoly':0, 'road':0, 'knights':0, 'plenty':0}, 'onHold':{'victory':0, 'monopoly':0, 'road':0, 'knights':0, 'plenty':0}, 'playedKnights':0, 'points':0, 'flag':"0", 'initialPlacements':{'settlement':0, 'road':0}},'1':{'playerName': "Player 2", 'resources':{'ore':0, 'wheat':0, 'sheep':0, 'clay':0, 'wood':0}, 'cards':{'victory':0, 'monopoly':0, 'road':0, 'knights':0, 'plenty':0}, 'onHold':{'victory':0, 'monopoly':0, 'road':0, 'knights':0, 'plenty':0}, 'playedKnights':0, 'points':0, 'flag':"0", 'initialPlacements':{'settlement':0, 'road':0}},'2':{'playerName': "Player 3", 'resources':{'ore':0, 'wheat':0, 'sheep':0, 'clay':0, 'wood':0}, 'cards':{'victory':0, 'monopoly':0, 'road':0, 'knights':0, 'plenty':0}, 'onHold':{'victory':0, 'monopoly':0, 'road':0, 'knights':0, 'plenty':0}, 'playedKnights':0, 'points':0, 'flag':"0", 'initialPlacements':{'settlement':0, 'road':0}},'3':{'playerName': "Player 4", 'resources':{'ore':0, 'wheat':0, 'sheep':0, 'clay':0, 'wood':0}, 'cards':{'victory':0, 'monopoly':0, 'road':0, 'knights':0, 'plenty':0}, 'onHold':{'victory':0, 'monopoly':0, 'road':0, 'knights':0, 'plenty':0}, 'playedKnights':0, 'points':0, 'flag':"0", 'initialPlacements':{'settlement':0, 'road':0}}}}
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
	import random
	gameState = getGameStatus()
	gameState['gameStart'] = 1
	gameState['firstPlayer'] = random.randint(0, int(gameState['numPlayers'])-1)
	gameState['currentPlayer'] = gameState['firstPlayer']
	writeGameInfo("gameState", gameState)

def endTurn(playerID):
	gameState = getGameStatus()
	playerInfo = getPlayerInfo(playerID)
	for resource in playerInfo['cards']:
		playerInfo['cards'][resource] += playerInfo['onHold'][resource]
		playerInfo['onHold'][resource] = 0
	gameState['devCardPlayed'] = 0
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
		elif gameState['reverse'] == 1:
			if gameState['currentPlayer'] == 0:
				nextPlayerId = gameState['numPlayers'] - 1
			else:
				nextPlayerId = gameState['currentPlayer'] - 1
			#getResources(playerID)
	gameState['currentPlayer'] = nextPlayerId
	newPlayerInfo = getPlayerInfo(nextPlayerId)
	newPlayerInfo['flag'] = "1"
	playerInfo['flag'] = "0"
	writeGameInfo("gameState", gameState)
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
	for resource in playerInfo['resources']:
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
			tradeInfo = getTradeStatus()
			if chkResources(playerID, tradeInfo['get']) == False:
				return template('trade', cannotTrade=True)
			else:
				getString = ""
				giveString = ""
				if len(tradeInfo['get']) == 1:
					getString = tradeInfo['get'][resource] + " " + resource
				else:
					for resource in tradeInfo['get']:
						getSting = getString + " " + str(tradeInfo['get'][resource]) + " " + resource + ", "
				if len(tradeInfo['give']) == 1:
					giveString = tradeInfo['give'][resource] + " " + resource
				else:
					for resource in tradeInfo['give']:
						giveString = giveString + " " + str(tradeInfo['give'][resource]) + " " + resource + ", "
				return template('trade', confirm=True, getStuff=getString, giveStuff=giveString)
		elif mid == "returnTrade":
			tradeInfo = getTradeStatus()
			if tradeInfo['accepted'] == 1:
				return template('trade', success=True)
			elif tradeInfo['accepted'] == 0:
				return template('trade', denied=True)
			else:
				return template('trade')
		elif mid == "purchase":
			return "purchase"
		elif mid == "devCards":
			return "Dev card stuff!"
		
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
			return template('layout', name=playerInfo['playerName'], points=str(playerInfo['points'] + playerInfo['cards']['victory'] + playerInfo['onHold']['victory']), devCards=str(sum(playerInfo['cards'].values())), resources=dict((key, str(val)) for key, val in playerInfo['resources'].items()), currentTurn=True if playerID == gameStatus['currentPlayer'] else False)
		else:
			return template('error', gameStarted=True)

bottle.debug(True)
bottle.app().catchall = False
application=bottle.default_app()       # run in a WSGI server
#bottle.run(host='localhost', port=8080) # run in a local test server
