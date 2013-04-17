function submitForm()
{
	var xmlhttp;
	xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange = function()
	{
		console.log(xmlhttp.responseText);
		closeModal()
	}
	xmlhttp.open("GET","submitForm?id=" + document.forms[0].name + "&value=" + document.forms[0].user.value,true);
	xmlhttp.send();
	return false
}
function submitName()
{
	var xmlhttp;
	xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange = function()
	{
		console.log(xmlhttp.responseText);
		document.getElementById("playerName").innerHTML=xmlhttp.responseText;
		closeModal()
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

/*function ajaxRefresh() 
{
	var xmlhttp;
	xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange=function()
	{
		//console.log(xmlhttp.status);
		console.log(xmlhttp.responseText);
		//if(xmlhttp.status == 200) {
			if (xmlhttp.responseText == "showModal0")
			{
				//closeAllModals();
				openModal(0);
			}
		//}
	}
	xmlhttp.open("GET", "refresh", true);
	xmlhttp.send();
}*/
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
function heartbeat(playerID)
{
	var xmlhttp;
	xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange=function()
	{
		if(xmlhttp.readyState == 4 && xmlhttp.status == 200)
		{
			if(xmlhttp.responseText == 1)
			{
				refreshContent("resources", 0);
			}
			/*else if(xmlhttp.responseText == 2)
			{
				window.location = "./index.py?trade=check#modal";
			}
			else if(xmlhttp.responseText == 3)
			{
				window.location = "./index.py?trade=confirm#modal";
			}
			else if(xmlhttp.responseText == 4)
			{
				window.location = "./index.py?trade=deny#modal";
			}
			else if(xmlhttp.responseText == 5)
			{
				window.location = "./index.py?trade=fail#modal";
			}
			else if(xmlhttp.responseText == 6)
			{
				window.location = "./index.py?against=monoCardd#modal";
			}
			else if(xmlhttp.responseText == 7)
			{
				window.location = "./index.py?dice=new";
			}
			else if(xmlhttp.responseText == 9)
			{
				window.location = "./index.py?i2c=flown";
			}*/
		}
	}
	xmlhttp.open("GET", "/chkRefresh/chk.py?id=" + playerID, true);
	xmlhttp.send();
}

