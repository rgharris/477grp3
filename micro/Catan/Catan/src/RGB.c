/*
 * RGB.c
 *
 * Created: 3/30/2013 12:59:11 PM
 *  Author: team3
 */ 

#include <RGB.h>
#include <Catan.h>

void rgb_clear_all() {
	lightRGB(7,0x2E,0,0);
}

void clockRGB()
{
	delay_ms(0.2);
	ioport_set_pin_level(RGB_CLK,false);
	delay_ms(0.2);
	ioport_set_pin_level(RGB_CLK,true);
}

void lightRGB(int deviceAddress,  int colorAddress, int brightness, int transTime) {
	// transTime is in range 0 to 31 (5-bit)
	// brightness is in range 0 to 15 (4-bit)
	// colorAddress is in range 0 to 63 (6-bit)
	// deviceAddress is in range 0 to 63 (6-bit)
	int control = 1;
	int pin;
	
	long long output  =  ((long long) 0xFF8 << 28) +
	((deviceAddress & 63) << 22) +
	((control & 1) << 20) +
	((colorAddress & 63) << 14) +
	((transTime & 8) << 13) +
	((0) << 12) +
	((transTime & 7) << 8) +
	((brightness & 15) << 4);
	
	long long mask = (long long) 0x1 << 39;
	
	for (int i = 40; i>0; i--) {
	  if (output & mask) { ioport_set_pin_level(RGB_DATA, true); pin =1; }
      else { ioport_set_pin_level(RGB_DATA, false); pin = 0;}
      clockRGB();
      mask = mask >> 1;
    }
}
void rgb_hex_set(int hex_num, int color) {
	//RBG
	int red_int = (color & (0xF00000)) >> 20;
	int green_int = (color & (0x00F000)) >> 12;
	int blue_int = (color & (0x0000F0)) >> 4;
	switch (hex_num)
	{
		case 0:
		  lightRGB(3,A2,red_int,TRANS_TIME); // Device 3, Channel A2
		  lightRGB(3,B2,blue_int,TRANS_TIME); // Device 3, Channel B2
		  lightRGB(3,C2,green_int,TRANS_TIME); // Device 3, Channel C2
		  break;
		case 1:
		  lightRGB(6,A2,red_int,TRANS_TIME); // Device 4, Channel A2
		  lightRGB(6,B2,blue_int,TRANS_TIME); // Device 4, Channel B2
		  lightRGB(6,C2,green_int,TRANS_TIME); // Device 4, Channel C2
		  break;
		case 2:
		  lightRGB(6,A1,red_int,TRANS_TIME); // Device 3, Channel A1
		  lightRGB(6,B1,blue_int,TRANS_TIME); // Device 3, Channel B1
		  lightRGB(6,C1,green_int,TRANS_TIME); // Device 3, Channel C1
		  break;
		case 3:
		  lightRGB(6,A0,red_int,TRANS_TIME); // Device 4, Channel A0
		  lightRGB(6,B0,blue_int,TRANS_TIME); // Device 4, Channel B0
		  lightRGB(6,C0,green_int,TRANS_TIME); // Device 4, Channel C0
		  break;
	    case 4:
		  lightRGB(5,A1,red_int,TRANS_TIME); // Device 5, Channel A1
		  lightRGB(5,B1,blue_int,TRANS_TIME); // Device 5, Channel B1
		  lightRGB(5,C1,green_int,TRANS_TIME); // Device 5, Channel C1
		  break;
		case 5:
		  lightRGB(5,A2,red_int,TRANS_TIME); // Device 5, Channel A2
		  lightRGB(5,B2,blue_int,TRANS_TIME); // Device 5, Channel B2
		  lightRGB(5,C2,green_int,TRANS_TIME); // Device 5, Channel C2
		  break;
		case 6:
		  lightRGB(0,A2,red_int,TRANS_TIME); // Device 0, Channel A2
		  lightRGB(0,B2,blue_int,TRANS_TIME); // Device 0, Channel B2
		  lightRGB(0,C2,green_int,TRANS_TIME); // Device 0, Channel C2
		  break;
		case 7:
		  lightRGB(1,A2,red_int,TRANS_TIME); // Device 1, Channel A2
		  lightRGB(1,B2,blue_int,TRANS_TIME); // Device 1, Channel B2
		  lightRGB(1,C2,green_int,TRANS_TIME); // Device 1, Channel C2
		  break;
		case 8:
		  lightRGB(0,A1,red_int,TRANS_TIME); // Device 0, Channel A1
		  lightRGB(0,B1,blue_int,TRANS_TIME); // Device 0, Channel B1
		  lightRGB(0,C1,green_int,TRANS_TIME); // Device 0, Channel C1
		  break;
		case 9:
		  lightRGB(1,A0,red_int,TRANS_TIME); // Device 1, Channel A0
		  lightRGB(1,B0,blue_int,TRANS_TIME); // Device 1, Channel B0
		  lightRGB(1,C0,green_int,TRANS_TIME); // Device 1, Channel C0
		  break;
		case 10:
		  lightRGB(1,A1,red_int,TRANS_TIME); // Device 1, Channel A1
		  lightRGB(1,B1,blue_int,TRANS_TIME); // Device 1, Channel B1
		  lightRGB(1,C1,green_int,TRANS_TIME); // Device 1, Channel C1
		  break;
		case 11:
		  lightRGB(2,A1,red_int,TRANS_TIME); // Device 2, Channel A1
		  lightRGB(2,B1,blue_int,TRANS_TIME); // Device 2, Channel B1
		  lightRGB(2,C1,green_int,TRANS_TIME); // Device 2, Channel C1
		  break;		  
		case 12:
		  lightRGB(2,A2,red_int,TRANS_TIME); // Device 2, Channel A2
		  lightRGB(2,B2,blue_int,TRANS_TIME); // Device 2, Channel B2
		  lightRGB(2,C2,green_int,TRANS_TIME); // Device 2, Channel C2
		  break;
		case 13:
		  lightRGB(2,A0,red_int,TRANS_TIME); // Device 2, Channel A0
		  lightRGB(2,B0,blue_int,TRANS_TIME); // Device 2, Channel B0
		  lightRGB(2,C0,green_int,TRANS_TIME); // Device 2, Channel C0
		  break;
		case 14:
		  lightRGB(3,A0,red_int,TRANS_TIME); // Device 3, Channel A0
		  lightRGB(3,B0,blue_int,TRANS_TIME); // Device 3, Channel B0
		  lightRGB(3,C0,green_int,TRANS_TIME); // Device 3, Channel C0
		  break;
		case 15:
		  lightRGB(3,A1,red_int,TRANS_TIME); // Device 3, Channel A1
		  lightRGB(3,B1,blue_int,TRANS_TIME); // Device 3, Channel B1
		  lightRGB(3,C1,green_int,TRANS_TIME); // Device 3, Channel C1
		  break;
		case 16:
		  lightRGB(5,A0,red_int,TRANS_TIME); // Device 5, Channel A0
		  lightRGB(5,B0,blue_int,TRANS_TIME); // Device 5, Channel B0
		  lightRGB(5,C0,green_int,TRANS_TIME); // Device 5, Channel C0
		  break;
		case 17:
		  lightRGB(0,A0,red_int,TRANS_TIME); // Device 0, Channel A0
		  lightRGB(0,B0,blue_int,TRANS_TIME); // Device 0, Channel B0
		  lightRGB(0,C0,green_int,TRANS_TIME); // Device 0, Channel C0
		  break;
		case 18:
		  lightRGB(4,A0,red_int,TRANS_TIME); // Device 6, Channel A0
		  lightRGB(4,B0,blue_int,TRANS_TIME); // Device 6, Channel B0
		  lightRGB(4,C0,green_int,TRANS_TIME); // Device 6, Channel C0
		  break;
		default:
		  break;		
	}
}


void rgb_loop_test() {
	lightRGB(7, 40, 0, TRANS_TIME);
	lightRGB(7, 42, 0, TRANS_TIME);
	lightRGB(7, 44, 0, TRANS_TIME);
	while(1) {
		// int deviceAddress,  int colorAddress, int brightness, int transTime
		lightRGB(7, 40, 15, TRANS_TIME);
		delay_ms(1000);
		lightRGB(7, 44, 0, TRANS_TIME);
		delay_ms(1000);
		lightRGB(7, 42, 15, TRANS_TIME);
		delay_ms(1000);
		lightRGB(7, 40,  0, TRANS_TIME);
		delay_ms(1000);
		lightRGB(7, 44, 15, TRANS_TIME);
		delay_ms(1000);
		lightRGB(7, 42,  0, TRANS_TIME);
		delay_ms(1000);
	}
}

void rgb_display_resource(int hexnum, int resource){
	switch (resource)
	{
	case ORE:
		rgb_hex_set(hexnum,COLOR_ORE);
		break;
	case WHEAT:
		rgb_hex_set(hexnum,COLOR_WHEAT);
		break;
	case SHEEP:
		rgb_hex_set(hexnum,COLOR_SHEEP);
		break;
	case BRICK:
		rgb_hex_set(hexnum,COLOR_BRICK);
		break;
	case WOOD:
		rgb_hex_set(hexnum,COLOR_WOOD);
		break;
	case DESERT:
		rgb_hex_set(hexnum,COLOR_DESERT);
		break;
	default:
		rgb_hex_set(hexnum,COLOR_ERROR);
		break;
	}
}