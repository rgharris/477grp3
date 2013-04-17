<h2>Game Status</h2>
<ul class="gameStatus">
%for info in playerInfo.values():
<li>{{info}}</li>
<!--
%#score = str(player['points'])
	<li><b>player["playerName"]</b> &nbsp; &nbsp; score points\\
%#if len(player['awards']) > 0:
%#if len(playerInfo['awards']) == 1:
%#if playerInfo['awards'][0] == "road":
<br /><i>Has the longest road</i>
%#else:
<br /><i>Has the largest army</i>
%#end
%#else:
<br /><i>Has the longest road and the largest army</i>
%#end
%#end
</li>
-->
%end
</ul>
<input type="submit" value="Got it!" class="bottom left" />
