/**
 * \file
 *
 * \brief User board configuration template
 *
 */

#ifndef CONF_BOARD_H
#define CONF_BOARD_H

// external oscillator
#define BOARD_OSC0_HZ			BOARD_XOSC_HZ
#define BOARD_OSC0_IS_XTAL		false
#define BOARD_OSC0_STARTUP_US	1100

// RGB
#define RGB_CLK		AVR32_PIN_PB10
#define RGB_DATA	AVR32_PIN_PB11

// SPI Connections
#define SPI						(&AVR32_SPI)
#define SPI_NPCS				0
#define SPI_SCK_PIN				AVR32_SPI_SCK_0_0_PIN
#define SPI_SCK_FUNCTION		AVR32_SPI_SCK_0_0_FUNCTION

#define SPI_MISO_PIN			AVR32_SPI_MISO_0_2_PIN
#define SPI_MISO_FUNCTION		AVR32_SPI_MISO_0_2_FUNCTION
#define SPI_MOSI_PIN			AVR32_SPI_MOSI_0_0_PIN
#define SPI_MOSI_FUNCTION		AVR32_SPI_MOSI_0_0_FUNCTION

#define SPI_NPCS0_PIN			AVR32_SPI_NPCS_0_0_PIN
#define SPI_NPCS0_FUNCTION		AVR32_SPI_NPCS_0_0_FUNCTION

// HALL EFFECT MUX return pins (configure as input)
#define HE_COL0					AVR32_PIN_PA03
#define HE_COL1					AVR32_PIN_PA04
#define HE_COL2					AVR32_PIN_PA05
#define HE_COL3					AVR32_PIN_PA06
#define HE_COL4					AVR32_PIN_PA07
#define HE_COL5					AVR32_PIN_PA08
#define HE_COL6					AVR32_PIN_PA11
#define HE_COL7					AVR32_PIN_PA12
#define HE_COL8					AVR32_PIN_PA13
#define HE_COL9					AVR32_PIN_PA17
#define HE_COL10				AVR32_PIN_PA19
#define HE_COL11				AVR32_PIN_PA23
#define HE_COL12				AVR32_PIN_PA24
#define HE_COL13				AVR32_PIN_PA25
#define HE_COL14				AVR32_PIN_PA26
#define HE_COL15				AVR32_PIN_PA27
#define HE_COL16				AVR32_PIN_PA30
#define HE_COL17				AVR32_PIN_PA31

#define HE_RETURN_PORT			AVR32_PORT_A
// \todo Should replace CF8A1CFC without a more robust way of making mask. No time to address right now.
#define HE_RETURN_MASK			0xCF8A39F8
#define HE_ADDR_PORT			AVR32_PORT_A
#define HE_ADDR_PIN_0			AVR32_PIN_PA20
#define HE_ADDR_PINS_MASK		(7<<HE_ADDR_PIN_0)



//#define PUSHBUTTON				AVR32_PIN_PB10

#define MIDDLE_SENSOR			AVR32_PIN_PB00


#endif // CONF_BOARD_H
