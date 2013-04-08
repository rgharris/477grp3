/*
 * RGB.h
 *
 * Created: 3/30/2013 12:57:03 PM
 *  Author: team3
 */ 


#ifndef RGB_H_
#define RGB_H_

#include <asf.h>

#define TRANS_TIME	0 // A number 0-4 will define the time taken to change color

// RG Color Address
#define A0 0
#define A1 1
#define A2 2
#define B0 8
#define B1 9
#define B2 10
#define C0 16
#define C1 17
#define C2 18

// RGB COLOURS
#define COLOR_RED 0xFF0000
#define COLOR_GREEN 0x00FF00
#define COLOR_LIME 0x00ff7f
#define COLOR_BLUE 0x0000FF
#define COLOR_BRICK 0xE07000
#define COLOR_PINK 0xff69b4
#define COLOR_TEAL 0x008080
#define COLOR_BLACK 0x000000
#define COLOR_WHITE 0xFFFFFF
#define COLOR_SHEEP 0xFFFF00
#define COLOR_WHEAT 0xFAC520
#define COLOR_SGREEN 0x00ff5f
#define COLOR_WOOD  0x00fF00
#define COLOR_ERROR 0xFF0000
#define COLOR_ORE	0xB09090  //0xB0B090
#define COLOR_DESERT 0xF0F0B0


void clockRGB( void );
void lightRGB(int deviceAddress, int colorAddress, int brightness, int transTime);
void rgb_loop_test( void );
void rgb_hex_set(int hex_num, int color); 
void rgb_clear_all();
void rgb_display_resource(int hex_num,int resource);




#endif /* RGB_H_ */