%if !defined(newTrade):
%newTrade = False
%end
%if !defined(invalidTrade):
%invalidTrade = False
%end
%if !defined(players):
%players = {"-1":{"playerName":"error"}}
%end
%if !defined(cannotTrade):
%cannotTrade = False
%end
%if !defined(confirm):
%confirm = False
%end
%if !defined(giveStuff):
%giveStuff = "null"
%end
%if !defined(getStuff):
%getStuff = "null"
%end
%if !defined(denied):
%denied = False
%end
%if !defined(success):
%success = False
%end
<form onsubmit="return submitForm()" class="trade">
%if newTrade == True:
	<h2 style="margin-bottom: 15px">Trade</h2>
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
      <input name="giveClay" type="text" pattern="[0-9]" class="countValue" value="0"  onfocus="if(this.value == '0') { this.value = ''; }" onblur="if(this.value == '') {this.value = '0';}"/>
      <input name="giveOre" type="text" pattern="[0-9]" class="countValue" value="0"  onfocus="if(this.value == '0') { this.value = ''; }" onblur="if(this.value == '') {this.value = '0';}"/>
      <input name="giveSheep" type="text" pattern="[0-9]" class="countValue" value="0"  onfocus="if(this.value == '0') { this.value = ''; }" onblur="if(this.value == '') {this.value = '0';}"/>
      <input name="giveWheat" type="text" pattern="[0-9]" class="countValue" value="0"  onfocus="if(this.value == '0') { this.value = ''; }" onblur="if(this.value == '') {this.value = '0';}"/>
      <input name="giveWood" type="text" pattern="[0-9]" class="countValue" value="0"  onfocus="if(this.value == '0') { this.value = ''; }" onblur="if(this.value == '') {this.value = '0';}"/>
    </div>
    <div class="countColumn">
      <h3 class="countHeader">Get</h3>
      <input name="getClay" type="text" pattern="[0-9]" class="countValue" value="0"  onfocus="if(this.value == '0') { this.value = ''; }" onblur="if(this.value == '') {this.value = '0';}"/>
      <input name="getOre" type="text" pattern="[0-9]" class="countValue" value="0"  onfocus="if(this.value == '0') { this.value = ''; }" onblur="if(this.value == '') {this.value = '0';}"/>
      <input name="getSheep" type="text" pattern="[0-9]" class="countValue" value="0"  onfocus="if(this.value == '0') { this.value = ''; }" onblur="if(this.value == '') {this.value = '0';}"/>
      <input name="getWheat" type="text" pattern="[0-9]" class="countValue" value="0"  onfocus="if(this.value == '0') { this.value = ''; }" onblur="if(this.value == '') {this.value = '0';}"/>
      <input name="getWood" type="text" pattern="[0-9]" class="countValue" value="0"  onfocus="if(this.value == '0') { this.value = ''; }" onblur="if(this.value == '') {this.value = '0';}"/>
    </div>
  </div>
  <h3>Player to trade with: </h3>
	  <select name="playerid" class="playerSelect">
%for playerid in players:
  	  <option value="{{playerid}}">{{players[playerid]["playerName"]}}</option>
%end
    </select>
<a href="javascript:closeModal();" class="bottom half left" name="noDeal">No Deal!</a>
<input type="submit" value="Deal!" class="bottom half right" name="deal" />
%elif invalidTrade == True:
	<h2>Trade Error</h2>
		<p>You don't have enough resources to trade or you have selected an invalid option.</p>
		<a href="javascript:closeModal();" class="bottom left" name="gotit">Got it!</a>
%elif cannotTrade == True:
	<h2>Trade Error</h2>
		<p>You don't have enough resources to trade.
		<a href="javascript:denyTrade();" class="bottom left">Got it!</a>
%elif confirm == True:
	<h2>Confirm Trade</h2>
		<p>Would you like to trade {{getStuff}} for {{giveStuff}}?</p>
		<a href="javascript:denyTrade();" class="bottom half left">No I don't!</a>
		<a href="javascript:acceptTrade();" class="bottom half right">Yes I do!</a>
%elif denied == True:
	<h2>Trade Denied</h2>
		<p>Your trade has been denied from the player you were trading with.</p>
		<a href="javascript:closeModal();" class="bottom left">Got it!</a>
%elif success == True:
	<h2>Trade Successful</h2>
		<p>Your trade has been accepted and has taken place.</p>
		<a href="javascript:closeModal();" class="bottom left">Got it!</a>
%else:
	<h2>Error</h2>
		<p>There was an error with the trade form. Please try again.</p>
	<a href="javascript:closeModal();" class="bottom left" name="gotit">Got it.</a>
%end
</form>

