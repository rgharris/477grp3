/*
 * I2C.h
 *
 * Created: 3/28/2013 6:29:44 PM
 *  Author: team3
 */ 

#ifndef I2C_H_
#define I2C_H_

#include <asf.h>

//--------------------------------------------------------------------------------------------------------------
//------------------------------------------ T W I   S L A V E -------------------------------------------------
//--------------------------------------------------------------------------------------------------------------

//! Defines & Variables to manage a virtual TWI memory
#define TWI_MEM_SIZE    20 // The size of the virtual mem
#define TWI_MEM_IDLE    0  // Idle state
#define TWI_MEM_ADDR    1  // Address state
#define TWI_MEM_DATA    2  // Data state

#define FOSC0 48000000



//------------------  C O N F I G U R A T I O N S  -------------------

#define EEPROM_ADDRESS        0x50        // EEPROM's TWI address
#define EEPROM_ADDR_LGT       3           // Address length of the EEPROM memory
#define VIRTUALMEM_ADDR_START 0x0         // Address of the virtual mem in the EEPROM
#define TWI_SPEED             100000       // Speed of TWI

//------------------  D E F I N I T I O N S  -------------------

//! \brief Constants to define the sent and received pattern
#define  PATTERN_TEST_LENGTH        (sizeof(test_pattern)/sizeof(U8))





void I2C_test( void );
/*static void twi_slave_rx( U8 u8_value );
static U8 twi_slave_tx( void );
static void twi_slave_stop( void );*/

#endif /* I2C_H_ */