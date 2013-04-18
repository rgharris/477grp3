<!DOCTYPE HTML>
   <html>
      <head>
         <!-- Required for mobile devices -->
         <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no"/>
         <!-- Not really a good practice, but this basically just needs to work in demo. If anyone has any better ideas, PLEASE IMPLEMENT THEM. -->
         <link rel="stylesheet" href="styles/style.css" type="text/css" />
         <script src="js/functions.js"></script> 
      </head>
		<body class="error">
			<div id="container">
				<div id="head">
					<h2>Error!</h2>
				</div>
			</div>
			<div id="body">
%if not defined('gameStarted'):
%gameStarted = False
%end
%if not defined('maxPlayers'):
%maxPlayers = False
%end
%if gameStarted == True:
			<p>This game is currently in progress. Enjoy watching this game, and try to join the next one!</p>
%elif maxPlayers == True:
			<p>This game has reached the maximum number of players. Enjoy watching this game, and try to join the next one!</p>
%else:
			<p>An unknown error has occurred. Try refreshing, and if that doesn't work, whoops.</p>
%end
			</div>
		</body>
	</html>
