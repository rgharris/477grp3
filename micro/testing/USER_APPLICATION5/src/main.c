/**
 * \file
 *
 * \brief Empty user application template
 *
 */

/*
 * Include header files for all drivers that have been imported from
 * Atmel Software Framework (ASF).
 */


#include <asf.h>
#include <avr32/uc3b064.h>
#include <board.h>
#include <ioport.h>
#include <delay.h>
#include <spi_master.h>
#include <twi.h>
/*
// I2C MACROS
#define SET(x,y) (x|=(1<<y))
#define CLR(x,y) (x&=(~(1<<y)))
#define CHK(x,y) (x&(1<<y))
#define TOG(x,y) (x^=(1<<y))

//global variables
#define BUFLEN_RECV 12
uint8_t r_index =0;
uint8_t recv[BUFLEN_RECV]; //buffer to store received bytes
#define BUFLEN_TRAN 3
uint8_t t_index=0;
//test bytes to transmit
uint8_t tran[BUFLEN_TRAN] = {0x12, 0x34, 0x56}; 
 
//variable to indicate if something went horribly wrong
 uint8_t reset=0 
 
//prototypes
void handleI2C();
void blinkLED(uint32_t led);
void spi_init_pins(void);


int main (void)
{
	board_init();
	sysclk_init();
	ioport_init();
	
	ioport_set_pin_dir(LED,IOPORT_DIR_OUTPUT);
	
	// Insert application code here, after the board has been initialized.
	//load slave address
	TWAR = (0x01<<1); //we're using address 0x01
	//enable I2C hardware
	TWCR = (1<<TWEN)|(1<<TWEA);
	 
	while(1){
	    handleI2C();
		blinkLED(LED);
	}
}

void blinkLED(uint32_t led)
{
	ioport_set_pin_level(led,true);
	delay_ms(500);
	ioport_set_pin_level(led,false);
	delay_ms(500);
}

void spi_init_pins(void)
{
	//disable SPI pins so they can be controlled by SPI peripheral
	ioport_disable_pin(SS);
	ioport_disable_pin(MOSI);
	ioport_disable_pin(MISO);
	ioport_disable_pin(CS0);
	ioport_disable_pin(SCK);
	
	ioport_set_pin_dir(SS,IOPORT_DIR_INPUT);
	ioport_set_pin_mode(SS,IOPORT_MODE_PULLUP);
	
	ioport_set_pin_dir(SCK, IOPORT_DIR_OUTPUT);
	ioport_set_pin_mode(SCK,IOPORT_MODE_MUX_A);
	
	ioport_set_pin_dir(MOSI,IOPORT_DIR_OUTPUT);
	ioport_set_pin_mode(MOSI,IOPORT_MODE_MUX_A);
	
	ioport_set_pin_dir(CS0, IOPORT_DIR_OUTPUT);
	ioport_set_pin_mode(CS0, IOPORT_MODE_MUX_A);
	
	ioport_set_pin_dir(MISO, IOPORT_DIR_INPUT);
	ioport_set_pin_mode(MISO, IOPORT_MODE_MUX_C);
}

   void spi_init_module(void)
   {
      struct spi_device spi_device_conf = {
          .id = CS0
      };

      spi_master_init(&AVR32_SPI);
      spi_master_setup_device(&AVR32_SPI, &spi_device_conf, SPI_MODE_0, 1000000, 0);
      spi_enable(&AVR32_SPI);
   }
   
//setup the I2C hardware to ACK the next transmission
//and indicate that we've handled the last one.
#define TWACK (TWCR=(1<<TWINT)|(1<<TWEN)|(1<<TWEA))
//setup the I2C hardware to NACK the next transmission
#define TWNACK (TWCR=(1<<TWINT)|(1<<TWEN))
//reset the I2C hardware (used when the bus is in a illegal state)
#define TWRESET (TWCR=(1<<TWINT)|(1<<TWEN)|(1<<TWSTO)|(1<<TWEA))

void handleI2C(){
  //check if we need to do any software actions
  if(CHK(TWCR,TWINT)){
    switch(TW_STATUS){
//--------------Slave receiver------------------------------------
    //SLA_W received and acked, prepare for data receiving
    case 0x60:  
      TWACK;
      r_index =0;
      break;
    case 0x80:  //a byte was received, store it and 
                //setup the buffer to recieve another
      recv[r_index] = TWDR;
      r_index++;
      //don't ack next data if buffer is full
      if(r_index >= BUFLEN_RECV){
          TWNACK;
      }else {
          TWACK;
      }
      break;
    
	case 0x68://adressed as slave while in master mode.
              //should never happen, better reset;
      reset=1;
    
	case 0xA0: //Stop or rep start, reset state machine
      TWACK;
      break;
//-------------- error recovery ----------------------------------
    case 0x88: //data received  but not acked
      //should not happen if the master is behaving as expected
      //switch to not addressed mode
      TWACK;
      break;
//---------------Slave Transmitter--------------------------------
    case 0xA8:  //SLA R received, prep for transmission
		        //and load first data
      t_index=1;
      TWDR = tran[0];
      TWACK;
      break;
    case 0xB8:  //data transmitted and acked by master, load next
      TWDR = tran[t_index];
      t_index++;
      //designate last byte if we're at the end of the buffer
      if(t_index >= BUFLEN_ACC_DATA) TWNACK;
      else TWACK;
      break;
    case 0xC8: //last byte send and acked by master
    //last bytes should not be acked, ignore till start/stop
      //reset=1;
    case 0xC0: //last byte send and nacked by master 
		//(as should be)
      TWACK;
      break;
//--------------------- bus error---------------------------------
    //illegal start or stop received, reset the I2C hardware
	case 0x00: 
      TWRESET;
      break;
    }
  }
}*/

//------------------  C O N F I G U R A T I O N S  -------------------

#define EEPROM_ADDRESS        0x50        // EEPROM's TWI address
#define EEPROM_ADDR_LGT       3           // Address length of the EEPROM memory
#define VIRTUALMEM_ADDR_START 0x123456    // Address of the virtual mem in the EEPROM
#define TWI_SPEED             50000       // Speed of TWI
//------------------  D E F I N I T I O N S  -------------------
#define  PATTERN_TEST_LENGTH        (sizeof(test_pattern)/sizeof(U8))
 const U8 test_pattern[] =  {
   0xAA,
   0x55,
   0xA5,
   0x5A,
   0x77,
   0x99};
//--------------------------------------------------------------------------------------------------------------
//------------------------------------------ T W I   S L A V E -------------------------------------------------
//--------------------------------------------------------------------------------------------------------------

#define TWI_MEM_SIZE    20 // The size of the virtual mem
#define TWI_MEM_IDLE    0  // Idle state
#define TWI_MEM_ADDR    1  // Address state
#define TWI_MEM_DATA    2  // Data state
U8  s_status_cmd = TWI_MEM_IDLE; // State variable
U8  s_u8_addr_pos;               // Offset in the address value (because we receive the address one Byte at a time)
U32 s_u32_addr;                  // The current address in the virtual mem
U8  s_memory[TWI_MEM_SIZE]={0};  // Content of the Virtual mem

 
static void  twi_slave_rx( U8 u8_value )
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


static void twi_slave_stop( void )
{
   s_status_cmd = TWI_MEM_IDLE;
}


int main(void)
{
  static const gpio_map_t TWI_GPIO_MAP =
  {
    {AVR32_TWI_SDA_0_0_PIN, AVR32_TWI_SDA_0_0_FUNCTION},
    {AVR32_TWI_SCL_0_0_PIN, AVR32_TWI_SCL_0_0_FUNCTION}
  };
  twi_options_t opt;
  twi_slave_fct_t twi_slave_fct;
  int status;

  // Switch to oscillator 0
  //pm_switch_to_osc0(&AVR32_PM, FOSC0, OSC0_STARTUP);

  // Init debug serial line
 //init_dbg_rs232(FOSC0);

 // Display a header to user
  //print_dbg("\x0C\r\nTWI Example\r\nSlave!\r\n");

 // TWI gpio pins configuration
 gpio_enable_module(TWI_GPIO_MAP, sizeof(TWI_GPIO_MAP) / sizeof(TWI_GPIO_MAP[0]));

  // options settings
  opt.pba_hz = BOARD_OSC0_HZ;
  opt.speed = TWI_SPEED;
  opt.chip = EEPROM_ADDRESS;

   // initialize TWI driver with options
   twi_slave_fct.rx = &twi_slave_rx;
   twi_slave_fct.tx = &twi_slave_tx;
   twi_slave_fct.stop = &twi_slave_stop;
   status = twi_slave_init(&AVR32_TWI, &opt, &twi_slave_fct );
  // check init result
  /*if (status == TWI_SUCCESS)
  {
    // display test result to user
     print_dbg("Slave start:\tPASS\r\n");
  }
  else
  {
    // display test result to user
    print_dbg("slave start:\tFAIL\r\n");
  }*/
 
  while(1);
 }