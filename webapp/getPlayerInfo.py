#!/usr/bin/python3

#Just a quick script to give everyone resources.
import json, sys

with open("./gameStatus.json", 'r') as f:
	gameStatus = json.load(f)
print(gameStatus["playerInfo"][sys.argv[1]])
