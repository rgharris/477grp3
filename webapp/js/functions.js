/*this function runs whenever a form is submitted.*/
function submitForm()
{
	var xmlhttp, values;
	xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange = function()
	{
		console.log(xmlhttp.responseText);
		/*If the form is not one of these, then close the modal box it was in.*/
		if(document.forms[0].name != "trade" && document.forms[0].name != "yearofplenty" && document.forms[0].name != "monopoly" && document.forms[0].name != "knight" && document.forms[0].name != "discard")
		{
			closeModal();
		}
		//Otherwise if the form was one of these, then replace it's content with the response from
		//the server.
		else if(document.forms[0].name == "monopoly" || document.forms[0].name == "yearofplenty" || document.forms[0].name == "knight" || document.forms[0].name == "discard"){
				document.getElementById("boxContent").innerHTML = xmlhttp.responseText;
		}
	}
	//Package the values to be sent to the server appropriately.
	if(document.forms[0].name == "endTurn")
	{
		values = "0";
	}
	else if(document.forms[0].name == "trade")
	{
		var trade = {
			give: {
				ore: document.forms[0].giveOre.value,
				wheat: document.forms[0].giveWheat.value,
				sheep: document.forms[0].giveSheep.value,
				clay: document.forms[0].giveClay.value,
				wood: document.forms[0].giveWood.value
			},
			get: {
				ore: document.forms[0].getOre.value,
				wheat: document.forms[0].getWheat.value,
				sheep: document.forms[0].getSheep.value,
				clay: document.forms[0].getClay.value,
				wood: document.forms[0].getWood.value
			},
			to: document.forms[0].playerid[document.forms[0].playerid.selectedIndex].value
		};
		values = JSON.stringify(trade);
		document.getElementById('tradeContent').innerHTML = "<p>Please wait for a response from " + document.forms[0].playerid[document.forms[0].playerid.selectedIndex].text + ".</p>";
	}
	else if(document.forms[0].name == "discard")
	{
		var discard = { 
				ore: document.forms[0].giveOre.value,
				wheat: document.forms[0].giveWheat.value,
				sheep: document.forms[0].giveSheep.value,
				clay: document.forms[0].giveClay.value,
				wood: document.forms[0].giveWood.value
			};
		values = JSON.stringify(discard)
	}
	else if(document.forms[0].name == "yearofplenty")
	{
		var plenty = {
			resources: {
				resource1:document.forms[0].resource1[document.forms[0].resource1.selectedIndex].value,
				resource2:document.forms[0].resource2[document.forms[0].resource2.selectedIndex].value,
			}
		};
		values = JSON.stringify(plenty);
	}
	else if(document.forms[0].name == "monopoly")
	{
		values = document.forms[0].resource[document.forms[0].resource.selectedIndex].value;
	}
	else if(document.forms[0].name == "knight")
	{
		values = document.forms[0].stealFrom[document.forms[0].stealFrom.selectedIndex].value;
	}
	xmlhttp.open("GET","submitForm?id=" + document.forms[0].name + "&value=" + values,true);
	xmlhttp.send();
	return false
}
//Let the server know that we're ready.
function setReady()
{
	var xmlhttp;
	xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange = function()
	{
		console.log("setReady: " + xmlhttp.responseText);
		document.getElementById("playersReady").innerHTML = xmlhttp.responseText;
		document.getElementById("readyLinks").innerHTML="<span class=\"waitLink\">Waiting...</span><a href=\"javascript:unsetReady();\" class=\"notReadyLink\">I'm not ready!</a>";
	}
	xmlhttp.open("GET","ready?set=true", true);
	xmlhttp.send();

}
//Start the game!
function startGame()
{
	var xmlhttp;
	xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange = function()
	{
		console.log("startGame: " + xmlhttp.responseText);
	}
	xmlhttp.open("GET","ready?start=go", true);
	xmlhttp.send();

}
//Tell the server we lied and we aren't actually ready.
function unsetReady()
{
	var xmlhttp;
	xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange = function()
	{
		console.log("unset ready: " +  xmlhttp.responseText);
		document.getElementById("playersReady").innerHTML = xmlhttp.responseText;
		document.getElementById("readyLinks").innerHTML="<a href=\"javascript:setReady();\" class=\"readyLink\">I'm ready!</a>";
	}
	xmlhttp.open("GET","ready?set=false", true);
	xmlhttp.send();
}
//Run an i2c command on the server to the board.
function runi2c(todo)
{
        var xmlhttp;
        xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function()
        {
		console.log(xmlhttp.responseText);
        }
        xmlhttp.open("GET","i2c?todo=" + todo, true);
        xmlhttp.send();
}
//Submit a new username to the server. I don't know why this is seperate from submitForm.
function submitName()
{
	var xmlhttp;
	xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange = function()
	{
		console.log(xmlhttp.responseText);
		document.getElementById("playerName").innerHTML=xmlhttp.responseText;
		closeModal();
	}
	if (document.forms[0].user.value == "") {
		document.forms[0].user.value = nameValue;
	}
	xmlhttp.open("GET","submitForm?id=name&value=" + document.forms[0].user.value, true);
	xmlhttp.send();
	return false
}
//Open the modalBox with a specific input.
function openModal(id)
{
  refreshContent("ModalBox", id);
	console.log("refreshed content");
	var elem = document.getElementById("ModalBox");
	elem.style.visibility = "visible";
	elem.style.top = (window.pageYOffset + 25).toString()+ "px";
	elem = document.getElementById("modal");
	elem.style.visibility = "visible";
}
//Close the modalBox.
function closeModal()
{
	var elem = document.getElementById("ModalBox");
	elem.style.visibility = "hidden";
	elem = document.getElementById("modal");
	elem.style.visibility = "hidden";
}
//Purchase an item, accept it or deny it.
function purchase(action,type)
{
	var xmlhttp;
	xmlhttp = new XMLHttpRequest();
	document.getElementById("purchaseContent").innerHTML = "Please wait...";
	xmlhttp.onreadystatechange = function()
	{
		console.log(xmlhttp.responseText);
		if(action != "deny"){
			document.getElementById("purchaseContent").innerHTML = xmlhttp.responseText;
		}else{
			closeModal();
		}
	}
	var purchase = {
			action: action,
			type: type
		};
	var values = JSON.stringify(purchase);

	xmlhttp.open("GET","submitForm?id=purchase&value=" + values, true);
	xmlhttp.send();
}
//Play a development card.
function playCard(type,play)
{
	var xmlhttp;
	xmlhttp = new XMLHttpRequest();
	document.getElementById("cardContent").innerHTML = "Please wait...";
	xmlhttp.onreadystatechange = function()
	{
		console.log(xmlhttp.responseText);
		document.getElementById("cardContent").innerHTML = xmlhttp.responseText;
	}
	var devCard = {
			type: type,
			play: play
	};
	var values = JSON.stringify(devCard);
	xmlhttp.open("GET","submitForm?id=playDevCard&value=" + values, true);
	xmlhttp.send();

}
//Accept the trade offered by a player.
function acceptTrade()
{
	var xmlhttp;
	xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange = function()
	{
		console.log(xmlhttp.responseText);
		closeModal();
	}
	xmlhttp.open("GET","submitForm?id=trade&value=accept", true);
	xmlhttp.send();
}
//Deny the trade offered by a player.
function denyTrade()
{
	var xmlhttp;
	xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange = function()
	{
		console.log(xmlhttp.responseText);
		closeModal();
	}
	xmlhttp.open("GET","submitForm?id=trade&value=deny", true);
	xmlhttp.send();
}
//Tell the server that we've seen the dice roll.
function seenRoll()
{
	var xmlhttp;
	xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange = function()
	{
		console.log(xmlhttp.responseText);
		closeModal();
	}
	xmlhttp.open("GET","rollDice?seen=True", true);
	xmlhttp.send();
}

//Tell the server to roll the dice.
function rollDice()
{        
	var xmlhttp;
        xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function()
        {
                console.log(xmlhttp.responseText);
		openModal('rollBox');
        }
        xmlhttp.open("GET","rollDice", true);
        xmlhttp.send();
}
function settings(todo)
{
	var xmlhttp;
        xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function()
        {
                console.log(xmlhttp.responseText);
		if(todo != 'shutdown' && todo != 'reallyShutdown'){
			closeModal();
		}else{
			document.getElementById('cardContent').innerHTML=xmlhttp.responseText;
		}
        }
        xmlhttp.open("GET","settings?todo=" + todo, true);
        xmlhttp.send();
}


//Generic AJAX Loading
function loadXMLDoc(div,loc)
{
	var xmlhttp;
	xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange=function()
	{
		if(xmlhttp.readyState == 4 && xmlhttp.status==200)
		{
			document.getElementById(div).innerHTML=xmlhttp.responseText;
		}
	}
	xmlhttp.open("GET",loc,true);
	xmlhttp.send();
}

//This is global so it stays persistent even after the function has finished.
var lastFlag = "-1";
//Refresh the content on the page based on flags and other information sent by the server.
function refreshContent(id, mid) 
{
	var xmlhttp;
	xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange=function()
	{
		console.log(xmlhttp.responseText);
		if (id == "resources"){
			resources = JSON.parse(xmlhttp.responseText);
			document.getElementById("clayAmt").innerHTML = resources.clay;
			document.getElementById("oreAmt").innerHTML = resources.ore;
			document.getElementById("wheatAmt").innerHTML = resources.wheat;
			document.getElementById("woodAmt").innerHTML = resources.wood;
			document.getElementById("sheepAmt").innerHTML = resources.sheep;
			document.getElementById("devAmt").innerHTML = resources.dev;
			document.getElementById("points").innerHTML = resources.points;
			if (resources.flag == lastFlag && resources.flag != "12") {
				 if (resources.dice != 0){
                                        document.getElementById('endTurnButton').innerHTML = "<a href=\"javascript:openModal('endTurn')\" id='turnButton' class='button borderTop'>End Turn</a>";
                                }
                                else {
                                        document.getElementById('endTurnButton').innerHTML = "<a href=\"javascript:rollDice()\" id='turnButton' class='button borderTop'>Roll Dice</a>";
                                }
				return;
			}
			else if (resources.flag != "12"){
				closeModal();
			}
			lastFlag = resources.flag;
			if (resources.flag == "1") //Indicates turn has started.
			{
				document.getElementById("footer").innerHTML = "<a href=\"javascript:openModal('purchase')\" id='purchaseButton' class='button borderRight spacingLeft'>Purchase</a>\n<a href=\"javascript:openModal('trade')\" id='tradeButton' class='button'>Trade</a>\n<a href=\"javascript:runi2c('confirm')\" id='confirmButton' class='button borderTop borderRight spacingLeft'>Confirm</a>\n<span id='endTurnButton'><a href=\"javascript:openModal('endTurn')\" id='turnButton' class='button borderTop'>End Turn</a></span>";
				document.getElementById("imageReplace").innerHTML = "<a class='headElement' href='javascript:showHideMenu()' id='leftHead'><img src='images/menu.png'/></a>";
				document.getElementById("head").style.backgroundColor = "rgba(207,181,59,.8)";
				if (resources.initSetup == "1"){
					openModal('initSetup')
				}
				if (resources.dice != 0){
					document.getElementById('endTurnButton').innerHTML = "<a href=\"javascript:openModal('endTurn')\" id='turnButton' class='button borderTop'>End Turn</a>";
				}
				else {
					document.getElementById('endTurnButton').innerHTML = "<a href=\"javascript:rollDice()\" id='turnButton' class='button borderTop'>Roll Dice</a>";
				}
			}
			else if (resources.flag == "2") //Indicates invalid trade.
			{
				openModal('invalidTrade');
			}
			else if (resources.flag == "3") //Indicates begin trade on remote player.
			{
				openModal('remoteTrade');
			}
			else if (resources.flag == "4") //Indicates trade response from remote player.
			{
				openModal('returnTrade');
			}
			else if (resources.flag == "5") //Indicates piece change on board.
			{
				openModal('pieceInfo');
			}
			else if (resources.flag == "6") //Indicates end of turn.
			{
				document.getElementById('footer').innerHTML = "";
				document.getElementById('footer').style.visibility = "hidden";
				document.getElementById('footer').style.height = "0px";
				document.getElementById("imageReplace").innerHTML = "<img id='leftHeadImg' src='images/menu_gray.png'/>";
				document.getElementById('head').style.backgroundColor = "rgba(255,253,208,.5)";
			}
			else if (resources.flag == "7") //Indicates Road Building.
			{
				openModal('buildRoads');
			}
			else if (resources.flag == "8") //Indicates playing a Knight (or a 7 roll)
			{
				openModal('knight');
			}
			else if (resources.flag == "9") //Indicates the END IS UPON US!
			{
				openModal('endGame');
			}
			else if (resources.flag == "10") //Indicates player needs to discard hand (7 roll)
			{
				openModal('discardHand');
			}
			else if (resources.flag == "11") //Indicates the dice has been rolled.
			{
				openModal('rollBox');
			}
			else if (resources.flag == "12") //Indicates waiting for player to discard
			{
				openModal('knight&player=' + document.forms[0].stealPlayer.value);
			}
			else if (resources.flag == "13") //Indicates new game starting.
			{
				location.reload(true);
			}
		}
		else if (id == "readyState"){
			ready = JSON.parse(xmlhttp.responseText);
			if (ready.gameStart == 1){ 
				document.getElementById("readyLinks").innerHTML="<span class=\"fullWidth waitLink\">Game is starting...</span>";
				location.reload(true); 
			}
			else{
				document.getElementById("readyLinks").innerHTML = ready.readyLink;
			}
			document.getElementById("playersReady").innerHTML = ready.players;
		}
		else{
			document.getElementById(id).innerHTML = xmlhttp.responseText;
		}
	}
	if(mid == 0){
		xmlhttp.open("GET", "refreshContent?id=" + id, true);
	} else {
		xmlhttp.open("GET", "refreshContent?id=" + id + "&modal=" + mid, true);
	}
	xmlhttp.send();
}
//Shows or hides the fancy menu with the fancy buttons that do fancy things.
function showHideMenu() {
  var elem = document.getElementById("footer");
	if (elem.style.visibility == "hidden")
	{
		elem.style.visibility = "visible";
		elem.style.height = "80px";
	} else {
		elem.style.visibility = "hidden";
		elem.style.height = "0px";
	}
}
