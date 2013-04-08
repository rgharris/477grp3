/**
 * \file
 *
 * \brief User board initialization template
 *
 */

#include <asf.h>
#include <board.h>
#include <conf_board.h>

void board_init(void)
{
	sysclk_init();
	ioport_init();
	//ioport_enable_pin(CLKOUT);
	//ioport_set_pin_dir(CLKOUT, IOPORT_DIR_OUTPUT);
	ioport_enable_pin(MIDDLE_SENSOR);
	ioport_set_pin_dir(MIDDLE_SENSOR, IOPORT_DIR_INPUT);
	ioport_set_pin_mode(MIDDLE_SENSOR,IOPORT_MODE_PULLUP);
	//ioport_set_pin_level(CLKOUT, IOPORT_PIN_LEVEL_HIGH);
	
	// SPI
	static const gpio_map_t SPI_GPIO_MAP = {
		{SPI_SCK_PIN, SPI_SCK_FUNCTION},
		{SPI_MISO_PIN, SPI_MISO_FUNCTION},
		{SPI_MOSI_PIN, SPI_MOSI_FUNCTION},
		{SPI_NPCS0_PIN, SPI_NPCS0_FUNCTION}
	};
	
	gpio_enable_module(SPI_GPIO_MAP,sizeof(SPI_GPIO_MAP)/sizeof(SPI_GPIO_MAP[0]));
		
}
