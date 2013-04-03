
/*! \brief Main function.
*/

#include <asf.h>
#include <RarityDisplay.h>
#include <I2C.h>
#include <RGB.h>


int main(void)
{
	int i,j;

	// Hall Effect Sensor
	ioport_port_mask_t RowReturn;
	int ColPins[]= {HE_COL0,HE_COL1,HE_COL2,HE_COL3,HE_COL4,HE_COL5,HE_COL6,HE_COL7, HE_COL8,HE_COL9,HE_COL10,HE_COL11,HE_COL12,HE_COL13,HE_COL14,HE_COL15,HE_COL16,HE_COL17};
	int magnetfound = 0;
	
	// Initialize the board
	board_init();
	// Delay for 100ms just to be safe
	//delay_ms(100);
	// Clear all of the 7-segment displays
	//rarity_clear_all();
	// Clear all of the RGB LEDs
	rgb_clear_all();


	while(ioport_get_pin_level(MIDDLE_SENSOR));
	
	for (i=0;i<19;i++){
		rarity_set(i, 10);
	}	

	// Loop through all the hall effect sensors and display error if hall effect triggered
	while (1)
	{
		// roads
		for (i=0;i<=7;i++)
		{
			ioport_set_port_level(HE_ADDR_PORT,HE_ADDR_PINS_MASK,i<<HE_ADDR_PIN_0);
			delay_ms(10);
			RowReturn = ioport_get_port_level(HE_RETURN_PORT,HE_RETURN_MASK);
			for (j=0;j<18;j++)
			{
				rgb_hex_set(j,WHEAT);
				//rarity_display_error(j,i,0);
				
				if (RowReturn & 1<<ColPins[j])
				{
					rgb_hex_set(j,ORE);
					rarity_display_error(j,i,0);
					delay_ms(1000);
					rarity_clear_all();
				}
			}
			//delay_s(2);
		}
	}
}	



/*
rarity_set(0,2);
rarity_set(1,3);
rarity_set(2,4);
rarity_set(3,5);
rarity_set(4,6);
rarity_set(5,7);
rarity_set(6,8);
rarity_set(7,9);
rarity_set(8,10);
rarity_set(9,11);
rarity_set(10,12);
rarity_set(11,20);
rarity_set(12,30);
rarity_set(13,40);
rarity_set(14,50);
rarity_set(15,60);
rarity_set(16,70);
rarity_set(17,80);
rarity_set(18,90);

*/

/*
	struct spi_device RARITY = {
		.id =  SPI_NPCS
	};
  int colors[] = {WHEAT, DESERT, WOOD, BRICK, SHEEP, ERROR, ORE, PINK};
  int hexes[] = {0,1,3,5,16,17,8,9,10,11,12,15,2,4,6,7,13,14,18};
  int numHexes = 19;
  int numColors = 8;
  
  int delay = 50;
  uint8_t nopSpiData = {0x0, 0x0};
  uint8_t spiData[2];
  */
 //for (i=0;i<145;i++) {
	 //display_error(i/8, i%8,1);
	 //
	 //delay_s(1);
	 //
	  //for (int j=0; j < 5; j++) {
		  //for (int k=1;k<=8;k++) {
			  ////delay_ms(100);
			  ////spiData[0] = reverse((4+i)%10);
			  //spiData[0] = reverse(0);
			  //spiData[1] = reverse(k);
			  //
			  ////delay_ms(200);
			  //spi_select_device(SPI,&RARITY);
			  //spi_write_packet(SPI,j==0 ? spiData : nopSpiData,2);
			  //spi_write_packet(SPI,j==1 ? spiData : nopSpiData,2);
			  //spi_write_packet(SPI,j==2 ? spiData : nopSpiData,2);
			  //spi_write_packet(SPI,j==3 ? spiData : nopSpiData,2);
			  //spi_write_packet(SPI,j==4 ? spiData : nopSpiData,2);
			  //spi_deselect_device(SPI,&RARITY);
			  //
		  //}
	  //}
	 //
 //}
// while (1) {
 /*for(j=0;j<numColors;j++){
	 if (j%2) {
		 for (i=0;i<numHexes;i++) {
			 rgb_hex_set(hexes[i], colors[j]);
			 rarity_set(hexes[i], i);
			 delay_ms(delay);
		 }
	 } else {
		 for (i=numHexes-1;i>=0;i--) {
			 rgb_hex_set(hexes[i], colors[j]);
			 rarity_set(hexes[i], 19-i);
			 delay_ms(delay);
		 }
	 }
	}	*/

	//for(j=0;j<numColors;j++){
		//if (j%2) {
			//for (i=0;i<numHexes;i++) {
				//rgb_hex_set(hexes[i], colors[j]);
				//delay_ms(delay);
			//}
		//} else {
			//for (i=numHexes-1;i>=0;i--) {
				//rgb_hex_set(hexes[i], colors[j]);
				//delay_ms(delay);
			//}			
		//}	
		//