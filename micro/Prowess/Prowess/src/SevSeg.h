/*
 * SevSeg.h
 *
 * Created: 3/29/2013 10:27:52 PM
 *  Author: Team Hex Me Baby
 */ 


#ifndef SEVSEG_H_
#define SEVSEG_H_

// AS1116 7 Segment Driver Registers

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




#endif /* SEVSEG_H_ */