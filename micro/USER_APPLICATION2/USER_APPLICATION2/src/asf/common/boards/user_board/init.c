/**
 * \file
 *
 * \brief User board initialization template
 *
 */

#include <asf.h>
#include <board.h>
#include <conf_board.h>

void spi_init_pins(void);
void spi_init_module(void);
void seg_init(void);

spi_options_t spi_7seg_options={
	// Slave number
	SPI_7SEG_CS,
	// Baud rate
	1000,
	// number bits per char
	8,
	// Delay before first clock pulse after slave select
	0,
	// Delay between each transfer
	0,
	// Set chip to stay active after transfer
	1,
	// SPI MODE
	SPI_MODE_0,
	// Disable mode fault detection
	1
};

void board_init(void)
{
	/* This function is meant to contain board-specific initialization code
	 * for, e.g., the I/O pins. The initialization can rely on application-
	 * specific board configuration, found in conf_board.h.
	 */
	ioport_init();
	board_init();
	sysclk_init();
	spi_init_pins();
	spi_init_module();
	seg_init();
	
	ioport_enable_pin(LED);
	ioport_set_pin_dir(LED,IOPORT_DIR_OUTPUT);
	
}

void seg_init(void)
{
	spi_write((&AVR32_SPI),0x0C01);  // normal operation
	spi_write((&AVR32_SPI),0x0900);  // decode mode off
	spi_write((&AVR32_SPI),0x0A0F);  // intensity high
	spi_write((&AVR32_SPI),0x0B07);  // set scan limit to maximum
}

void spi_init_pins(void)
{
	//disable SPI pins so they can be controlled by SPI peripheral
	ioport_disable_pin(SS);
	ioport_disable_pin(MOSI);
	ioport_disable_pin(MISO);
	ioport_disable_pin(CS0);
	ioport_disable_pin(SCK);
	
	ioport_set_pin_dir(SS,IOPORT_DIR_INPUT);
	ioport_set_pin_mode(SS,IOPORT_MODE_PULLUP);
	
	ioport_set_pin_dir(SCK, IOPORT_DIR_OUTPUT);
	ioport_set_pin_mode(SCK,IOPORT_MODE_MUX_A);
	
	ioport_set_pin_dir(MOSI,IOPORT_DIR_OUTPUT);
	ioport_set_pin_mode(MOSI,IOPORT_MODE_MUX_A);
	
	ioport_set_pin_dir(CS0, IOPORT_DIR_OUTPUT);
	ioport_set_pin_mode(CS0, IOPORT_MODE_MUX_A);
	
	ioport_set_pin_dir(MISO, IOPORT_DIR_INPUT);
	ioport_set_pin_mode(MISO, IOPORT_MODE_MUX_C);
}

void spi_init_module(void) {
	spi_initMaster(SPI_7SEG,&spi_7seg_options);
	// Setup chip config
	spi_setupChipReg(SPI_7SEG,&spi_7seg_options,sysclk_get_pba_hz());
	spi_enable(SPI_7SEG);
}

/*void spi_init_module(void)
{
	struct spi_device spi_device_conf = {
		.id = CS0
	};

	spi_master_init(&AVR32_SPI);
	spi_master_setup_device(&AVR32_SPI, &spi_device_conf, SPI_MODE_0, 1000, 0);
	spi_enable(&AVR32_SPI);
}*/
