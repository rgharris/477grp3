<h2>Game Status</h2>
<ul class="gameStatus">
%for player,info in playerInfo.items():
%score = str(info['points'])
	<li><b>{{info["playerName"]}}</b> &nbsp; &nbsp; {{score}} points\\
%if player == longestRoad:
<br /><i>Has the longest road\\
%if player == largestArmy:
and the largest army</i>\\
%else:
</i>\\
%end
%elif player == largestArmy:
<br /><i>Has the largest army</i>\\
%end
</li>
%end
</ul>
<input type="submit" value="Got it!" class="bottom left" />