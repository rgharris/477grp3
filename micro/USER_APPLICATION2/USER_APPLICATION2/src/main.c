/**
 * \file
 *
 * \brief Empty user application template
 *
 */

/*
 * Include header files for all drivers that have been imported from
 * Atmel Software Framework (ASF).
 */
#include <asf.h>
#include <avr32/uc3b064.h>

//prototypes
void blinkLED(uint32_t led);
void seg_write(uint16_t);
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

	while(1) {
	  // int deviceAddress,  int colorAddress, int brightness, int transTime
	  lightRGB(0, 0, 15, 4);
	  delay_ms(1000);
	  lightRGB(0, 16, 0, 4);
	  delay_ms(1000);
	  lightRGB(0, 8, 15, 4);
	  delay_ms(1000);
	  lightRGB(0, 0,  0, 4);
	  delay_ms(1000);
	  lightRGB(0, 16, 15, 4);
	  delay_ms(1000);
	  lightRGB(0, 8,  0, 4);
	  delay_ms(1000);
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

void blinkLED(uint32_t led)
{
	ioport_set_pin_level(led,true);
	delay_ms(500);
	ioport_set_pin_level(led,false);
	delay_ms(500);
}

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