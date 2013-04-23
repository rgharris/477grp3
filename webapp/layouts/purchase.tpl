%if not defined('newPurchase'):
%newPurchase = False
%end
%if not defined('invalidPurchase'):
%invalidPurchase = False
%end
%if not defined('confirmPurchase'):
%confirmPurchase = False
%end
%if not defined('purchaseItem'):
%purchaseItem = {'null':'no resources'}
%end
%if not defined('placePiece'):
%placePiece = False
%end
%if not defined('devCard'):
%devCard = False
%end
<span id="purchaseContent">
%if newPurchase == True:
	<h2>Purchase</h2>
	<p class="purchase">
	<a href="javascript:purchase('get','settlement')" class="bottom half top left">Settlement</a>
	<a href="javascript:purchase('get','city')" class="bottom half top right">City</a>
	<a href="javascript:purchase('get','road')" class="bottom half bot left">Road</a>
	<a href="javascript:purchase('get','development card')" class="bottom half bot right">Dev. Card</a>
	</p>
%elif invalidPurchase == True:
	<h2>Purchase Error</h2>
		<p class="generic">You don't have enough resources to purchase a {{list(purchaseItem)[0]}}.</p>
		<a href="javascript:closeModal();" class="bottom left" name="gotit">Got it!</a>
%elif confirmPurchase == True:
	<h2>Confirm Purchase</h2>
		<p class="generic">Do you wish to purchase a {{list(purchaseItem)[0]}} for {{list(purchaseItem.values())[0]}}?</p>
		<a href="javascript:purchase('deny', '{{list(purchaseItem)[0]}}');" class="bottom half left">No I don't!</a>
		<a href="javascript:purchase('accept','{{list(purchaseItem)[0]}}');" class="bottom half right">Yes I do!</a>
%elif placePiece == True:
	<h2>Place Piece</h2>
		<p class="generic">Please place your piece now.</p>
%elif devCard == 'victory':
	<h2>Victory Card!</h2>
		<p class="generic">Congratulations! You are one step closer to victory! You have obtained a victory point card. No one will see this victory point until the end of the game, and it will not show up in the status screen. It will only show up on your main point count next to your name.</p>
		<a href="javascript:closeModal();" class="bottom left">Got it!</a>
%elif devCard == 'none':
	<h2>No development cards!</h2>
	<p>There are no more development cards to draw! Pick another thing to purchase, if you are able.</p>
	<a href="javascript:closeModal();" class="bottom left">Got it!</a>
%elif devCard != False:
	<h2>Development Card!</h2>
		<p class="generic">You have received a {{devCard}} card! You can play it any time, starting next turn, by selecting the "Dev Cards" item on the resource screen.</p>
		<a href="javascript:closeModal();" class="bottom left">Got it!</a>
%else:
	<h2>Error</h2>
		<p class="generic">There was an error with the purchase form. Please try again.</p>
	<a href="javascript:closeModal();" class="bottom left" name="gotit">Got it.</a>
%end
</span>
