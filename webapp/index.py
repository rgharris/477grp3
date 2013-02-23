#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Enables debugging
import cgitb
cgitb.enable()

print "Content-Type: text/html;charset=utf-8"
print
print """<!DOCTYPE HTML>
<html>
	<head>
		<!-- Required for mobile devices -->
		<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1"/>
		<link rel="stylesheet" href="styles/catron.css" type="text/css" />
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
