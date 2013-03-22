/**
 * \file
 *
 * \brief User board configuration template
 *
 */

#ifndef CONF_BOARD_H
#define CONF_BOARD_H

#define BOARD_OSC0_HZ			BOARD_XOSC_HZ
#define BOARD_OSC0_IS_XTAL		false
#define BOARD_OSC0_STARTUP_US	17000

// This the HEARTBEAT.  Thats why this is named
// HEARTBEAT project. HEAR DA HEARTBEATBEAT
#define	CLKOUT					AVR32_PIN_PB02


#endif // CONF_BOARD_H
