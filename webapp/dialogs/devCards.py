#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# This is the modal dialog that asks the user
# for their username.
#import debugging
#import cgitb
#Everything else.
from os import environ
from cgi import parse_qs
from json import load

query = environ["QUERY_STRING"]
PLAYER_FILE = "../players/"
pairs = parse_qs(query)

print("Content-type: text/html;charset=utf-8\n\n")


if len(pairs) == 0:
	output = """<form method="post" action="index.py">
      	      <h2>Error!</h2>
		<p>This should never happen.</p>
				"""
else:
	playerFile = open(PLAYER_FILE + str(pairs["player"][0]) + ".json")
	playerInfo = load(playerFile)
	playerFile.close()
	if "success" in pairs:
		if pairs['success'][0] == "plenty":
			output = """<h2>Success!</h2>
							<p>You have recieved your two additional resources.</p>
							<a href=\"#x\" class=\"bottom left\">Got it!</a>"""
		elif pairs['success'][0] == "monopoly":
			output = "<h2>Success!</h2><p>You have recieved " + pairs['num'][0] + " " + pairs['resource'][0] + "!</p><a href=\"#x\" class=\"bottom left\">Got it!</a>"
		elif pairs['success'][0] == "road":
			pass
		elif pairs['success'][0] == "knights":
			pass
	elif "confirm" in pairs:
		if pairs['confirm'][0] == "plenty":
			output  = """<form method="post" action="index.py">
							<h2>Year of Plenty</h2>
							<p>Select your two free resources!</p>
							<select name="resource1" class="resourceSelect">
								<option value="none">Select a resource...</option>
								<option value="ore">Ore</option>
								<option value="wheat">Wheat</option>
								<option value="sheep">Sheep</option>
								<option value="clay">Clay</option>
								<option value="wood">Wood</option>
							</select>
							<select name="resource2" class="resourceSelect">
								<option value="none">Select a resource...</option>
								<option value="ore">Ore</option>
								<option value="wheat">Wheat</option>
								<option value="sheep">Sheep</option>
								<option value="clay">Clay</option>
								<option value="wood">Wood</option>
							</select>
							<input type="submit" value="Got it!" class="bottom left" name="plentySelected">
						</form>"""

		elif pairs['confirm'][0] == "monopoly":
			output = """<form method="post" action="index.py">
							<h2>Monopoly</h2>
							<p>Select the resource you would like to have a monopoly on.</p>
							<select name="resource" class="resourceSelect">
								<option value="none">Select a resource...</option>
								<option value="ore">Ore</option>
								<option value="wheat">Wheat</option>
								<option value="sheep">Sheep</option>
								<option value="clay">Clay</option>
								<option value="wood">Wood</option>
							</select>
							<input type="submit" value="Got it!" class="bottom left" name="monopolySelected">
						"""

		elif pairs['confirm'][0] == "road":
			pass
		elif pairs['confirm'][0] == "knights":
			pass

	elif "card" in pairs:
		playedDevCard = pairs['playedDev'][0]
		if pairs['card'][0] == "plenty":
			if playerInfo['cards']['plenty'] > 0 and int(playedDevCard) == 0:
				output = """<form method="post" action="index.py">
						<h2>Year of Plenty Card</h2>
						<p>This card allows you to take two of any one resource you have a settlement on. You currently have {0} Year of Plenty cards available. Would you like to play one?</p>            
				<input type="submit" value="Yes I do!" class="bottom half left" name="playPlenty"/>
            <input type="submit" value="Not yet!" class="bottom half right" name="noDeal"/>
					"""
			elif int(playedDevCard) == 1:
				output = "<h2>Year of Plenty Card</h2>\n<p>This card allows you to take two of any one resource you have a settlement on. You currently have {0} Year of Plenty cards available, but cannot play another development card this turn.</p><a href=\"#x\" class=\"bottom left\">Got it!</a>"
			else:
				output = "<h2>Year of Plenty Card</h2>\n<p>This card allows you to take two of any one resource you have a settlement on. You currently have no Year of Plenty cards available.</p><a href=\"#x\" class=\"bottom left\">Got it!</a>"
		elif pairs['card'][0] == "monopoly":
			if playerInfo['cards']['monopoly'] > 0 and int(playedDevCard) == 0:
				output = """<form method="post" action="index.py">
						<h2>Monopoly Card</h2>
						<p>This card allows you to take a monopoly on a single resource, forcing all players currently holding that resource to hand it over to you. You currently have {1} Monopoly cards available. Would you like to play one?</p>
				<input type="submit" value="Yes I do!" class="bottom half left" name="playMonopoly"/>
            <input type="submit" value="Not yet!" class="bottom half right" name="noDeal"/>
					"""
			elif int(playedDevCard) == 1:
				output = "<h2>Monopoly card</h2>\n<p>This card allows you to take a monopoly on a single resource, forcing all players currently holding that resource to hand it over to you. You currently have {1} Monopoly cards available, but cannot play another development card this turn.</p><a href=\"#x\" class=\"bottom left\">Got it!</a>"
			else:
				output = "<h2>Monopoly card</h2>\n<p>This card allows you to take a monopoly on a single resource, forcing all players currently holding that resource to hand it over to you. You currently have no Monopoly cards available.</p><a href=\"#x\" class=\"bottom left\">Got it!</a>"
		elif pairs['card'][0] == "road":
			if playerInfo['cards']['road'] > 0 and int(playedDevCard) == 0:
				output = """<form method="post" action="index.py">
						<h2>Road Building Card</h2>
						<p>This card allows you to place two roads at no additional cost. You currently have {2} Road Building cards available. Would you like to play one?</p>
				<input type="submit" value="Yes I do!" class="bottom half left" name="playRoadDev"/>
            <input type="submit" value="Not yet!" class="bottom half right" name="noDeal"/>
					"""
			elif int(playedDevCard) == 1:
				output = "<h2>Road Building Card</h2>\n<p>This card allows you to place two roads at no additional cost. You have {2} Road Building cards available, but cannot play another development card this turn.</p><a href=\"#x\" class=\"bottom left\">Got it!</a>"
			else:
				output = "<h2>Road Building Card</h2>\n<p>This card allows you to place two roads at no additional cost. You have no road building cards available.</p><a href=\"#x\" class=\"bottom left\">Got it!</a>"
		elif pairs['card'][0] == "knights":
			if playerInfo['cards']['knights'] > 0 and int(playedDevCard) == 0:
				output = """<form method="post" action="index.py">	
						<h2>Knight card</h2>
						<p>This card allows you to move the thief and steal a single, random resource from a given player. You have played {5} knight cards, and currently have {3} unplayed Knight cards available. Would you like to play one?</p>
				<input type="submit" value="Yes I do!" class="bottom half left" name="playKnights"/>
            <input type="submit" value="Not yet!" class="bottom half right" name="noDeal"/>
					"""
			elif int(playedDevCard) == 1:
				output = "<h2>Knight card</h2>\n<p>This card allows you to move the thief and steal a single, random resource from a given player. You have played {5} knight cards, and currently have {3} unplayed Knight cards available, but you cannot play another development card this turn.</p><a href=\"#x\" class=\"bottom left\">Got it!</a>"
			else:
				output = "<h2>Knight card</h2>\n<p>This card allows you to move the thief and steal a single, random resource from a given player. You have played {5} knight cards, and have none available.</p><a href=\"#x\" class=\"bottom left\">Got it!</a>"
		elif pairs['card'][0] == "victory":
			output = """<h2>Victory card</h2>
					<p>This card gets you an additional victory point, hidden from the other players. It cannot be played, but counts toward your total score. Your opponents will only see your score without these cards. You currently have {4} victory cards.</p><a href=\"#x\" class=\"bottom left\">Got it!</a>
				"""
	elif "against" in pairs:
		if pairs['against'][0] == "monopoly":
			output = """<h2>Monopoly!</h2>
						<p>The current player has just taken a monopoly on a resource!</p><a href=\"#x\" class=\"bottom left\">Got it!</a>"""
	else:
		#In retrospect, these should just be links, not buttons. Ah, well, I'm not going to change it now. Maybe later.
		output = """<form method="post" action="index.py" class="cards">
				<h2>Development Cards</h2>
				<p>You have the following available.</p>
				<input type="submit" value="Victory: {4}" class="bottom moreTop left" name="victory" />
				<input type="submit" value="Monopoly: {1}" class="bottom half top left" name="monopoly" />
				<input type="submit" value="Road Building: {2}" class="bottom half top right" name="roadDev" />
				<input type="submit" value="Knight: {3}" class="bottom half bot left" name="knights" />
				<input type="submit" value="Year of Plenty: {0}" class="bottom half bot right" name="plenty" />
			    </form>"""


output = output.format(playerInfo['cards']['plenty'], playerInfo['cards']['monopoly'], playerInfo['cards']['road'], playerInfo['cards']['knights'], playerInfo['cards']['victory'] + playerInfo['onHold']['victory'], playerInfo['playedKnights'])
print(output)
