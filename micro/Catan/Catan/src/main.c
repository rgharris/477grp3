
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
	int8_t j,i;
	uint8_t pos;
	int ColPins[]= {HE_COL0,HE_COL1,HE_COL2,HE_COL3,HE_COL4,HE_COL5,HE_COL6,HE_COL7, HE_COL8,HE_COL9,HE_COL10,HE_COL11,HE_COL12,HE_COL13,HE_COL14,HE_COL15,HE_COL16,HE_COL17};
    int8_t player;
	wdt_opt_t opt_WATCH;
	opt_WATCH.us_timeout_period = 1000000;


	// Initialize the board
	board_init();	
	// Clear all of the 7-segment displays
	rarity_clear_all();
	// Clear all of the RGB LEDs
	rgb_clear_all();
	
	onAnimate();
	
	//////////////////////////////////////////////////////////////////////////
	// Initialize the board with resources and rarities
	//////////////////////////////////////////////////////////////////////////
	generate_board();
	refresh_display();
	
	//////////////////////////////////////////////////////////////////////////
	// Initial Placement of Pieces
	//////////////////////////////////////////////////////////////////////////
	for(i=0;i<s_memory[PLAYER_COUNT_REG];i++) {
		buildRoad(1, buildSettlement(1));
	}
	// Clear out the resources registers
	for(i=0;i<20;i++) {
		s_memory[RESOURCE_REC_REG+i]=0;
	}
			
	for(i=0;i<s_memory[PLAYER_COUNT_REG];i++) {
		pos = buildSettlement(1);
		buildRoad(1, pos);
		assign_initial_resources(pos);
	}
	refresh_display();
	

	
	
	//////////////////////////////////////////////////////////////////////////
	// Play the game
	//////////////////////////////////////////////////////////////////////////
	mainGameLoop();
	
	//rgb_clear_all();
	//rarity_clear_all();
	
	
	//////////////////////////////////////////////////////////////////////////
	// End Game, want to play a new one?
	//////////////////////////////////////////////////////////////////////////
	while(s_memory[PI_EVENT_REG]!=PI_NEW_GAME) {
		delay_ms(200);
	}
	
	offAnimate();

	wdt_enable(&opt_WATCH);
	
	while(1) {
		delay_ms(200);
	}
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
