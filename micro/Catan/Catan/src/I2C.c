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
U8  s_memory[TWI_MEM_SIZE]={1,2,3,4,5,6,7,8,9,0};  // Content of the Virtual mem

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