/*
 * RarityDisplay.c
 *
 * Created: 3/28/2013 6:16:25 PM
 *  Author: team3
 */ 


/*
 * RarityDisplay.c
 *
 * Uses: This interface will provide a layer of abstraction to
 * Set the seven segments on the board.
 * Toplevel functions will include:
 *   rarity_init()
 *     - initialize the driver mode of operation for all drivers on the board
 *   rarity_set(uint hex_num, uint rarity_value)
 *     - will take a value 0-18 and set that display to the desired rarity value
 *     - sends no ops to other positions
 *     - not sure if will be used
 *   rarity_set_all(uint *rarity_value_arr)
 *     - pointer to the array that stores all the hex rarities for the entire game
 *     - can be used after an error piece is fixed to correct the rarity display
 *   rarity_disp_error(uint error_position)
 *     - will take the error position and find the corresponding hex and display the error code
 * Created: 3/27/2013 7:34:26 PM
 *  Author: team3
 */ 

#include <RarityDisplay.h>



// This routine initializes the 7seg drivers using the SPI interface
// This is done by sending the following commands:
// NormalOperation (0x0C,0x01): Change mode to normal operation
// DecodeOff (0x09,0x00): Set decode mode off (data sent to digits will be interpreted as segments)
// IntHigh (0x0A,0x0F): Set the intensity of the display to maximum
// scanLimit (0x0B,0x07): Set the scan limit to 7, meaning all 7segs can be used
void rarity_init()

{
	uint8_t spiData[2];
	struct spi_device RARITY = {
		.id =  SPI_NPCS
	};

	spi_master_init(SPI);
	spi_master_setup_device(SPI,&RARITY,SPI_MODE_0,SPI_BAUDRATE, 0);
	spi_enable(SPI);
	
	// Normal Operation
	spi_select_device(SPI,&RARITY);
	spiData[0] = reverse(0x01);
	spiData[1] = reverse(0x0C);
	spi_write_packet(SPI,spiData,2);
	spi_write_packet(SPI,spiData,2);
	spi_write_packet(SPI,spiData,2);
	spi_write_packet(SPI,spiData,2);
	spi_write_packet(SPI,spiData,2);
	spi_deselect_device(SPI,&RARITY);
	
	// Decode Mode Off
	spi_select_device(SPI,&RARITY);
	spiData[0] = reverse(0x00);
	spiData[1] = reverse(0x09);
	spi_write_packet(SPI,(spiData),2);
	spi_write_packet(SPI,(spiData),2);
	spi_write_packet(SPI,(spiData),2);
	spi_write_packet(SPI,(spiData),2);
	spi_write_packet(SPI,(spiData),2);
	spi_deselect_device(SPI,&RARITY);
	
	// 8/15 Brightness
	spi_select_device(SPI,&RARITY);
	spiData[0] = reverse(8);
	spiData[1] = reverse(0x0A);
	spi_write_packet(SPI,(spiData),2);
	spi_write_packet(SPI,(spiData),2);
	spi_write_packet(SPI,(spiData),2);
	spi_write_packet(SPI,(spiData),2);
	spi_write_packet(SPI,(spiData),2);
	spi_deselect_device(SPI,&RARITY);
	
	// Scan all digits on all drivers
	spi_select_device(SPI,&RARITY);
	spiData[0] = reverse(0x07); 
	spiData[1] = reverse(0x0B);
	spi_write_packet(SPI,(spiData),2);
	spi_write_packet(SPI,(spiData),2);
	spi_write_packet(SPI,(spiData),2);
	spi_write_packet(SPI,(spiData),2);
	spi_write_packet(SPI,(spiData),2);
	spi_deselect_device(SPI,&RARITY);
}


void display_error(unsigned int hex_num, unsigned int position, unsigned int isCity){
	// Sets the 2 digit seven segment display for a single hexagon
	uint8_t spiData[2];
	struct spi_device RARITY = {
		.id =  SPI_NPCS
	};
	unsigned int driver_num;
	unsigned int driver_tens_digit;
	unsigned int driver_ones_digit;
	unsigned int tens_digit;
	unsigned int ones_digit;
	uint8_t nopSpiData = {0x0, 0x0};
	// Do we perhaps need a new function to do error codes on the hexes? I think that might be best, considering C-T won't actually
	// be displayed, here.
	//
	// Or maybe we need to have a simple check if the rarity passed is, say, 20 or greater, and use a different decode map.
	// I've moved the error map out for this purpose.
	//                    {  0 ,  1 ,  2 ,  3 ,  4 ,  5 ,  6 ,  7 ,  8 ,  9 }
	uint8_t digit_map[] = {0x7E,0x30,0x6D,0x79,0x33,0x5B,0x5F,0x70,0x7F,0x7B};
	/*
	Move To new function	
	// "error" mappings will be done with numbers greater than 100. 
	// Roads:		100-106
	// Cities:		110-116
	// Settlements:	120-126
	// Thief:		137
	// For cities/settlements/thiefs (i.e. 10's digit greater than 0), position = 2 * 1's digit
	// For roads, position = 2* 1's digit + 1
	// This isn't the best way, but it should work.
	//							{ "r", "C", "S", "T"}
	uint8_t piece_type_map[] =	{0x05,0x7E,0x5B,0x70}
	//							{ TRs, TRr, Rs, BRr,  BRs, Br, BLs,  BLr,  Ls, TLr, TLs, Tr,  T }
	uint8_t position_map[] =	{0x60,0x20,0x30,0x10,0x18,0x08,0x0C,0x04,0x06,0x02,0x42,0x40,0x70};
	*/	
	//							{ "r", "C", "S", "T"}
	//uint8_t piece_type_map[] =	{0x05,0x7E,0x5B,0x70}
	//							{ TRs, TRr, Rs, BRr,  BRs, Br, BLs,  BLr,  Ls, TLr, TLs, Tr}//, T }
	uint8_t position_map[] = {0x60,0x20,0x30,0x10,0x18,0x08,0x0C,0x04,0x06,0x02,0x42,0x40};//,0x70};
	uint8_t starting_positions[] = {5,5,7,7,9,7,11,1,11,11,1,1,3,3,5,4,9,9,0};
	if (hex_num==18 || position == 7) {
		tens_digit = SEVSEG_THIEF;
		ones_digit = SEVSEG_THIEF;
	} else {
		if (position % 2 == 0) {
			tens_digit = SEVSEG_ROAD;
		} else if (isCity) {
			tens_digit = SEVSEG_CITY;
		} else {
			tens_digit = SEVSEG_SETTLEMENT;
		}	
		
		ones_digit = reverse(position_map[(position + starting_positions[hex_num]) % 12]);	
	}
	switch (hex_num)
	{
	case 0:
		driver_num = 3;
		driver_tens_digit = SEVSEG_DIG7;
		driver_ones_digit = SEVSEG_DIG6;
		break;
	case 1:
		driver_num = 3;
		driver_tens_digit = SEVSEG_DIG5;
		driver_ones_digit = SEVSEG_DIG4;
		break;
	case 2:
		driver_num = 3;
		driver_tens_digit = SEVSEG_DIG1;
		driver_ones_digit = SEVSEG_DIG0;
		break;
	case 3:
		driver_num = 3;
		driver_tens_digit = SEVSEG_DIG3;
		driver_ones_digit = SEVSEG_DIG2;
		break;
	case 4:
		driver_num = 4;
		driver_tens_digit = SEVSEG_DIG5;
		driver_ones_digit = SEVSEG_DIG4;
		break;
	case 5:
		driver_num = 4;
		driver_tens_digit = SEVSEG_DIG7;
		driver_ones_digit = SEVSEG_DIG6;
		break;
	case 6:
		driver_num = 0;
		driver_tens_digit = SEVSEG_DIG3;
		driver_ones_digit = SEVSEG_DIG2;
		break;
	case 7:
		driver_num = 1;
		driver_tens_digit = SEVSEG_DIG1;
		driver_ones_digit = SEVSEG_DIG0;
		break;
	case 8:
		driver_num = 0;
		driver_tens_digit = SEVSEG_DIG5;
		driver_ones_digit = SEVSEG_DIG4;
		break;
	case 9:
		driver_num = 1;
		driver_tens_digit = SEVSEG_DIG7;
		driver_ones_digit = SEVSEG_DIG6;
		break;
	case 10:
		driver_num = 1;
		driver_tens_digit = SEVSEG_DIG5;
		driver_ones_digit = SEVSEG_DIG4;
		break; 
	case 11:
		driver_num = 2;
		driver_tens_digit = SEVSEG_DIG7;
		driver_ones_digit = SEVSEG_DIG6;
		break;
	case 12:
		driver_num = 2;
		driver_tens_digit = SEVSEG_DIG5;
		driver_ones_digit = SEVSEG_DIG4;
		break;
	case 13:
		driver_num = 1;
		driver_tens_digit = SEVSEG_DIG3;
		driver_ones_digit = SEVSEG_DIG2;
		break;
	case 14:
		driver_num = 2;
		driver_tens_digit = SEVSEG_DIG1;
		driver_ones_digit = SEVSEG_DIG0;
		break;
	case 15:
		driver_num = 2;
		driver_tens_digit = SEVSEG_DIG3;
		driver_ones_digit = SEVSEG_DIG2;
		break;
	case 16:
		driver_num = 0;
		driver_tens_digit = SEVSEG_DIG1;
		driver_ones_digit = SEVSEG_DIG0;
		break;
	case 17:
		driver_num = 0;
		driver_tens_digit = SEVSEG_DIG7;
		driver_ones_digit = SEVSEG_DIG6;
		break;
	case 18:
		driver_num = 4;
		driver_tens_digit = SEVSEG_DIG3;
		driver_ones_digit = SEVSEG_DIG2;
		break;
	}
		//ones_digit = rarity_value % 10;
		//tens_digit = (rarity_value - ones_digit) / 10;
		
		// write ones value
		
		spiData[0]=ones_digit;//reverse(digit_map[ones_digit]);
		spiData[1]=driver_ones_digit;
		spi_select_device(SPI,&RARITY);
		spi_write_packet(SPI,driver_num==4 ? spiData : nopSpiData,2);
		spi_write_packet(SPI,driver_num==3 ? spiData : nopSpiData,2);
		spi_write_packet(SPI,driver_num==2 ? spiData : nopSpiData,2);
		spi_write_packet(SPI,driver_num==1 ? spiData : nopSpiData,2);
		spi_write_packet(SPI,driver_num==0 ? spiData : nopSpiData,2);
		spi_deselect_device(SPI,&RARITY);
		
		// write tens value
		//if (tens_digit == 0) {
		//	spiData[0]= 0;
		//} else {
		spiData[0]=tens_digit;//reverse(digit_map[tens_digit]);
		//}
		spiData[1]=driver_tens_digit;
		spi_select_device(SPI,&RARITY);
		spi_write_packet(SPI,driver_num==4 ? spiData : nopSpiData,2);
		spi_write_packet(SPI,driver_num==3 ? spiData : nopSpiData,2);
		spi_write_packet(SPI,driver_num==2 ? spiData : nopSpiData,2);
		spi_write_packet(SPI,driver_num==1 ? spiData : nopSpiData,2);
		spi_write_packet(SPI,driver_num==0 ? spiData : nopSpiData,2);
		spi_deselect_device(SPI,&RARITY);
}

void rarity_set(unsigned int hex_num, unsigned int rarity_value){
	// Sets the 2 digit seven segment display for a single hexagon
	uint8_t spiData[2];
	struct spi_device RARITY = {
		.id =  SPI_NPCS
	};
	unsigned int driver_num;
	unsigned int driver_tens_digit;
	unsigned int driver_ones_digit;
	unsigned int tens_digit;
	unsigned int ones_digit;
	uint8_t nopSpiData = {0x0, 0x0};
	// Do we perhaps need a new function to do error codes on the hexes? I think that might be best, considering C-T won't actually
	// be displayed, here.
	//
	// Or maybe we need to have a simple check if the rarity passed is, say, 20 or greater, and use a different decode map.
	// I've moved the error map out for this purpose.
	//                    {  0 ,  1 ,  2 ,  3 ,  4 ,  5 ,  6 ,  7 ,  8 ,  9 }
	uint8_t digit_map[] = {0x7E,0x30,0x6D,0x79,0x33,0x5B,0x5F,0x70,0x7F,0x7B};
	/*
	Move To new function	
	// "error" mappings will be done with numbers greater than 100. 
	// Roads:		100-106
	// Cities:		110-116
	// Settlements:	120-126
	// Thief:		137
	// For cities/settlements/thiefs (i.e. 10's digit greater than 0), position = 2 * 1's digit
	// For roads, position = 2* 1's digit + 1
	// This isn't the best way, but it should work.
	//							{ "r", "C", "S", "T"}
	uint8_t piece_type_map[] =	{0x05,0x7E,0x5B,0x70}
	//							{ TRs, TRr, Rs, BRr,  BRs, Br, BLs,  BLr,  Ls, TLr, TLs, Tr,  T }
	uint8_t position_map[] =	{0x60,0x20,0x30,0x10,0x18,0x08,0x0C,0x04,0x06,0x02,0x42,0x40,0x70};
	*/	
		
	switch (hex_num)
	{
	case 0:
		driver_num = 3;
		driver_tens_digit = SEVSEG_DIG7;
		driver_ones_digit = SEVSEG_DIG6;
		break;
	case 1:
		driver_num = 3;
		driver_tens_digit = SEVSEG_DIG5;
		driver_ones_digit = SEVSEG_DIG4;
		break;
	case 2:
		driver_num = 3;
		driver_tens_digit = SEVSEG_DIG1;
		driver_ones_digit = SEVSEG_DIG0;
		break;
	case 3:
		driver_num = 3;
		driver_tens_digit = SEVSEG_DIG3;
		driver_ones_digit = SEVSEG_DIG2;
		break;
	case 4:
		driver_num = 4;
		driver_tens_digit = SEVSEG_DIG5;
		driver_ones_digit = SEVSEG_DIG4;
		break;
	case 5:
		driver_num = 4;
		driver_tens_digit = SEVSEG_DIG7;
		driver_ones_digit = SEVSEG_DIG6;
		break;
	case 6:
		driver_num = 0;
		driver_tens_digit = SEVSEG_DIG3;
		driver_ones_digit = SEVSEG_DIG2;
		break;
	case 7:
		driver_num = 1;
		driver_tens_digit = SEVSEG_DIG1;
		driver_ones_digit = SEVSEG_DIG0;
		break;
	case 8:
		driver_num = 0;
		driver_tens_digit = SEVSEG_DIG5;
		driver_ones_digit = SEVSEG_DIG4;
		break;
	case 9:
		driver_num = 1;
		driver_tens_digit = SEVSEG_DIG7;
		driver_ones_digit = SEVSEG_DIG6;
		break;
	case 10:
		driver_num = 1;
		driver_tens_digit = SEVSEG_DIG5;
		driver_ones_digit = SEVSEG_DIG4;
		break; 
	case 11:
		driver_num = 2;
		driver_tens_digit = SEVSEG_DIG7;
		driver_ones_digit = SEVSEG_DIG6;
		break;
	case 12:
		driver_num = 2;
		driver_tens_digit = SEVSEG_DIG5;
		driver_ones_digit = SEVSEG_DIG4;
		break;
	case 13:
		driver_num = 1;
		driver_tens_digit = SEVSEG_DIG3;
		driver_ones_digit = SEVSEG_DIG2;
		break;
	case 14:
		driver_num = 2;
		driver_tens_digit = SEVSEG_DIG1;
		driver_ones_digit = SEVSEG_DIG0;
		break;
	case 15:
		driver_num = 2;
		driver_tens_digit = SEVSEG_DIG3;
		driver_ones_digit = SEVSEG_DIG2;
		break;
	case 16:
		driver_num = 0;
		driver_tens_digit = SEVSEG_DIG1;
		driver_ones_digit = SEVSEG_DIG0;
		break;
	case 17:
		driver_num = 0;
		driver_tens_digit = SEVSEG_DIG7;
		driver_ones_digit = SEVSEG_DIG6;
		break;
	case 18:
		driver_num = 4;
		driver_tens_digit = SEVSEG_DIG3;
		driver_ones_digit = SEVSEG_DIG2;
		break;
	}
		ones_digit = rarity_value % 10;
		tens_digit = (rarity_value - ones_digit) / 10;
		
		// write ones value
		
		spiData[0]=reverse(digit_map[ones_digit]);
		spiData[1]=driver_ones_digit;
		spi_select_device(SPI,&RARITY);
		spi_write_packet(SPI,driver_num==4 ? spiData : nopSpiData,2);
		spi_write_packet(SPI,driver_num==3 ? spiData : nopSpiData,2);
		spi_write_packet(SPI,driver_num==2 ? spiData : nopSpiData,2);
		spi_write_packet(SPI,driver_num==1 ? spiData : nopSpiData,2);
		spi_write_packet(SPI,driver_num==0 ? spiData : nopSpiData,2);
		spi_deselect_device(SPI,&RARITY);
		
		// write tens value
		if (tens_digit == 0) {
			spiData[0]= 0;
		} else {
			spiData[0]=reverse(digit_map[tens_digit]);
		}
		spiData[1]=driver_tens_digit;
		spi_select_device(SPI,&RARITY);
		spi_write_packet(SPI,driver_num==4 ? spiData : nopSpiData,2);
		spi_write_packet(SPI,driver_num==3 ? spiData : nopSpiData,2);
		spi_write_packet(SPI,driver_num==2 ? spiData : nopSpiData,2);
		spi_write_packet(SPI,driver_num==1 ? spiData : nopSpiData,2);
		spi_write_packet(SPI,driver_num==0 ? spiData : nopSpiData,2);
		spi_deselect_device(SPI,&RARITY);
}

void rarity_clear_all() {
	struct spi_device RARITY = {
		.id =  SPI_NPCS
	};
	uint8_t nopSpiData = {0x0, 0x0};
	uint8_t spiData[2];
	 for (int j=0; j < 5; j++) {
		 for (int i=1;i<=8;i++) {
			 //delay_ms(100);
			 //spiData[0] = reverse((4+i)%10);
			 spiData[0] = reverse(0);
			 spiData[1] = reverse(i);
			 
			 //delay_ms(200);
			 spi_select_device(SPI,&RARITY);
			 spi_write_packet(SPI,j==0 ? spiData : nopSpiData,2);
			 spi_write_packet(SPI,j==1 ? spiData : nopSpiData,2);
			 spi_write_packet(SPI,j==2 ? spiData : nopSpiData,2);
			 spi_write_packet(SPI,j==3 ? spiData : nopSpiData,2);
			 spi_write_packet(SPI,j==4 ? spiData : nopSpiData,2);
			 spi_deselect_device(SPI,&RARITY);
			 
		 }
	 }
}
// Will want to move this to an area reserved for all SPI functions
unsigned int reverse(unsigned int v) {
	static const unsigned char BitReverseTable256[] =
	{
		0x00, 0x80, 0x40, 0xC0, 0x20, 0xA0, 0x60, 0xE0, 0x10, 0x90, 0x50, 0xD0, 0x30, 0xB0, 0x70, 0xF0,
		0x08, 0x88, 0x48, 0xC8, 0x28, 0xA8, 0x68, 0xE8, 0x18, 0x98, 0x58, 0xD8, 0x38, 0xB8, 0x78, 0xF8,
		0x04, 0x84, 0x44, 0xC4, 0x24, 0xA4, 0x64, 0xE4, 0x14, 0x94, 0x54, 0xD4, 0x34, 0xB4, 0x74, 0xF4,
		0x0C, 0x8C, 0x4C, 0xCC, 0x2C, 0xAC, 0x6C, 0xEC, 0x1C, 0x9C, 0x5C, 0xDC, 0x3C, 0xBC, 0x7C, 0xFC,
		0x02, 0x82, 0x42, 0xC2, 0x22, 0xA2, 0x62, 0xE2, 0x12, 0x92, 0x52, 0xD2, 0x32, 0xB2, 0x72, 0xF2,
		0x0A, 0x8A, 0x4A, 0xCA, 0x2A, 0xAA, 0x6A, 0xEA, 0x1A, 0x9A, 0x5A, 0xDA, 0x3A, 0xBA, 0x7A, 0xFA,
		0x06, 0x86, 0x46, 0xC6, 0x26, 0xA6, 0x66, 0xE6, 0x16, 0x96, 0x56, 0xD6, 0x36, 0xB6, 0x76, 0xF6,
		0x0E, 0x8E, 0x4E, 0xCE, 0x2E, 0xAE, 0x6E, 0xEE, 0x1E, 0x9E, 0x5E, 0xDE, 0x3E, 0xBE, 0x7E, 0xFE,
		0x01, 0x81, 0x41, 0xC1, 0x21, 0xA1, 0x61, 0xE1, 0x11, 0x91, 0x51, 0xD1, 0x31, 0xB1, 0x71, 0xF1,
		0x09, 0x89, 0x49, 0xC9, 0x29, 0xA9, 0x69, 0xE9, 0x19, 0x99, 0x59, 0xD9, 0x39, 0xB9, 0x79, 0xF9,
		0x05, 0x85, 0x45, 0xC5, 0x25, 0xA5, 0x65, 0xE5, 0x15, 0x95, 0x55, 0xD5, 0x35, 0xB5, 0x75, 0xF5,
		0x0D, 0x8D, 0x4D, 0xCD, 0x2D, 0xAD, 0x6D, 0xED, 0x1D, 0x9D, 0x5D, 0xDD, 0x3D, 0xBD, 0x7D, 0xFD,
		0x03, 0x83, 0x43, 0xC3, 0x23, 0xA3, 0x63, 0xE3, 0x13, 0x93, 0x53, 0xD3, 0x33, 0xB3, 0x73, 0xF3,
		0x0B, 0x8B, 0x4B, 0xCB, 0x2B, 0xAB, 0x6B, 0xEB, 0x1B, 0x9B, 0x5B, 0xDB, 0x3B, 0xBB, 0x7B, 0xFB,
		0x07, 0x87, 0x47, 0xC7, 0x27, 0xA7, 0x67, 0xE7, 0x17, 0x97, 0x57, 0xD7, 0x37, 0xB7, 0x77, 0xF7,
		0x0F, 0x8F, 0x4F, 0xCF, 0x2F, 0xAF, 0x6F, 0xEF, 0x1F, 0x9F, 0x5F, 0xDF, 0x3F, 0xBF, 0x7F, 0xFF
	};

	// Return reverse
	return (BitReverseTable256[v & 0xff]);
}