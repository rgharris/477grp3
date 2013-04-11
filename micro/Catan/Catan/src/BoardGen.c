/*
 * BoardGen.c
 *
 * Created: 4/5/2013 1:25:01 PM
 *  Author: team3
 */ 

#include <BoardGen.h>
/*
void generate_board(uint8_t* Hex2Resource, uint8_t* Hex2Rarity) {
	// This function should track user input before a game starts to generate "random" numbers in order to pick the resources
	// and rarities for each hex.
	
	// \todo add code to check if pi is awake and new game has been started. polling loop and generate remaining board using
	// psuedo random rand() function.
	
	// \todo add code to give fancy visual feedback as player drags magnets across board.
	
	uint8_t i,k,j;
//							{ORE WHEAT SHEEP BRICK WOOD DESERT}
	uint8_t ResourcesInDeck[] = { 3 ,  4  ,  4  ,  3  , 4  ,  1   };
	uint8_t ResourcesRemaining = 19;
	uint8_t ResourceIndexCompare;
	uint8_t address;
	int ResourceAssigned;
	// Hall Effect Sensor
	ioport_port_mask_t RowReturn;
	int ColPins[]= {HE_COL0,HE_COL1,HE_COL2,HE_COL3,HE_COL4,HE_COL5,HE_COL6,HE_COL7, HE_COL8,HE_COL9,HE_COL10,HE_COL11,HE_COL12,HE_COL13,HE_COL14,HE_COL15,HE_COL16,HE_COL17};
	
	// initialize the hexes so that they have no resource or rarity
	for (i=0;i<19;i++){
		//rarity_set(i, 22);
		Hex2Resource[i] = NO_RESOURCE;
		Hex2Rarity[i] = 0;
	}
	
	//initialize board at nothing
	rgb_clear_all();
	rarity_clear_all();
			
	// Keep checking all sensor positions until all hexes have been assigned a resource
	while (ResourcesRemaining)
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
					rgb_hex_set(i,COLOR_RED);
					rarity_display_error(i,address,0);
					
					
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
			rgb_hex_set(18,COLOR_RED);
			rarity_display_error(18,7,0);
			
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
}

void refresh_display(uint8_t* Hex2Resource, uint8_t* Hex2Rarity){
	for (int i=0;i<=18;i++)
	{
		rgb_display_resource(i,Hex2Resource[i]);
		rarity_set(i,Hex2Rarity[i]);
	}
}			

uint8_t roll_die(void){
	unsigned long cycles_count;
	uint8_t diceValue1,diceValue2;
	cycles_count = Get_sys_count();
	diceValue1 = ((cycles_count & 0xFF0)>>4) % 6 + 1;
	diceValue2 = ((cycles_count & 0xFF00)>>8) % 6 + 1;
	//diceValue2 = diceValue2 % 6 + 1;
	return diceValue1+diceValue2;
}*/