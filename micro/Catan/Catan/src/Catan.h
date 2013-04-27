/*
 * Catan.h
 *
 * Created: 4/3/2013 6:06:08 PM
 *  Author: team3
 */ 


#ifndef CATAN_H_
#define CATAN_H_

#include <asf.h>
#include <RarityDisplay.h>
#include <RGB.h>
#include <I2C.h>

#define DISPLAY_DELAY	200
#define DISPLAY_DELAY_LOOP	200
#define ORE	0
#define WHEAT	1
#define SHEEP	2
#define BRICK	3
#define WOOD	4
#define DESERT	5
#define NO_RESOURCE	6

// Check Board State States
#define ALL_CONFIRMED	1
#define NEW_PIECE		0
#define ERROR		   -1

#define MIDDLE_THIEF_POS	144

#define BLINK_RATE 0x380
#define BLINK_RANGE 3

// Decided to go with the large map since all the adjacent positions were already figured
// in the spreadsheet without the adjustment

// Identified which positions are owned by which players (1-4).
// 0 for easy check for unowned

// Position map -- Everything you need to look up about a position!
// [hex position] [data field]
static int8_t pos_map[145][7] = {
	//adj pos 1,adj pos 2,adj pos 3,adj hex 1,adj hex 2,adj hex 3,Port
	{105,18,-1,0,-1,-1,-1},
	{54,19,-1,1,-1,-1,-1},
	{90,20,-1,2,1,-1,-1},
	{91,21,-1,3,-1,-1,-1},
	{93,22,-1,4,5,-1,-1},
	{57,23,-1,5,-1,-1,-1},
	{106,24,-1,6,17,-1,-1},
	{98,25,-1,7,9,-1,-1},
	{107,26,-1,8,-1,-1,-1},
	{62,27,-1,9,-1,-1,-1},
	{99,28,-1,10,-1,-1,-1},
	{64,29,-1,11,-1,-1,-1},
	{101,30,-1,12,-1,-1,-1},
	{100,31,-1,13,11,-1,-1},
	{102,32,-1,14,15,-1,-1},
	{66,33,-1,15,-1,-1,-1},
	{95,34,-1,16,-1,-1,-1},
	{70,35,-1,17,-1,-1,-1},
	{0,36,-1,0,-1,-1,ORE},
	{1,37,-1,1,-1,-1,DESERT},
	{2,109,38,2,1,3,-1},
	{3,39,-1,3,-1,-1,SHEEP},
	{4,113,40,4,5,16,-1},
	{5,41,-1,5,-1,-1,-1},
	{6,42,125,6,17,8,-1},
	{7,43,117,7,9,10,-1},
	{8,44,-1,8,-1,-1,BRICK},
	{9,45,-1,9,-1,-1,-1},
	{10,46,-1,10,-1,-1,WOOD},
	{11,47,-1,11,-1,-1,DESERT},
	{12,48,-1,12,-1,-1,WHEAT},
	{13,49,119,13,11,12,-1},
	{14,50,123,14,15,0,-1},
	{15,51,-1,15,-1,-1,-1},
	{16,52,-1,16,-1,-1,DESERT},
	{17,53,-1,17,-1,-1,DESERT},
	{18,54,-1,0,-1,-1,-1},
	{19,55,-1,1,-1,-1,-1},
	{20,56,-1,2,3,-1,-1},
	{21,57,-1,3,-1,-1,-1},
	{22,58,-1,4,16,-1,-1},
	{23,59,-1,5,-1,-1,-1},
	{24,60,-1,6,8,-1,-1},
	{25,61,-1,7,10,-1,-1},
	{26,62,-1,8,-1,-1,-1},
	{27,63,-1,9,-1,-1,-1},
	{28,64,-1,10,-1,-1,-1},
	{29,65,-1,11,-1,-1,-1},
	{30,66,-1,12,-1,-1,-1},
	{31,67,-1,13,12,-1,-1},
	{32,68,-1,14,0,-1,-1},
	{33,69,-1,15,-1,-1,-1},
	{34,70,-1,16,-1,-1,-1},
	{35,71,-1,17,-1,-1,-1},
	{36,1,72,0,1,-1,-1},
	{37,73,-1,1,-1,-1,DESERT},
	{38,111,74,2,3,4,-1},
	{39,5,75,3,5,-1,SHEEP},
	{40,124,76,4,16,6,-1},
	{41,77,-1,5,-1,-1,-1},
	{42,78,116,6,8,7,-1},
	{43,79,118,7,10,13,-1},
	{44,80,9,8,9,-1,BRICK},
	{45,81,-1,9,-1,-1,-1},
	{46,82,11,10,11,-1,-1},
	{47,83,-1,11,-1,-1,DESERT},
	{48,84,15,12,15,-1,WHEAT},
	{49,85,120,13,12,14,-1},
	{50,86,108,14,0,2,-1},
	{51,87,-1,15,-1,-1,-1},
	{52,88,17,16,17,-1,-1},
	{53,89,-1,17,-1,-1,DESERT},
	{54,90,-1,0,1,-1,-1},
	{55,91,-1,1,-1,-1,-1},
	{56,92,-1,2,4,-1,-1},
	{57,93,-1,3,5,-1,-1},
	{58,94,-1,4,6,-1,-1},
	{59,95,-1,5,-1,-1,-1},
	{60,96,-1,6,7,-1,-1},
	{61,97,-1,7,13,-1,-1},
	{62,98,-1,8,9,-1,-1},
	{63,99,-1,9,-1,-1,-1},
	{64,100,-1,10,11,-1,-1},
	{65,101,-1,11,-1,-1,-1},
	{66,102,-1,12,15,-1,-1},
	{67,103,-1,13,14,-1,-1},
	{68,104,-1,14,2,-1,-1},
	{69,105,-1,15,-1,-1,-1},
	{70,106,-1,16,17,-1,-1},
	{71,107,-1,17,-1,-1,-1},
	{72,2,108,0,1,2,-1},
	{73,3,109,1,3,-1,-1},
	{74,112,110,2,4,18,-1},
	{75,111,4,3,5,4,-1},
	{76,112,114,4,6,18,-1},
	{77,113,16,5,16,-1,DESERT},
	{78,114,115,6,7,18,-1},
	{79,115,121,7,13,18,-1},
	{80,116,7,8,9,7,-1},
	{81,117,10,9,10,-1,WOOD},
	{82,118,13,10,11,13,-1},
	{83,119,12,11,12,-1,-1},
	{84,120,14,12,15,14,-1},
	{85,121,122,13,14,18,-1},
	{86,122,110,14,2,18,-1},
	{87,123,0,15,0,-1,ORE},
	{88,124,6,16,17,6,-1},
	{89,125,8,17,8,-1,-1},
	{90,68,-1,0,2,-1,-1},
	{91,20,-1,1,3,-1,-1},
	{92,104,-1,2,18,-1,-1},
	{93,56,-1,3,4,-1,-1},
	{94,92,-1,4,18,-1,-1},
	{95,22,-1,5,16,-1,-1},
	{96,94,-1,6,18,-1,-1},
	{97,96,-1,7,18,-1,-1},
	{98,60,-1,8,7,-1,-1},
	{99,25,-1,9,10,-1,-1},
	{100,61,-1,10,13,-1,-1},
	{101,31,-1,11,12,-1,-1},
	{102,67,-1,12,14,-1,-1},
	{103,97,-1,13,18,-1,-1},
	{104,103,-1,14,18,-1,-1},
	{105,32,-1,15,0,-1,-1},
	{106,58,-1,16,6,-1,-1},
	{107,24,-1,17,8,-1,-1},
	{105,32,68,0,-1,-1,-1},
	{54,90,20,1,-1,-1,-1},
	{90,68,104,2,-1,-1,-1},
	{91,20,56,3,-1,-1,-1},
	{93,56,92,4,-1,-1,-1},
	{57,93,22,5,-1,-1,-1},
	{106,58,94,6,-1,-1,-1},
	{98,60,96,7,-1,-1,-1},
	{107,24,60,8,-1,-1,-1},
	{62,98,25,9,-1,-1,-1},
	{99,25,61,10,-1,-1,-1},
	{64,100,31,11,-1,-1,-1},
	{101,31,67,12,-1,-1,-1},
	{100,61,97,13,-1,-1,-1},
	{102,67,103,14,-1,-1,-1},
	{66,102,32,15,-1,-1,-1},
	{95,22,58,16,-1,-1,-1},
	{70,106,24,17,-1,-1,-1},
	{-1,-1,-1,18,-1,-1,-1},
};

static int8_t MiddleThiefAdjSettlements[] = {104,103,97,96,94,92};


void generate_board(void);
void mainGameLoop(void);
void refresh_display(void);
uint8_t roll_die(void);
void assign_resources(void);
void assign_initial_resources(int pos);
void checkBoardState(int8_t settlement, int8_t road, int8_t city, int8_t thief, int8_t initial_placement, uint8_t last_pos);
void confirmNewPiece(void);
void rejectNewPiece(void);
uint8_t maxBranch(uint8_t player, uint8_t road_index, uint8_t city_link);
uint8_t longestRoad(void);

uint8_t buildRoad(int8_t initial_placement, uint8_t last_settlement);

uint8_t buildSettlement(int8_t initial_placement);

uint8_t buildCity(void);

uint8_t moveThief(void);

void show_remaining_piece(void);

// Given a position and flags, checks if the placement is valid
// - In normal play, settlements, roads can be placed, settlements can be removed
// - Owner of 0 means it was removed, otherwise owner is whoever's turn it is
// - In some cases only a particular piece can be placed
//   - such as after a purchase
//   - Thieves can only be placed after knight card or roll of 7
// - Returns a 1 if valid, 0 otherwise
//int isLegal (int pos, int owner, int settlement, int road, int city, int theif);

int8_t isLegalInit (uint8_t pos, int8_t settlement, int8_t road, uint8_t last_settlement_pos);

int8_t isLegal (uint8_t pos, int8_t settlement, int8_t road, int8_t city, int8_t thief, uint8_t thief_pos_last);

// Translate a row and col number to a position number; returns -1 on failure
int rowCol2Pos(int row, int col);

// Given a position and an index 0-2, will return adjacent positions; returns -1 when no adjacent positions found
int pos2AdjPos(int pos, int adj_num );

// Given a position and an index 0-2, will return adjacent hexes; returns -1 when no adjacent hex found
int pos2AdjHex(int pos, int adj_num );

// Given position returns the portcode
int pos2Port(int pos);

// given a position, will return the owner of the position 1-4; if the position is unowned, returns a 0
int pos2Owner(int pos);

// Given a position and player 1-4, will set the position to be owned by that player
void posSetOwner(int pos, int owner);

// Given a position, will add the position as part of the legal, expected state (i.e. after a confirm of New Piece)
void setPosLegal(int pos);
// Given a position, will remove the position as part of the legal, expected state (useful for settlement->city, thief move)
void clearPosLegal(int pos);
// Returns the current state of a particular row of sensors.
ioport_port_mask_t getLegalRow(int row);
// Returns a 1 if row given is same as row in legal board state
int	compareLegal2Row(ioport_port_mask_t senseRow, int row);

// Loop this test to run the static map check
// Adjacent hexes to the triggered position light up WHEAT colored
// Adjacent positions are pointed to by error codes
void AdjHexTest( void );

// Test for ports by lighting the hex the color of the resource and pointing to the port with the error code
void PortTest ( void );

void TestGameSetup(void);

int8_t chkstateTest(void);

void bootLoop (void);

void onAnimate (void);

void offAnimate (void);

void fanimate (void);

void clear_resources(void);

void shutdown(void);

void RoadmapTest (void);


#endif /* CATAN_H_ */