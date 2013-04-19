%if not defined('newTrade'):
%newTrade = False
%end
%if not defined('invalidTrade'):
%invalidTrade = False
%end
%if not defined('players'):
%players = {"-1":{"playerName":"error"}}
%end
%if not defined('numPlayers'):
%numPlayers = 0
%end
%if not defined('cannotTrade'):
%cannotTrade = False
%end
%if not defined('confirm'):
%confirm = False
%end
%if not defined('giveStuff'):
%giveStuff = "null"
%end
%if not defined('getStuff'):
%getStuff = "null"
%end
%if not defined('denied'):
%denied = False
%end
%if not defined('success'):
%success = False
%end
%if newTrade == True:
<form onsubmit="return submitForm()" class="trade" name="trade">
	<h2 style="margin-bottom: 15px">Trade</h2>
	<span id="tradeContent">
  <div style="width: 100%; height: 155px">
  	<div class="resourceColumn">
    	<h3 class="resourceHeader">Resource</h3>  
      <div class="resourceName">Clay</div>
      <div class="resourceName">Ore</div>
      <div class="resourceName">Sheep</div>
      <div class="resourceName">Wheat</div>
      <div class="resourceName">Wood</div>
   </div>
   <div class="countColumn">
      <h3 class="countHeader">Give</h3>
      <input name="giveClay" type="number" class="countValue" value="0"  onfocus="if(this.value == '0') { this.value = ''; }" onblur="if(this.value == '') {this.value = '0';}"/>
      <input name="giveOre" type="number" class="countValue" value="0"  onfocus="if(this.value == '0') { this.value = ''; }" onblur="if(this.value == '') {this.value = '0';}"/>
      <input name="giveSheep" type="number" class="countValue" value="0"  onfocus="if(this.value == '0') { this.value = ''; }" onblur="if(this.value == '') {this.value = '0';}"/>
      <input name="giveWheat" type="number" class="countValue" value="0"  onfocus="if(this.value == '0') { this.value = ''; }" onblur="if(this.value == '') {this.value = '0';}"/>
      <input name="giveWood" type="number" class="countValue" value="0"  onfocus="if(this.value == '0') { this.value = ''; }" onblur="if(this.value == '') {this.value = '0';}"/>
    </div>
    <div class="countColumn">
      <h3 class="countHeader">Get</h3>
      <input name="getClay" type="number" class="countValue" value="0"  onfocus="if(this.value == '0') { this.value = ''; }" onblur="if(this.value == '') {this.value = '0';}"/>
      <input name="getOre" type="number" class="countValue" value="0"  onfocus="if(this.value == '0') { this.value = ''; }" onblur="if(this.value == '') {this.value = '0';}"/>
      <input name="getSheep" type="number" class="countValue" value="0"  onfocus="if(this.value == '0') { this.value = ''; }" onblur="if(this.value == '') {this.value = '0';}"/>
      <input name="getWheat" type="number" class="countValue" value="0"  onfocus="if(this.value == '0') { this.value = ''; }" onblur="if(this.value == '') {this.value = '0';}"/>
      <input name="getWood" type="number" class="countValue" value="0"  onfocus="if(this.value == '0') { this.value = ''; }" onblur="if(this.value == '') {this.value = '0';}"/>
    </div>
  </div>
  <h3>Player to trade with: </h3>
	  <select name="playerid" class="playerSelect">
%for playerid in players:
%if int(playerid)+1 <= numPlayers:
  	  <option value="{{playerid}}">{{players[playerid]["playerName"]}}</option>
%end
%end
    </select>
<a href="javascript:closeModal();" class="bottom half left" name="noDeal">No Deal!</a>
<input type="submit" value="Deal!" class="bottom half right" name="deal" />
</span>
</form>
%elif invalidTrade == True:
	<h2>Trade Error</h2>
		<p class="generic">You don't have enough resources to trade or you have selected an invalid option.</p>
		<a href="javascript:closeModal();" class="bottom left" name="gotit">Got it!</a>
%elif cannotTrade == True:
	<h2>Trade Error</h2>
		<p class="generic">You don't have enough resources to trade.</p>
		<a href="javascript:denyTrade();" class="bottom left">Got it!</a>
%elif confirm == True:
	<h2>Confirm Trade</h2>
		<p class="generic">Would you like to trade {{getStuff}} for {{giveStuff}}?</p>
		<a href="javascript:denyTrade();" class="bottom half left">No I don't!</a>
		<a href="javascript:acceptTrade();" class="bottom half right">Yes I do!</a>
%elif denied == True:
	<h2>Trade Denied</h2>
		<p class="generic">Your trade has been denied from the player you were trading with.</p>
		<a href="javascript:closeModal();" class="bottom left">Got it!</a>
%elif success == True:
	<h2>Trade Successful</h2>
		<p class="generic">Your trade has been accepted and has taken place.</p>
		<a href="javascript:closeModal();" class="bottom left">Got it!</a>
%else:
	<h2>Error</h2>
		<p class="generic">There was an error with the trade form. Please try again.</p>
	<a href="javascript:closeModal();" class="bottom left" name="gotit">Got it.</a>
%end

