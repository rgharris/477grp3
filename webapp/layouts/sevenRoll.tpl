%if complete==False:
<form onsubmit="return submitForm()" class="trade" name="discard">
	<span id="boxContent">
	<h2 style="margin-bottom: 15px">Discard half your hand!</h2>
%if error==True:
	<p>Error...you must discard {{numDiscard}} resources that you own.</p>
%end
	<p>A seven was rolled, so you must discard {{numDiscard}} resources.</p>
  <div style="width: 100%; /*height: 155px*/">
    <div>  
			<div class="resourceColumn">
				<h3 class="resourceHeader">Resource</h3>
			</div>
			<div class="countColumn">
				<h3 class="countHeader">Give</h3>
			</div>
		</div>
		<div>  
			<div class="resourceColumn">
				<div class="resourceName">Clay</div>
			</div>
			<div class="countColumn">
				<input name="giveClay" type="number" class="countValue" value="0"  onfocus="if(this.value == '0') { this.value = ''; }" onblur="if(this.value == '') {this.value = '0';}"/>
			</div>
		</div>
		<div>  
			<div class="resourceColumn">
				<div class="resourceName">Ore</div>
			</div>
			<div class="countColumn">
				<input name="giveOre" type="number" class="countValue" value="0"  onfocus="if(this.value == '0') { this.value = ''; }" onblur="if(this.value == '') {this.value = '0';}"/>
			</div>
		</div>
		<div>  
			<div class="resourceColumn">
				<div class="resourceName">Sheep</div>
			</div>
			<div class="countColumn">
				<input name="giveSheep" type="number" class="countValue" value="0"  onfocus="if(this.value == '0') { this.value = ''; }" onblur="if(this.value == '') {this.value = '0';}"/>
			</div>
		</div>
		<div>  
			<div class="resourceColumn">
				<div class="resourceName">Wheat</div>
			</div>
			<div class="countColumn">
				<input name="giveWheat" type="number" class="countValue" value="0"  onfocus="if(this.value == '0') { this.value = ''; }" onblur="if(this.value == '') {this.value = '0';}"/>
			</div>
		</div>
		<div>  
			<div class="resourceColumn">
				<div class="resourceName">Wood</div>
			</div>
			<div class="countColumn">
				<input name="giveWood" type="number" class="countValue" value="0"  onfocus="if(this.value == '0') { this.value = ''; }" onblur="if(this.value == '') {this.value = '0';}"/>
			</div>
		</div>
	</div>
<input type="submit" value="Discard these." class="bottom left" name="deal" />
</span>
</form>
%elif complete == True:
	<h2>Discard Complete!</h2>
		<p class="generic">Your resources have been returned to the bank.</p>
		<a href="javascript:closeModal();" class="bottom left">Got it.</a>
%end

