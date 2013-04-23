#!/usr/bin/python3

#Just a quick script to give everyone resources.
import json

with open("./gameStatus.json", 'r') as f:
	gameStatus = json.load(f)
for player in gameStatus['playerInfo']:
	for resource in gameStatus['playerInfo'][player]['resources']:
		gameStatus['playerInfo'][player]['resources'][resource] = 100
with open("./gameStatus.json", 'w') as f:
	json.dump(gameStatus, f, ensure_ascii=False)
