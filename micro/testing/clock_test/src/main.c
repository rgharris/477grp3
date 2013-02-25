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
#include <pll.h>
#include <sysclk.h>
#include <delay.h>
void clkrgb(void);

int main (void)
{
	sysclk_init();
    board_init();
	struct pll_config pcfg;
	
	osc_enable(OSC_ID_OSC0);
	osc_wait_ready(OSC_ID_OSC0);
	
	pll_enable_source(CONFIG_PLL0_SOURCE);
	pll_config_defaults(&pcfg, 0);
	pll_config_set_option(&pcfg, PLL_OPT_OUTPUT_DIV);
	pll_enable(&pcfg, 0);
	pll_wait_for_lock(0);
	
	sysclk_set_prescalers(1,1,1);
	sysclk_set_source(SYSCLK_SRC_PLL0);
	
	//osc_enable(OSC_ID_OSC0);
	//osc_wait_ready(OSC_ID_OSC0);
	//sysclk_set_source(SYSCLK_SRC_OSC0);
	
	 // pll_config_init(&pcfg, PLL_SRC_OSC0, 1,
	 //  40000000 / BOARD_OSC0_HZ);
	 //  pll_enable(&pcfg, 0);
	 //  sysclk_set_prescalers(1,1,1);
	 //  pll_wait_for_lock(0);
	 // sysclk_set_source(SYSCLK_SRC_PLL0);
	//sysclk_set_source(SYSCLK_SRC_OSC0);
	
	
	while(1){
		clkrgb();
	}
	
	
	// Insert application code here, after the board has been initialized.
}

void clkrgb(void)
{
	ioport_set_pin_level(RGB_CLK, IOPORT_PIN_LEVEL_HIGH);
	delay_us(1);
	//asm("nop");
	ioport_set_pin_level(RGB_CLK, IOPORT_PIN_LEVEL_LOW);
	delay_us(1);
	//asm("nop");
}