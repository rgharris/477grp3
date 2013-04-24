<!DOCTYPE HTML>
   <html>
      <head>
         <!-- Required for mobile devices -->
         <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no"/>
         <!-- Not really a good practice, but this basically just needs to work in demo. If anyone has any better ideas, PLEASE IMPLEMENT THEM. -->
         <link rel="stylesheet" href="styles/style.css" type="text/css" />
         <script src="js/functions.js"></script> 
      </head>
		<body class="wait">
			<script>setInterval("refreshContent(\"readyState\", 0)", 1000)</script>
			<div id="container">
				<div id="head">
					<h2>Waiting for players</h2>
					<!--img src="images/settings.png" class="settingsImg" /--->
				</div>
				<div id="body">
%numPlayersDisplay = str(numPlayers)
					Waiting for players! Currently have <span id="playersReady">{{numPlayersDisplay}}</span> players ready.<br />
					<span id="readyLinks">
%if joined == False:
					<a href="javascript:setReady();" class="readyLink">I'm ready!</a>
%else:
%if numPlayers <= 2:
					<span class="waitLink">Waiting...</span><a href="javascript:unsetReady();" class="notReadyLink">I'm not ready!</a>
%else:
					<a href="javascript:startGame();" class="halfReadyLink">Start game!</a><a href="javascript:unsetReady();" class="notReadyLink">I'm not ready!</a>
%end
%end
					</span>
				</div>
			</div>
		</body>
	</html>
