/*
 * RGB.h
 *
 * Created: 3/30/2013 12:57:03 PM
 *  Author: team3
 */ 


#ifndef RGB_H_
#define RGB_H_

#include <asf.h>
#include <Catan.h>

#define TRANS_TIME	7 // A number 0-4 will define the time taken to change color
#define FAST_TIME 0

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
#define COLOR_BRICK 0xE08000 //0xE07000
#define COLOR_ORANGE 0xD09000
#define COLOR_YELLOW 0xF0C000
#define COLOR_PINK 0xff69b4
#define COLOR_TEAL 0x00F0B0
#define COLOR_SEA  0x00D080
#define COLOR_BLACK 0x000000
#define COLOR_WHITE 0xFFFFFF
#define COLOR_SHEEP 0xFFFF00
#define COLOR_WHEAT 0xFAC520
#define COLOR_SGREEN 0x00ff5f
#define COLOR_WOOD  0x00fF00
#define COLOR_ERROR 0xFF0000 //0xFF
#define COLOR_PURPLE 0xC000A0
#define COLOR_INDIGO 0x8060C0
#define COLOR_MAGENTA 0xC0A070
#define COLOR_ORE	 0xB0B070 //0xB09090  //0xB0B090
#define COLOR_DESERT 0xD0A050//0xF0F0A0
#define COLOR_TAN	 0xD0B060
#define COLOR_GREY   0xB0B070
#define COLOR_DGREY  0x808030
#define COLOR_CONFIRM 0x0000FF


void clockRGB( void );
void lightRGB(int deviceAddress, int colorAddress, int brightness, int transTime);
void rgb_loop_test( void );
void rgb_hex_set(int hex_num, int color); 
void rgb_clear_all( void );
void rgb_display_resource(int hex_num,int resource);
void rgb_hex_set_variable(int hex_num, int color, uint8_t speed);




#endif /* RGB_H_ */