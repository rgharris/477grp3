#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# This is the dialog that deals with trading.
# It should deal with both traders.

from os import environ
from cgi import parse_qs
from json import dump
import quick2wire.i2c as i2c

PLAYER_FILE = "../players/"
GAME_STATE_FILE = "../chkRefresh/gamestate.json"
RESOURCE_FILE = "../chkRefresh/resources.json"
DICE_FILE = "../chkRefresh/dice"
MICROADDR = 0x50
RESOURCEREG = 10
DIEREG = 9
PIREG = 0
DICEFLAG = 3

query = environ["QUERY_STRING"]

pairs = parse_qs(query)

print("Content-type: text/html;charset=utf-8\n\n")

if len(pairs) == 0:
	output = """<h2>Error!</h2>\n<p>This should never happen.</p>"""

else:
	playerID = int(pairs['player'][0])
	with i2c.I2CMaster() as bus:
		diceRoll = bus.transaction(i2c.writing_bytes(MICROADDR, DIEREG), i2c.reading(MICROADDR, 1))
		bus.transaction(i2c.writing_bytes(MICROADDR, PIREG, DICEFLAG))
		MCUresources = bus.transaction(i2c.writing_bytes(MICROADDR, RESOURCEREG), i2c.reading(MICROADDR, 20))
	resources = []
	for i in range(0,20):
		resources.append(MCUresources[0][i])
	with open(DICE_FILE, 'w') as f:
		f.write(str(diceRoll[0][0]))
		f.close()
	if diceRoll[0][0] != 7:
		resourceDict = {}
		for i in range(0,3):
			resourceDict[str(i)] = {'ore': resources[(i*5)], 'wheat': resources[(i*5)+1], 'sheep': resources[(i*5)+2], 'clay': resources[(i*5)+3], 'wood':resources[(i*5)+4]}
		with open(RESOURCE_FILE, 'w') as f:
			dump(resourceDict, f, ensure_ascii=False)
			f.close()
		for i in range(0,3):
			if (i != playerID):
				with open("../chkRefresh/" + str(i), 'w') as f:
					f.write('7')
					f.close()      
	else:
		for i in range(0,3):
			with open("../chkRefresh/" + str(i), 'w') as f:
				f.write('7')
				f.close()
		with i2c.I2CMaster() as bus:
			bus.transaction(i2c.writing_bytes(MICROADDR, PIREG, 6))

	output = "complete"

print(output)
