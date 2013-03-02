#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# This is the modal dialog that asks the user
# for their username.
#import debugging
import cgitb
#Everything else.
import os, sys, cgi, json

PLAYER_FILE="players/"

for fn in os.listdir(PLAYER_FILE):
	if os.path.isfile(fn):
		print fn

output = """Content-type: text/html;charset=utf-8

				<h2>Game Status</h2>
            <ul class="gameStatus">
               <li><b>Player 1</b> &nbsp; &nbsp; 2 points</li>
               <li><b>Player 2</b> &nbsp; &nbsp; 4 points<br />
               <i>Has the longest road</i></li>
               <li><b>Player 3</b> &nbsp; &nbsp; 2 points<br />
               <i>Has the largest army</i></li>
               <li><b>Player 4</b> &nbsp; &nbsp; 3 points</li>
            </ul>
            <a href="#x" class="bottom">Got it!</a>
			"""

print output;
