<span id="cardContent">
%if winner != False:
<h2>Game over!</h2>
<p>Congratulations to {{winner}}, as they have won!</p>
<a href="javascript:settings('restartGame');" class="bottom half left">New Game!</a>
<a href="javascript:settings('shutdown');" class="bottom half right">Shutdown.</a>
%else:
<h2>Game over!</h2>
<p>The game has been ended prematurely.</p>
<a href="javascript:settings('restartGame');" class="bottom half left">New Game!</a>
<a href="javascript:settings('shutdown');" class="bottom half right">Shutdown.</a>
%end
</span>
