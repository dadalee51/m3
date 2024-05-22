/**
  this is a unbricking first aid project to open in arduino.
  NOTE: this file is not to be used in vscode.
  Software copyright 2024, tigo.robotics
 */
#include <ArduinoOTA.h>
#include <ESP8266WiFi.h>
#include <Wire.h>
#define FOR(I,N) for(int I=0;I<N;I++)
const char*apid = "TIGO_m3a_A8";
const char*pswd = "12345678";
#define AT1_SLAVE 0x12
#define AT2_SLAVE 0x14

#define TF_OFF
#define ACC_OFF
#define CLR_OFF

#ifdef ACC_ON
  #include "SparkFun_LIS2DH12.h"
  SPARKFUN_LIS2DH12 accel;
  float z_acc=0.0;
#endif
#ifdef TF_ON
  #include <VL53L0X.h>
  VL53L0X sensor; //0x29
  int head=0;
#endif
#ifdef CLR_ON
  #include "veml6040.h"
  VEML6040 RGBWSensor;
  int red=0; int mred=0;
  int blue=0; int mblue=0; 
  int green=0; int mgreen=0;
#endif
//function header 
void TCA9548A(uint8_t bus);
void to_MotorA(int dir, int speed);
void to_RGB(long color);
void to_WLED1(char val);
void signalling(int);

void setup() {
  WiFi.mode(WIFI_AP_STA);
  WiFi.softAP(apid, pswd);
  IPAddress IP = WiFi.softAPIP();
  WiFi.begin("TIGO5G2.12", "abcdefab");
  delay(1000);
  ArduinoOTA.begin();
  pinMode(2, OUTPUT);
  Wire.setClock(400000); //set i2c fast mode.
  Wire.begin(4,14); //join i2c as master //sda4,scl14
}

void loop() {
  ArduinoOTA.handle();
  digitalWrite(2,1);
}



//This is the Multiplexor control
void TCA9548A(uint8_t bus){
  Wire.beginTransmission(0x70);  // TCA9548A address
  Wire.write(1 << bus);          // send byte to select bus
  Wire.endTransmission();
}

// SENDING to COLOR RGB
void to_RGB(long color){
  Wire.beginTransmission(AT1_SLAVE); 
  Wire.write('R');
  Wire.write('G');
  Wire.write('B');//padding byte
  Wire.write(color>>16 & 0xFF); //R
  Wire.write(color>>8 & 0xFF); //G
  Wire.write(color & 0xFF); //B
  Wire.write('E'); 
  Wire.endTransmission(); 
  delay(1);
}

void to_MotorA(int dir, int speed){
  //control motor
  Wire.beginTransmission(AT1_SLAVE); 
  Wire.write('M');//0
  Wire.write('A');//1
  Wire.write('1'); //2
  Wire.write((char)dir); //3 --> 1 or -1 to drive
  Wire.write((char)speed); //4 1 to 127
  Wire.write('E'); //this was required!!
  Wire.endTransmission(); 
}

//sending 0 as string ?
void to_WLED1(char val){
  Wire.beginTransmission(AT1_SLAVE); 
  Wire.write('W');
  Wire.write('L');
  Wire.write('1');//padding byte
  Wire.write((char)val);
  Wire.write('E');//padding byte was required!!
  Wire.endTransmission(); 
}

//sending 0 as string ?
void to_WLED2(char val){
  Wire.beginTransmission(AT2_SLAVE); 
  Wire.write('W');
  Wire.write('L');
  Wire.write('2');//padding byte
  Wire.write((char)val);
  Wire.write('E');//padding byte was required!!
  Wire.endTransmission(); 
}

void signalling(int delaytime) {
  // Blink the LED as a signal
  for (int i = 0; i < 3; i++) {
    digitalWrite(2, HIGH);
    delay(delaytime);
    digitalWrite(2, LOW);
    delay(delaytime);
  }
}
