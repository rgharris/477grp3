<!DOCTYPE HTML>
   <html>
      <head>
         <!-- Required for mobile devices -->
         <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no"/>
         <!-- Not really a good practice, but this basically just needs to work in demo. If anyone has any better ideas, PLEASE IMPLEMENT THEM. -->
			<link rel="stylesheet" href="styles/style.css" type="text/css" />
			<script src="js/functions.js"></script> 
      </head>


		<body>
			<!--script>setInterval("ajaxRefresh()", 5000)</script-->
			
         <!--Modal Boxes-->
         <a href="javascript:closeModal()" class="overlay" id="modal"></a>
         <div class="modal" id="ModalBox">
				 <p>Test Junk!</p>
         </div>
			<!--Main Body-->
			<div id="container">
				<div id="head">
					<a href="javascript:openModal();" id="name_pop" ><h2>Player 2: 1 Points</h2></a>
					<img src="images/settings.png" class="settingsImg" />
				</div>
				<div id="resources">
					<div id="clay" class="resource">
						<img src="images/clay.png" class="resourceImg"/>
						<p class="resourceTitle">Clay</p>
						<p id="clayAmt" class="amount">0</p>
					</div>
					<div id="ore"  class="resource">
						<img src="images/ore.png" class="resourceImg"/>
						<p class="resourceTitle">Ore</p>
						<p id="oreAmt" class="amount">0</p>
					</div>
					<div id="sheep" class="resource">
						<img src="images/sheep.png" class="resourceImg"/>
						<p class="resourceTitle">Sheep</p>
						<p id="sheepAmt" class="amount">0</p>
					</div>
					<div id="wheat" class="resource">
						<img src="images/wheat.png" class="resourceImg"/>
						<p class="resourceTitle">Wheat</p>
						<p id="wheatAmt" class="amount">0</p>
					</div>
					<div id="wood" class="resource">
						<img src="images/wood.png" class="resourceImg"/>
						<p class="resourceTitle">Wood</p>
						<p id="woodAmt" class="amount">0</p>
					</div>
					<div id="cards" class="resource">
						<a href="javascript:openModal()" id="cardsLink" >
							<img src="images/sea.png" class="resourceImg"/>
							<p class="resourceTitle">Dev. Cards</p>
							<p id="devCardAmt" class="amount">0</p>
						</a>
					</div>
				</div>
				<div class="clear"></div>
				<div id="footer">
					<span class="button fade borderRight spacingLeft">&nbsp;</span>
					<span class="button fade">&nbsp;</span>
					<a href="javascript: openModal()" id='statusButton' class="button borderTop borderRight spacingLeft"><!--onclick="loadXMLDoc('ModalBox', '/dialogs/gameStatus.py')"-->Status</a>
					<span class="button fade borderTop">&nbsp;</span>
					<span class="button fade borderTop borderRight spacingLeft">&nbsp;</span>
					<span class="button fade borderTop">&nbsp;</span>
				</div>
			</div>
		</body>
	
</html>

