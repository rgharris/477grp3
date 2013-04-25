%#These need to be the opposite of what the variable returns.
%if not defined('quickConfirm'):
%quickConfirm = 'On'
%elif quickConfirm == 0:
%quickConfirm = 'On'
%else:
%quickConfirm = 'Off'
%end
%if not defined('confirmShutdown'):
%confirmShutdown = False
%end
%if not defined('endGame'):
%endGame = False
%end
%if not defined('restartGame'):
%restartGame = False
%end
%if confirmShutdown == True:
	<h2>Shutdown</h2>
	<p class="generic">Are you sure you want to shutdown?</p>
	<a href="javascript:settings('reallyShutdown')" class="bottom half left">Yes, Shutdown.</a>
	<a href="javascript:settings('cancel');" class="bottom half right">No, wait, don't!</a>
%elif endGame == True:
	<h2>End Game</h2>
	<p class="generic">Are you sure you want to end this game?</p>
	<a href="javascript:settings('reallyEndGame')" class="bottom half left">Yes!</a>
	<a href="javascript:settings('cancel');" class="bottom half right">No, wait, don't!</a>
%elif restartGame == True:
	<h2>Restart Game</h2>
	<p class="generic">Are you sure you want to end this game and start a new one?</p>
	<a href="javascript:settings('reallyRestartGame')" class="bottom half left">Yes!</a>
	<a href="javascript:settings('cancel');" class="bottom half right">No, wait, don't!</a>
%else:
<span id="cardContent">
	<h2>Settings</h2>
	<p class="resourceBox devCardSpacing">&nbsp;</p>
	<a href="javascript:settings('quickConfirm')" class="bottom moreTop left">Turn Quick Confirm {{quickConfirm}}</a>
	<a href="javascript:settings('restartGame')" class="bottom half top left">Restart Game</a>
	<a href="javascript:settings('endGame')" class="bottom half top right">End Game</a>
	<a href="javascript:settings('shutdown')" class="bottom half bot left">Shutdown</a>
	<a href="javascript:closeModal();" class="bottom half bot right">Close Settings</a>
</span>
%end
