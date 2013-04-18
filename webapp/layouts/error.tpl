<body class="error">
	<div id="container">
		<div id="head">
			<h2>Error!</h2>
		</div>
	</div>
	<div id="body">
%if gameStarted == True:
	<p>This game is currently in progress. Enjoy watching this game, and try to join the next one!</p>
%elif maxPlayers == True:
	<p>This game has reached the maximum number of players. Enjoy watching this game, and try to join the next one!</p>
%else
	<p>An unknown error has occurred. Try refreshing, and if that doesn't work, whoops.</p>
%end
	</div>
</body>
