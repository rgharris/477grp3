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
#include <board.h>
#include <ioport.h>
#include <delay.h>
#include <spi_master.h>

void blinkLED(uint32_t led);
void spi_init_pins(void);


int main (void)
{
	board_init();
	sysclk_init();
	ioport_init();
	

	
	ioport_set_pin_dir(LED,IOPORT_DIR_OUTPUT);
		

	// Insert application code here, after the board has been initialized.
	
	while (1){
		blinkLED(LED);
	}
	
}

void blinkLED(uint32_t led)
{
	ioport_set_pin_level(led,true);
	delay_ms(500);
	ioport_set_pin_level(led,false);
	delay_ms(500);
}

void spi_init_pins(void)
{
	//disable SPI pins so they can be controlled by SPI peripheral
	ioport_disable_pin(SS);
	ioport_disable_pin(MOSI);
	ioport_disable_pin(MISO);
	ioport_disable_pin(CS0);
	ioport_disable_pin(SCK);
	
	ioport_set_pin_dir(SS,IOPORT_DIR_INPUT);
	ioport_set_pin_mode(SS,IOPORT_MODE_PULLUP);
	
	ioport_set_pin_dir(SCK, IOPORT_DIR_OUTPUT);
	ioport_set_pin_mode(SCK,IOPORT_MODE_MUX_A);
	
	ioport_set_pin_dir(MOSI,IOPORT_DIR_OUTPUT);
	ioport_set_pin_mode(MOSI,IOPORT_MODE_MUX_A);
	
	ioport_set_pin_dir(CS0, IOPORT_DIR_OUTPUT);
	ioport_set_pin_mode(CS0, IOPORT_MODE_MUX_A);
	
	ioport_set_pin_dir(MISO, IOPORT_DIR_INPUT);
	ioport_set_pin_mode(MISO, IOPORT_MODE_MUX_C);
}

   void spi_init_module(void)
   {
      struct spi_device spi_device_conf = {
          .id = CS0
      };

      spi_master_init(&AVR32_SPI);
      spi_master_setup_device(&AVR32_SPI, &spi_device_conf, SPI_MODE_0, 1000000, 0);
      spi_enable(&AVR32_SPI);
   }