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
#define LED			AVR32_PIN_PA18

// RGB 
#define RGB_CLK		AVR32_PIN_PB10
#define RGB_DATA	AVR32_PIN_PB11

// RGB COLOURS
#define RED "FF0000"
#define GREEN "00FF00"
#define LIME "00ff7f"
#define BLUE "0000FF"
#define ORANGE "ff4500"
#define PINK "ff69b4"
#define TEAL "008080"
#define BLACK "000000"
#define WHITE "FFFFFF"

// SPI Pins
#define MOSI		AVR32_PIN_PA14
#define SCK			AVR32_PIN_PA15
#define CS0			AVR32_PIN_PA16
#define MISO		AVR32_PIN_PA28
#define SS			AVR32_PIN_PB01

// SPI
#define SPI_7SEG    (&AVR32_SPI)
#define SPI_7SEG_CS (0)

#endif // USER_BOARD_H
