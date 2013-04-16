/*
 * I2C.c
 *
 * Created: 3/28/2013 6:29:33 PM
 *  Author: team3
 */ 

#include <I2C.h>

static void twi_slave_rx( U8 u8_value );
static U8 twi_slave_tx( void );
static void twi_slave_stop( void );

const U8 test_pattern[] =  {
	0xAA,
	0x55,
	0xA5,
	0x5A,
	0x77,
0x99};

U8  s_status_cmd = TWI_MEM_IDLE; // State variable
U8  s_u8_addr_pos;               // Offset in the address value (because we receive the address one Byte at a time)
U32 s_u32_addr;                  // The current address in the virtual mem
// Content of the Virtual memory
U8  s_memory[TWI_MEM_SIZE]={0};



static const gpio_map_t TWI_GPIO_MAP =
{
{AVR32_TWI_SDA_0_0_PIN, AVR32_TWI_SDA_0_0_FUNCTION},
{AVR32_TWI_SCL_0_0_PIN, AVR32_TWI_SCL_0_0_FUNCTION}
};


int I2C_init( void ) {

  twi_options_t opt;
  twi_slave_fct_t twi_slave_fct;
  int status;
  double total = 0;

  // Initialize and enable interrupt
  irq_initialize_vectors();
  cpu_irq_enable();

  // TWI gpio pins configuration
  gpio_enable_module(TWI_GPIO_MAP, sizeof(TWI_GPIO_MAP) / sizeof(TWI_GPIO_MAP[0]));
  
  // initialize the interrupt flag for alerting the Pi of new data (TWI = Three Wire Interface for us)
  ioport_enable_pin(I2C_FLAG);
  ioport_set_pin_dir(I2C_FLAG,IOPORT_DIR_OUTPUT);
  ioport_set_pin_level(I2C_FLAG,false);

  // options settings
  opt.pba_hz = FOSC0;
  opt.speed = TWI_SPEED;
  opt.chip = EEPROM_ADDRESS;

  // initialize TWI driver with options
  twi_slave_fct.rx = &twi_slave_rx;
  twi_slave_fct.tx = &twi_slave_tx;
  twi_slave_fct.stop = &twi_slave_stop;
  status = twi_slave_init(&AVR32_TWI, &opt, &twi_slave_fct );
 
  return (&s_memory[0] );
}


static void twi_slave_rx( U8 u8_value )
{

   switch( s_status_cmd )
   {
   case TWI_MEM_IDLE:
      s_u8_addr_pos = EEPROM_ADDR_LGT; // Init before receiving the target address.
      s_u32_addr = 0;
      // No break to continue on next case

   case TWI_MEM_ADDR:
      s_u8_addr_pos--;
      // Receiving the Nth Byte that makes the address (MSB first).
      s_u32_addr += ((U32)u8_value << (s_u8_addr_pos*8));
      if( 0 == s_u8_addr_pos )
      {  // the address is completely received => switch to data mode.
         s_status_cmd = TWI_MEM_DATA;
      }else{
         s_status_cmd = TWI_MEM_ADDR;
      }
      break;

   case TWI_MEM_DATA:      // We are receiving data
      // Check that we're still in the range of the virtual mem
      if( TWI_MEM_SIZE > (s_u32_addr-VIRTUALMEM_ADDR_START) )
      {
         s_memory[s_u32_addr-VIRTUALMEM_ADDR_START] = u8_value;
		 
		 // Do something if the Pi writes to the PI EVENT register
		 if ((s_u32_addr-VIRTUALMEM_ADDR_START)==PI_EVENT_REG)
		 {
			 if (s_memory[PI_EVENT_REG])
			 {
				 ioport_set_pin_level(I2C_FLAG,false);
				  switch (s_memory[PI_EVENT_REG])
				  {
					  case PI_NEW_PIECE_CONFIRM:
						if (s_memory[PIECE_TYPE_REG]/PIECE_TYPE_TBC == 1)
						{
							confirmNewPiece();
						}
						s_memory[PI_EVENT_REG] = 0;
						break;
					  case PI_NEW_PIECE_REJECT:
						rejectNewPiece();
						s_memory[PI_EVENT_REG] = 0;
						break;					  					
				  }
				  //s_memory[PI_EVENT_REG] = 0;
			 }
			
			 
			 
		 }
      }
      s_u32_addr++;  // Update to next position
      break;
   }
}

/*! \brief Transmit a data on TWI
 */
static U8 twi_slave_tx( void )
{
   U8 u8_value;

   // This callback is called after a read request from the TWI master, for each
   // Byte to transmit.
   s_status_cmd = TWI_MEM_DATA;
   // Check that we're still in the range of the virtual mem
   if( TWI_MEM_SIZE > (s_u32_addr-VIRTUALMEM_ADDR_START) )
   {
      u8_value = s_memory[s_u32_addr-VIRTUALMEM_ADDR_START];
   }else{
      u8_value = 0xFF;
   }
   s_u32_addr++;  // Update to next position
   return u8_value;
}


/*! \brief Manage stop transfer reception on TWI
 */
static void twi_slave_stop( void )
{
   s_status_cmd = TWI_MEM_IDLE;
}

uint8_t isDiceRolled(void){
	if (s_memory[PI_EVENT_REG] == PI_DICE_ROLLED)
	{
		return 1;
	}
	return 0;
}

uint8_t isTurnOver(void){
	if (s_memory[PI_EVENT_REG] == PI_END_TURN)
	{
		return 1;
	}
	return 0;
}

uint8_t isNewGame(void){
	if (s_memory[PI_EVENT_REG] == PI_NEW_GAME)
	{
		return 1;
	}
	return 0;
}

uint8_t isRoadBuildingPlayed(void)
{
	if (s_memory[PI_EVENT_REG] == PI_DEV_ROAD)
	{
		return 1;
	}
	return 0;
}

uint8_t isKnightPlayed(void){
	if (s_memory[PI_EVENT_REG] == PI_DEV_KNIGHT)
	{
		return 1;
	}
	return 0;
}

uint8_t isNewPieceConfirm(void){
	if (s_memory[PI_EVENT_REG] == PI_NEW_PIECE_CONFIRM)
	{
		return 1;
	}
	return 0;
}
uint8_t isNewPieceReject(void){
	if (s_memory[PI_EVENT_REG] == PI_NEW_PIECE_REJECT)
	{
		return 1;
	}
	return 0;
}
uint8_t PiecePurchased(void){
	if (s_memory[PI_EVENT_REG] >= PI_ROAD_PURCHASE)
	{
		return s_memory[PI_EVENT_REG] - PI_ROAD_PURCHASE;
	}
}