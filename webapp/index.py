#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

#My thoughts:
#Perhaps we should create 4 seperate flat files
#as a sort of database (instead of running an actual
#database, as that could be tough on this little
#guy) that use a JSON or YAML format. I'm leaning
#toward JSON because it basically maps directly to 
#python structures.
#
#The json file should contain each player's name,
#their resources, cards, etc., and the active status.
#We'll also need a way to keep track of the active status...
#The last one will determine what player number the attaching
#player is (if 1 is active, check 2, etc.)
#
#I don't think anything else needs stored on the server, right?
#Everything else can be done by live communication with the micro.

#Remove the next line at some point, just for debugging
import time
times = []
start = time.time()

# Import debugging
#import cgitb
#times.append(time.time()-start)
#Everything else.
import os
times.append(time.time()-start)
import sys
times.append(time.time()-start)
from json import load, dump
times.append(time.time()-start)
from http.cookies import SimpleCookie
times.append(time.time()-start)
from cgi import FieldStorage, parse_qs, escape
times.append(time.time()-start)
import random
times.append(time.time()-start)
import shutil
times.append(time.time()-start)
import quick2wire.i2c as i2c
times.append(time.time()-start)
#from quick2wire.gpio import pins,In


#Enable debugging
#cgitb.enable()
#Debug variable, append strings for debugging to this variable
#and they will be output after the main HTML.
debug = ''

#i2c constants
MICROADDR = 0x50
PIREG = 0
CURPLAYERREG = 1
NUMPLAYERREG = 2
MCUEVENTREG = 3
PIECETYPEREG = 6
LONGESTROADREG = 8

STARTGAMEFLAG = 2
RESETGPIOFLAG = 9
CONFIRMPIECE = 7
DENYPIECE = 8
ENDTURNFLAG = 4
ROADPURCHASEDFLAG = 10
SETTLEMENTPURCHASEFLAG = 11
CITYPURCHASEFLAG = 12
ROADDEVFLAG = 5
KNIGHTDEVFLAG = 6
ENDGAME = 13

#Some basic "constants"
PLAYER_FILE="players/"
DEV_CARD_FILE="players/dev.json"
TRADE_FILE = "players/trade.json"
RESOURCES_FILE = "chkRefresh/resources.json"
TIMEOUT = 3600 #one hour (3600 seconds)
#This is a map of values that could be in the refresh file, and are checked in javascript.
REFRESH_VALUE = {'reset':0, 'generic':1, 'tradeRequest':2, 'tradeConfirm':3, 'tradeDeny':4, 'cannotTrade':5, 'monopoly':6, 'dice':7, 'i2c':9, 'lostRoad':'a','lostArmy':'b'}
GAME_STATE_FILE="chkRefresh/gamestate.json"

#####################USEFUL FUNCTIONS###########################
#Weighted random number - used for picking a development card
#Discovered at http://eli.thegreenplace.net/2010/01/22/weighted-random-generation-in-python/
def weighted_choice_sub(weights):
	rnd = random.random() * sum(weights)
	for i, w in enumerate(weights):
		rnd -= w
		if rnd < 0:
			return i

def cookieChk(cookies, playerFile, timeout):
	cookie.load(cookies)
	#"cookies" exist, but don't contain our cookies.
	if 'catronLastactive' not in cookie or 'catronPlayerid' not in cookie:
		return (-1,'')
	lastactive = float(cookie['catronLastactive'].value)
	#We have timed out.
	if (lastactive + timeout <= time.time()):
		return (-1,'')
	playerID = int(cookie['catronPlayerid'].value)
	#The player file doesn't exist, so make a new one.
	if not os.path.isfile(playerFile + str(playerID) + ".json"):
		return (-1,'')
	jsonInfo = open(playerFile + str(playerID) + ".json")
	checkInfo = load(jsonInfo)
	jsonInfo.close
	#The file has timed out.
	if (checkInfo['active'] + timeout <= time.time()):
		return (-1,'')
	playerID = int(cookie['catronPlayerid'].value)
	playerInfo = load(open(playerFile + str(playerID) + ".json"))
	return (playerID, playerInfo)

def writeJson(jfile, info):
	info['active'] = time.time()
	with open(jfile, 'w') as f:
		dump(info, f, ensure_ascii=False)
		f.close()
	return info

def createPlayer(playerFile, playerID):
		#Dictionary Setup:
		#playerName: The player's username. Defaults to Player X, where X is their player ID + 1.
		#resources: A dictionary that contains the resources the player has available. 
		#	Resources are ore, wheat, sheep, clay, and wood, which correspond to the keys.
		#The amount available is the value.
		#cards: Available development cards to play. Victory point cards are not played, but are also stored here.
		#onHold: Development cards not yet available to play. These are development point cards picked up this turn.
		#active: The last time this file was written to. Times out after a period of time to allow overwriting, 
		#	just in case the board is turned off and not back on.
		#awards: This is where Longest Road and Largest Army are stored. A simple list.
		#points: The player's current score, minus their Victory Point cards.
		#playedKnights: The number of knights the player has played.
		#currentTurn: 1 if it's the player's turn, 0 if it is not.
		#playedDevCard: only 1 dev card per turn, so turns to 1 after a dev card has been played, and 0 at turn end.
	newPlayer = {'playerName':"Player " + str(playerID+1), 'resources':{'ore':0, 'wheat':0, 'sheep':0, 'clay':0, 'wood':0}, 'cards':{'victory':0, 'monopoly':0, 'road':0, 'knights':0, 'plenty':0}, 'onHold':{'victory':0, 'monopoly':0, 'road':0, 'knights':0, 'plenty':0}, 'playedKnights':0, 'active':time.time(), 'awards':[], 'points':0, 'currentTurn':0, 'playedDevCard':0, 'initialPlacements':{'settlement':0,'road':0}}
	writeJson(playerFile, newPlayer)
	return newPlayer

def readJson(jfile):
	jsonInfo = open(jfile)
	info = load(jsonInfo)
	jsonInfo.close()
	return info
	
def setRefresh(playerID, value):
	f = open("./chkRefresh/" + str(playerID), 'w')
	f.write(str(value))
	f.close()

def refreshAll(value):
	for i in range(-1,4):
		setRefresh(i, value)

def payForPurchase(playerInfo, resourceDict):
	for resource in resourceDict:
		playerInfo['resources'][resource] = playerInfo['resources'][resource] - resourceDict[resource]
	return playerInfo
	
def performTrade(playerFile, playerInfo, tradeInfo):
	tradingPlayerInfo = readJson(PLAYER_FILE + str(tradeInfo['from']) + ".json")
	for resource in tradeInfo['give']:
		playerInfo['resources'][resource] = playerInfo['resources'][resource] + tradeInfo['give'][resource]
		tradingPlayerInfo['resources'][resource] = int(tradingPlayerInfo['resources'][resource]) - tradeInfo['give'][resource]
	for resource in tradeInfo['get']:
		playerInfo['resources'][resource] = playerInfo['resources'][resource] - tradeInfo['get'][resource]
		tradingPlayerInfo['resources'][resource] = tradingPlayerInfo['resources'][resource] + tradeInfo['get'][resource]
	writeJson(playerFile, playerInfo)
	writeJson(PLAYER_FILE + str(tradeInfo['from']) + ".json", tradingPlayerInfo)

def checkLongestRoad(playerID, playerInfo):
	#Check for longest road.
	longestRoad = 0
	with i2c.I2CMaster() as bus:
		readMCU = bus.transaction(i2c.writing_bytes(MICROADDR, LONGESTROADREG), i2c.reading(MICROADDR, 1))
	if readMCU[0][0] - 1 == playerID:
		longestRoad = 1
		if 'road' not in playerInfo['awards']:
			playerInfo['awards'].append('road')
			for fn in os.listdir(PLAYER_FILE):
				if fn != 'dev.json' and fn != 'trade.json' and fn != str(playerID) + ".json":
					testPlayerInfo = readJson(PLAYER_FILE + fn)
					if 'road' in testPlayerInfo['awards']:
						testPlayerInfo['awards'].remove('road')
						writeJson(PLAYER_FILE + fn, testPlayerInfo)
						setRefresh(fn.split('.')[0], REFRESH_VALUE['lostRoad'])
	return playerInfo, longestRoad

def checkLargestArmy(playerID, playerInfo):
	playerInfo['awards'].append('army')
	largestArmy = 1
	playerInfo, win = editPoints(playerInfo, 2)
	for fn in os.listdir(PLAYER_FILE):
		if fn != 'dev.json' and fn != 'trade.json' and fn != str(playerID) + ".json":
			testPlayerInfo = readJson(PLAYER_FILE + fn)
			if testPlayerInfo['knightsPlayed'] > playerInfo['knightsPlayed']:
				playerInfo['awards'].remove('army')
				playerInfo = editPoints(playerInfo, 2, add=False)
				largestArmy = 0
			elif 'army' in testPlayerInfo['awards']:
				testPlayerInfo['awards'].remove('army')
				testPlayerInfo['points'] = testPlayerInfo['points'] - 2
				setRefresh(fn.split('.')[0], REFRESH_VALUE['lostArmy'])
				writeJson(PLAYER_FILE + fn, testPlayerInfo)
	return playerInfo, largestArmy, win

def editPoints(playerInfo, points, add=True):
	win = False
	if add == True:
		playerInfo['points'] = playerInfo['points'] + points
		if playerInfo['points'] >= 10:
			win = True
			with i2c.I2CMaster() as bus:
				bus.transaction(i2c.writing_bytes(MICROADDR, PIREG, ENDGAMEFLAG))
	else:
		playerInfo['points'] = playerInfo['points'] - points
	return playerInfo, win

def chkResources(playerInfo, resourceDict):
	for resource in resourceDict:
		if playerInfo['resources'][resource] < resourceDict[resource]:
			return False
	return True

def chkDeck(deckFile, timeout):
		if not os.path.isfile(deckFile):
			return True
		devBase = readJson(deckFile)
		if devBase['active'] + timeout <= time.time():
			return True
		if sum(devBase.values())-devBase['active'] >= 0:
			return True
		return False

def getResources(playerID, playerFile, playerInfo):
	startReg = (playerID * 5) + 10
	with i2c.I2CMaster() as bus:
		readMCU = bus.transaction(i2c.writing_bytes(MICROADDR, startReg), i2c.reading(MICROADDR, 5))
	playerInfo['resources']['ore'] = playerInfo['resources']['ore'] + readMCU[0][0]
	playerInfo['resources']['wheat'] = playerInfo['resources']['wheat'] +  readMCU[0][1]
	playerInfo['resources']['sheep'] = playerInfo['resources']['sheep'] + readMCU[0][2]
	playerInfo['resources']['clay'] = playerInfo['resources']['clay'] + readMCU[0][3]
	playerInfo['resources']['wood'] = playerInfo['resources']['wood'] + readMCU[0][4]
	writeJson(playerFile, playerInfo)

def endTurn(playerFile, playerInfo, gameState):
   for resource in playerInfo['cards']:
      playerInfo['cards'][resource] = playerInfo['cards'][resource] + playerInfo['onHold'][resource]
   playerInfo['onHold'] = {'victory':0, 'monopoly':0, 'road':0, 'knights':0, 'plenty':0}
   playerInfo['playedDevCard'] = 0
   playerInfo['currentTurn'] = 0
   writeJson(playerFile, playerInfo)
   numPlayers = len(dict((key, val) for key, val in gameState['ready'].items() if val != 0))
   gameState['diceRolled'] = 0
   if gameState['firstPlayer'] == numPlayers -1:
      lastPlayer = 0
   else:
      lastPlayer = gameState['firstPlayer'] - 1
   if gameState['setupComplete'] == 1:
      if playerID == numPlayers - 1:
         nextPlayerID = 0
      else:
         nextPlayerID = playerID + 1
      with i2c.I2CMaster() as bus:
         bus.transaction(i2c.writing_bytes(MICROADDR, PIREG, ENDTURNFLAG)) 
   else:
      if gameState['reverse'] == 0:
         if playerID == numPlayers - 1:
            nextPlayerID = 0
         else:
            nextPlayerID = playerID + 1
         if nextPlayerID == gameState['firstPlayer']:
            nextPlayerID = playerID
            gameState['reverse'] = 1
            writeJson(GAME_STATE_FILE, gameState)
      else:
         if playerID == gameState['firstPlayer']:
            gameState['setupComplete'] = 1
            writeJson(GAME_STATE_FILE, gameState)
            nextPlayerID = playerID
            getResources(playerID, playerFile, playerInfo)
            with i2c.I2CMaster() as bus:
               bus.transaction(i2c.writing_bytes(MICROADDR, PIREG, ENDTURNFLAG)) 
         else:
            if playerID == 0:
               nextPlayerID = numPlayers - 1
            else:
               nextPlayerID = playerID - 1
         getResources(playerID, playerFile, playerInfo)
   nextPlayerInfo = readJson(PLAYER_FILE + str(nextPlayerID) + ".json")
   nextPlayerInfo['currentTurn'] = 1
   writeJson(PLAYER_FILE + str(nextPlayerID) + ".json", nextPlayerInfo)
   writeJson(GAME_STATE_FILE, gameState)
   with i2c.I2CMaster() as bus:
      bus.transaction(i2c.writing_bytes(MICROADDR, CURPLAYERREG, nextPlayerID + 1))
   setRefresh(nextPlayerID, 1)

	
####################PRE DISPLAY IS BELOW###################


#Remove the next 2 lines at some point, just for debugging
elapsedTime = time.time() - start
debug = debug + "\nDone importing all libraries and setting up functions: " + str(elapsedTime) + " seconds\n"

#Store form data
form = FieldStorage()


#Get cookies!
cookies = os.environ.get('HTTP_COOKIE')
cookie = SimpleCookie()

#Throw query string in a var for later.
query = os.environ.get('QUERY_STRING')
pairs = parse_qs(query)

#First start by checking and seeing if they have a cookie. If so, check it and use it!
if cookies:
	playerID, playerInfo = cookieChk(cookies, PLAYER_FILE, TIMEOUT)
else:
	playerInfo = ''
	playerID = -1

#Remove the next 2 lines at some point, just for debugging
elapsedTime = time.time() - start
debug = debug + "\nDone checking cookies: " + str(elapsedTime) + " seconds\n"

#Get the game state.
if not os.path.isfile(GAME_STATE_FILE):
	gameState = {'gameStart':0, 'ready':{'0':0, '1':0, '2':0, '3':0}, 'diceRolled': 0, 'setupComplete':0, 'firstPlayer':-1, 'reverse':0}
	writeJson(GAME_STATE_FILE, gameState)
	#If we're writing a new one, delete all old player files.
	for fn in os.listdir(PLAYER_FILE):
		shutil.move(PLAYER_FILE + fn, "backup" + PLAYER_FILE + fn)
else:
	gameState = readJson(GAME_STATE_FILE)
	if gameState['active'] + TIMEOUT < time.time():
		gameState = {'gameStart':0, 'ready':{'0':0,'1':0, '2':0, '3':0}, 'diceRolled':0, 'setupComplete':0, 'firstPlayer':-1, 'reverse':0}
		#If we're writing a new one, delete all old player files.
		for fn in os.listdir(PLAYER_FILE):
			shutil.move(PLAYER_FILE + fn, "backup" + PLAYER_FILE + fn)
	else:
		if gameState['active'] + TIMEOUT*0.75 < time.time():
			#refresh the gamestate file if we're nearing the timeout.
			writeJson(GAME_STATE_FILE, gameState)
if playerInfo == '' and gameState['gameStart'] == 0 and "ready" in pairs:
	#First, go through and remove all player files that have timed out.
	#(Move them to a backup file for testing purposes)
	for i in range(0, 4):
		playerFile = PLAYER_FILE + str(i) + ".json"
		if os.path.isfile(playerFile):
			playerInfo = readJson(playerFile)
			if(playerInfo["active"] == 0 or playerInfo["active"] + TIMEOUT < time.time()):
				shutil.move(playerFile, "backup" + playerFile)

	#Next start by checking if json files exist. If not, create them.
	#If so, check if they are set to "active". If not, we have this player's ID!
	for i in range(0, 4):
		playerFile = PLAYER_FILE + str(i) + ".json"
		if not os.path.isfile(playerFile):
			playerID = i
			refreshAll(1)
			playerInfo = createPlayer(playerFile, playerID)
			break
		else:
			#That json file exists, so check it's timeout!
			#This bit of code should never be executed now, but I'm leaving it for historical purposes.
			playerInfo = readJson(playerFile)
			if (playerInfo["active"] == 0 or playerInfo["active"] + TIMEOUT < time.time()):
				#This player is inactive or has timed out, so here we go!
				playerID = i
				refreshAll(1)
				playerInfo = createPlayer(playerFile, playerID)				
				break
			else:
				continue

#This will make it easy later.
playerFile = PLAYER_FILE + str(playerID) + ".json"

if playerID != -1:
	#Set cookie for player ID and last active time.
	#This should have the effect of just resetting
	#last active time if the the cookie existed
	#already.
	#(Clear cookie var in the process)
	cookie = SimpleCookie()
	cookie['catronPlayerid'] = str(playerID)
	cookie['catronLastactive'] = str(time.time())
	#Cookies need to be sent before other headers
	print(cookie)

#Now that we've set the cookie, we need to simply overwrite
#the "autorefresh" file with a 0, so it doesn't autorefresh again.
setRefresh(playerID,REFRESH_VALUE['reset'])

#Remove the next 2 lines at some point, just for debugging
elapsedTime = time.time() - start
debug = debug + "\nDone checking json files and setting cookies: " + str(elapsedTime) + " seconds\n"

#################################i2c CHECK#############################################
if "i2c" in pairs:		
	if playerInfo != '' and playerInfo['currentTurn'] == 1:
		with i2c.I2CMaster() as bus:
			readMCU = bus.transaction(i2c.writing_bytes(MICROADDR, MCUEVENTREG), i2c.reading(MICROADDR, 1))
			if readMCU[0][0] == 4 or readMCU[0][0] == 5:
				readMCU = bus.transaction(i2c.writing_bytes(MICROADDR, PIECETYPEREG), i2c.reading(MICROADDR, 1))
				readMCU = readMCU[0][0]
				bus.transaction(i2c.writing_bytes(MICROADDR, PIREG, RESETGPIOFLAG))
				print("Location: index.py?modalConfirm=1&readMCU=" + str(readMCU) + "#modal")
			elif readMCU == 6:
				readMCU = bus.transaction(i2c.writing_bytes(MICROADDR, PIECETYPEREG), i2c.reading(MICROADDR, 1))
				readMCU = readMCU[0][0]
				bus.transaction(i2c.writing_bytes(MICROADDR, PIREG, RESETGPIOFLAG))
				print("Location: index.py?modalConfirm=2&readMCU=" + str(readMCU) + "#modal")
			elif readMCU == 11:
				bus.transaction(i2c.writing_bytes(MICROADDR, PIREG, RESETGPIOFLAG))
				print("Location: index.py")
#Remove the next 2 lines at some point, just for debugging
elapsedTime = time.time() - start
debug = debug + "\nDone with I2C check: " + str(elapsedTime) + " seconds\n"
#################################FORM RETRIEVAL BELOW##################################
if 'user' in form:
	newUsername = form.getvalue("user", "Player " + str(playerID + 1))
	playerInfo['playerName'] = escape(newUsername)
	writeJson(playerFile, playerInfo)
elif "endTurn" in form:
	endTurn(playerFile, playerInfo, gameState)
elif "noEndTurn" in form:
	pass
elif "confirmPurchase" in form:
	purchaseItem = form.getvalue("purchase")

	if(purchaseItem == "settle"):
		playerInfo = payForPurchase(playerInfo, {'wood':1, 'clay':1, 'sheep':1, 'wheat':1})
		playerInfo, win = editPoints(playerInfo, 1)
		with i2c.I2CMaster() as bus:
			bus.transaction(i2c.writing_bytes(MICROADDR, PIREG, SETTLEMENTPURCHASEDFLAG))
		writeJson(playerFile, playerInfo)
		#Notify board to place piece.
		if win == False:
			print("Location: index.py?place=piece#modal")
		else:
			print("Location: index.py?place=piece&win=true#modal")

	elif(purchaseItem == "city"):
		playerInfo = payForPurchase(playerInfo, {'wheat':2, 'ore':3})
		#Since a city must be placed where a settlement was, it's only 1 additional point
		playerInfo, win = editPoints(playerInfo, 1)
		with i2c.I2CMaster() as bus:
			bus.transaction(i2c.writing_bytes(MICROADDR, PIREG, CITYPURCHASEDFLAG))
		if win == False:
			print("Location: index.py?place=piece#modal")
		else:
			print("Location: index.py?place=piece&win=true#modal")
		writeJson(playerFile, playerInfo)
		#Notify board to place piece.
		print("Location: index.py?place=piece#modal")

	elif(purchaseItem == "road"):
		playerInfo = payForPurchase(playerInfo, {'wood':1, 'clay':1})
		playerInfo, longestRoad = checkLongestRoad(playerID, playerInfo)
		with i2c.I2CMaster() as bus:
			bus.transaction(i2c.writing_bytes(MICROADDR, PIREG, ROADPURCHASEDFLAG))
		writeJson(playerFile, playerInfo)
		#Notify board to place piece.
		if longestRoad == 1:
			print("Location: index.py?place=piece&longestRoad=1#modal")
		else:
			print("Location: index.py?place=piece#modal")

	elif(purchaseItem == "dev"):
		newDevBase = {'active':time.time(), 'knights':14, 'monopoly':2, 'road':2, 'plenty':2, 'victory':5}
		#Store current available dev cards in external json store.
		if not os.path.isfile(DEV_CARD_FILE):
			devBase = writeJson(DEV_CARD_FILE, newDevBase)
		else:
			devBase = readJson(DEV_CARD_FILE)
			if devBase['active']+TIMEOUT < time.time():
				devBase = writeJson(DEV_CARD_FILE, newDevBase)
		#Make sure the next two lists are in the same order!
		#If there are no cards available of a particular kind, it's weight will be '0', thus making it
		#impossible to be selected.
		weights = [devBase['knights'], devBase['monopoly'], devBase['road'], devBase['plenty'], devBase['victory']]
		cardList = ['knights','monopoly','road','plenty','victory']
		if sum(weights) == 0:
			#If the sum of weights is 0, that means there are 0 cards in our deck. Nothing to draw!
			print("Location: index.py?development=none#modal")
		else:
			#This will return an integer between 0 and 4. The order is the same as the lists above.
			randNum = weighted_choice_sub(weights)
			if cardList[randNum] in playerInfo['onHold']:
				playerInfo['onHold'][cardList[randNum]] = playerInfo['onHold'][cardList[randNum]]+1
			else:
				playerInfo['onHold'][cardList[randNum]] = 1
			#We're done, output the player to the json file and the current availablity to the devBase file.
			playerInfo = payForPurchase(playerInfo, {'wheat':1, 'sheep':1, 'ore':1})
			writeJson(playerFile, playerInfo)
			#Change the amount of that type of card available.
			devBase[cardList[randNum]] = devBase[cardList[randNum]] - 1
			writeJson(DEV_CARD_FILE, devBase)
			#NOW We're done. Redirect to modal box to show what they got.
			print("Location: index.py?obtained=" + cardList[randNum] + "#modal")

elif "doNotPurchase" in form:
	pass
elif "settle" in form:
	if (chkResources(playerInfo, {'wood':1, 'clay':1, 'wheat':1, 'sheep':1}) == False):
		#Redirect to self with query string that identifies lack of resources and type of purchase; query string brings up modal box.
		print("Location: index.py?resources=false&purchase=settle#modal")
	else:
		#Redirect to self - query string identifies resources and type of purchase.
		print("Location: index.py?resources=true&purchase=settle#modal")
elif "city" in form:
	if (chkResources(playerInfo, {'wheat':2, 'ore':3}) == False):
		#Redirect to self with query string that identifies lack of resources and type of purchase; query string brings up modal box.
		print("Location: index.py?resources=false&purchase=city#modal")
	else:
		#Redirect to self - query string identifies resources and type of purchase.
		print("Location: index.py?resources=true&purchase=city#modal")
elif "road" in form:
	if (chkResources(playerInfo, {'clay':1, 'wood':1}) == False):
		#Redirect to self with query string that identifies lack of resources and type of purchase; query string brings up modal box.
		print("Location: index.py?resources=false&purchase=road#modal")
	else:
		#Redirect to self - query string identifies resources and type of purchase.
		print("Location: index.py?resources=true&purchase=road#modal")
elif "dev" in form:
	if (chkResources(playerInfo, {'sheep':1, 'wheat':1, 'ore':1}) == False):
		#Redirect to self with query string that identifies lack of resources and type of purchase; query string brings up modal box.
		print("Location: index.py?resources=false&purchase=dev#modal")
	else:
		#Redirect to self - query string identifies resources and type of purchase.
		if chkDeck(DEV_CARD_FILE,TIMEOUT) == False:
			print("Location: index.py?development=none#modal")
		else:
			print("Location: index.py?resources=true&purchase=dev#modal")
elif "deal" in form:
	#obtaining what we want to trade and what for.
	#First check if we can do the trade.
	give = {'clay': int(form.getvalue('giveClay')),'ore': int(form.getvalue('giveOre')), 'wheat': int(form.getvalue('giveWheat')),'sheep': int(form.getvalue('giveSheep')),'wood': int(form.getvalue('giveWood'))}
	get = {'clay': int(form.getvalue('getClay')),'ore': int(form.getvalue('getOre')), 'wheat': int(form.getvalue('getWheat')),'sheep': int(form.getvalue('getSheep')),'wood': int(form.getvalue('getWood'))}
	give = dict((key, val) for key, val in give.items() if val != 0)
	get = dict((key, val) for key, val in get.items() if val != 0)
	if (len(give) == 0 or len(get) == 0):
		print("Location: index.py?trade=invalid#modal")
	elif (chkResources(playerInfo, give) == False):
		print("Location: index.py?trade=invalid#modal")
	else:
		#So now we're sure we can do the trade on this end, so save this info in a json store.
		writeJson(TRADE_FILE, {'from':playerID, 'give':give, 'get':get})
		#Now, obtain the player we want to trade with
		tradePlayer = form.getvalue('playerid')
		#Check if remote player can trade. If so, submit proper request, if not, submit cannot trade.
		tradeInfo = readJson(TRADE_FILE)
		tradingPlayerInfo = readJson(PLAYER_FILE + str(tradePlayer) + ".json")
		if(chkResources(tradingPlayerInfo, get) == False):
			setRefresh(int(tradePlayer), REFRESH_VALUE['cannotTrade'])
		else:
			setRefresh(int(tradePlayer), REFRESH_VALUE['tradeRequest'])
elif "noDeal" in form:
	#canceled trade. Just pass.
	pass
elif "confirmTrade" in form:
	#From remote player, confirming trade.
	#Perform trade (checks have already been done at this point).
	tradeInfo = readJson(TRADE_FILE)
	performTrade(playerFile, playerInfo, tradeInfo)
	setRefresh(int(form.getvalue('tradeFrom')), REFRESH_VALUE['tradeConfirm'])
elif "doNotTrade" in form:
	#From remote player, denying trade.
	setRefresh(int(form.getvalue('tradeFrom')), REFRESH_VALUE['tradeDeny'])
elif "victory" in form:
	print("Location: index.py?play=victory#modal")
elif "monopoly" in form:
	print("Location: index.py?play=monopoly#modal")
elif "roadDev" in form:
	print("Location: index.py?play=road#modal")
elif "knights" in form:
	print("Location: index.py?play=knights#modal")
elif "plenty" in form:
	print("Location: index.py?play=plenty#modal")
elif "playMonopoly" in form:
	print("Location: index.py?playing=monopoly#modal")
elif "playRoadDev" in form:
	pass
elif "playKnights" in form:
	pass
elif "playPlenty" in form:
	print("Location: index.py?playing=plenty#modal")
elif "plentySelected" in form:
	playerInfo['resources'][form.getvalue('resource1')] = playerInfo['resources'][form.getvalue('resource1')] + 1
	playerInfo['resources'][form.getvalue('resource2')] = playerInfo['resources'][form.getvalue('resource2')] + 1
	playerInfo['playedDevCard'] = 1
	playerInfo['cards']['plenty'] = playerInfo['cards']['plenty'] - 1
	writeJson(playerFile, playerInfo)
	print("Location: index.py?played=plenty#modal")
elif "monopolySelected" in form:
	obtained = 0
	for fn in os.listdir(PLAYER_FILE):
		if fn != 'dev.json' and fn != 'trade.json' and fn != str(playerID) + ".json":
			monopolyPlayerInfo = readJson(PLAYER_FILE + fn)
			playerInfo['resources'][form.getvalue('resource')] = monopolyPlayerInfo['resources'][form.getvalue('resource')] + playerInfo['resources'][form.getvalue('resource')]
			obtained = obtained + monopolyPlayerInfo['resources'][form.getvalue('resource')]
			monopolyPlayerInfo['resources'][form.getvalue('resource')] = 0
			writeJson(PLAYER_FILE + fn, monopolyPlayerInfo)
			monopolyPlayerID = fn.split('.')[0]
			setRefresh(monopolyPlayerID, REFRESH_VALUE['monopoly'])
	playerInfo['playedDevCard'] = 1
	playerInfo['cards']['monopoly'] = playerInfo['cards']['monopoly'] - 1
	writeJson(playerFile, playerInfo)
	print("Location: index.py?played=monopoly&received=" + str(obtained) + "&resource=" + str(form.getvalue('resource')) + "#modal")
elif "knightsSelected" in form:
	playerInfo, largestArmy, win = checkLargestArmy(playerID, playerInfo)
	with i2c.I2CMaster() as bus:
		bus.transaction(i2c.writing_bytes(MICROADDR, PIREG, KNIGHTDEVFLAG))
	writeJson(playerFile, playerInfo)
	if win == False:
		print("Location: index.py?played=knights&largestArmy=" + largestArmy + "#modal")
	else:
		print("Location: index.py?played=knights&largestArmy=" + largestArmy + "&win=true#modal")
elif "roadDevSelected" in form:
	with i2c.I2CMaster() as bus:
		bus.transaction(i2c.writing_bytes(MICROADDR, PIREG, ROADDEVFLAG))
elif "confirmPiecePlacement" in form:
	with i2c.I2CMaster() as bus:
		bus.transaction(i2c.writing_bytes(MICROADDR, PIREG, CONFIRMPIECE))
	if gameState['setupComplete'] == 0:
		playerInfo['initialPlacements'][str(form.getvalue('piecetype'))] = playerInfo['initialPlacements'][str(form.getvalue('piecetype'))] + 1	
		writeJson(playerFile, playerInfo)
		if form.getvalue('piecetype') == 'road':
			endTurn(playerFile, playerInfo, gameState)
		if form.getvalue('piecetype') == 'settlement':
			playerInfo, win = editPoints(playerInfo, 1)
			writeJson(playerFile, playerInfo)
			if win == True:
				print("Location: index.py?win=true#modal")
	setRefresh(playerID, REFRESH_VALUE['generic']) 
elif "simpleConfirm" in pairs:
	with i2c.I2CMaster() as bus:
		readMCU = bus.transaction(i2c.writing_bytes(MICROADDR, PIECETYPEREG), i2c.reading(MICROADDR, 1))
		readMCU = readMCU[0][0]
		bus.transaction(i2c.writing_bytes(MICROADDR, PIREG, RESETGPIOFLAG))
		bus.transaction(i2c.writing_bytes(MICROADDR, PIREG, CONFIRMPIECE))
	if readMCU >= 10 and readMCU < 20:
		if readMCU % 10 == 0:
			pieceConfirmed = "thief"
		elif readMCU % 10 == 1:
			pieceConfirmed = "road"
		elif readMCU % 10 == 2:
			pieceConfirmed = "settlement"
		elif readMCU % 10 == 3:
			pieceConfirmed = "city"
		if gameState['setupComplete'] == 0:
			playerInfo['initialPlacements'][pieceConfirmed] = playerInfo['initialPlacements'][pieceConfirmed] + 1	
			writeJson(playerFile, playerInfo)
			if pieceConfirmed == 'road':
				endTurn(playerFile, playerInfo, gameState)
	print("Location: index.py")
elif "denyPiecePlacement" in form:
	with i2c.I2CMaster() as bus:
		bus.transaction(i2c.writing_bytes(MICROADDR, PIREG, DENYPIECE))
	setRefresh(playerID, REFRESH_VALUE['generic']) 
elif "simpleDeny" in pairs:
	with i2c.I2CMaster() as bus:
		bus.transaction(i2c.writing_bytes(MICROADDR, PIREG, DENYPIECE))
	print("Location: index.py")
elif "splitHand" in form:
	splitClay = int(form.getvalue("splitClay"))
	splitOre = int(form.getvalue("splitOre"))
	splitWheat = int(form.getvalue("splitWheat"))
	splitSheep = int(form.getvalue("splitSheep"))
	splitWood = int(form.getvalue("splitWood"))
	if splitClay < 0:
		splitClay = 0
	if splitOre < 0:
		splitOre = 0
	if splitWheat < 0:
		splitWheat = 0
	if splitSheep < 0:
		splitSheep = 0
	if splitWood < 0:
		splitWood = 0
	playerInfo['resources']['ore'] = playerInfo['resources']['ore'] - splitOre
	playerInfo['resources']['ore'] = playerInfo['resources']['clay'] - splitClay
	playerInfo['resources']['ore'] = playerInfo['resources']['wheat'] - splitWheat
	playerInfo['resources']['ore'] = playerInfo['resources']['sheep'] - splitSheep
	playerInfo['resources']['ore'] = playerInfo['resources']['wood'] - splitWood
	if (sum(playerInfo['resources'].itervalues()) > 7):
		print("Location: index.py?splitHand=" + str(playerID) + "#modal")
	else:
		print("Location: index.py")
	if(playerInfo['currentTurn'] == 1):
		with i2c.I2CMaster() as bus:
			bus.transaction(i2c.writing_bytes(MICROADDR, PIREG, KNIGHTDEVFLAG))

elif "dice" in pairs:
	diceNum = int(open("chkRefresh/dice", 'r').read())
	if diceNum != 7:
		newResources = readJson(RESOURCES_FILE)
		newResources = newResources[str(playerID)]
		playerInfo['resources']['ore'] += newResources['ore']
		playerInfo['resources']['wheat'] += newResources['wheat']
		playerInfo['resources']['clay'] += newResources['clay']
		playerInfo['resources']['sheep'] += newResources['sheep']
		playerInfo['resources']['wood'] += newResources['wood']
		setRefresh(playerID, REFRESH_VALUE['generic'])
	else:
		numResources = sum(playerInfo['resources'].itervalues())
		if numResources > 7:
			print("Location: index.py?splithand=true")
	gameState['diceRolled'] = 1
	writeJson(GAME_STATE_FILE, gameState)

#Remove the next 2 lines at some point, just for debugging
elapsedTime = time.time() - start
debug = debug + "\nDone form processing: " + str(elapsedTime) + " seconds\n"
#################################GAME START AND READY CHECK#############################
if "ready" in pairs:
	if (playerID != -1):
		gameState['ready'][str(playerID)] = 1
		writeJson(GAME_STATE_FILE, gameState)
		refreshAll(1)
		#Refresh again to get rid of 'ready' in pairs. Prevents infinite refresh.
	print("Location: index.py")
if "notready" in pairs:
	if (playerID != -1):
		gameState['ready'][str(playerID)] = 0
		writeJson(GAME_STATE_FILE, gameState)
		refreshAll(1)
	print("Location: index.py")
if "start" in pairs:
	gameState['gameStart'] = 1
	writeJson(GAME_STATE_FILE, gameState)
	ready = dict((key, val) for key, val in gameState['ready'].items() if val != 0)
	startPlayer = random.randint(0,int(len(ready))-1)
	gameState['firstPlayer'] = startPlayer
	writeJson(GAME_STATE_FILE, gameState)
	startPlayerInfo = readJson(PLAYER_FILE + str(startPlayer) + ".json")
	startPlayerInfo['currentTurn'] = 1
	writeJson(PLAYER_FILE + str(startPlayer) + ".json", startPlayerInfo)
	####i2c - write info to micro###
	with i2c.I2CMaster() as bus:
		bus.transaction(i2c.writing_bytes(MICROADDR, NUMPLAYERREG, int(len(ready))))
		bus.transaction(i2c.writing_bytes(MICROADDR, CURPLAYERREG, startPlayer + 1))
		bus.transaction(i2c.writing_bytes(MICROADDR, PIREG, STARTGAMEFLAG))
	refreshAll(1)
	#Locate to index to get rid of infinite refresh.
	print("Location: index.py")
#Remove the next 2 lines at some point, just for debugging
elapsedTime = time.time() - start
debug = debug + "\nDone with game start and ready check: " + str(elapsedTime) + " seconds\n"

#################################PAGE GENERATION BELOW##################################

#This stuff needs to go at the top of all pages.
print("Content-Type: text/html;charset=utf-8")
print()
print("""<!DOCTYPE HTML>
   <html>
      <head>
         <!-- Required for mobile devices -->
         <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no"/>
         <!-- Not really a good practice, but this basically just needs to work in demo. If anyone has any better ideas, PLEASE IMPLEMENT THEM. -->
         <!--<link rel="stylesheet" href="styles/catronNormal.css" type="text/css" media="screen"/>
         <link rel="stylesheet" href="styles/catronMobilePortrait.css" type="text/css" media="screen and (max-device-width: 720px) and (orientation: portrait)"/>
			<!--Interestingly, whenever the keyboard opens on the S3 (and presumably most android devices), it switches to landscape mode. I don't know how to get around this right now.
         <link rel="stylesheet" href="styles/catronMobileLandsacpe.css" type="text/css" media="screen and (max-device-width: 1280px) and (orientation: landscape)"/>-->
			<link rel="stylesheet" href="styles/catronMobilePortrait.css" type="text/css" />
			<script>
				function loadXMLDoc(div,loc)
				{
					var xmlhttp;
					xmlhttp = new XMLHttpRequest();
					xmlhttp.onreadystatechange=function()
					{
						if(xmlhttp.readyState == 4 && xmlhttp.status==200)
						{
							document.getElementById(div).innerHTML=xmlhttp.responseText;
						}
					}
					xmlhttp.open("GET",loc,true);
					xmlhttp.send();
				}
				function heartbeat(playerID)
				{
					var xmlhttp;
					xmlhttp = new XMLHttpRequest();
					xmlhttp.onreadystatechange=function()
					{
						if(xmlhttp.readyState == 4 && xmlhttp.status == 200)
						{
							if(xmlhttp.responseText == 1)
							{
								location.reload(true);
							}
							else if(xmlhttp.responseText == 2)
							{
								window.location = "./index.py?trade=check#modal";
							}
							else if(xmlhttp.responseText == 3)
							{
								window.location = "./index.py?trade=confirm#modal";
							}
							else if(xmlhttp.responseText == 4)
							{
								window.location = "./index.py?trade=deny#modal";
							}
							else if(xmlhttp.responseText == 5)
							{
								window.location = "./index.py?trade=fail#modal";
							}
							else if(xmlhttp.responseText == 6)
							{
								window.location = "./index.py?against=monoCardd#modal";
							}
							else if(xmlhttp.responseText == 7)
							{
								window.location = "./index.py?dice=new";
							}
							else if(xmlhttp.responseText == 9)
							{
								window.location = "./index.py?i2c=flown";
							}
						}
					}
					xmlhttp.open("GET", "/chkRefresh/chk.py?id=" + playerID, true);
					xmlhttp.send();
				}
				
   		</script>
      </head>
""")
if gameState['gameStart'] == 1 and playerID == -1:
	print("""<body class="error">
        		 <div id="container">
           		 <div id="head">
               	<h2>Error!</h2>
		          </div>
      	       <div id="body">
           		    <p>This game is currently in progress. Enjoy watching this game, and try to join the next one!</p>
	             </div>
    	      </div>
	      </body>
	""")

elif gameState['gameStart'] == 0:
	ready = dict((key, val) for key, val in gameState['ready'].items() if val != 0)
	if len(ready) >= 4 and playerID == -1:
		print("""<body class="error">
     	   		 <div id="container">
     	      		 <div id="head">
     	          	<h2>Error!</h2>
			          </div>
     	 	       <div id="body">
     	      		    <p>This game has reached the maximum number of players. Enjoy watching this game, and try to join the next one!</p>
	  	           </div>
    		      </div>
	  	    </body>
		""")
	else:
		output = """<body class="wait">
						<script>setInterval("heartbeat({2})", 5000)</script>
						<div id="container">
							<div id="head">
								<h2>Waiting for Players</h2>
								<img src="images/settings.png" class="settingsImg" />
							</div>
							<div id="body">
								Waiting for players! Currently have {0} players ready.<br />
								{1}
							</div>
						</div>
						</body>"""
		if playerID == -1 or gameState['ready'][str(playerID)] == 0:
			stateLink = "<a href=\"index.py?ready=" + str(playerID) + "\" class=\"readyLink\">I'm ready!</a>"
		elif gameState['ready'][str(playerID)] == 1:
			if len(ready) < 3:
				stateLink = "<span class=\"waitLink\">Waiting...</span><a href=\"index.py?notready=" + str(playerID) +  "\" class=\"notReadyLink\">I'm not ready!</a>"
			else:
				stateLink = "<a href=\"index.py?start=true\" class=\"halfReadyLink\">Start game!</a><a href=\"index.py?notready=" + str(playerID) + "\" class=\"notReadyLink\">I'm not ready!</a>"
		print(output.format(str(len(ready)),stateLink,str(playerID)))
	
elif gameState['gameStart'] == 1:
	script = ""
	#Go through the query string, and check for queries that would bring up a box. If we see one,
	#add a script that calls AJAX to bring in the correct box.
	if "purchase" in pairs:
		if pairs["resources"][0] == "false":
			script = "<script>loadXMLDoc('ModalBox', '/dialogs/purchase.py?invalid=" + pairs["purchase"][0] + "')</script>"
		elif pairs["resources"][0] == "true":
			script = "<script>loadXMLDoc('ModalBox', '/dialogs/purchase.py?confirm=" + pairs["purchase"][0] + "')</script>"
	elif "obtained" in pairs:
		script = "<script>loadXMLDoc('ModalBox', '/dialogs/purchase.py?obtained=" + pairs["obtained"][0] + "')</script>"
	elif "development" in pairs:
		if pairs["development"][0] == "none":
			script = "<script>loadXMLDoc('ModalBox', '/dialogs/purchase.py?development=none')</script>"
	elif "place" in pairs:
		script = "<script>loadXMLDoc('ModalBox', '/dialogs/purchase.py?place=piece')</script>"
	elif "trade" in pairs:
		if pairs["trade"][0] == "invalid":
			script = "<script>loadXMLDoc('ModalBox', '/dialogs/trade.py?invalid=current')</script>"
		elif pairs["trade"][0] == "check":
			script = "<script>loadXMLDoc('ModalBox', '/dialogs/trade.py?confirm=true')</script>"
		elif pairs["trade"][0] == "confirm":
			script = "<script>loadXMLDoc('ModalBox', '/dialogs/trade.py?success=true')</script>"
		elif pairs["trade"][0] == "deny":
			script = "<script>loadXMLDoc('ModalBox', '/dialogs/trade.py?deny=true')</script>"
		elif pairs["trade"][0] == "fail":
			script = "<script>loadXMLDoc('ModalBox', '/dialogs/trade.py?invalid=remote')</script>"
	elif "play" in pairs:
		if pairs["play"][0] == "victory":
			script = "<script>loadXMLDoc('ModalBox', '/dialogs/devCards.py?card=victory&player=" + str(playerID) + "&playedDev=" + str(playerInfo['playedDevCard']) + "')</script>"
		elif pairs["play"][0] == "monopoly":
			script = "<script>loadXMLDoc('ModalBox', '/dialogs/devCards.py?card=monopoly&player=" + str(playerID) + "&playedDev=" + str(playerInfo['playedDevCard']) + "')</script>"
		elif pairs["play"][0] == "road":
			script = "<script>loadXMLDoc('ModalBox', '/dialogs/devCards.py?card=road&player=" + str(playerID) + "&playedDev=" + str(playerInfo['playedDevCard']) + "')</script>"
		elif pairs["play"][0] == "knights":
			script = "<script>loadXMLDoc('ModalBox', '/dialogs/devCards.py?card=knights&player=" + str(playerID) + "&playedDev=" + str(playerInfo['playedDevCard']) + "')</script>"
		elif pairs["play"][0] == "plenty":
			script = "<script>loadXMLDoc('ModalBox', '/dialogs/devCards.py?card=plenty&player=" + str(playerID) + "&playedDev=" + str(playerInfo['playedDevCard']) + "')</script>"
	elif "playing" in pairs:
		if pairs["playing"][0] == "monopoly":
			script = "<script>loadXMLDoc('ModalBox', '/dialogs/devCards.py?confirm=monopoly&player=" + str(playerID) + "')</script>"
		elif pairs["playing"][0] == "plenty":
			script = "<script>loadXMLDoc('ModalBox', '/dialogs/devCards.py?confirm=plenty&player=" + str(playerID) + "')</script>"
		elif pairs["playing"][0] == "road":
			pass
		elif pairs["playing"][0] == "knights":
			pass
	elif "played" in pairs:
		if pairs["played"][0] == "monopoly":
			script = "<script>loadXMLDoc('ModalBox', '/dialogs/devCards.py?success=monopoly&player=" + str(playerID) + "&num=" + str(pairs["received"][0]) + "&resource=" + str(pairs["resource"][0]) + "')</script>"
		elif pairs["played"][0] == "plenty":
			script = "<script>loadXMLDoc('ModalBox', '/dialogs/devCards.py?success=plenty&player=" + str(playerID) + "')</script>"
		elif pairs["played"][0] == "road":
			pass
		elif pairs["played"][0] == "knights":
			pass
	elif "against" in pairs:
		script = "<script>loadXMLDoc('ModalBox', '/dialogs/devCards.py?against=monopoly&player=" + str(playerID) + "')</script>"
	#Put elif in for i2c stuff
	elif "modalConfirm" in pairs:
			script = "<script>loadXMLDoc('ModalBox', '/dialogs/i2c.py?read=" + str(pairs['readMCU'][0]) + "&confirm=" + str(pairs['modalConfirm'][0]) + "')</script>"
	elif "splithand" in pairs:
			script = "<script>loadXMLDoc('ModalBox', '/dialogs/splitHand.py?player=" + str(playerID) + "')</script>"
	elif gameState['setupComplete'] == 0:
			script = "<script>loadXMLDoc('ModalBox', '/dialogs/initSetup.py?player=" + str(playerID) + "')</script>"
	output = """
		<body>
			<script>setInterval("heartbeat({9})", 5000)</script>
			{0}
         <!--Modal Boxes-->
         <a href="#x" class="overlay" id="modal"></a>
         <div class="modal" id="ModalBox">
         </div>
		
			<!--Main Body-->
			<div id="container">
				<div id="head">
					<a href="#modal" id="name_pop" onclick="loadXMLDoc('ModalBox', '/dialogs/username.py?user={1}')"><h2>{1}: {2} Points</h2></a>
					<img src="images/settings.png" class="settingsImg" />
				</div>
				<div id="resources">
					<div id="clay" class="resource">
						<img src="images/clay.png" class="resourceImg"/>
						<p class="resourceTitle">Clay</p>
						<p class="amount">{3}</p>
					</div>
					<div id="ore"  class="resource">
						<img src="images/ore.png" class="resourceImg"/>
						<p class="resourceTitle">Ore</p>
						<p class="amount">{4}</p>
					</div>
					<div id="sheep" class="resource">
						<img src="images/sheep.png" class="resourceImg"/>
						<p class="resourceTitle">Sheep</p>
						<p class="amount">{5}</p>
					</div>
					<div id="wheat" class="resource">
						<img src="images/wheat.png" class="resourceImg"/>
						<p class="resourceTitle">Wheat</p>
						<p class="amount">{6}</p>
					</div>
					<div id="wood" class="resource">
						<img src="images/wood.png" class="resourceImg"/>
						<p class="resourceTitle">Wood</p>
						<p class="amount">{7}</p>
					</div>
					<div id="cards" class="resource">
						<a href="#modal" id="cardsLink" onclick="loadXMLDoc('ModalBox', '/dialogs/devCards.py?player={9}')">
							<img src="images/sea.png" class="resourceImg"/>
							<p class="resourceTitle">Dev. Cards</p>
							<p class="amount">{8}</p>
						</a>
					</div>
				</div>
				<div class="clear"></div>
				<div id="footer">
					{10}
					{11}
					<a href="#modal" class="button borderTop borderRight spacingLeft" onclick="loadXMLDoc('ModalBox', '/dialogs/gameStatus.py')">Status</a>
					{12}
					{13}
					{14}
				</div>
			</div>
		</body>
	"""

	confirmLink = "<span class=\"button fade borderTop borderRight spacingLeft\">&nbsp;</span>"
	denyLink = "<span class=\"button fade borderTop\">&nbsp;</span>"
	curPoints = playerInfo['points']
	if 'victory' in playerInfo['onHold']:
		curPoints = curPoints + playerInfo['onHold']['victory']
	if 'victory' in playerInfo['cards']:
		curPoints = curPoints + playerInfo['cards']['victory']
	if playerInfo['currentTurn'] == 1:
		purchaseLink = "<a href=\"#modal\" class=\"button borderRight spacingLeft\" onclick=\"loadXMLDoc('ModalBox', '/dialogs/purchase.py')\">Purchase</a>"
		tradeLink = "<a href=\"#modal\" class=\"button\" onclick=\"loadXMLDoc('ModalBox', '/dialogs/trade.py')\">Trade</a>"
		confirmLink = "<a href=\"index.py?simpleConfirm=true\" class=\"button borderTop borderRight spacingLeft\" onclick=\"\">Confirm</a>"
		denyLink = "<a href=\"index.py?simpleDeny=true\" class=\"button borderTop\" onclick=\"\">Deny</a>"
		if gameState['diceRolled'] == 0:
			turnLink = "<a href=\"#dice\" class=\"button borderTop\" onclick=\"loadXMLDoc('dierolled', '/dialogs/dice.py?player=" + str(playerID) + "')\">Roll Dice</a><div id=\"dierolled\" style=\"display:none\"></div>"
		else:
			turnLink = "<a href=\"#modal\" class=\"button borderTop\" onclick=\"loadXMLDoc('ModalBox', '/dialogs/endTurn.py')\">End Turn</a>"
	else:
		purchaseLink = "<span class=\"button fade borderRight spacingLeft\">&nbsp;</span>"
		tradeLink = "<span class=\"button fade\">&nbsp;</span>"
		turnLink = "<span class=\"button fade borderTop\">&nbsp;</span>"

	print(output.format(script,playerInfo['playerName'], str(curPoints), str(playerInfo['resources']['clay']), str(playerInfo['resources']['ore']), str(playerInfo['resources']['sheep']), str(playerInfo['resources']['wheat']), str(playerInfo['resources']['wood']), str(sum(playerInfo['cards'].values()) + sum(playerInfo['onHold'].values())),playerID,purchaseLink,tradeLink,turnLink,confirmLink,denyLink))
#This needs to go at the end of all pages.
print("</html>")
#Remove the next 2 lines at some point, just for debugging
elapsedTime = time.time() - start
debug = debug + "\nNow done with everything: " + str(elapsedTime) + " seconds\n"
#Debug variable, prints after main html. Most browsers will still render.
print(debug)
print(times)
