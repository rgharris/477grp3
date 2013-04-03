/*
 * RarityDisplay.h
 *
 * Created: 3/28/2013 6:16:41 PM
 *  Author: team3
 */ 


#ifndef RARITYDISPLAY_H_
#define RARITYDISPLAY_H_

#include <asf.h>

// Rarity Display Registers (already reversed)
#define SEVSEG_NOOP				0x00
#define SEVSEG_DIG0				0x80
#define SEVSEG_DIG1				0x40
#define SEVSEG_DIG2				0xC0
#define SEVSEG_DIG3				0x20
#define SEVSEG_DIG4				0xA0
#define SEVSEG_DIG5				0x60
#define SEVSEG_DIG6				0xE0
#define SEVSEG_DIG7				0x10
#define SEVSEG_DECODE			0x90
#define SEVSEG_INTENSITY_ALL	0x50
#define SEVSEG_SCANLIMIT		0xD0
#define SEVSEG_SHUTDOWN			0x30
#define SEVSEG_FEATURE			0x70
#define SEVSEG_TESTMODE			0xF0
#define SEVSEG_INTENSITY_01		0x08
#define SEVSEG_INTENSITY_23		0x88
#define SEVSEG_INTENSITY_45		0x48
#define SEVSEG_INTENSITY_67		0xC8
#define SEVSEG_ROAD				0xA0	// "r"
#define SEVSEG_CITY				0x72	// "C"
#define SEVSEG_SETTLEMENT		0xDA	// "S"
#define SEVSEG_THIEF			0x0E	// "T"

void rarity_init( void );
void rarity_set(unsigned int hex_num, unsigned int rarity_value);
void rarity_set_all(unsigned int * rarity_value_arr);
void rarity_clear_all(); 
void rarity_disp_error(unsigned int error_position);
unsigned int reverse(unsigned int v);
void display_error(unsigned int hex_num, unsigned int position, unsigned int isCity);



#endif /* RARITYDISPLAY_H_ */