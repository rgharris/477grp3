/**
 * \file
 *
 * \brief	Cycles through a selected column (TESTCOL) of Hall Effect sensors.
 *			RGB stays red until the desired sensor is tripped. Turns green
 *			for a second then back to red for the next sensor. 
 * \todo	test for multiple columns, add column to hex map so not all the RGBs turn on
 */

/*
 * Include header files for all drivers that have been imported from
 * Atmel Software Framework (ASF).
 */
#include <asf.h>
#include <avr32/uc3b064.h>


#define DRIVER_ADDRESS	7 // A number 0-6
//#define RGB_ADDRESS		0 // A number 0-2
#define TRANS_TIME		0 // A number 0-4ish

#define TESTCOL			HE_COL1	// Multiplexer to test

//prototypes
//void blinkLED(uint32_t led);
//void seg_write(uint16_t);
void clockRGB();
void lightRGB(int deviceAddress,  int colorAddress, int brightness, int transTime);

int main (void)
{
	board_init();
	
	/*//seg_write(0x01FF);
	//Buffer to send data to SPI slave
	uint16_t txdata;
	//Buffer to receive data from SPI slave
	uint16_t rxdata;
	//Select given device on the SPI bus
	spi_selectChip(SPI_7SEG, SPI_7SEG_CS);
	//Wait for the transmitter to be ready
	while(!spi_is_tx_ready(SPI_7SEG));
	// Send the data to slave (ie = AT45DBX_CMDC_RD_STATUS_REG)
	txdata=0xD7;
	spi_put(SPI_7SEG,txdata);
	//Wait for a complete transmission
	while(!spi_is_tx_empty(SPI_7SEG))

	//Wait for the transmitter to be ready
	while(!spi_is_tx_ready(SPI_7SEG));
	// Send dummy data to slave (ie = 0x00)
	txdata=0x00;
	spi_put(SPI_7SEG,txdata);
	//Wait for a complete transmission
	while(!spi_is_tx_empty(SPI_7SEG));
	//Now simply read the data in the receive register
	rxdata=spi_get(SPI_7SEG);

	// Deselect the slave
	spi_unselectChip(SPI_7SEG,SPI_7SEG_CS);
    */
	
	// Row to Address
	ioport_port_mask_t he_addr = 0;
	
	// Initialize RGBs to off
	lightRGB(DRIVER_ADDRESS, 40, 0, TRANS_TIME);
	lightRGB(DRIVER_ADDRESS, 42, 0, TRANS_TIME);
	lightRGB(DRIVER_ADDRESS, 44, 0, TRANS_TIME);
	
	// Sensor return value (1 = magnet detected, 0 = else)
	int	he_return=0;
	
	
	while(1) {
		// For each mux position, 0-7, turn RGB red,
		// wait for magnet to be sensed, turn RGB green
		// and advance to the next position
		for (int i=0;i<8;i++)
		{
			// RGBs Red
			lightRGB(DRIVER_ADDRESS,42,0,TRANS_TIME);
			lightRGB(DRIVER_ADDRESS,40,15,TRANS_TIME);
			he_addr = i<<HE_ADDR_PIN_0;						// this line probably not needed can do in ioport function call
			ioport_set_port_level(HE_ADDR_PORT,HE_ADDR_PINS_MASK,he_addr);
			delay_ms(1000);
			//wait for magnet sensor
			he_return = 0;
			while (!he_return)
			{
				he_return=ioport_get_pin_level(TESTCOL);
			}
			// RGBs Green
			lightRGB(DRIVER_ADDRESS,40,0,TRANS_TIME);
			lightRGB(DRIVER_ADDRESS,42,15,TRANS_TIME);
			delay_ms(1000);
		}
		/*
		//he_new = ioport_get_pin_level(HE_COL0);
		//if (he_new != he_last)
		//{
			//he_last = he_new;
			//lightRGB(DRIVER_ADDRESS,44,he_new*15,TRANS_TIME);
		//}
		//delay_ms(20);
	  // int deviceAddress,  int colorAddress, int brightness, int transTime
	  //lightRGB(DRIVER_ADDRESS, 40, 15, TRANS_TIME);
	  //delay_ms(1000);
	  //lightRGB(DRIVER_ADDRESS, 44, 0, TRANS_TIME);
	  //delay_ms(1000);
	  //lightRGB(DRIVER_ADDRESS, 42, 15, TRANS_TIME);
	  //delay_ms(1000);
	  //lightRGB(DRIVER_ADDRESS, 40,  0, TRANS_TIME);
	  //delay_ms(1000);
	  //lightRGB(DRIVER_ADDRESS, 44, 15, TRANS_TIME);
	  //delay_ms(1000);
	  //lightRGB(DRIVER_ADDRESS, 42,  0, TRANS_TIME);
	  //delay_ms(1000);*/
	}
}


/*void shift_write(uint16_t data)
{
	
}

void seg_write(uint16_t spi_data)
{
	ioport_set_pin_level(LOAD,false);
	spi_write((&AVR32_SPI),spi_data);  // set segments high for dig 0
	ioport_set_pin_level(LOAD,true);
	delay_us(100);
}*/

void clockRGB()
{
	delay_ms(0.2);
	ioport_set_pin_level(RGB_CLK,false);
	delay_ms(0.2);
	ioport_set_pin_level(RGB_CLK,true);
}	

void lightRGB(int deviceAddress,  int colorAddress, int brightness, int transTime) {
	// transTime is in range 0 to 31 (5-bit)
	// brightness is in range 0 to 15 (4-bit)
	// colorAddress is in range 0 to 63 (6-bit)
	// deviceAddress is in range 0 to 63 (6-bit)
	int control = 1;
	int pin;
	
	long long output  =  ((long long) 0xFF8 << 28) +
	((deviceAddress & 63) << 22) +
	((control & 1) << 20) +
	((colorAddress & 63) << 14) +
	((transTime & 8) << 13) +
	((0) << 12) +
	((transTime & 7) << 8) +
	((brightness & 15) << 4);
	
	long long mask = (long long) 0x1 << 39;
	
	for (int i = 40; i>0; i--) {
	  if (output & mask) { ioport_set_pin_level(RGB_DATA, true); pin =1; }
      else { ioport_set_pin_level(RGB_DATA, false); pin = 0;}
      clockRGB();
      mask = mask >> 1;
    }
}