<body class="wait">
	<script>setInterval("refreshContent(\"readyState\", 0)", 5000)</script>
	<div id="container">
		<div id="head">
			<h2>Waiting for players</h2>
			<img src="images/settings.png" class="settingsImg" />
		</div>
		<div id="body">
			Waiting for players! Currently have <span id="playersReady">{{numPlayers}}</span> players ready.<br />
			<span id="readyLinks">
%if joined == False:
			<a href="javascript:setReady();" class="readyLink">I'm ready!</a>
%else:
%if numPlayers <= 2:
			<span class="waitingLink">Waiting...</span><a href="javascript:unsetReady();" class="notReadyLink">I'm not ready!</a>
%else:
			<a href="/?start=true" class="halfReadyLink">Start game!</a><a href="javascript:unsetReady();" class="notReadyLink">I'm not ready!</a>
%end
%end
			</span>
		</div>
	</div>
</body>
