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
	
	
	// Init pins for Hall Effect Sensor Network
	ioport_enable_port(HE_RETURN_PORT,HE_RETURN_MASK);
	ioport_set_port_dir(HE_RETURN_PORT,HE_RETURN_MASK,IOPORT_DIR_INPUT);
	ioport_enable_port(HE_RETURN_PORT,HE_ADDR_PINS_MASK);
	ioport_set_port_dir(HE_RETURN_PORT,HE_ADDR_PINS_MASK,IOPORT_DIR_OUTPUT);
	
	// Init pins for RGB Display
	ioport_enable_pin(RGB_CLK);
	ioport_set_pin_dir(RGB_CLK,IOPORT_DIR_OUTPUT);
	ioport_enable_pin(RGB_DATA);
	ioport_set_pin_dir(RGB_DATA,IOPORT_DIR_OUTPUT);
	
	// Init pins for debug
	ioport_enable_pin(CLKOUT);
	ioport_set_pin_dir(CLKOUT, IOPORT_DIR_OUTPUT);
	ioport_set_pin_level(CLKOUT, IOPORT_PIN_LEVEL_LOW);
	
	// Init pins for pushbutton
	ioport_enable_pin(PUSHBUTTON);
	ioport_set_pin_dir(PUSHBUTTON, IOPORT_DIR_INPUT);
	//ioport_set_pin_level(CLKOUT, IOPORT_PIN_LEVEL_LOW);
}
