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
#define TWI_MEM_SIZE    29 // The size of the virtual mem
#define TWI_MEM_IDLE    0  // Idle state
#define TWI_MEM_ADDR    1  // Address state
#define TWI_MEM_DATA    2  // Data state

#define FOSC0 48000000



//------------------  C O N F I G U R A T I O N S  -------------------

#define EEPROM_ADDRESS        0x50        // EEPROM's TWI address
#define EEPROM_ADDR_LGT       1           // Address length of the EEPROM memory
#define VIRTUALMEM_ADDR_START 0x0         // Address of the virtual mem in the EEPROM
#define TWI_SPEED             100000       // Speed of TWI

//------------------  D E F I N I T I O N S  -------------------

//! \brief Constants to define the sent and received pattern
#define  PATTERN_TEST_LENGTH        (sizeof(test_pattern)/sizeof(U8))

// Register Map
#define PI_EVENT_REG				0		// Flags for the Pi to set
#define MCU_EVENT_REG				1		// Flags for the MCU to set
#define NEW_PIECE_LOC_REG			2		// Position of the piece to be confirmed, used as a check for the Pi
#define PIECE_TYPE_REG				3		// The Type of the piece of interest (To be confirmed or error)
#define NEW_PIECE_PORT_REG			4		// Set to appropriate value if new piece is next to port
#define PLAYER_COUNT_REG			5		// Number of players playing this game
#define CURRENT_PLAYER_REG			6		// The current turn's player
#define LONGEST_ROAD_REG			7		// Which player has the longest road?
#define DIE_VALUE_REG				8		// The value on the die roll
#define RESOURCE_REC_REG			9		// 4x5 Array of resources each player receives on the die roll

// Register 0: Pi Event Flags
#define PI_NEW_GAME				0x01		// Set if New Game should start
#define PI_DICE_ROLL			0x02		// Set if a player has rolled the dice
#define PI_END_TURN				0x04		// Set if the current player ended their turn
#define PI_DEV_ROAD				0x08		// Set if the player played a Road Building development card
#define PI_DEV_KNIGHT			0x10		// Set if the player played a Knight development card or after a 7 roll
#define PI_NEW_PIECE_CONFIRM	0x20		// Set if the piece in the NEW_PIECE_LOC_REG is confirmed by player
#define PI_NEW_PIECE_REJECT		0x40		// Set if the piece in NEW_PIECE_LOC_REG is rejected
#define PI_PIECE_PURCHASE		0xC0		// 0 = no purchase, 1 = road, 2 = settlement, 3 = city

// Register 1: MCU Event Flags
#define MCU_NEW_PIECE_TBC		0x01		// Set if the MCU finds a new piece to be confirmed (indicated in NEW_PIECE_LOC_REG)
#define MCU_ERROR_REMOVE		0x02		// Set if MCU detects piece that needs to be removed
#define MCU_ERROR_REPLACE		0x04		// Set if MCU detects piece that needs to be replaced

// Global Variables
extern U8  s_memory[TWI_MEM_SIZE];




int I2C_init( void );
uint8_t isDiceRolled(void);
uint8_t isTurnOver(void);
uint8_t isNewGame(void);
uint8_t isRoadBuildingPlayed(void);
uint8_t isKnightPlayed(void);
uint8_t isNewPieceConfirm(void);
uint8_t isNewPieceReject(void);
uint8_t PiecePurchased(void);

/*static void twi_slave_rx( U8 u8_value );
static U8 twi_slave_tx( void );
static void twi_slave_stop( void );*/

#endif /* I2C_H_ */