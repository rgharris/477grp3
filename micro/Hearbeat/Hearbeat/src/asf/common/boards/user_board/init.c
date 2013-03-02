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
	ioport_enable_pin(CLKOUT);
	ioport_set_pin_dir(CLKOUT, IOPORT_DIR_OUTPUT);
	ioport_set_pin_level(CLKOUT, IOPORT_PIN_LEVEL_HIGH);
}
