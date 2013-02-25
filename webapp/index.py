#!/usr/bin/env python
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

# Import debugging
import cgitb
#Everything else.
import os, sys, json, Cookie, time

#Enable debugging
cgitb.enable()

#The prefix of the player json files - PLAYER_FILE[num].json
PLAYER_FILE="player"
TIMEOUT = 3600 #one hour (3600 seconds)
playerID = -1

#Starting with really crappy python to get a feel for the process.
#Will make it better later...maybe.

#Get cookies!
cookies = os.environ.get('HTTP_COOKIE')
cookie = Cookie.SimpleCookie()

#First start by checking if json files exist. If not, create them.
#If so, check if they are set to "active". If not, we have this player's ID!
for i in range(0, 4):
	filename=PLAYER_FILE + str(i) + ".json"
	#Ignores directories, which is fine, but creates a race condition
	#if multiple people access the site within a few micro/milliseconds
	#of each other (not sure which, depends on the speed of the pi).
	#Need a way to solve this.
	newPlayer = {'playerName':"player" + str(i), 'resources':{'ore':0, 'wheat':0, 'sheep':0, 'clay':0, 'wood':0}, 'cards':{}, 'active':1, 'points':0}
	if not os.path.isfile(filename):
		#Need a way of doing timeouts without timeouts - arch's ntp service is not reliable, and generally returns Jan 1 1970.
		with open(filename, 'w') as f:
			json.dump(newPlayer, f, ensure_ascii=False)	
		playerID = i
		break
	else:
		#All json files exist, so check cookies!
		if not cookies:
			#No cookies. Check if player is active, if not, use this player. If so, carry on.
			jsonInfo = open(filename)
			playerInfo = json.load(jsonInfo)
			jsonInfo.close()
			if(playerInfo["active"] == 0):
				#This player is inactive, so here we go!
				playerID = i
				playerInfo["active"] = 1
				with open(filename, 'w') as f:
					json.dump(newPlayer, f, ensure_ascii=False)
				break
			else:
				continue
		else:
			#We have delicious cookies (are they snickerdoodle?).
			cookie.load(cookies)
			lastactive = float(cookie['lastactive'].value)
			if (lastactive + TIMEOUT > time.time()):
				#We didn't time out! We have the player ID, and the JSON file is still valid.
				playerID = int(cookie['playerid'].value)
				playerInfo = json.load(open(PLAYER_FILE + str(playerID) + ".json"))
				break
			else:
				#Cookies aren't valid anymore. Reset the cookies string.
				cookies = ''

if playerID != -1:
	#Set cookie for player ID and last active time.
	#This should have the effect of just resetting
	#last active time if the the cookie existed
	#already.
	#(Clear cookie var in the process)
	cookie = Cookie.SimpleCookie()
	cookie['playerid'] = str(playerID)
	cookie['lastactive'] = str(time.time())
	#Cookies need to be sent before other headers
	print cookie




#################################PAGE GENERATION BELOW##################################

#This stuff needs to go at the top of all pages.
print "Content-Type: text/html;charset=utf-8"
print
print """<!DOCTYPE HTML>
   <html>
      <head>
         <!-- Required for mobile devices -->
         <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no"/>
         <!-- Not really a good practice, but this basically just needs to work in demo. If anyone has any better ideas, PLEASE IMPLEMENT THEM. -->
         <link rel="stylesheet" href="styles/catronNormal.css" type="text/css" media="screen"/>
         <link rel="stylesheet" href="styles/catronMobilePortrait.css" type="text/css" media="screen and (max-device-width: 480px) and (orientation: portrait)"/> 
         <link rel="stylesheet" href="styles/catronMobileLandscape.css" type="text/css" media="screen and (max-device-width: 640px) and (orientation: landscape)"/>
         <!--<link rel="stylesheet" href="styles/catronMobilePortrait.css" type="text/css" />-->
   
      </head>
"""
if playerID == -1:
	print """<body class="error">
        		 <div id="container">
           		 <div id="head">
               	<h2>Max Players Reached!</h2>
		          </div>
      	       <div id="body">
           		    <p>This game already has the maximum number of players. Enjoy watching this game, and try to join the next one!</p>
	             </div>
    	      </div>
	      </body>
	"""

else:
	#The below HTML is just an example page. It only works in portrait mode on my S3,
	#and I don't know how it would look on, say, a One X or an iPhone. Additionally,
	#it doesn't do any setup (get user ID) and none of the buttons work yet.
	#
	#I'm working on it.

	output = """
		<body>
			<div id="container">
				<div id="head">
					<h2>Player {0}: 0 Points</h2>
					<img src="images/settings.png" class="settingsImg" />
				</div>
				<div id="resources">
					<div id="clay" class="resource">
						<img src="images/clay.png" class="resourceImg"/>
						<p class="resourceTitle">Clay</p>
						<p class="amount">10</p>
					</div>
					<div id="ore"  class="resource">
						<img src="images/ore.png" class="resourceImg"/>
						<p class="resourceTitle">Ore</p>
						<p class="amount">10</p>
					</div>
					<div id="sheep" class="resource">
						<img src="images/sheep.png" class="resourceImg"/>
						<p class="resourceTitle">Sheep</p>
						<p class="amount">10</p>
					</div>
					<div id="wheat" class="resource">
						<img src="images/wheat.png" class="resourceImg"/>
						<p class="resourceTitle">Wheat</p>
						<p class="amount">10</p>
					</div>
					<div id="wood" class="resource">
						<img src="images/wood.png" class="resourceImg"/>
						<p class="resourceTitle">Wood</p>
						<p class="amount">10</p>
					</div>
					<div id="cards" class="resource">
						<img src="images/sea.png" class="resourceImg"/>
						<p class="resourceTitle">Dev. Cards</p>
						<p class="amount">10</p>
					</div>
				</div>
				<div class="clear"></div>
				<div id="footer">
					<div id="b1" class="button">
						Purchase
					</div>
					<div id="b2" class="button">
						Trade
					</div>
					<div id="b3" class="button">
						Status
					</div>
					<div id="b4" class="button">
						End Turn
					</div>
				</div>
			</div>
		</body>
	"""

	print output.format(str(playerID))
#This needs to go at the end of all pages.
print "</html>"
