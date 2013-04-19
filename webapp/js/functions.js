function submitForm()
{
	var xmlhttp, values;
	xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange = function()
	{
		console.log(xmlhttp.responseText);
		if(document.forms[0].name != "trade")
		{
			closeModal()
		}
	}
	if(document.forms[0].name == "endTurn")
	{
		values = "0"
		document.getElementById('footer').innerHTML = "<span class=\"button fade borderRight spacingLeft\">&nbsp;</span>\n<span class=\"button fade\">&nbsp;</span>\n<a href=\"javascript:openModal('status')\" id='statusButton' class=\"button borderTop borderRight spacingLeft\">Status</a>\n<span class=\"button fade borderTop\">&nbsp;</span>\n<span class=\"button fade borderTop borderRight spacingLeft\">&nbsp;</span>\n<span class=\"button fade borderTop\">&nbsp;</span>";
	}
	if(document.forms[0].name == "trade")
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
	xmlhttp.open("GET","submitForm?id=" + document.forms[0].name + "&value=" + values,true);
	xmlhttp.send();
	return false
}
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
	xmlhttp.open("GET","submitForm?id=name&value=" + document.forms[0].user.value, true);
	xmlhttp.send();
	return false
}
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
function closeModal()
{
	var elem = document.getElementById("ModalBox");
	elem.style.visibility = "hidden";
	elem = document.getElementById("modal");
	elem.style.visibility = "hidden";
}
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
			if (resources.flag == "1") //Indicates turn has started.
			{
				document.getElementById("footer").innerHTML = "<a href=\"javascript:openModal('purchase')\" id='purchaseButton' class=\"button borderRight spacingLeft\">Purchase</a>\n<a href=\"javascript:openModal('trade')\" id='tradeButton' class=\"button\">Trade</a>\n<a href=\"javascript:openModal('status')\" id='statusButton' class=\"button borderTop borderRight spacingLeft\">Status</a>\n<span id='endTurnButton'><a href=\"javascript:openModal('endTurn')\" id='turnButton' class='button borderTop'>End Turn</a></span>\n <a href=\"javascript:runi2c('confirm')\" id='confirmButton' class='button borderTop borderRight spacingLeft'>Confirm</a><a href=\"javascript:runi2c('deny')\" id='denyButton' class='button borderTop'>Deny</a>";
			}
			else if (resources.flag == "2") //Indicates invalid trade.
			{
				closeModal()
				openModal('invalidTrade')
			}
			else if (resources.flag == "3") //Indicates begin trade on remote player.
			{
				closeModal()
				openModal('remoteTrade')
			}
			else if (resources.flag == "4") //Indicates trade response from remote player.
			{
				closeModal()
				openModal('returnTrade')
			}
		}
		else if (id == "readyState"){
			ready = JSON.parse(xmlhttp.responseText);
			if (ready.gameStart == 1){ location.reload(true); }
			document.getElementById("readyLinks").innerHTML = ready.readyLink;
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
