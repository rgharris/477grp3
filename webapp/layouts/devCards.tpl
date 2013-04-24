%if not defined('showCards'):
%showCards = False
%end
%if not defined('devCards'):
%devCards = {'victory':0, 'monopoly':0, 'road':0, 'knight':0, 'plenty':0, 'knightsPlayed':0}
%end
%if not defined('playedDevCard'):
%playedDevCard = 1
%end
%if not defined('showCard'):
%showCard = False
%end
%if not defined('playCard'):
%playCard = False
%end
%if not defined('success'):
%success = False
%end
%if not defined('resources'):
%resources = None
%end
%if not defined('steal'):
%steal = {'-1':'Nobody'}
%end
%if showCards == True:
<span id="cardContent">
	<h2>Development Cards</h2>
	<p class="resourceBox devCardSpacing">Your available devlopment cards are shown here.</p>
	<a href="javascript:playCard('victory','false')" class="bottom moreTop left">Victory: {{devCards['victory']}}</a>
	<a href="javascript:playCard('monopoly','false')" class="bottom half top left">Monopoly: {{devCards['monopoly']}}</a>
	<a href="javascript:playCard('road','false')" class="bottom half top right">Road Building: {{devCards['road']}}</a>
	<a href="javascript:playCard('knight','false')" class="bottom half bot left">Knight: {{devCards['knight']}}</a>
	<a href="javascript:playCard('plenty','false')" class="bottom half bot right">Year of Plenty: {{devCards['plenty']}}</a>
</span>
%elif showCard != False:
%if showCard == 'plenty':
	<h2>Year of Plenty card</h2>
	<p class="generic">This card allows you to take any two resources. 
%if devCards['plenty'] != 0 and playedDevCard == 0:
		You currently have {{devCards['plenty']}} Year of Plenty cards available. Would you like to play one?</p>            
		<a href="javascript:playCard('plenty','playing')" class="bottom half left">Yes I would!</a>
		<a href="javascript:closeModal();" class="bottom half right">No I wouldn't.</a>
%elif devCards['plenty'] != 0 and playedDevCard != 0:
		You currently have {{devCards['plenty']}} Year of Plenty cards available, but have already played a development card this turn.</p>
		<a href="javascript:closeModal();" class="bottom left">Got it!</a>
%else:
		You currently have no Year of Plenty cards available.</p>
		<a href="javascript:closeModal();" class="bottom left">Got it!</a>
%end

%elif showCard == 'monopoly':
	<h2>Monopoly card</h2>
	<p class="generic">This card allows you to take a monopoly on a single resource, forcing all players currently holding that resource to hand it over to you.
%if devCards['monopoly'] != 0 and playedDevCard == 0:
		You currently have {{devCards['monopoly']}} Monopoly cards available. Would you like to play one?</p>            
		<a href="javascript:playCard('monopoly','playing')" class="bottom half left">Yes I would!</a>
		<a href="javascript:closeModal();" class="bottom half right">No I wouldn't.</a>
%elif devCards['monopoly'] != 0 and playedDevCard != 0:
		You currently have {{devCards['monopoly']}} Monopoly cards available, but have already played a development card this turn.</p>
		<a href="javascript:closeModal();" class="bottom left">Got it!</a>
%else:
		You currently have no Monopoly cards available.</p>
		<a href="javascript:closeModal();" class="bottom left">Got it!</a>
%end

%elif showCard == 'victory':
	<h2>Victory card</h2>
	<p class="generic">This card gets you an additional victory point, hidden from the other players. It cannot be played, but counts toward your total score. Your opponents will only see your score without these cards. You currently have {{devCards['victory']}} victory cards.</p>
	<a href="javascript:closeModal();" class="bottom left">Got it!</a>

%elif showCard == 'road':
	<h2>Road Building card</h2>
	<p class="generic">This card allows you to take two roads at no additional cost. 
%if devCards['road'] != 0 and playedDevCard == 0:
		You currently have {{devCards['road']}} Road Building cards available. Would you like to play one?</p>            
		<a href="javascript:playCard('road','playing')" class="bottom half left">Yes I would!</a>
		<a href="javascript:closeModal();" class="bottom half right">No I wouldn't.</a>
%elif devCards['road'] != 0 and playedDevCard != 0:
		You currently have {{devCards['road']}} Road Building cards available, but have already played a development card this turn.</p>
		<a href="javascript:closeModal();" class="bottom left">Got it!</a>
%else:
		You currently have no Road Building cards available.</p>
		<a href="javascript:closeModal();" class="bottom left">Got it!</a>
%end

%elif showCard == 'knight':
	<h2>Knight card</h2>
	<p class="generic">This card allows you to move the thief and steal a single, random resource from a given player. You have played {{devCards['knightsPlayed']}},
%if devCards['knight'] != 0 and playedDevCard == 0:
		and currently have {{devCards['knight']}} Knight cards available. Would you like to play one?</p>            
		<a href="javascript:playCard('knight','playing')" class="bottom half left">Yes I would!</a>
		<a href="javascript:closeModal();" class="bottom half right">No I wouldn't.</a>
%elif devCards['knight'] != 0 and playedDevCard != 0:
		and currently have {{devCards['knight']}} Knight cards available, but have already played a development card this turn.</p>
		<a href="javascript:closeModal();" class="bottom left">Got it!</a>
%else:
		and currently have no Knight cards available.</p>
		<a href="javascript:closeModal();" class="bottom left">Got it!</a>
%end

%else:
	<h2>Error</h2>
	<p class="generic">That is not a valid card type.</p>
	<a href="javascript:closeModal();" class="bottom left" name="gotit">Got it!</a>
%end
%elif playCard != False:
%if playCard == 'plenty':
	<form name='yearofplenty' onsubmit='return submitForm()' id='yearofplenty'>
	<span id="boxContent">
	<h2>Year of Plenty</h2>
  <p>Select your two free resources!</p>
  <select name="resource1" class="resourceSelect">
  	<option value="none">Select a resource...</option>
    <option value="ore">Ore</option>
    <option value="wheat">Wheat</option>
    <option value="sheep">Sheep</option>
    <option value="clay">Clay</option>
    <option value="wood">Wood</option>
  </select>
  <select name="resource2" class="resourceSelect">
    <option value="none">Select a resource...</option>
    <option value="ore">Ore</option>
    <option value="wheat">Wheat</option>
    <option value="sheep">Sheep</option>
    <option value="clay">Clay</option>
    <option value="wood">Wood</option>
  </select>
	<input type="submit" value="Got it!" class="bottom left" name="plentySelected" />
	</span>
	</form>
%elif playCard == 'knight':
	<form name="knight" onsubmit="return submitForm()" id="knight">
	<span id="boxContent">
	<h2>Knight</h2>
	<p>Once the thief has been moved, select a player to steal from.</p>
%if len(steal) == 0:
	<p>There are no players to steal from here!</p>
	<a href="javascript:closeModal();" class="bottom left">Got it!</a>
%else:
	<select name="stealFrom" class="stealSelect">
%for playerID in steal:
	<option value="{{playerID}}">{{steal[playerID]}}</option>
%end
	</select>
	<input type="submit" value="This person!" class="bottom left" name="stealSelected" />
%end
	</span>
	</form>
%elif playCard == 'monopoly':
	<form name='monopoly' onsubmit='return submitForm()' id='monopoly'>
	<span id="boxContent">
  <h2>Monopoly</h2>
    <p>Select the resource you would like to have a monopoly on.</p>
      <select name="resource" class="resourceSelect">
        <option value="none">Select a resource...</option>
        <option value="ore">Ore</option>
        <option value="wheat">Wheat</option>
        <option value="sheep">Sheep</option>
        <option value="clay">Clay</option>
        <option value="wood">Wood</option>
      </select>
      <input type="submit" value="Got it!" class="bottom left" name="monopolySelected">	
	</span>
%elif playCard == 'road':
	<h2>Road Building</h2>
	<p>Place your two free roads now!</p>
%else:
	<h2>Error</h2>
	<p class="generic">That is not a valid card to play.</p>
	<a href="javascript:closeModal();" class="bottom left" name="gotit">Got it!</a>
%end
%elif success != 'false':
%if success == 'plenty':
	<h2>Year of Plenty</h2>
	<p>You have recieved your two additional resources.</p>
	<a href="javascript:closeModal();" class="bottom left" name="gotit">Got it!</a>
%elif success == 'monopoly':
	<h2>Monopoly</h2>
	<p>You have recieved {{resources[list(resources)[0]]}} {{list(resources)[0]}}!</p>
	<a href="javascript:closeModal();" class="bottom left" name="gotit">Got it!</a>
%elif success == 'knight':
	<h2>Knight</h2>
%if list(resources)[0] != 'none':
	<p>You have received a {{list(resources)[0]}}!</p>
%else:
	<p>This player has no resources to steal! Too bad.</p>
%end
	<a href="javascript:closeModal();refreshContent('clearFlag', 0);" class="bottom left" name="gotit">Got it!</a>
%elif success == 'road':
	<h2>Road Building</h2>
	<p>Your roads have been built!</p>
	<a href="javascript:closeModal();" class="bottom left" name="gotit">Got it!</a>
%else:
	<h2>Development Card Error</h2>
		<p class="generic">There was an error displaying the Development Card form. Please try again.</p>
		<a href="javascript:closeModal();" class="bottom left" name="gotit">Got it!</a>
%end

