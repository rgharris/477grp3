<form onsubmit="return submitName()">
	<h2>Please enter your username.</h2>
	<div>
		<input type="text" id="user" name="user" value="{{name}}" onfocus="var nameValue=this.value; this.value=''" />
	</div>
	<input type="submit" value="Got it!" class="bottom left" />
</form>
