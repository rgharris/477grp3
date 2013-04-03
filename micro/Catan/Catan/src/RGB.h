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
#define RED 0xFF0000
#define GREEN 0x00FF00
#define LIME 0x00ff7f
#define BLUE 0x0000FF
#define BRICK 0xE07000
#define PINK 0xff69b4
#define TEAL 0x008080
#define BLACK 0x000000
#define WHITE 0xFFFFFF
#define SHEEP 0xFFFF00
#define WHEAT 0xFAC520
#define SGREEN 0x00ff5f
#define WOOD  0x00fF00
#define ERROR 0xFF0000
#define ORE	  0xB0B090
#define DESERT 0xF0F0B0


void clockRGB( void );
void lightRGB(int deviceAddress, int colorAddress, int brightness, int transTime);
void rgb_loop_test( void );
void rgb_hex_set(int hex_num, int color); 
void rgb_clear_all();




#endif /* RGB_H_ */