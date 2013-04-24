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
			<script>setInterval("refreshContent(\"resources\", 0)", 1000)</script>
			
         <!--Modal Boxes-->
         <!--<a href="javascript:closeModal()" class="overlay" id="modal"></a>-->
	 <div class="overlay" id="modal"></div>
         <div class="modal" id="ModalBox">
				 <!--img class="loadingGif" src="images/loading.gif" alt="Loading..." /-->
				 <p>Loading...</p>
         </div>
			<!--Main Body-->
			<div id="container">
%if currentTurn == True:
				<div id="head" style="background-color: rgba(207,181,59,.8)">
%else:
				<div id="head" style="background-color: rgba(255,253,208,.5)">
%end
				  <span  class="headElement" id="imageReplace">
%if currentTurn == True:
						<a class='headElement' href='javascript:showHideMenu()' id='leftHead'><img src='images/menu.png'/></a>
%else:
						<img id="leftHeadImg" src="images/menu_gray.png"/>
%end
					</span>
					<div id="middleHead" class="headElement">
						<div class="centered">
							<a href="javascript:openModal('name');" id="name_pop" class="h2"><span id="playerName">{{name}}</span>:</a> 
							<a href="javascript:openModal('status')" id="word_pop" class="h2"><span id="points">{{points}}</span> pts</a>
						</div>
					</div>
					<a class="headElement" href="javascript:void()" id="rightHead"><img src="images/settings.png"/></a>
				</div>
				<div id="footer" style="visibility: hidden">
%if currentTurn == False:
						<span class="button fade borderRight spacingLeft">&nbsp;</span>
						<span class="button fade">&nbsp;</span>
						<a href="javascript:openModal('status')" id='statusButton' class="button borderTop borderRight spacingLeft">Status</a>
						<span class="button fade borderTop">&nbsp;</span>
						<span class="button fade borderTop borderRight spacingLeft">&nbsp;</span>
						<span class="button fade borderTop">&nbsp;</span>
%else:
					<a href="javascript:openModal('purchase')" id='purchaseButton' class="button borderRight spacingLeft">Purchase</a>
					<a href="javascript:openModal('trade')" id='tradeButton' class="button">Trade</a>
					<a href="javascript:runi2c('confirm')" id='confirmButton' class='button borderTop borderRight spacingLeft'>Confirm</a>
%if diceRolled == True:
					<span id='endTurnButton'><a href="javascript:openModal('endTurn')" id='turnButton' class='button borderTop'>End Turn</a></span>
%else:
					<span id='endTurnButton'><a href="javascript:rollDice()" id='turnButton' class='button borderTop'>Roll Dice</a></span>
%end
					<!--a href="javascript:runi2c('deny')" id='denyButton' class='button borderTop'>Deny</a-->
					<!--a href="javascript:openModal('status')" id='statusButton' class="button borderTop borderRight spacingLeft">Status</a-->
%end
				</div>

				<div id="resources">
					<div id="clay" class="resource">
						<img src="images/clay.png" class="resourceImg"/>
						<p class="resourceTitle">Clay</p>
						<p id="clayAmt" class="amount">{{resources['clay']}}</p>
					</div>
					<div id="ore"  class="resource">
						<img src="images/ore.png" class="resourceImg"/>
						<p class="resourceTitle">Ore</p>
						<p id="oreAmt" class="amount">{{resources['ore']}}</p>
					</div>
					<div id="sheep" class="resource">
						<img src="images/sheep.png" class="resourceImg"/>
						<p class="resourceTitle">Sheep</p>
						<p id="sheepAmt" class="amount">{{resources['sheep']}}</p>
					</div>
					<div id="wheat" class="resource">
						<img src="images/wheat.png" class="resourceImg"/>
						<p class="resourceTitle">Wheat</p>
						<p id="wheatAmt" class="amount">{{resources['wheat']}}</p>
					</div>
					<div id="wood" class="resource">
						<img src="images/wood.png" class="resourceImg"/>
						<p class="resourceTitle">Wood</p>
						<p id="woodAmt" class="amount">{{resources['wood']}}</p>
					</div>
					<div id="cards" class="resource">
						<a href="javascript:openModal('devCards')" id="cardsLink" >
							<img src="images/sea.png" class="resourceImg"/>
							<p class="resourceTitle">Dev. Cards</p>
							<p class="resourceCaption">Tap for details</p>
							<p id="devAmt" class="devCardsAmount">{{devCards}}</p>
						</a>
					</div>
				</div>
				<div class="clear"></div>
			</div>
		</body>
	
</html>

