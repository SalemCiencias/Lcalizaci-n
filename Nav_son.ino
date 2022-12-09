#include <NewPing.h>

#define SONAR_NUM     6 // Number of sensors.
#define MAX_DISTANCE 500 // Maximum distance (in cm) to ping.
#define PING_INTERVAL 33

NewPing sonar[SONAR_NUM] = { // Sensor object array.

       //trig_pin,echo_pin
  NewPing(11, 12, MAX_DISTANCE), // Each sensor's trigger pin, echo pin, and max distance to ping.
  NewPing(9,10, MAX_DISTANCE),
  NewPing(7,8,MAX_DISTANCE),
  NewPing(5,6,MAX_DISTANCE),
  NewPing(3,4,MAX_DISTANCE),
  NewPing(13,2,MAX_DISTANCE),
};

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  for (uint8_t i = 0; i < SONAR_NUM; i++){
    int distance = sonar[i].ping_cm();
    byte distance1 = highByte(distance);
    byte distance2 = lowByte(distance);
    //Serial.print(i);
    //Serial.println(":");
    //Serial.println(distance);
    //YY<sonar><distancia>
    byte packet[5]={0x59,0x59,i,distance1,distance2};
    Serial.write(packet,sizeof(packet));
    delay(1000);
  }
       
}
