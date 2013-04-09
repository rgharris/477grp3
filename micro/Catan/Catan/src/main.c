
/*! \brief Main function.
*/

#include <asf.h>
#include <RarityDisplay.h>
#include <I2C.h>
#include <RGB.h>
#include <Catan.h>


void PositionTest(void);
//void refresh_display(uint8_t* Hex2Resource, uint8_t* Hex2Rarity);

int main(void)
{

	// Hexagon Maps
	int i;
	uint8_t Hex2Rarity[19];
	uint8_t Hex2Resource[19];
	
	// Initialize the board
	board_init();
	// Delay for 100ms just to be safe
	//delay_ms(100);
	// Clear all of the 7-segment displays
	rarity_clear_all();
	// Clear all of the RGB LEDs
	rgb_clear_all();

	
	// Wait for middle sensor to trip before advancing (safety feature)
	while(ioport_get_pin_level(MIDDLE_SENSOR));
	
	delay_ms(500);
	/*
	for (int i=0; i<19; i++)
	{
		rarity_set(i,i);
		
	}
	while(ioport_get_pin_level(MIDDLE_SENSOR));
	
	rarity_clear_all();
	
	// Test the static map
	while (1) {PositionTest();}	
    */
	//while (1) {PositionTest();}	
		
	// Testing die roll value
	/*
	for (i=0;i<14;i++)
	{
		s_memory[i] = 0;
	}
	while (1)
	{
		if (!ioport_get_pin_level(MIDDLE_SENSOR))
		{
			s_memory[0] = (roll_die());
			if (s_memory[0]>0)
			{
				if (s_memory[0]<13)
				{
					s_memory[s_memory[0]]++;
					rarity_set(18,s_memory[0]);
				}
				else{
					s_memory[13]++;
				}
			}
			else{
				s_memory[13]++;
			}
			
			delay_ms(500);
			rarity_clear_all();
		}
	}
	*/
	//while(1) {PortTest();}
	generate_board(Hex2Resource,Hex2Rarity);
	refresh_display(Hex2Resource,Hex2Rarity);
	while(1);
}	

void PositionTest(void){
	ioport_port_mask_t RowReturn;
	int j,i;
	int ColPins[]= {HE_COL0,HE_COL1,HE_COL2,HE_COL3,HE_COL4,HE_COL5,HE_COL6,HE_COL7, HE_COL8,HE_COL9,HE_COL10,HE_COL11,HE_COL12,HE_COL13,HE_COL14,HE_COL15,HE_COL16,HE_COL17};

	while (1)
	{
		
		for (i=0;i<=7;i++)
		{
			ioport_set_port_level(HE_ADDR_PORT,HE_ADDR_PINS_MASK,i<<HE_ADDR_PIN_0);
			delay_ms(1);
			RowReturn = ioport_get_port_level(HE_RETURN_PORT,HE_RETURN_MASK);
			for (j=0;j<18;j++)
			{
				//rgb_hex_set(j,COLOR_BLACK);
				//rarity_display_error(j,i,0);
				
				if (RowReturn & 1<<ColPins[j])
				{
					//rgb_hex_set(j,COLOR_ORE);
					rarity_display_error(j,i,0);
					s_memory[PI_EVENT_REG] = s_memory[PI_EVENT_REG] | 1<<i;
					delay_ms(500);
					rarity_clear_all();
				}
			}
			//delay_s(2);
		}
		if (isDiceRolled())
		{
			rgb_hex_set(18,COLOR_ORE);
		}
	}
}
