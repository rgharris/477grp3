/*
 * I2C.h
 *
 * Created: 3/28/2013 6:29:44 PM
 *  Author: team3
 */ 

#ifndef I2C_H_
#define I2C_H_

#include <asf.h>
#include <Catan.h>

//--------------------------------------------------------------------------------------------------------------
//------------------------------------------ T W I   S L A V E -------------------------------------------------
//--------------------------------------------------------------------------------------------------------------

//! Defines & Variables to manage a virtual TWI memory
#define TWI_MEM_SIZE    30 // The size of the virtual mem
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
#define CURRENT_PLAYER_REG			1		// The current turn's player
#define PLAYER_COUNT_REG			2		// Number of players playing this game
#define MCU_EVENT_REG				3		// Flags for the MCU to set
#define PLAYERS_THIEFED_REG			4		// Players which are adjacent to the thief
#define NEW_PIECE_LOC_REG			5		// Position of the piece to be confirmed, used as a check for the Pi
#define PIECE_TYPE_REG				6		// The Type of the piece of interest (To be confirmed or error)
#define NEW_PIECE_PORT_REG			7		// Set to appropriate value if new piece is next to port
#define LONGEST_ROAD_REG			8		// Which player has the longest road?
#define DIE_VALUE_REG				9		// The value on the die roll
#define RESOURCE_REC_REG			10		// 4x5 Array of resources each player receives on the die roll

// Register 0: Pi Events
#define PI_TURN_ON				1			// Pi is booted
#define PI_NEW_GAME				2			// Start a new game
#define PI_DICE_ROLLED			3			// A player wants to roll the dice
#define PI_END_TURN				4			// End the current player's turn
#define PI_DEV_ROAD				5			// A road building card was played
#define PI_DEV_KNIGHT			6			// A knight was played
#define PI_NEW_PIECE_CONFIRM	7			// Confirm the new piece in NEW_PIECE_LOC_REG
#define PI_NEW_PIECE_REJECT		8			// Deny the new piece in NEW_PIECE_LOC_REG
#define PI_CLEAR_I2CFLG			9			// So the Pi can tell the MCU to turn off the I2C flag if it needs to
#define PI_ROAD_PURCHASE		10			// A road was purchased
#define PI_SETTLEMENT_PURCHASE	11			// A settlement was purchased
#define PI_CITY_PURCHASE		12			// A city was purchased via web interface
#define PI_END_GAME				13			// The Game is Over
#define PI_SHUTDOWN				14			// The Pi is shutting down 
 

// Register 3: MCU Events (points to first register I2c should read)
#define MCU_NEW_PIECE_TBC		NEW_PIECE_LOC_REG		// Set if the MCU finds a new piece to be confirmed (indicated in NEW_PIECE_LOC_REG)
#define MCU_NEW_THIEF_TBC		PLAYERS_THIEFED_REG		// Set if the MCU is asking a thief to be confirmed
#define MCU_ERROR				PIECE_TYPE_REG			// Set if MCU detects piece that needs to be removed or replaced
#define MCU_DICE_READY			DIE_VALUE_REG			// Set when the Pi requests a dice roll
#define MCU_NEW_LONG_ROAD		LONGEST_ROAD_REG		// Set when a new player has longest road (0 if none)
#define MCU_ALL_CLEAR			11						// Set when there are no errors or new pieces on the board after there were before

// Register 6: Piece Type Code (10's digit is what action is needed, 1's digit is the type of piece
#define PIECE_TYPE_TBC			10			// The piece needs confirmation from the player	
#define PIECE_TYPE_REMOVE		20			// The piece needs to be removed by the player
#define PIECE_TYPE_REPLACE		30			// The piece needs to be replaced by the player
#define PIECE_TYPE_THIEF		 0			// The piece is a thief
#define PIECE_TYPE_ROAD			 1			// The piece is a road
#define PIECE_TYPE_SETTLEMENT	 2			// The piece is a settlement
#define PIECE_TYPE_CITY			 3			// The piece is a city

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