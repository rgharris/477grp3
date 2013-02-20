/**
 * \file
 *
 * \brief User board definition template
 *
 */

 /* This file is intended to contain definitions and configuration details for
 * features and devices that are available on the board, e.g., frequency and
 * startup time for an external crystal, external memory devices, LED and USART
 * pins.
 */

#ifndef USER_BOARD_H
#define USER_BOARD_H

#include <conf_board.h>

// External oscillator settings.
// Uncomment and set correct values if external oscillator is used.

// External oscillator frequency
//#define BOARD_XOSC_HZ          8000000

// External oscillator type.
//!< External clock signal
//#define BOARD_XOSC_TYPE        XOSC_TYPE_EXTERNAL
//!< 32.768 kHz resonator on TOSC
//#define BOARD_XOSC_TYPE        XOSC_TYPE_32KHZ
//!< 0.4 to 16 MHz resonator on XTALS
//#define BOARD_XOSC_TYPE        XOSC_TYPE_XTAL

// External oscillator startup time
//#define BOARD_XOSC_STARTUP_US  500000

// Internal oscillator
#define BOARD_OSC0_HZ			12000000
#define BOARD_OSC0_STARTUP_US	1100
#define BOARD_OSC0_IS_XTAL		false

// LED on portA pin 11
#define LED			AVR32_PIN_PA11

// SPI Pins
#define MOSI		AVR32_PIN_PA14
#define SCK			AVR32_PIN_PA15
#define CS0			AVR32_PIN_PA16
#define MISO		AVR32_PIN_PA28
#define SS			AVR32_PIN_PB00

#endif // USER_BOARD_H
