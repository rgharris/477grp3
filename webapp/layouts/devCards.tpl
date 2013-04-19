%if not defined('showCards'):
%showCards = False
%end
%if not defined('devCards'):
%devCards = {'victory':0, 'monopoly':0, 'road':0, 'knight':0, 'plenty':0}
%end
%if not defined('playedDevCard'):
%playedDevCard = 1
%end
%if not defined('showCard'):
%showCard = False
$end
%if showCards == True:
<span id="cardContent">
	<h2>Development Cards</h2>
	<p class="devCards">You have the following available.</p>
	<a href="javascript:playCard('victory',false)" class="bottom moreTop left">Victory: {{devCards['victory']}}</a>
	<a href="javascript:playCard('monopoly',false)" class="bottom half top left">Monopoly: {{devCards['monopoly']}}</a>
	<a href="javascript:playCard('road',false)" class="bottom half top right">Road Building: {{devCards['road']}}</a>
	<a href="javascript:playCard('knight',false)" class="bottom half bot left">Knight: {{devCard['knight']}}</a>
	<a href="javascript:playCard('plenty',false)" class="bottom half bot right">Year of Plenty: {{devCard['plenty']}}</a>
</span>
%elif showCard != False:
%if showCard == 'plenty':
	<h2>Year of Plenty card</h2>
	<p class="generic">This card allows you to take two of any one resource you have a settlement on. 
%if devCards['plenty'] != 0 and playedDevCard == 0:
		You currently have {{devCards['plenty']}} Year of Plenty cards available. Would you like to play one?</p>            
		<a href="javascript:playCard('plenty',true)" class="bottom half left">Yes I would!</a>
		<a href="javascript:closeModal();" class="bottom half right">No I wouldn't.</a>
%elif devCards['plenty'] != 0 and playedDevCard != 0:
		You currently have {{devCards['plenty']}} Year of Plenty cards available, but have already played a development card this turn.</p>
		<a href="javascript:closeModal();" class="bottom left">Got it!</a>
%else:
		You currently have no Year of Plenty cards available.</p>
		<a href="javascript:closeModal();" class="bottom left">Got it!</a>
%elif showCard == 'monopoly':
	<h2>Monopoly card</h2>
	<p class="generic"> You currently have {{devCards['plenty']}} Year of Plenty cards available. Would you like to play one?</p>            
	<a href="javascript:playCard('plenty',true)" class="bottom half left">Yes I would!</a>
	<a href="javascript:closeModal();" class="bottom half right">No I wouldn't.</a>
%elif showCard == 'victory':
	<h2>Year of Plenty card</h2>
	<p class="generic">This card allows you to take two of any one resource you have a settlement on. You currently have {{devCards['plenty']}} Year of Plenty cards available. Would you like to play one?</p>            
	<a href="javascript:playCard('plenty',true)" class="bottom half left">Yes I would!</a>
	<a href="javascript:closeModal();" class="bottom half right">No I wouldn't.</a>
%elif showCard == 'road':
	<h2>Year of Plenty card</h2>
	<p class="generic">This card allows you to take two of any one resource you have a settlement on. You currently have {{devCards['plenty']}} Year of Plenty cards available. Would you like to play one?</p>            
	<a href="javascript:playCard('plenty',true)" class="bottom half left">Yes I would!</a>
	<a href="javascript:closeModal();" class="bottom half right">No I wouldn't.</a>
%elif showCard == 'knight':
	<h2>Year of Plenty card</h2>
	<p class="generic">This card allows you to take two of any one resource you have a settlement on. You currently have {{devCards['plenty']}} Year of Plenty cards available. Would you like to play one?</p>            
	<a href="javascript:playCard('plenty',true)" class="bottom half left">Yes I would!</a>
	<a href="javascript:closeModal();" class="bottom half right">No I wouldn't.</a>
%else:
	<h2>Error</h2>
	<p class="generic">That is not a valid card type.</p>
	<a href="javascript:closeModal();" class="bottom left" name="gotit">Got it!</a>
%end
	<h2>Purchase Error</h2>
		<p class="generic">You don't have enough resources to purchase a {{list(purchaseItem)[0]}}.</p>
		<a href="javascript:closeModal();" class="bottom left" name="gotit">Got it!</a>
%elif  == True:
	<h2>Confirm Purchase</h2>
		<p class="generic">Do you wish to purchase a {{list(purchaseItem)[0]}} for {{list(purchaseItem.values())[0]}}?</p>
		<a href="javascript:closeModal();" class="bottom half left">No I don't!</a>
		<a href="javascript:purchase('accept','{{list(purchaseItem)[0]}}');" class="bottom half right">Yes I do!</a>
%end

