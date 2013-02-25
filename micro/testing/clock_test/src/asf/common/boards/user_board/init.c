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
	ioport_init();
	
	ioport_enable_pin(LED);
	ioport_set_pin_dir(RGB_DATA, IOPORT_DIR_OUTPUT);
	ioport_set_pin_dir(RGB_CLK, IOPORT_DIR_OUTPUT);
	ioport_set_pin_dir(LED, IOPORT_DIR_OUTPUT);
}	
	/* This function is meant to contain board-specific initialization code
	 * for, e.g., the I/O pins. The in
}
itialization can rely on application-
* specific board configuration, found in conf_board.h.
*/