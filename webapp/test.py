import bottle
from bottle import get, post, request, response, static_file, template, TEMPLATE_PATH

##########################USEFUL FUNCTIONS################################
def readJson(jfile):
	from json import load
	jsonInfo = open(jfile)
	info = load(jsonInfo)
	jsonInfo.close()
	return info

def writeJson(jfile, info):
	from json import dump
	with open(jfile, 'w') as f:
		dump(info, f, ensure_ascii=False)
		f.close()
	return info

def displayResources(playerID):
	playerInfo = getPlayerInfo(playerID)
	from json import dumps
	playerInfo['resources']['dev'] = sum(playerInfo['cards'].values())
	return dumps(playerInfo['resources'])

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
	gameStatus = {'gameTime':time(), 'trade':{'from':-1, 'to':-1, 'give':{'ore':0, 'wheat':0, 'clay':0, 'sheep':0, 'wood':0}, 'get':{'ore':0, 'wheat':0, 'clay':0, 'sheep':0, 'wood':0}}, 'dev':{'knights':14, 'monopoly':2, 'road':2, 'plenty':2, 'victory':5}, 'gameState':{'gameStart':0, 'ready':{'0':0, '1':0, '2':0, '3':0}, 'numPlayers':0, 'diceRolled':0, 'setupComplete':0, 'firstPlayer':-1, 'reverse':0, 'longestRoad':-1, 'largestArmy':-1, 'currentPlayer':-1, 'devCardPlayed':0}, 'playerInfo':{'0':{'playerName': "Player 1", 'resources':{'ore':0, 'wheat':0, 'sheep':0, 'clay':0, 'wood':0}, 'cards':{'victory':0, 'monopoly':0, 'road':0, 'knights':0, 'plenty':0}, 'onHold':{'victory':0, 'monopoly':0, 'road':0, 'knights':0, 'plenty':0}, 'playedKnights':0, 'points':0, 'flag':0, 'initialPlacements':{'settlement':0, 'road':0}},'1':{'playerName': "Player 2", 'resources':{'ore':0, 'wheat':0, 'sheep':0, 'clay':0, 'wood':0}, 'cards':{'victory':0, 'monopoly':0, 'road':0, 'knights':0, 'plenty':0}, 'onHold':{'victory':0, 'monopoly':0, 'road':0, 'knights':0, 'plenty':0}, 'playedKnights':0, 'points':0, 'flag':0, 'initialPlacements':{'settlement':0, 'road':0}},'2':{'playerName': "Player 3", 'resources':{'ore':0, 'wheat':0, 'sheep':0, 'clay':0, 'wood':0}, 'cards':{'victory':0, 'monopoly':0, 'road':0, 'knights':0, 'plenty':0}, 'onHold':{'victory':0, 'monopoly':0, 'road':0, 'knights':0, 'plenty':0}, 'playedKnights':0, 'points':0, 'flag':0, 'initialPlacements':{'settlement':0, 'road':0}},'3':{'playerName': "Player 4", 'resources':{'ore':0, 'wheat':0, 'sheep':0, 'clay':0, 'wood':0}, 'cards':{'victory':0, 'monopoly':0, 'road':0, 'knights':0, 'plenty':0}, 'onHold':{'victory':0, 'monopoly':0, 'road':0, 'knights':0, 'plenty':0}, 'playedKnights':0, 'points':0, 'flag':0, 'initialPlacements':{'settlement':0, 'road':0}}}}
	gameStatus = writeJson(filename, gameStatus)
	return gameStatus

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

#@get('/modal')
#def display_modal():
#  return template('layout', modal=True) 

# This request happens every X seconds in case anything needs to be updated in the webapp
@get('/refreshContent')
def handle_ajax():
	rid = request.query.id
	if rid == "resources":
		return displayResources(request.get_cookie("playerID"))
	elif rid == "ModalBox":
		mid = request.query.modal
		playerInfo = getPlayerInfo(request.get_cookie("playerID"))
		if mid == "name":
			return template('nameBox', name=playerInfo['playerName'])
		if mid == "status":
			gameStatus = getGameStatus()
			return template('statusBox', playerInfo=getGameInfo()['playerInfo'], longestRoad=gameStatus['longestRoad'], largestArmy=gameStatus['largestArmy'])
		elif mid == "devCards":
			return "Dev card stuff!"
		
	return "<p>Your request was invalid. Please try again.</p>"

#This request happens whenever a form is submitted from the webapp.
@get('/submitForm')
def handle_form():
	fid = request.params.id
	if fid == "name":
		return updatePlayerName(request.get_cookie("playerID"), request.params.name)

# This request handles a 

@get('/')
def show_webapp():
	playerID = "0"
	response.set_cookie("playerID", playerID)
	response.set_cookie("gameTime", str(getGameInfo()['gameTime']))
	playerInfo = getPlayerInfo(0)
	return template('layout', name=playerInfo['playerName'], points=str(playerInfo['points'] + playerInfo['cards']['victory'] + playerInfo['onHold']['victory']), devCards=str(sum(playerInfo['cards'].values())), resources=dict((key, str(val)) for key, val in playerInfo['resources'].items()), currentTurn=getGameStatus()['currentPlayer'])

#@get('/blah')
#def show_form():
#	return '''\
#<img src="/images/wood.png" />
#<form action="" method="POST">
#    <label for="name">What is your name?</label>
#    <input type="text" name="name"/>
#    <input type="submit"/>
#</form>'''

#@post('/')
#def show_name():
#	return "Hello, {}!".format(request.POST.name)

application=bottle.default_app()       # run in a WSGI server
#bottle.run(host='localhost', port=8080) # run in a local test server
