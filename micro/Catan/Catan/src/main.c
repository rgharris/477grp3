
/*! \brief Main function.
*/

#include <asf.h>
#include <RarityDisplay.h>
#include <I2C.h>
#include <RGB.h>
#include <Catan.h>


void PositionTest(void);
void SetThiefPos(void);


int main(void)
{
	ioport_port_mask_t RowReturn, TestRow;
	int j,i;
	int pos;
	int ColPins[]= {HE_COL0,HE_COL1,HE_COL2,HE_COL3,HE_COL4,HE_COL5,HE_COL6,HE_COL7, HE_COL8,HE_COL9,HE_COL10,HE_COL11,HE_COL12,HE_COL13,HE_COL14,HE_COL15,HE_COL16,HE_COL17};
    int player;

	// Initialize the board
	board_init();
	// Clear all of the 7-segment displays
	rarity_clear_all();
	// Clear all of the RGB LEDs
	rgb_clear_all();

	
	// Wait for middle sensor to trip before advancing (safety feature)
	while(ioport_get_pin_level(MIDDLE_SENSOR));
	
	delay_ms(500);
	
	//while (1)
	//{
		//AdjHexTest();
	//}
	
	//generate_board();
	TestGameSetup();
	assign_resources();
	refresh_display();
	
	// initial placement
	
	//for(player=1;player<=4;player++) {
		//s_memory[CURRENT_PLAYER_REG] = player;
		//buildRoad(1, buildSettlement(1));
	//}
	//for(player=4;player>=1;player--) {
		//s_memory[CURRENT_PLAYER_REG] = player;
		//buildRoad(1, buildSettlement(1));
	//}
	s_memory[CURRENT_PLAYER_REG] = 1;
	moveThief();
	s_memory[10] = 4;
	
	while(1);
	/*{
		delay_s(2);
		//SetThiefPos();
		refresh_display();
		//PositionTest();
		//delay_s(1);
		//refresh_display();
		checkBoardState(1,1,1,1,0,0);
		show_remaining_piece();
		//assign_resources();
		
		
	}*/

}	

// Prototyping

void SetThiefPos(void)
{
	uint8_t i;
	int ColPins[]= {HE_COL0,HE_COL1,HE_COL2,HE_COL3,HE_COL4,HE_COL5,HE_COL6,HE_COL7, HE_COL8,HE_COL9,HE_COL10,HE_COL11,HE_COL12,HE_COL13,HE_COL14,HE_COL15,HE_COL16,HE_COL17};
	ioport_port_mask_t RowReturn = 0;
	
	ioport_set_port_level(HE_ADDR_PORT,HE_ADDR_PINS_MASK,7<<HE_ADDR_PIN_0);
	delay_ms(1);
	RowReturn = ioport_get_port_level(HE_RETURN_PORT,HE_RETURN_MASK);
	
	for (i=0;i<=17;i++)
	{
		if ((RowReturn & 1<<ColPins[i]))
		{
			if (!pos2Owner(126+i))
			{
				posSetOwner(126+i,1);
				rarity_display_error(i,7,0);
				delay_ms(500);
			}			
		}
		else
		{
			posSetOwner(126+i,0);
		}
	}
	if (!ioport_get_pin_level(MIDDLE_SENSOR))
	{
		if (!pos2Owner(MIDDLE_THIEF_POS))
		{
			posSetOwner(MIDDLE_THIEF_POS,1);
			rarity_display_error(18,7,0);
			delay_ms(500);
		}
	}
	else
	{
		posSetOwner(MIDDLE_THIEF_POS,0);
	}
}

void PositionTest(void){
	ioport_port_mask_t RowReturn;
	int j,i;
	int ColPins[]= {HE_COL0,HE_COL1,HE_COL2,HE_COL3,HE_COL4,HE_COL5,HE_COL6,HE_COL7, HE_COL8,HE_COL9,HE_COL10,HE_COL11,HE_COL12,HE_COL13,HE_COL14,HE_COL15,HE_COL16,HE_COL17};

	//while (1)
	//{
		//
		for (i=0;i<=7;i++)
		{
			ioport_set_port_level(HE_ADDR_PORT,HE_ADDR_PINS_MASK,i<<HE_ADDR_PIN_0);
			delay_ms(.1);
			RowReturn = ioport_get_port_level(HE_RETURN_PORT,HE_RETURN_MASK);
			for (j=0;j<18;j++)
			{
				//rgb_hex_set(j,COLOR_BLACK);
				//rarity_display_error(j,i,0);
				
				if (RowReturn & 1<<ColPins[j])
				{
					rgb_hex_set(j,COLOR_BLUE);
					rarity_display_error(j,i,1);
					//s_memory[PI_EVENT_REG] = s_memory[PI_EVENT_REG] | 1<<i;
					delay_ms(500);
					rarity_clear_all();
				}
			}
			//delay_s(2);
		}
		//if (isDiceRolled())
		//{
			//rgb_hex_set(18,COLOR_ORE);
		//}
	//}
}
