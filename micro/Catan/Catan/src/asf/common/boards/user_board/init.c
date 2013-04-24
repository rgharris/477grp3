/**
 * \file
 *
 * \brief User board initialization template
 *
 */

#include <asf.h>
#include <board.h>
#include <conf_board.h>
#include <RarityDisplay.h>
#include <I2C.h>

void board_init(void)
{
	wdt_disable();
	sysclk_init();
	ioport_init();
	
	
	// Init pins for Hall Effect Sensor Network
	ioport_enable_port(HE_RETURN_PORT,HE_RETURN_MASK);
	ioport_set_port_dir(HE_RETURN_PORT,HE_RETURN_MASK,IOPORT_DIR_INPUT);
	ioport_enable_port(HE_RETURN_PORT,HE_ADDR_PINS_MASK);
	ioport_set_port_dir(HE_RETURN_PORT,HE_ADDR_PINS_MASK,IOPORT_DIR_OUTPUT);
	ioport_enable_pin(MIDDLE_SENSOR);
	ioport_set_pin_dir(MIDDLE_SENSOR, IOPORT_DIR_INPUT);
	ioport_set_pin_mode(MIDDLE_SENSOR,IOPORT_MODE_PULLUP);
	
	// Init pins for RGB Display
	ioport_enable_pin(RGB_CLK);
	ioport_set_pin_dir(RGB_CLK,IOPORT_DIR_OUTPUT);
	ioport_enable_pin(RGB_DATA);
	ioport_set_pin_dir(RGB_DATA,IOPORT_DIR_OUTPUT);
	
	// SPI init
	static const gpio_map_t SPI_GPIO_MAP = {
	{SPI_SCK_PIN, SPI_SCK_FUNCTION},
	{SPI_MISO_PIN, SPI_MISO_FUNCTION},
	{SPI_MOSI_PIN, SPI_MOSI_FUNCTION},
	{SPI_NPCS0_PIN, SPI_NPCS0_FUNCTION}
	};
	
	gpio_enable_module(SPI_GPIO_MAP,sizeof(SPI_GPIO_MAP)/sizeof(SPI_GPIO_MAP[0]));
	delay_ms(100);
	rarity_init();
	I2C_init();
	
	
}