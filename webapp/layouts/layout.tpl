<!DOCTYPE HTML>
   <html>
      <head>
         <!-- Required for mobile devices -->
         <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no"/>
         <!-- Not really a good practice, but this basically just needs to work in demo. If anyone has any better ideas, PLEASE IMPLEMENT THEM. -->
         <!--<link rel="stylesheet" href="styles/catronNormal.css" type="text/css" media="screen"/>
         <link rel="stylesheet" href="styles/catronMobilePortrait.css" type="text/css" media="screen and (max-device-width: 720px) and (orientation: portrait)"/>
			<!--Interestingly, whenever the keyboard opens on the S3 (and presumably most android devices), it switches to landscape mode. I don't know how to get around this right now.
         <link rel="stylesheet" href="styles/catronMobileLandsacpe.css" type="text/css" media="screen and (max-device-width: 1280px) and (orientation: landscape)"/>-->
			<link rel="stylesheet" href="styles/style.css" type="text/css" />
			<script>
			  var modalNumber = 0;
			  function openModal(i)
				{
					modalNumber = i;
					var elem = document.getElementById("ModalBox" + i.toString());
					elem.style.opacity = "1";
					elem.style.visibility = "visible";
					elem.style.top = (window.pageYOffset + 25).toString()+ "px";
					elem = document.getElementById("modal");
					elem.style.opacity = "0.75";
					elem.style.visibility = "visible";
				}
				function closeModal()
				{
					var elem = document.getElementById("ModalBox" + modalNumber.toString());
					elem.style.opacity = "0";
					elem.style.visibility = "hidden";
					elem = document.getElementById("modal");
					elem.style.opacity = "0";
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
								location.reload(true);
							}
							else if(xmlhttp.responseText == 2)
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
							}
						}
					}
					xmlhttp.open("GET", "/chkRefresh/chk.py?id=" + playerID, true);
					xmlhttp.send();
				}
				
   		</script>
      </head>


		<body>
			<!--script>setInterval("heartbeat(1)", 5000)</script-->
			
         <!--Modal Boxes-->
         <a href="javascript:closeModal()" class="overlay" id="modal"></a>
         <div class="modal" id="ModalBox0">
				 This modal box allows you to change your name!
				 <p>Test Junk!</p>
				 <p>Test Junk!</p>
				 <p>Test Junk!</p>
				 <p>Test Junk!</p>
				 <p>Test Junk!</p>
				 <p>Test Junk!</p>
				 <p>Test Junk!</p>
				 <p>Test Junk!</p>
				 <p>Test Junk!</p>

         </div>
         <div class="modal" id="ModalBox1">
				 This modal box is used to view the game status!
				 <p>Test Junk!</p>
				 <p>Test Junk!</p>
				 <p>Test Junk!</p>
				 <p>Test Junk!</p>
				 <p>Test Junk!</p>
         </div>
         <div class="modal" id="ModalBox2">
				 This modal box is used to purchase development cards!
				 <p>Test Junk!</p>
				 <p>Test Junk!</p>
				 <p>Test Junk!</p>
         </div>
         <div class="modal" id="ModalBox3">
         </div>
         <div class="modal" id="ModalBox4">
         </div>
         <div class="modal" id="ModalBox5">
         </div>
			<!--Main Body-->
			<div id="container">
				<div id="head">
					<a href="javascript:openModal(0)" id="name_pop" ><h2>Player 2: 1 Points</h2></a>
					<img src="images/settings.png" class="settingsImg" />
				</div>
				<div id="resources">
					<div id="clay" class="resource">
						<img src="images/clay.png" class="resourceImg"/>
						<p class="resourceTitle">Clay</p>
						<p class="amount">1</p>
					</div>
					<div id="ore"  class="resource">
						<img src="images/ore.png" class="resourceImg"/>
						<p class="resourceTitle">Ore</p>
						<p class="amount">0</p>
					</div>
					<div id="sheep" class="resource">
						<img src="images/sheep.png" class="resourceImg"/>
						<p class="resourceTitle">Sheep</p>
						<p class="amount">0</p>
					</div>
					<div id="wheat" class="resource">
						<img src="images/wheat.png" class="resourceImg"/>
						<p class="resourceTitle">Wheat</p>
						<p class="amount">1</p>
					</div>
					<div id="wood" class="resource">
						<img src="images/wood.png" class="resourceImg"/>
						<p class="resourceTitle">Wood</p>
						<p class="amount">0</p>
					</div>
					<div id="cards" class="resource">
						<a href="javascript:openModal(2)" id="cardsLink" >
							<img src="images/sea.png" class="resourceImg"/>
							<p class="resourceTitle">Dev. Cards</p>
							<p class="amount">0</p>
						</a>
					</div>
				</div>
				<div class="clear"></div>
				<div id="footer">
					<span class="button fade borderRight spacingLeft">&nbsp;</span>
					<span class="button fade">&nbsp;</span>
					<a href="javascript:openModal(1)" class="button borderTop borderRight spacingLeft"><!--onclick="loadXMLDoc('ModalBox', '/dialogs/gameStatus.py')"-->Status</a>
					<span class="button fade borderTop">&nbsp;</span>
					<span class="button fade borderTop borderRight spacingLeft">&nbsp;</span>
					<span class="button fade borderTop">&nbsp;</span>
				</div>
			</div>
		</body>
	
</html>

