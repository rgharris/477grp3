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
import os, sys, json, Cookie, time, cgi

#Enable debugging
cgitb.enable()

#Store form data
form = cgi.FieldStorage()

#The prefix of the player json files - PLAYER_FILE[num].json
PLAYER_FILE="player"
TIMEOUT = 3600 #one hour (3600 seconds)
playerID = -1

#Starting with really crappy python to get a feel for the process.
#Will make it better later...maybe.

#Get cookies!
cookies = os.environ.get('HTTP_COOKIE')
cookie = Cookie.SimpleCookie()

#Variable to check if we need to go through each possible file
checkAll = True

#First start by checking and seeing if they have a cookie. If so, check it and use it!
if cookies:
	cookie.load(cookies)
	lastactive = float(cookie['lastactive'].value)
	if(lastactive + TIMEOUT > time.time()):
		checkAll = False
		#No timeout! We can also assume the json file is valid (generally not safe,
		#but for our purposes, acceptable.)
		playerID = int(cookie['playerid'].value)
		CUR_PLAYER_FILE = PLAYER_FILE + str(playerID) + ".json"
		playerInfo = json.load(open(CUR_PLAYER_FILE))
	else:
		#We timed out, reset the cookies string and go through files.
		cookies = ''

if checkAll == True:
	#Next start by checking if json files exist. If not, create them.
	#If so, check if they are set to "active". If not, we have this player's ID!
	for i in range(0, 4):
		filename=PLAYER_FILE + str(i) + ".json"
		CUR_PLAYER_FILE = filename
		#Ignores directories, which is fine, but creates a race condition
		#if multiple people access the site within a few micro/milliseconds
		#of each other (not sure which, depends on the speed of the pi).
		#Need a way to solve this.
		newPlayer = {'playerName':"Player " + str(i+1), 'resources':{'ore':0, 'wheat':0, 'sheep':0, 'clay':0, 'wood':0}, 'cards':{}, 'active':time.time(), 'points':0}
		if not os.path.isfile(filename):
			#Need a way of doing timeouts without timeouts - arch's ntp service is not reliable, and generally returns Jan 1 1970.
			with open(filename, 'w') as f:
				json.dump(newPlayer, f, ensure_ascii=False)	
			playerID = i
			playerInfo = newPlayer.copy()
			break
		else:
			#All json files exist, so check timeouts!
			jsonInfo = open(filename)
			playerInfo = json.load(jsonInfo)
			jsonInfo.close()
			if (playerInfo["active"] == 0 or playerInfo["active"] + TIMEOUT < time.time()):
				#This player is inactive or has timed out, so here we go!
				playerID = i
				playerInfo["active"] = time.time();
				with open(filename, 'w') as f:
					json.dump(newPlayer, f, ensure_ascii=False)
					f.close()
				break
			else:
				continue

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


#################################FORM RETRIEVAL BELOW##################################
if form.has_key('user'):
	newUsername = form.getvalue("user", "Player " + str(playerID + 1))
	playerInfo['playerName'] = cgi.escape(newUsername)
	playerInfo['active'] = time.time()
	with open(CUR_PLAYER_FILE, 'w') as f:
		json.dump(playerInfo, f, ensure_ascii=False)
		f.close()



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
         <link rel="stylesheet" href="styles/catronMobilePortrait.css" type="text/css" media="screen and (max-device-width: 720px) and (orientation: portrait)"/>
			<!--Interestingly, whenever the keyboard opens on the S3 (and presumably most android devices), it switches to landscape mode. I don't know how to get around this right now.-->
         <link rel="stylesheet" href="styles/catronMobileLandsacpe.css" type="text/css" media="screen and (max-device-width: 1280px) and (orientation: landscape)"/>
   
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
         <!--Modal Boxes-->
         <a href="#x" class="overlay" id="getName"></a>
         <div class="modal" id="user">
            <form method="post" action="index.py">
            <h2>Please enter your username.</h2>
            <div>
               <input type="text" id="user" name="user" value="{0}" />
            </div>
            <input type="submit" value="Got it!" class="bottom" />
            </form>
         </div>
		
			<!--Main Body-->
			<div id="container">
				<div id="head">
					<a href="#getName" id="name_pop"><h2>{0}: {1} Points</h2></a>
					<img src="images/settings.png" class="settingsImg" />
				</div>
				<div id="resources">
					<div id="clay" class="resource">
						<img src="images/clay.png" class="resourceImg"/>
						<p class="resourceTitle">Clay</p>
						<p class="amount">{2}</p>
					</div>
					<div id="ore"  class="resource">
						<img src="images/ore.png" class="resourceImg"/>
						<p class="resourceTitle">Ore</p>
						<p class="amount">{3}</p>
					</div>
					<div id="sheep" class="resource">
						<img src="images/sheep.png" class="resourceImg"/>
						<p class="resourceTitle">Sheep</p>
						<p class="amount">{4}</p>
					</div>
					<div id="wheat" class="resource">
						<img src="images/wheat.png" class="resourceImg"/>
						<p class="resourceTitle">Wheat</p>
						<p class="amount">{5}</p>
					</div>
					<div id="wood" class="resource">
						<img src="images/wood.png" class="resourceImg"/>
						<p class="resourceTitle">Wood</p>
						<p class="amount">{6}</p>
					</div>
					<div id="cards" class="resource">
						<img src="images/sea.png" class="resourceImg"/>
						<p class="resourceTitle">Dev. Cards</p>
						<p class="amount">{7}</p>
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

	print output.format(playerInfo['playerName'], str(playerInfo['points']), str(playerInfo['resources']['clay']), str(playerInfo['resources']['ore']), str(playerInfo['resources']['sheep']), str(playerInfo['resources']['wheat']), str(playerInfo['resources']['wood']), str(len(playerInfo['cards'])))
#This needs to go at the end of all pages.
print "</html>"
