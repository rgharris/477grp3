#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# This is the dialog that deals with trading.
# It should deal with both traders.

from os import environ
from cgi import parse_qs
from json import load

PLAYER_FILE = "../players/"
GAME_STATE_FILE = "../chkRefresh/gamestate.json"

query = environ["QUERY_STRING"]

pairs = parse_qs(query)

print("Content-type: text/html;charset=utf-8\n\n")

if len(pairs) == 0:
	output = """<h2>Error!</h2>\n<p>This should never happen.</p>"""

else:
	playerID = pairs['player'][0]
	playerFile = open(PLAYER_FILE + playerID + ".json")
	playerInfo = load(playerFile)
	playerFile.close()
	stateFile = open(GAME_STATE_FILE)
	stateInfo = load(stateFile)
	stateFile.close()
	if playerInfo['currentTurn'] == 1:
		if playerInfo['initialPlacements']['settlement'] == 0:
			output = """<h2>Place Settlement.</h2>
							<p>Place your settlement now.</p>
						"""
		if playerInfo['initialPlacements']['settlement'] == 1 and playerInfo['initialPlacements']['road'] == 0:
			output = """<h2>Place Road.</h2>
							<p>Place your road now.</p>
						"""
		if playerInfo['initialPlacements']['settlement'] == 1 and playerInfo['initialPlacements']['road'] == 1:
			output = """<h2>Place Settlement.</h2>
							<p>Place your second settlement now.</p>
						"""
		if playerInfo['initialPlacements']['settlement'] == 2 and playerInfo['initialPlacements']['road'] == 1:
			output = """<h2>Place Road.</h2>
							<p>Place your second road now.</p>
						"""
	if playerInfo['currentTurn'] == 0:
		output = """<h2>Waiting for turn</h2>
						<p>Waiting for your turn to place a settlement.</p>"""
print(output)
