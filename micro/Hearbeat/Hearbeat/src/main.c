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

int main (void)
{
	board_init();
	
	while(1)
	{
		ioport_set_pin_level(CLKOUT, IOPORT_PIN_LEVEL_HIGH);
	    asm("nop");
		ioport_set_pin_level(CLKOUT, IOPORT_PIN_LEVEL_LOW);
		asm("nop");
	}

}
