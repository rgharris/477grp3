/*
 * Catan.c
 *
 * Created: 4/9/2013 12:44:37 PM
 *  Author: team3
 */

// This file should be used for functions related to the main game loop
// (e.g. check board state, error check, accessing static maps, etc)
// The main game loop itself could probably go in main
 
#include <Catan.h>


uint8_t owner_map[145] = {0};
ioport_port_mask_t legalBoardState[8] = {0};
uint8_t city_map[145] = {0};
// Hexagon Maps
uint8_t Hex2Rarity[19];
uint8_t Hex2Resource[19];
uint8_t DesertHex = 0;
// Pieces each player has remaining of each type [player][piecetype] {roads,settlements,cities}
uint8_t pieces_remaining[4][3] ={{15,5,4},{15,5,4},{15,5,4},		 {15,		5,		     4}};
uint8_t roadmap[4][15][3] = {0};	// [player][road][{adjacent city1, adjacent city2,mark}]
uint8_t longestRoadOwnerPrev = 0;					
uint8_t dice_roll_state = 0;		// Has the dice been rolled yet?
uint8_t last_pos_confirmed = 0xFF;		// Gives the position of the last piece to be confirmed as placed. Needs to be set to -1 once it serves its purpose
uint8_t last_pos_rejected = 0xFF;		// Gives position of last piece to be rejected. Should be cleared (-1) at end of clean run of check board state
int ColPins[]= {HE_COL0,HE_COL1,HE_COL2,HE_COL3,HE_COL4,HE_COL5,HE_COL6,HE_COL7, HE_COL8,HE_COL9,HE_COL10,HE_COL11,HE_COL12,HE_COL13,HE_COL14,HE_COL15,HE_COL16,HE_COL17};

void generate_board(void) {
	// This function should track user input before a game starts to generate "random" numbers in order to pick the resources
	// and rarities for each hex.
	
	uint8_t i,k,j;
	uint8_t rand_red,rand_blue,rand_green;
	//							{ORE WHEAT SHEEP BRICK WOOD DESERT}
	uint8_t ResourcesInDeck[] = { 3 ,  4  ,  4  ,  3  , 4  ,  1   };
	uint8_t ResourcesRemaining = 19;
	uint8_t ResourceIndexCompare;
	uint8_t address;
	int ResourceAssigned;
	// Hall Effect Sensor
	ioport_port_mask_t RowReturn;
		
	// initialize the hexes so that they have no resource or rarity
	for (i=0;i<19;i++){
		//rarity_set(i, 22);
		Hex2Resource[i] = NO_RESOURCE;
		Hex2Rarity[i] = 0;
	}
	
	//initialize board at nothing
	rgb_clear_all();
	rarity_clear_all();
			
	// Keep checking all sensor positions until the Pi has turned on
	while (!(s_memory[PI_EVENT_REG] == PI_TURN_ON))
	{
		for (address=0;address<8;address++)
		{

			// Grab the sensor data for every row
			ioport_set_port_level(HE_RETURN_PORT,HE_ADDR_PINS_MASK,address<<HE_ADDR_PIN_0);
			delay_ms(.1);
			RowReturn = ioport_get_port_level(HE_RETURN_PORT,HE_RETURN_MASK);
			
			// Check each hex (Hex# = i)
			for (i=0;i<18;i++)
			{
				if (RowReturn & 1<<ColPins[i])
				{
					

					// INSERT FANCY GRAPHICS STUFF HERE
					rand_red = ((Get_sys_count() & 0xF0)>>4);
					rand_blue =  ((Get_sys_count() & 0xF00)>>8);
					rand_green = ((Get_sys_count() & 0xF000)>>12);
					rgb_hex_set(i,rand_red<<20|rand_blue<<12|rand_green<<4);
					if (pos2AdjHex(address*18+i,1)!= -1)
					{
						rgb_hex_set(pos2AdjHex(address*18+i,1),rand_red<<20|rand_blue<<12|rand_green<<4);
					}
					if (pos2AdjHex(address*18+i,2) != -1)
					{
						rgb_hex_set(pos2AdjHex(address*18+i,2),rand_red<<20|rand_blue<<12|rand_green<<4);
					}
					rarity_display_error(i,address,0);
					delay_ms(DISPLAY_DELAY);
					
					
					// Only assign a resource to a hex that doesn't have one already and its thief is activated by magnet
					//if ((address == 7) && (Hex2Resource[i] == NO_RESOURCE))
					// Only assign a resource to a hex that doesn't have one already
					if (Hex2Resource[i] == NO_RESOURCE)
					{
						// Create a random number based on how many resources are remaining
						j = ((Get_sys_count() & 0xFF0)>>4) % ResourcesRemaining;
						// How far into the remaining deck of resources did the random number get?
						ResourceIndexCompare = 0;
						ResourceAssigned = 0;
						for (k=0;k<7;k++)
						{
							ResourceIndexCompare += ResourcesInDeck[k];
							// Don't assign more than one resource to each hex
							if ((j < ResourceIndexCompare) && (ResourceAssigned == 0))
							{
								// Assign resource, take that resource from the deck, this hex has a resource assigned
								Hex2Resource[i] = k;
								ResourcesInDeck[k]--;
								ResourceAssigned = 1;
								ResourcesRemaining--;
																
							}
						}
					}
				}
			}
		}
		
		
		
		// Don't forget to check the middle thief.
		if (!ioport_get_pin_level(MIDDLE_SENSOR)){
			
			// MOAR FANCY GRAPHICS
			rand_red = ((Get_sys_count() & 0xF0)>>4);
			rand_blue =  ((Get_sys_count() & 0xF00)>>8);
			rand_green = ((Get_sys_count() & 0xF000)>>12);
			rgb_hex_set(18,rand_red<<20|rand_blue<<12|rand_green<<4);
			rarity_display_error(18,7,0);
			delay_ms(DISPLAY_DELAY);
			
			if (Hex2Resource[18] == NO_RESOURCE)
			{
			
				// Create a random number based on how many resources are remaining
				j = ((Get_sys_count() & 0xFF0)>>4) % ResourcesRemaining;
				//rarity_set(i,j);
				// How far into the remaining deck of resources did the random number get?
				ResourceIndexCompare = 0;
				ResourceAssigned = 0;
				for (k=0;k<7;k++)
				{
					ResourceIndexCompare += ResourcesInDeck[k];
					// Don't assign more than one resource to each hex
					if ((j < ResourceIndexCompare) && (ResourceAssigned == 0))
					{
						// Assign resource, take that resource from the deck, this hex has a resource assigned
						Hex2Resource[18] = k;
						ResourcesInDeck[k]--;
						ResourceAssigned = 1;
						ResourcesRemaining--;
					
					
						// Update the display
						//rgb_display_resource(18,k);
						//rarity_set(18,k);
					}
				}
			}
		}			
	}
	

	
	// Finish assigning resources using random numbers given by RPi
	
	for (i=0;i<19;i++)
	{
		// Only assign resources to Hex's that don't have one yet
		if (Hex2Resource[i] == NO_RESOURCE)
		{
			// Get a random number between 0 and the remaining resources
			j = s_memory[RESOURCE_REC_REG+i] % ResourcesRemaining;
			ResourceAssigned = 0;
			ResourceIndexCompare = 0;
			//
			for (k=0;k<7;k++)
			{
				ResourceIndexCompare += ResourcesInDeck[k];
				// Don't assign more than one resource to each hex
				if ((j < ResourceIndexCompare) && (ResourceAssigned == 0))
				{
					// Assign resource, take that resource from the deck, this hex has a resource assigned
					Hex2Resource[i] = k;
					ResourcesInDeck[k]--;
					ResourceAssigned = 1;
					ResourcesRemaining--;
				}
			}
		}
	}
	
	//Doesn't always start at the same time, so seed with current cpu count HERE as opposed to board_init.
	uint32_t start = ((Get_sys_count() & 0xFF0)>>4) % 12;
	uint8_t hex_order[] = {0,1,3,5,16,17,8,9,10,11,12,15,2,4,6,7,13,14,18};		// Used to lay out rarity values
	uint8_t rarity_order[] = {5,2,6,3,8,10,9,12,11,4,8,10,9,4,5,6,3,11};
	//first generate random number between 0 and 11
	uint8_t desertFix = 0;
	for (i=0;i<12;i++){
		if(Hex2Resource[hex_order[(start+i) % 12]] == 5){
			desertFix = 1;
			Hex2Rarity[hex_order[(start+i) % 12]] = -1;
		}
		else{
			//rarity_set(hex_order[(start+i) % 12],rarity_order[i-desertFix]);
			Hex2Rarity[hex_order[(start+i) % 12]] = rarity_order[i-desertFix];
		}
	}
	start = (start/2) + 11;
	for (i=0;i<6;i++){
		if(Hex2Resource[hex_order[(start+i) % 6 + 12]] == 5){
			desertFix = 1;
			Hex2Rarity[hex_order[((start+i) % 6 + 12)]] = -1;
		}
		else {
			//rarity_set(hex_order[((start+i) % 6 + 12)],rarity_order[12+i-desertFix]);
			Hex2Rarity[hex_order[((start+i) % 6 + 12)]] = rarity_order[12+i-desertFix];
		}
	}
	if(Hex2Resource[18] != 5){
		//rarity_set(hex_order[18],rarity_order[17]);
		Hex2Rarity[hex_order[18]] = rarity_order[17];
	}		
	else{
		Hex2Rarity[hex_order[18]] = -1;
	}
	//////////////////////////////////////////////////////////////////////////
	// WAITING FOR PI TO SAY A NEW GAME HAS BEGUN
	//////////////////////////////////////////////////////////////////////////
	
	while (!(s_memory[PI_EVENT_REG] == PI_NEW_GAME))
	{
		bootLoop();
		/*for (address=0;address<8;address++)
		{

			// Grab the sensor data for every row
			ioport_set_port_level(HE_RETURN_PORT,HE_ADDR_PINS_MASK,address<<HE_ADDR_PIN_0);
			delay_ms(.1);
			RowReturn = ioport_get_port_level(HE_RETURN_PORT,HE_RETURN_MASK);
			
			// Check each hex (Hex# = i)
			for (i=0;i<18;i++)
			{
				if (RowReturn & 1<<ColPins[i])
				{
					
					// INSERT FANCY GRAPHICS STUFF HERE
					rand_red = ((Get_sys_count() & 0xF0)>>4);
					rand_blue =  ((Get_sys_count() & 0xF00)>>8);
					rand_green = ((Get_sys_count() & 0xF000)>>12);
					rgb_hex_set(i,rand_red<<20|rand_blue<<12|rand_green<<4);
					if (pos2AdjHex(address*18+i,1)!= -1)
					{
						rgb_hex_set(pos2AdjHex(address*18+i,1),rand_red<<20|rand_blue<<12|rand_green<<4);
					}
					if (pos2AdjHex(address*18+i,2) != -1)
					{
						rgb_hex_set(pos2AdjHex(address*18+i,2),rand_red<<20|rand_blue<<12|rand_green<<4);
					}
					rarity_display_error(i,address,0);	
					delay_ms(DISPLAY_DELAY);									
				}
			}
		}
		
		
		
		// Don't forget to check the middle thief.
		if (!ioport_get_pin_level(MIDDLE_SENSOR)){
			
			// MOAR FANCY GRAPHICS
			rand_red = ((Get_sys_count() & 0xF0)>>4);
			rand_blue =  ((Get_sys_count() & 0xF00)>>8);
			rand_green = ((Get_sys_count() & 0xF000)>>12);
			rgb_hex_set(18,rand_red<<20|rand_blue<<12|rand_green<<4);
			rarity_display_error(18,7,0);
			delay_ms(DISPLAY_DELAY);
		}		*/	
	}
	
	// Put the thief on the desert
	for (i=0;i<=18;i++)
	{
		if (Hex2Resource[i] == DESERT)
		{
			posSetOwner(7*18+i,1);	// Doesn't matter who owns the thief, so long as someone does
			setPosLegal(7*18+i);   // We should expect to see the thief on the sensor
			DesertHex = i;
		}
	}
}

void mainGameLoop(void)
{
	int8_t dice_rolled_flag = 0;
	uint32_t CPU_COUNT1,CPU_COUNT2;
	
	//// Make sure there is something for the first dice roll
	//s_memory[DIE_VALUE_REG] = roll_die();
	//assign_resources();
	refresh_display();
		
	while(1) {
		
		checkBoardState(dice_rolled_flag,dice_rolled_flag,dice_rolled_flag,0,0,0);
		if (last_pos_confirmed/18<7)
		{
			longestRoad();
			last_pos_confirmed = 0xFF;
		}
		
		// Check if the dice has been rolled
		if (isDiceRolled() && (dice_rolled_flag == 0)) {
			//s_memory[PI_EVENT_REG] = 0;
			if(s_memory[DIE_VALUE_REG] == 7) {
				while(!isKnightPlayed());
				s_memory[PI_EVENT_REG] = 0;
				// Move the thief
				moveThief();
			}
						
			dice_rolled_flag = 1;
			Hex2Rarity[DesertHex] = s_memory[DIE_VALUE_REG];
			refresh_display();	
			
		}
		// Check for knight cards played
		if (isKnightPlayed()) {
			s_memory[PI_EVENT_REG] = 0;
			moveThief();
			if (!dice_rolled_flag) {
				assign_resources();
			}
		}
		// Check for road building played
		if (isRoadBuildingPlayed()) {
			s_memory[PI_EVENT_REG] = 0;
			buildRoad(0,0);
			buildRoad(0,0);
			longestRoad();
		}
		// Check if a road was purchased
		if ((s_memory[PI_EVENT_REG] == PI_ROAD_PURCHASE) && (dice_rolled_flag)) {
			s_memory[PI_EVENT_REG] = 0;
			buildRoad(0,0);
			longestRoad();
		}
		if ((s_memory[PI_EVENT_REG] == PI_SETTLEMENT_PURCHASE) && (dice_rolled_flag)) {
			s_memory[PI_EVENT_REG] = 0;
			buildSettlement(0);
			longestRoad();
		}
		if ((s_memory[PI_EVENT_REG] == PI_CITY_PURCHASE) && (dice_rolled_flag)) {
			s_memory[PI_EVENT_REG] = 0;
			buildCity();
		}
		
		if (isTurnOver()) {
			s_memory[PI_EVENT_REG] = 0;
			dice_rolled_flag = 0;
			s_memory[DIE_VALUE_REG] = roll_die();
			assign_resources();
			Hex2Rarity[DesertHex] = -1;
			refresh_display();
		}
		if (s_memory[PI_EVENT_REG] == PI_END_GAME) {
			s_memory[PI_EVENT_REG] = 0;
			return;
		}
	}
}	

void checkBoardState(int8_t settlement, int8_t road, int8_t city, int8_t thief, int8_t initial_placement, uint8_t last_pos)
{
	uint8_t piecetype = 0;
	int8_t boardState = ALL_CONFIRMED;
	int8_t NewboardState = ALL_CONFIRMED;
	uint8_t pos_interest = 0xFF;
	uint8_t remove = 0;
	int8_t errorflg = 0;
	int8_t newflg = 0;
	uint8_t i,j,thief_index,k;
	ioport_port_mask_t RowReturn;
	uint16_t blink_counter = 0;
	uint8_t blink_state = 0;
	uint8_t hex0,hex1,hex2,res0,res1,res2;
	
	// No piece could have been rejected when we enter this function
	last_pos_rejected = 0xFF;
	
	while (1)
	{
		NewboardState = ALL_CONFIRMED;
		pos_interest = 0xFF;
		errorflg = 0;
		newflg = 0;
		remove = 0;
		piecetype = 0;
		
		//////////////////////////////////////////////////////////////////////////
		// Sensor Polling Loop
		// Check every Hall Effect sensor. Exit poll if error is found
		//////////////////////////////////////////////////////////////////////////
		
		for (j=0;(j<8)&&!(errorflg&&remove);j++) //&&!errorflag
		{
			// Grab the sensor data for every row
			ioport_set_port_level(HE_RETURN_PORT,HE_ADDR_PINS_MASK,j<<HE_ADDR_PIN_0);
			delay_ms(1);
			RowReturn = ioport_get_port_level(HE_RETURN_PORT,HE_RETURN_MASK);
			
			// Increment the blink counter
			blink_counter++;
			
			// Only need to check individual positions if the whole row does not match
			if (!compareLegal2Row(RowReturn,j))
			{
				for (i=0;(i<18)&&!(errorflg&&remove);i++) //&&!errorflag
				{
					
					// If the sensor value is not the same as what we have in the legal state, see if it's a legal move
					if ((RowReturn & 1<<ColPins[i])!=(getLegalRow(j)& 1<<ColPins[i]))
					{
						// Is the piece present or gone?
						remove = (RowReturn>>ColPins[i])&1;
												
						// Are we in the initial placement phase or normal game play? (also update position of interest)
						if (initial_placement)
						{
							if (isLegalInit(j*18+i,settlement,road,last_pos))
							{
								newflg = 1;
								if (!errorflg)
								{
									pos_interest = j*18+i;
								}
							}
							else
							{
								if (!errorflg || remove)
								{
									pos_interest = j*18+i;
								}
								errorflg = 1;
								
							}
						}
						else
						{
							if (isLegal(j*18+i,settlement,road,city,thief,last_pos))
							{
								newflg = 1;
								if (!errorflg)
								{
									pos_interest = j*18+i;
								}
							}
							else
							{								
								if (!errorflg || remove)
								{
									pos_interest = j*18+i;
								}
								errorflg = 1;
							}
						}
					}
				}
			}
		}
		// Don't forget to check the middle thief.
		if (!(errorflg&&remove))
		{
			if ( (!ioport_get_pin_level(MIDDLE_SENSOR) && !pos2Owner(MIDDLE_THIEF_POS)) || (ioport_get_pin_level(MIDDLE_SENSOR)&& pos2Owner(MIDDLE_THIEF_POS)))
			{
				// Definitely an interesting position
				remove = !pos2Owner(MIDDLE_THIEF_POS);
				if (initial_placement)
				{
					if (!errorflg || remove)
					{
						pos_interest = MIDDLE_THIEF_POS;
					}
					errorflg = 1;
				}
				else
				{
					if (isLegal(MIDDLE_THIEF_POS,settlement,road,city,thief,last_pos))
					{
						newflg = 1;
						if (!errorflg)
						{
							pos_interest = MIDDLE_THIEF_POS;
						}
					}
					else
					{
						if (!errorflg || remove)
						{
							pos_interest = MIDDLE_THIEF_POS;
						}
						errorflg = 1;
					}
				}
			}
		}
		

		
		//////////////////////////////////////////////////////////////////////////
		// End Sensor Polling loop
		//////////////////////////////////////////////////////////////////////////
		
		// Set the new board state based on the findings from above
		if (errorflg)
		{
			NewboardState = ERROR;
		}
		else if (newflg)
		{
			NewboardState = NEW_PIECE;			
		}
		else
		{
			NewboardState = ALL_CONFIRMED;
		}
		
		// See if something has changed from the last time we checked the board
		if ((NewboardState != boardState) || ((pos_interest != s_memory[NEW_PIECE_LOC_REG]) && (pos_interest != last_pos_confirmed)))
		{
			// Refresh the board to be ready to add new things
			refresh_display();
			// Reset the blink counter
			blink_counter = 0;
			blink_state = 1;
			
			// initialize the relevant I2C registers
			s_memory[NEW_PIECE_LOC_REG] = pos_interest;
			s_memory[PIECE_TYPE_REG] = 0;
			s_memory[NEW_PIECE_PORT_REG] = pos2Port(pos_interest);
			//s_memory[PLAYERS_THIEFED_REG] = 0;
			
			// That is all we have to do if everything is ALL CONFIRMED, otherwise:
			if ((NewboardState == ERROR)||(NewboardState == NEW_PIECE))
			{
				// If the piece is in error, do we need to remove or replace it?
				if (NewboardState == ERROR)
				{
					if (remove)
					{
						piecetype = PIECE_TYPE_REMOVE;
					}
					else
					{
						piecetype = PIECE_TYPE_REPLACE;
					}
				}
				// If it's not in error, it must need to be confirmed
				else
				{
					piecetype = PIECE_TYPE_TBC;
				}
				
				//// Make the board's display reflect the change with both color and pointing
				if (pos_interest == MIDDLE_THIEF_POS) {
					rgb_hex_set(18,NewboardState == ERROR ? COLOR_ERROR : COLOR_CONFIRM);
					rarity_display_error(18,7,0);
				} else {
					// Display error to all adjacent hexes
					for (k=0;k<BLINK_RANGE;k++) {
						if (pos2AdjHex(pos_interest,k)!=-1) {
							rgb_hex_set(pos2AdjHex(pos_interest,k),NewboardState == ERROR ? COLOR_ERROR : COLOR_CONFIRM);
						}
					}
					//rgb_hex_set(pos_interest % 18,NewboardState == ERROR ? COLOR_ERROR : COLOR_CONFIRM );
					switch (city_map[pos_interest])
					{
						case 0:
						rarity_display_error(pos_interest % 18,pos_interest/18,0);			
						break;
						case 1:
						if (piecetype == PIECE_TYPE_TBC)
						{
							rarity_display_error(pos_interest % 18,pos_interest/18,1);
						}
						else
						{
							rarity_display_error(pos_interest % 18,pos_interest/18,0);
						}
						break;
						case 2:
						rarity_display_error(pos_interest % 18,pos_interest/18,1);
					}
				}
				
				// Assign the I2C registers differently depending on what type of piece we are looking at
				
				// Type = Thief
				if (pos_interest/18>=7)
				{
					s_memory[PIECE_TYPE_REG] = piecetype + PIECE_TYPE_THIEF;
					// Need to tell Pi all the players that can be thieved at this position
					s_memory[PLAYERS_THIEFED_REG] = 0;
					if (pos_interest == MIDDLE_THIEF_POS)
					{
						// Check the positions adjacent to the middle thief if it's the middle thief that is of interest
						for (k=0;k<6;k++)
						{
							if (pos2Owner(MiddleThiefAdjSettlements[k]))
							{
								s_memory[PLAYERS_THIEFED_REG] = s_memory[PLAYERS_THIEFED_REG] | 1<<(pos2Owner(MiddleThiefAdjSettlements[k])-1);
							}
						}
					}
					else
					{
						// For other hexes, first check cities/settlements on same MUX
						for (k=1;k<7;k+=2)
						{
							if (pos2Owner(k*18+pos_interest%18))
							{
								s_memory[PLAYERS_THIEFED_REG] = s_memory[PLAYERS_THIEFED_REG] | 1<<(pos2Owner(k*18+pos_interest%18)-1);
							}
						}
						
						// Then check the hexes not on the same MUX
						for (k=0;k<3;k++)
						{
							if (pos2Owner(pos2AdjPos(pos_interest,k)))
							{
								s_memory[PLAYERS_THIEFED_REG] = s_memory[PLAYERS_THIEFED_REG] | 1<<(pos2Owner(pos2AdjPos(pos_interest,k))-1);
							}
						}
					}					
				}
				
				// Type = Road
				else if ((pos_interest/18)%2 == 0)
				{
					s_memory[PIECE_TYPE_REG] = piecetype + PIECE_TYPE_ROAD;
				}
				
				// Type = Settlement or City
				else
				{
					switch (city_map[pos_interest])
					{
						case 0:
							s_memory[PIECE_TYPE_REG] = piecetype + PIECE_TYPE_SETTLEMENT;
							break;
						case 1:
							if (piecetype == PIECE_TYPE_TBC)
							{
								s_memory[PIECE_TYPE_REG] = piecetype + PIECE_TYPE_CITY;
							}
							else
							{
								s_memory[PIECE_TYPE_REG] = piecetype + PIECE_TYPE_SETTLEMENT;
							}
							break;
						case 2:
							s_memory[PIECE_TYPE_REG] = piecetype + PIECE_TYPE_CITY;
					}
				}
				
				//Now that a new error or new piece was detected, and all the register update, need to alert PI
				if (NewboardState == NEW_PIECE)
				{
					if (s_memory[PIECE_TYPE_REG] % PIECE_TYPE_TBC == PIECE_TYPE_THIEF)
					{
						s_memory[MCU_EVENT_REG] = MCU_NEW_THIEF_TBC;
					}
					else 
					{
						s_memory[MCU_EVENT_REG] = MCU_NEW_PIECE_TBC;
					}
					// Alert the Pi that something should be confirmed
					ioport_set_pin_level(I2C_FLAG,true);
				}
				else
				{				
					s_memory[MCU_EVENT_REG] = MCU_ERROR;
				}
								
			}
			// If something's changed, but it's not a new or illegal piece, the whole board is all confirmed
			else
			{
				s_memory[MCU_EVENT_REG] = MCU_ALL_CLEAR;
			}
			
		}
		
		boardState = NewboardState;
		
		//////////////////////////////////////////////////////////////////////////
		// Blink logic
		//////////////////////////////////////////////////////////////////////////
		if (blink_counter > BLINK_RATE) {
			blink_counter = 0;
			if (blink_state) {
				blink_state = 0;
				// Make the board's display reflect the change with both color and pointing
				for (k=0;k<BLINK_RANGE;k++) {
						rgb_hex_set_variable(pos2AdjHex(pos_interest,k),COLOR_BLACK,0);
				}
				refresh_display();
			} else {

				blink_state = 1;
				for (k=0;k<BLINK_RANGE;k++) {
					rgb_hex_set_variable(pos2AdjHex(pos_interest,k),COLOR_BLACK,0);
				}
				// Make the board's display reflect the change with both color and pointing
				if (pos_interest == MIDDLE_THIEF_POS) {
					rgb_hex_set(18,NewboardState == ERROR ? COLOR_ERROR : COLOR_CONFIRM);
					rarity_display_error(18,7,0);
				} else {
					// Display error to all adjacent hexes
					for (k=0;k<BLINK_RANGE;k++) {
						if (pos2AdjHex(pos_interest,k)!=-1) {
							rgb_hex_set(pos2AdjHex(pos_interest,k),NewboardState == ERROR ? COLOR_ERROR : COLOR_CONFIRM);
						}
					}
					//rgb_hex_set(pos_interest % 18,NewboardState == ERROR ? COLOR_ERROR : COLOR_CONFIRM );
					switch (city_map[pos_interest])
					{
						case 0:
						rarity_display_error(pos_interest % 18,pos_interest/18,0);
						break;
						case 1:
						if (s_memory[PIECE_TYPE_REG] / PIECE_TYPE_TBC == 1)
						{
							rarity_display_error(pos_interest % 18,pos_interest/18,1);
						}
						else
						{
							rarity_display_error(pos_interest % 18,pos_interest/18,0);
						}
						break;
						case 2:
						rarity_display_error(pos_interest % 18,pos_interest/18,1);
					}
				}
			}			
		}
		
		// Don't leave check board state unless the entire board has confirmed pieces
		if (boardState == ALL_CONFIRMED)
		{
			return;
		}
		
	}
	
	
			
}

void refresh_display(void){
	for (int i=0;i<=18;i++)
	{
		rgb_display_resource(i,Hex2Resource[i]);
		rarity_set(i,Hex2Rarity[i]);
	}
}			

uint8_t roll_die(void){
	// roll 2 dice, add them together, return result
	unsigned long cycles_count;
	uint8_t diceValue1,diceValue2;
	cycles_count = Get_sys_count();
	diceValue1 = ((cycles_count & 0xFF0)>>4) % 6 + 1;
	diceValue2 = ((cycles_count & 0xFF00)>>8) % 6 + 1;
	return diceValue1+diceValue2;
}

int8_t isLegalInit (uint8_t pos, int8_t settlement, int8_t road, uint8_t last_settlement_pos){
	int8_t i,j;
	// Check if position is on the board
	if ((pos > MIDDLE_THIEF_POS) || (pos < 0)) { return 0; }
	// Make sure the position is not the last position that was rejected
	if (pos == last_pos_rejected){return 0;}
	// First determine the type of piece based on the position#
	// row even -- a road
	if (((pos/18) % 2) == 0) {
		// If the road already has an owner, it's being removed, and therefore is not legal
		if (!pos2Owner(pos) && road)
		{
			// check both adjacent cities. If either owned by player and the last settlement placed, it's a legal play
			if ((pos2Owner(pos2AdjPos(pos,0))==s_memory[CURRENT_PLAYER_REG]) && (pos2AdjPos(pos,0) == last_settlement_pos))
			{
				
				return 1;
			}
			if ((pos2Owner(pos2AdjPos(pos,1))==s_memory[CURRENT_PLAYER_REG]) && (pos2AdjPos(pos,1) == last_settlement_pos))
			{
				
				return 1;
			}		
		}
	}
	// Thieves not allowed
	else if ((pos/18) >= 7)
	{
		
		return 0;
		
	}
	// row odd and not thief -- a settlement or city
	else if (((pos/18) % 2) == 1) {
		// If the settlement already has an owner, it's being removed, and therefore is not legal
		if (!pos2Owner(pos) && settlement) {
			// If a settlement adjacent to the position, it is not legal
			for (i=0;i<3;i++) {
				// Be sure that the if the settlement is on the edge it only examines 2 positions
				if (pos2AdjPos(pos,i)!=-1) {
					for (j=0;j<2;j++) {
						// Exclude itself from the adjacent check of adjacent roads
						if (pos2AdjPos(pos2AdjPos(pos,i),j)!=pos) {
							if (pos2Owner(pos2AdjPos(pos2AdjPos(pos,i),j))) {
								// If the adjacent settlement is already owned, this placement is illegal
								
								return 0;
							}
						}
					}
				}
			}
			// No conflicts with adjacent cities, therefore legal
			
			return 1;
		}		
	}

	// No legal situations found, return false
	return 0;
}

int8_t isLegal (uint8_t pos, int8_t settlement, int8_t road, int8_t city, int8_t thief, uint8_t thief_pos_last) {
	int8_t i,j;
	// Check if position is on the board
	if ((pos > MIDDLE_THIEF_POS) || (pos < 0)) { return 0; }
	// Make sure it wasn't the last position rejected
	if (pos == last_pos_rejected){return 0;}
	
	// First determine the type of piece based on the position#
	// Position is a thief
	if (pos/18 >= 7) { 
		
		// Are thieves even allowed to be placed? And has it been moved?
		if (thief && (thief_pos_last!=pos))
		{
			return 1;
		}
	}
	
	// row even -- a road
	else if (((pos/18) % 2) == 0) { 
		// If the road already has an owner, it's being removed, and therefore is not legal
		if (!pos2Owner(pos) && road)
		{
			// If the player doesn't have any roads left, it can't be legal
			if (!pieces_remaining[s_memory[CURRENT_PLAYER_REG]-1][0])
			{
				return 0;
			}
			// check both adjacent cities first. If either owned by player, it's a legal play
			if ((pos2Owner(pos2AdjPos(pos,0))==s_memory[CURRENT_PLAYER_REG]) || (pos2Owner(pos2AdjPos(pos,1))==s_memory[CURRENT_PLAYER_REG]) )
			{
				return 1;
			}
			// Now check the adjacent roads, but only if they are not blocked by another player's settlement or city
			else
			{
				if (!pos2Owner(pos2AdjPos(pos,0)))
				{
					for (i=0;i<3;i++)
					{
						if ((pos2AdjPos(pos2AdjPos(pos,0),i)!=-1) && (pos2AdjPos(pos2AdjPos(pos,0),i)!= pos))
						{
							if (pos2Owner(pos2AdjPos(pos2AdjPos(pos,0),i)) == s_memory[CURRENT_PLAYER_REG])
							{
								return 1;
							}
						}
					}
				}
				if (!pos2Owner(pos2AdjPos(pos,1)))
				{
					for (i=0;i<3;i++)
					{
						if ((pos2AdjPos(pos2AdjPos(pos,1),i)!=-1) && (pos2AdjPos(pos2AdjPos(pos,1),i)!= pos))
						{
							if (pos2Owner(pos2AdjPos(pos2AdjPos(pos,1),i)) == s_memory[CURRENT_PLAYER_REG])
							{
								return 1;
							}
						}
					}
				}
			}
			
			
			
		}
		
	}
	// row odd and not thief -- a settlement or city
	else if (((pos/18) % 2) == 1) { 
		// If the settlement already has an owner, it's being removed, and therefore is not legal
		if (!pos2Owner(pos) && settlement) {
			// If the player doesn't have any settlements left, it can't be legal
			if (!pieces_remaining[s_memory[CURRENT_PLAYER_REG]-1][1])
			{
				return 0;
			}
			// If a settlement adjacent to the position, it is not legal
			for (i=0;i<3;i++) {
				// Be sure that the if the settlement is on the edge it only examines 2 positions
				if (pos2AdjPos(pos,i)!=-1) { 
					for (j=0;j<2;j++) {
						// Exclude itself from the adjacent check of adjacent roads 
						if (pos2AdjPos(pos2AdjPos(pos,i),j)!=pos) { 
							if (pos2Owner(pos2AdjPos(pos2AdjPos(pos,i),j))) {
								// If the adjacent settlement is already owned, this placement is illegal
								return 0;
							}							
						}
					}					  
				}				  
			}
			
			// check all adjacent roads. If any are owned by current player, it's a legal play
			for (i=0;i<3;i++) {
				if (pos2AdjPos(pos,i)!=-1) {
					if ((pos2Owner(pos2AdjPos(pos,i)))==s_memory[CURRENT_PLAYER_REG]) {
						return 1;
					}
				}
			}
		}
		// If the settlement already has an owner and that owner is the current player and cities are allowed, then it is legal
		else if ((pos2Owner(pos) == s_memory[CURRENT_PLAYER_REG]) && city)
		{
			// If the player doesn't have any cities left, it can't be legal
			if (!pieces_remaining[s_memory[CURRENT_PLAYER_REG]-1][2])
			{
				return 0;
			}
			// Need to make sure what is being removed is a settlement and not a city
			if (city_map[pos] == 1)
			{
				return 1;
			}
		}
	}	

	// No legal situations found, return false 
	return 0;
}

void assign_resources(void)
{
	// Should assign the resources to the resources to receive registers so the Pi can retrieve them
	uint8_t i,j,k;	//i=row, j= column (hex), k = adjacent hex number
	
	// Clear the resources received register
	for (i=0;i<20;i++)
	{
		s_memory[RESOURCE_REC_REG+i] = 0;
	}
	
	// Only need to look at rows which contain cities or settlements
	for (i=1;i<7;i+=2)
	{
		for (j=0;j<=18;j++)
		{
			// Only add resources from positions that are owned
			if (pos2Owner(i*18+j))
			{
				// For each adjacent hex, make sure the adjacent hexes exist and that they have valid resources and rarities
				for (k=0;k<3;k++)
				{
					if (pos2AdjHex(i*18+j,k)!=-1)
					{
						if ((Hex2Resource[pos2AdjHex(i*18+j,k)] < 6) && (Hex2Resource[pos2AdjHex(i*18+j,k)] > -1))
						{
							// Only assign resource if it is the same as the current dice value
							if (Hex2Rarity[pos2AdjHex(i*18+j,k)] == s_memory[DIE_VALUE_REG])
							{
								s_memory[RESOURCE_REC_REG+(pos2Owner(i*18+j)-1)*5+Hex2Resource[pos2AdjHex(i*18+j,k)]] += city_map[i*18+j];	
							}							
						}
					}
				}				
			}
		}
	}
	
	// Now need to subtract resources hidden by thief
	// Check each thief position (don't forget middle thief at end
	for (j=0;j<18;j++)
	{
		// wait for the hex that actually has a thief on it (thief owner is meaningless except to tell it exists)
		if (pos2Owner(126+j))
		{
			// Make sure the thief actually affects the next roll
			if (Hex2Rarity[j]==s_memory[DIE_VALUE_REG])
			{
				// Make sure the resource value was assigned correctly
				if ((Hex2Resource[j] < 6) && (Hex2Resource[j] > -1))
				{
					// 1st check the three cities on the same MUX
					for (i=1;i<7;i+=2)
					{
						// And if they are owned, subtract them from the total
						if (pos2Owner(i*18+j))
						{
							s_memory[RESOURCE_REC_REG+(pos2Owner(i*18+j)-1)*5+Hex2Resource[j]] -= city_map[i*18+j];
						}							
					}
					// 2nd check the three cities on different MUX's
					for (i=0;i<3;i++)
					{
						if (pos2AdjPos(126+j,i) != -1)
						{
							// And if they are owned, subtract them from the total
							if (pos2Owner(pos2AdjPos(126+j,i)))
							{
								s_memory[RESOURCE_REC_REG+(pos2Owner(pos2AdjPos(126+j,i))-1)*5+Hex2Resource[j]] -= city_map[pos2AdjPos(126+j,i)];
							}
						}
					}
				}
			}
		}
	}
	
	// Middle Thief Check
	if (pos2Owner(145))
	{
		// Make sure the thief actually affects the next roll
		if (Hex2Rarity[j]==s_memory[DIE_VALUE_REG])
		{
			// Make sure the resource value was assigned correctly
			if ((Hex2Resource[j] < 6) && (Hex2Resource[j] > -1))
			{
				// check all six city positions adjacent
				for (i=0;i<6;i++)
				{
					// And if they are owned, subtract them from the total
					if (pos2Owner(MiddleThiefAdjSettlements[i]))
					{
						s_memory[RESOURCE_REC_REG+(pos2Owner(MiddleThiefAdjSettlements)-1)*5+Hex2Resource[j]] -= city_map[MiddleThiefAdjSettlements[i]];
					}					
				}
			}
		}
	}
}

void assign_initial_resources(int pos)
{
	// Should assign the resources to the resources to receive registers so the Pi can retrieve them
	uint8_t i;
	
	for (i=0;i<3;i++)
	{
		// Assign the resources to the proper register for each of the 3 adjacent hexes
		if(pos2AdjHex(pos,i)!=-1) {
			s_memory[RESOURCE_REC_REG+(pos2Owner(pos)-1)*5+Hex2Resource[pos2AdjHex(pos,i)]]++;
		}		
	}
	
}

void show_remaining_piece(void)
{
	uint8_t i;
	for (i=0;i<12;i++)
	{
		s_memory[RESOURCE_REC_REG+i]=pieces_remaining[i/3][i%3];
	}
	
}

uint8_t buildRoad(int8_t initial_placement, uint8_t last_settlement)
{
	uint8_t temp_pos;
	last_pos_confirmed = 0xFF;
	while(last_pos_confirmed == 0xFF) {
		checkBoardState(0,1,0,0,initial_placement,last_settlement);
	}
	temp_pos = last_pos_confirmed;
	last_pos_confirmed = 0xFF;
	return temp_pos;
}

uint8_t buildSettlement(int8_t initial_placement)
{
	uint8_t temp_pos;
	last_pos_confirmed = 0xFF;
	while(last_pos_confirmed == 0xFF) {
		checkBoardState(1,0,0,0,initial_placement,0xFF);
	}
	temp_pos = last_pos_confirmed;
	last_pos_confirmed = 0xFF;
	return temp_pos;
}

uint8_t buildCity()
{
	uint8_t temp_pos;
	last_pos_confirmed = 0xFF;
	while(last_pos_confirmed == 0xFF) {
		checkBoardState(0,0,1,0,0,0xFF);
	}
	temp_pos = last_pos_confirmed;
	last_pos_confirmed = 0xFF;
	return temp_pos;
}

uint8_t moveThief()
{
	uint8_t last_thief_pos;
	uint8_t temp_pos;
	uint8_t i;
	for (i=7*18;i<=MIDDLE_THIEF_POS;i++)
	{
		if (pos2Owner(i)) {
			last_thief_pos = i;
		}
	}
	posSetOwner(last_thief_pos,0);
	clearPosLegal(last_thief_pos);
	last_pos_confirmed = 0xFF;
	while(last_pos_confirmed == 0xFF) {
		checkBoardState(0,0,0,1,0,last_thief_pos);
	}
	temp_pos = last_pos_confirmed;
	last_pos_confirmed = 0xFF;
	return temp_pos;
}

void confirmNewPiece(void)
{
	setPosLegal(s_memory[NEW_PIECE_LOC_REG]);
	posSetOwner(s_memory[NEW_PIECE_LOC_REG],s_memory[CURRENT_PLAYER_REG]);	
	last_pos_confirmed = s_memory[NEW_PIECE_LOC_REG];
	
	if (s_memory[NEW_PIECE_LOC_REG]/18 >= 7)
	{
		// Do something for thieves.
		// Thief Placement affects resource distribution, redo resources
	}
	else if ((s_memory[NEW_PIECE_LOC_REG]/18)%2 == 0)
	{
		
		// Add road to the roadmap
		//			[ Current Player ]				      [ Road #]									[Adjacent City #]	=		[Adjacent City]
		roadmap[s_memory[CURRENT_PLAYER_REG]-1][(uint8_t)15-pieces_remaining[s_memory[CURRENT_PLAYER_REG]-1][0]][0]=pos2AdjPos(s_memory[NEW_PIECE_LOC_REG],0);
		roadmap[s_memory[CURRENT_PLAYER_REG]-1][(uint8_t)15-pieces_remaining[s_memory[CURRENT_PLAYER_REG]-1][0]][1]=pos2AdjPos(s_memory[NEW_PIECE_LOC_REG],1);
		// Reduce the number of roads that player has remaining
		pieces_remaining[s_memory[CURRENT_PLAYER_REG]-1][0]--;
		// Do something for roads
		
		// Road placement affects longest road
		//s_memory[DEBUG_REG] = longestRoad();		// Placeholder function
		//longestRoad();
	}
	else 
	{
		// Do something for settlements/cities
		// Upgrade city status of position (nothing to settlement or settlement to city)
		city_map[s_memory[NEW_PIECE_LOC_REG]]++;
		
		// Reduce the number of settlements or cities that player has remaining
		if (city_map[s_memory[NEW_PIECE_LOC_REG]]>1)
		{
			// Remove a city, refill a settlement
			pieces_remaining[s_memory[CURRENT_PLAYER_REG]-1][2]--;
			pieces_remaining[s_memory[CURRENT_PLAYER_REG]-1][1]++;
		}
		else
		{
			// Remove a settlement
			pieces_remaining[s_memory[CURRENT_PLAYER_REG]-1][1]--;
		}
		
		// Settlement placement affects resource distribution
		// Settlement placement can affect longest road
		//s_memory[DEBUG_REG] = longestRoad();		// Placeholder function
		//longestRoad();
	}
	
	// Clear new piece location registers
	s_memory[NEW_PIECE_LOC_REG] = -1;
	s_memory[PIECE_TYPE_REG] = 0;
	s_memory[NEW_PIECE_PORT_REG] = -1;
	// s_memory[PLAYERS_THIEFED_REG] = 0;
	
}

void rejectNewPiece(void)
{
	last_pos_rejected = s_memory[NEW_PIECE_LOC_REG];
}

uint8_t longestRoad(void)
{
	uint8_t player_i,road_i,branch_i;
	uint8_t branchcount;
	uint8_t branchlength = 0;
	uint8_t longestbranch[4] = {0};
	uint8_t longestroad = 4;
	uint8_t longestOwnerNew;
	
	for (player_i=0;player_i<s_memory[PLAYER_COUNT_REG];player_i++)
	{
		// No need to find longest road for a player if they don't even have five roads on the board
		if (pieces_remaining[player_i][0]<11)
		{
			for (road_i=0;road_i<(15-pieces_remaining[player_i][0]);road_i++)
			{
				// First, see if one of the ends of the road is an endpoint
				for (branch_i=0;branch_i<3;branch_i++)
				{
					if (pos2Owner(pos2AdjPos(roadmap[player_i][road_i][0],branch_i)) == player_i+1)
					{
						branchcount++;
					}
				}
				// Only need to test one side or the other, but not both.
				if (branchcount%2 != 1)
				{
					branchlength = maxBranch(player_i+1,road_i,roadmap[player_i][road_i][0]);
				}
				else
				{
					branchlength = maxBranch(player_i+1,road_i,roadmap[player_i][road_i][1]);
				}
				// See if the count of roads along this branch is longer than any up to this point
				if (branchlength>longestbranch[player_i])
				{
					longestbranch[player_i] = branchlength;
				}
			}
		}
		else
		{
			longestbranch[player_i] = 0;
		}
		
		// Decide who gets longest road
		// If you have the most roads, you definitely have the longest road
		if (longestbranch[player_i]>longestroad)
		{
			longestroad = longestbranch[player_i];
			longestOwnerNew = player_i +1;
		}
		
		// If you have the same number or roads as someone else there's a matter of precedence
		else if (longestbranch[player_i] == longestroad)
		{
			// If you used to have longest road, you get to keep it
			if (longestRoadOwnerPrev == player_i+1)
			{
				longestOwnerNew = longestRoadOwnerPrev;
			}
			// If you weren't the previous holder and the other person who currently holds longest road isn't either, no one holds it
			else if (longestOwnerNew != longestRoadOwnerPrev)
			{
				longestOwnerNew = 0;
			}
			
		}
	}
	if (longestroad<5)
	{
		longestOwnerNew = 0;
	}
	// Only need to make updates if longest road has changed.
	if (longestRoadOwnerPrev != longestOwnerNew)
	{
		longestRoadOwnerPrev = longestOwnerNew;
		s_memory[LONGEST_ROAD_REG] = longestRoadOwnerPrev;
		s_memory[MCU_EVENT_REG] = MCU_NEW_LONG_ROAD;
		ioport_set_pin_level(I2C_FLAG,true);
	}
	
	return longestroad;
	
}

uint8_t maxBranch(uint8_t player, uint8_t road_index, uint8_t city_link)
{
	// This function should calculate the longest branch from a road using roadmap
	uint8_t i;
	uint8_t branch_count;
	uint8_t branch_length,max_branchlength;
	

	// First check to make sure some other player's settlement isn't blocking this road
	if ((pos2Owner(city_link)!=player) && (pos2Owner(city_link)!=0))
	{
		return 1;
	}
	// Second, make sure there is at least two roads branching from this city, otherwise its an endpoint and branchlength is nothing
	branch_count = 0;
	for (i=0;i<3;i++)
	{
		if (pos2Owner(pos2AdjPos(city_link,i)) == player)
		{			
			branch_count++;
		}
	}
	if (branch_count<2)
	{
		return 1;
	}
	
	// Now we have to find which of the remaining roads connect to this road
	branch_length = 0;
	max_branchlength = 0;
	roadmap[player-1][road_index][2] = 1;			// Mark the road, we've already traversed it
	for (i=0;i<(15-pieces_remaining[player-1][0]);i++)
	{
		branch_length = 0;
		// Don't traverse road if it's already marked
		if (!roadmap[player-1][i][2])
		{
			if (roadmap[player-1][i][0] == city_link)
			{
				branch_length = maxBranch(player,i,roadmap[player-1][i][1]);
			}
			else if (roadmap[player-1][i][1] == city_link)
			{
				branch_length = maxBranch(player,i,roadmap[player-1][i][0]);
			}
			if (branch_length>max_branchlength)
			{
				max_branchlength = branch_length;
			}
		}
	}
	// Unmark the road
	roadmap[player-1][road_index][2] = 0;

	return max_branchlength+1;
}

// Functions to access the Static Map
int rowCol2Pos(int row, int col) {
	int pos = row*18+col;
if ((pos > MIDDLE_THIEF_POS) || (pos < 0)) { return -1; }
return (pos);
}

int pos2AdjPos(int pos, int adj_num) {
	if ((pos > MIDDLE_THIEF_POS) || (pos < 0)) { return -1; }
	if ((adj_num > 2) || (adj_num < 0)) { return -1; }
	return (pos_map[pos][adj_num]);
}

int pos2AdjHex(int pos, int adj_num) {
    if ((pos > MIDDLE_THIEF_POS) || (pos < 0)) { return -1; }
	if ((adj_num > 2) || (adj_num < 0)) { return -1; }
    
	return (pos_map[pos][adj_num+3]);
}

int pos2Port(int pos) {
	if ((pos > MIDDLE_THIEF_POS) || (pos < 0)) { return -1; }
    return(pos_map[pos][6]);
}
// Functions to access the position owners
int pos2Owner(int pos) {
    if ((pos > MIDDLE_THIEF_POS) || (pos < 0)) { return -1; }
    return (owner_map[pos]);
}

void posSetOwner(int pos, int owner) {
    if ((pos <= MIDDLE_THIEF_POS) && (pos >= 0)) {
      if ((owner <= 4) && (owner >= 0)) {
	    owner_map[pos] = owner;
	  }
	}	  		
}

void setPosLegal(int pos){
	if ((pos<=MIDDLE_THIEF_POS) && (pos >=0))
	{
		legalBoardState[pos/18] = legalBoardState[pos/18] | 1<<ColPins[pos%18];
	}
}

void clearPosLegal(int pos){
	if ((pos<=MIDDLE_THIEF_POS) && (pos >=0))
	{
		legalBoardState[pos/18] = legalBoardState[pos/18] & ~(1<<ColPins[pos%18]);
	}
}

ioport_port_mask_t getLegalRow(int row){
	if ((row<=7) && (row>=0))
	{
		return legalBoardState[row];
	}
}

int	compareLegal2Row(ioport_port_mask_t senseRow, int row){
	if ((row<=7) && (row>=0))
	{
		if (senseRow == legalBoardState[row])
		{
			return 1;
		}
		
		return 0;
	}
}

void AdjHexTest( void ) {
	uint8_t i;
	uint8_t address;
	// Hall Effect Sensor
	ioport_port_mask_t RowReturn;
	//int ColPins[]= {HE_COL0,HE_COL1,HE_COL2,HE_COL3,HE_COL4,HE_COL5,HE_COL6,HE_COL7, HE_COL8,HE_COL9,HE_COL10,HE_COL11,HE_COL12,HE_COL13,HE_COL14,HE_COL15,HE_COL16,HE_COL17};
	
	//initialize board at nothing
	rgb_clear_all();
	rarity_clear_all();
	for (address=0;address<8;address++)
	{

		// Grab the sensor data for every row
		ioport_set_port_level(HE_RETURN_PORT,HE_ADDR_PINS_MASK,address<<HE_ADDR_PIN_0);
		delay_ms(.1);
		RowReturn = ioport_get_port_level(HE_RETURN_PORT,HE_RETURN_MASK);
	
		// Check each hex (Hex# = i)
		for (i=0;i<18;i++)
		{
			if (RowReturn & 1<<ColPins[i])
			{
			
				// TEST CODE TO CHECK THE Adj HEX MAP
				// Light RGBs on adjacent hexes
				if (pos2AdjHex(rowCol2Pos(address,i),0) != -1) {
					rgb_hex_set(pos2AdjHex(rowCol2Pos(address,i),0),COLOR_WHEAT);
				} 
				if (pos2AdjHex(rowCol2Pos(address,i),1) != -1) {
					rgb_hex_set(pos2AdjHex(rowCol2Pos(address,i),1),COLOR_WHEAT);
				}
				if (pos2AdjHex(rowCol2Pos(address,i),2) != -1 ) {
					rgb_hex_set(pos2AdjHex(rowCol2Pos(address,i),2),COLOR_WHEAT);
				}
			
				// display error code on adjacent positions
				if (pos2AdjPos(rowCol2Pos(address,i),0) != -1) {
					rarity_display_error(pos2AdjPos(rowCol2Pos(address,i),0)%18,pos2AdjPos(rowCol2Pos(address,i),0)/18,0);
					delay_ms(500);
					rarity_clear_all();
				}
				if (pos2AdjPos(rowCol2Pos(address,i),1) != -1) {
					rarity_display_error(pos2AdjPos(rowCol2Pos(address,i),1)%18,pos2AdjPos(rowCol2Pos(address,i),1)/18,0);
					delay_ms(500);
					rarity_clear_all();
				}
				if (pos2AdjPos(rowCol2Pos(address,i),2) != -1) {
					rarity_display_error(pos2AdjPos(rowCol2Pos(address,i),2)%18,pos2AdjPos(rowCol2Pos(address,i),2)/18,0);
					delay_ms(500);
					rarity_clear_all();
				}
				delay_ms(100);
			
				//delay_ms(250);
				rgb_hex_set(pos2AdjHex(rowCol2Pos(address,i),0),COLOR_BLACK);
				rarity_clear_all();
				if (pos2AdjHex(rowCol2Pos(address,i),1) != -1) {
					rgb_hex_set(pos2AdjHex(rowCol2Pos(address,i),1),COLOR_BLACK);
				}
				if (pos2AdjHex(rowCol2Pos(address,i),2) != -1 ) {
					rgb_hex_set(pos2AdjHex(rowCol2Pos(address,i),2),COLOR_BLACK);
				}
			}
		}
	}
	if (!ioport_get_pin_level(MIDDLE_SENSOR))
	{
		rgb_hex_set(18,COLOR_WHEAT);
		for (i=0;i<6;i++)
		{
			rarity_display_error(MiddleThiefAdjSettlements[i]%18,MiddleThiefAdjSettlements[i]/18,0);
			delay_ms(500);
			rarity_clear_all();
		}
		rgb_hex_set(18,COLOR_BLACK);
	}
			
}

void PortTest() {
	int i;
	for (i=0; i<145; i++) {
		if (pos2Port(i) != -1) {
			rgb_display_resource(pos2AdjHex(i,0),pos2Port(i));
			rarity_display_error(pos2AdjHex(i,0),i/18,0);
			delay_s(6);
			rgb_clear_all();
			rarity_clear_all();
		}
	}
}

void TestGameSetup(void){
	uint8_t resource_order[] = {ORE,WHEAT,SHEEP,WHEAT,BRICK,WOOD,ORE,SHEEP,SHEEP,WOOD,BRICK,WHEAT,ORE,BRICK,SHEEP,DESERT,WOOD,WHEAT,WOOD};
	uint8_t hex_order[] =		{0,1,3,5,16,17,8, 9,10,11,12,15,14,2,4,6,7,13,18};		// Used to lay out rarity values
	uint8_t rarity_order[] =	{5,2,6,3, 8,10,9,12,11, 4, 8,-1,10,9,4,5,6, 3,11};
	uint8_t i,j;
	//                    p1 pieces      p2 pieces     p3 pieces
	uint8_t ppos[3][4] = {{106,102,6,84},{60,56,42,74},{97,68,108,79}};
	s_memory[PLAYER_COUNT_REG] = 3;
	
	s_memory[DEBUG_REG] = 0xFF;
	
	for (i=0;i<19;i++)
	{
		Hex2Resource[i]=resource_order[i];
		Hex2Rarity[hex_order[i]] = rarity_order[i];
	}
	// Player 1-3 cities/settlements
	for (j=0;j<3;j++) {
		s_memory[CURRENT_PLAYER_REG]= j+1;
		for (i=0;i<sizeof(ppos[j])/sizeof(ppos[j][0]);i++)
		{
			s_memory[NEW_PIECE_LOC_REG] = ppos[j][i];
			confirmNewPiece();
			//rarity_display_error(ppos[j][i]%18,ppos[j][i]/18,0);
			//delay_ms(500);
		}
	}	
	
	//Thief proper
	posSetOwner(131,1);
	setPosLegal(131);
	
    // ********************************
	s_memory[CURRENT_PLAYER_REG] = 1;
	
	DesertHex = 15;

	delay_s(2);
}

int8_t chkstateTest(void)
{
	uint8_t i;
	uint8_t address;
	ioport_port_mask_t RowReturn;
	int8_t error = 0;
	
	for (address=0;address<8;address++)
	{

		// Grab the sensor data for every row
		ioport_set_port_level(HE_RETURN_PORT,HE_ADDR_PINS_MASK,address<<HE_ADDR_PIN_0);
		delay_ms(.1);
		RowReturn = ioport_get_port_level(HE_RETURN_PORT,HE_RETURN_MASK);
		if (!compareLegal2Row(RowReturn,address))
		{
			for (i=0;i<18;i++)
			{
				// If the sensor value is not the same as what we have in the legal state, see if it's a legal move
				if ((RowReturn & 1<<ColPins[i])!=(getLegalRow(address)& 1<<ColPins[i]))
				{
					if (isLegalInit(address*18+i,1,1,32))
					{
						rgb_hex_set(i,COLOR_BLACK);
						rarity_display_error(i,address,0);
					}
					else
					{
						rgb_hex_set(i,COLOR_ERROR);
						rarity_display_error(i,address,0);	
						error = 1;
					}					
				}
			}
		}
	}
	
	// Don't forget to check the middle thief.
	
	
	if ( (!ioport_get_pin_level(MIDDLE_SENSOR) && !pos2Owner(MIDDLE_THIEF_POS)) || (ioport_get_pin_level(MIDDLE_SENSOR)&& pos2Owner(MIDDLE_THIEF_POS))){
		
		if (!getLegalRow(7))
		{
			if (isLegalInit(address*18+i,1,1,32))
			{
				rgb_hex_set(18,COLOR_BLACK);
			}
			else{
				rgb_hex_set(18,COLOR_ERROR);
				rarity_display_error(18,7,0);
				error = 1;
			}
		}
		// MOAR FANCY GRAPHICS
		
	}		
	return !error;
}

void bootLoop (void) {
	uint8_t i,j;
	uint8_t rgbs[12] = {9,8,17,16,5,3,1,0,15,12,11,10};
    uint8_t rgbn[6] = {6,4,2,14,13,7};
	int colors1[8] = {COLOR_RED, COLOR_BRICK, COLOR_YELLOW, COLOR_SHEEP, COLOR_GREEN, COLOR_TEAL, COLOR_BLUE, COLOR_ORE};
	int colors2[8] = {COLOR_BRICK, COLOR_YELLOW, COLOR_SHEEP, COLOR_GREEN, COLOR_TEAL, COLOR_BLUE, COLOR_ORE, COLOR_RED};
	int colors3[8] = {COLOR_YELLOW, COLOR_SHEEP, COLOR_GREEN, COLOR_TEAL, COLOR_BLUE, COLOR_ORE, COLOR_RED, COLOR_ORANGE};
	
	rarity_clear_all();
	rgb_hex_set(18,COLOR_BLACK);
	
	for (i=0; i<12; i++) {
		rgb_hex_set(rgbn[i/2],COLOR_BLACK);
		rgb_hex_set(rgbs[(i+4)%12],COLOR_RED); 
		rgb_hex_set(rgbs[(i+2)%12],COLOR_BRICK); 
		rgb_hex_set(rgbs[i%12],COLOR_YELLOW);  
		delay_ms(100);
		rgb_hex_set(rgbs[i%12],COLOR_BLACK);
	}
	
	//for (j=0;j<16;j++) {
		//for (i=0; i<12; i++) {
			//rgb_hex_set_variable(rgbn[i/2],COLOR_BLACK,4);
			//rgb_hex_set_variable(rgbs[(i+4)%12],colors1[j/2],4);
			//rgb_hex_set_variable(rgbs[(i+2)%12],colors2[j/2],4);
			//rgb_hex_set_variable(rgbs[i%12],colors3[j/2],4);
			//delay_ms(200);
			//rgb_hex_set_variable(rgbs[i%12],COLOR_BLACK,4);
		//}
	//}
}

void onAnimate (void) {
	uint8_t i;
	uint8_t outer[12] = {9,8,17,16,5,3,1,0,15,12,11,10};
    uint8_t inner[6] = {6,4,2,14,13,7};
	
	rarity_clear_all();
	rgb_clear_all();
	
    for(i=0;i<12;i++) {
		rgb_hex_set(outer[i],COLOR_TEAL);
	}
	delay_ms(400);
	
	for(i=0;i<6;i++) {
		rgb_hex_set(inner[i],COLOR_TEAL);
	}
	for(i=0;i<12;i++) {
		rgb_hex_set(outer[i],COLOR_BLUE);
	}
    delay_ms(400);
	
	rgb_hex_set(18,COLOR_TEAL);
	for(i=0;i<6;i++) {
		rgb_hex_set(inner[i],COLOR_BLUE);
	}
	for(i=0;i<12;i++) {
		rgb_hex_set(outer[i],COLOR_BLACK);
	}
	delay_ms(400);
	
	rgb_hex_set(18,COLOR_BLUE);
	for(i=0;i<6;i++) {
		rgb_hex_set(inner[i],COLOR_BLACK);
	}
	delay_ms(400);
	
	rgb_hex_set(18,COLOR_BLACK);	
}

void offAnimate (void) {
	uint8_t i;
    uint8_t outer[12] = {9,8,17,16,5,3,1,0,15,12,11,10};
    uint8_t inner[6] = {6,4,2,14,13,7};
	
	rarity_clear_all();
	rgb_clear_all();
	
	rgb_hex_set(18,COLOR_BRICK);
	delay_ms(400);
	
	rgb_hex_set(18,COLOR_RED);
	for(i=0;i<6;i++) {
		rgb_hex_set(inner[i],COLOR_BRICK);
	}
	delay_ms(400);
	
	rgb_hex_set(18,COLOR_BLACK);
	for(i=0;i<6;i++) {
		rgb_hex_set(inner[i],COLOR_RED);
	}
    for(i=0;i<12;i++) {
		rgb_hex_set(outer[i],COLOR_BRICK);
	}
	delay_ms(400);
	
	for(i=0;i<6;i++) {
		rgb_hex_set(inner[i],COLOR_BLACK);
	}
	for(i=0;i<12;i++) {
		rgb_hex_set(outer[i],COLOR_RED);
	}
    delay_ms(400);
	
	for(i=0;i<12;i++) {
		rgb_hex_set(outer[i],COLOR_BLACK);
	}
	delay_ms(400);
}

void clear_resources(void)
{
	uint8_t i;
	for (i=0;i<20;i++)
	{
		s_memory[RESOURCE_REC_REG+i] = 0;
	}
}

void RoadmapTest (void)
{
	uint8_t i,j;
	refresh_display();
	for (j=0;j<4;j++)
	{
		for (i=0;i<(15-pieces_remaining[j][0]);i++)
		{
			rarity_display_error(roadmap[j][i][0]%18,roadmap[j][i][0]/18,0);
			delay_ms(500);
			rarity_display_error(roadmap[j][i][1]%18,roadmap[j][i][1]/18,0);
			delay_ms(500);
		}
	}
}