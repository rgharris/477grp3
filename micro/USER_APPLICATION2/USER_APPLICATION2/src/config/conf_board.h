/**
 * \file
 *
 * \brief User board configuration template
 *
 */

#ifndef CONF_BOARD_H
#define CONF_BOARD_H

// Internal oscillator
#define BOARD_OSC0_HZ			12000000
#define BOARD_OSC0_STARTUP_US	1100
#define BOARD_OSC0_IS_XTAL		false

#define CLKOUT					AVR32_PIN_PA11

#endif // CONF_BOARD_H
