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
import os, sys, json

#Enable debugging
cgitb.enable()

#The prefix of the player json files - PLAYER_FILE[num].json
PLAYER_FILE="player"

playerID = -1

#Starting with really crappy python to get a feel for the process.
#Will make it better later...maybe.

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

print "Content-Type: text/html;charset=utf-8"
print
#if playerID == -1:
	#We hit all 4 players, so disallow anyone else from joining.
	#Need to prettify.
#	print "Error! All four spots appear to be taken! Please wait until the next game."
#else:	
if True:
	# Need to set cookie with user ID, which is checked above. Should we have an external cgi page to
	# do resource management or do it all in this page?
	#
	#The below HTML is just an example page. It only works in portrait mode on my S3,
	#and I don't know how it would look on, say, a One X or an iPhone. Additionally,
	#it doesn't do any setup (get user ID) and none of the buttons work yet.
	#
	#I'm working on it.

	print """<!DOCTYPE HTML>
	<html>
		<head>
			<!-- Required for mobile devices -->
			<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no"/>
			<!-- Not really a good practice, but this basically just needs to work in demo. If anyone has any better ideas, PLEASE IMPLEMENT THEM. -->
			<!-- Should support up to 720p phones, which works for the iPhone 4s, Galaxy S3, and Galaxy Nexus we'll be testing with. -->
			<!--<link rel="stylesheet" href="styles/catronMobilePortrait.css" type="text/css" media="only screen and (max-device-width: 720px) and (orientation: portrait)/>	
			<link rel="stylesheet" href="styles/catronMobileLandscape.css" type="text/css" media="only screen and (max-device-width: 1280px) and (orientation: landscape)/>
			<link rel="stylesheet" href="styles/catronNormal.css" type="text/css" media="only screen and (min-device-width: 721px)/>-->
			<style type="text/css">
				@import url("styles/catronNormal.css");
				@media screen and (max-device-width: 720px) and (orientation:portrait){
					@import url("styles/catronMobilePortrait.css");
				}
				@media screen and (max-device-width: 1280px) and (orientation:landscape){
					@import url("styles/catronMobileLandscape.css");
				}
			</style>
			<!--<link rel="stylesheet" href="styles/catronMobilePortrait.css" type="text/css" />-->
	
		</head>
		<body>
			<div id="container">
				<div id="head">
					<h2>Player ID</h2>
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
						End Turn
					</div>
				</div>
			</div>
		</body>
	</html>"""
