#include <SPI.h>
#include <MFRC522.h>
#include <Servo.h>
#define SS_PIN 10
#define RST_PIN 9
#define OUT_PIN_GREEN 6
#define OUT_PIN_RED 7
#define NUMBER_OF_KEYS 4
int begin=0;
const int trigPin = 4;
const int echoPin = 3;
unsigned int pinStatus = 0;

MFRC522 mfrc522(SS_PIN, RST_PIN);
Servo servoBase;

static unsigned short code[NUMBER_OF_KEYS][4] = {{100,200,300,400},{111,222,333,444},{26,166,189,174},{5,106,45,197}};

void setup() {
  Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init();
  servoBase.attach(A0);
  servoBase.write(begin);
  pinMode(OUT_PIN_GREEN, OUTPUT);
  pinMode(OUT_PIN_RED, OUTPUT);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {
  long duration, inches, cm;
  int but,ldrvalue,light;

  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH);

  inches = microsecondsToInches(duration);
  cm = microsecondsToCentimeters(duration);

  Serial.print(inches);
  Serial.print("in, ");
  Serial.print(cm);
  Serial.print("cm "); 
  Serial.println();
  

  if(mfrc522.PICC_IsNewCardPresent()){
    unsigned short doOpen = checkID();
    if (doOpen != 0){
      digitalWrite(OUT_PIN_GREEN,HIGH);
      opendoor();
      delay(2000);
      digitalWrite(OUT_PIN_GREEN,LOW);
      closedoor();
    }else{
      digitalWrite(OUT_PIN_RED,HIGH);
      delay(2000);
      digitalWrite(OUT_PIN_RED,LOW);
    }
  }

  if(Serial.available()>0)
  {
   pinStatus = Serial.parseInt();

   switch(pinStatus){
     case 1:
     digitalWrite(OUT_PIN_GREEN,HIGH);
     opendoor();
     digitalWrite(OUT_PIN_GREEN,LOW);
     break;
     
     case 2:
     digitalWrite(OUT_PIN_RED,HIGH);
     closedoor();
     digitalWrite(OUT_PIN_RED,LOW);
     break;
     
   }

   
  }
  
}

unsigned short checkID(){
  if(! mfrc522.PICC_ReadCardSerial()){
    return 0;
  }

  Serial.print("Groesse: "); Serial.println(mfrc522.uid.size);
  Serial.print("UID 1: "); Serial.println(mfrc522.uid.uidByte[0]);
  Serial.print("UID 2: "); Serial.println(mfrc522.uid.uidByte[1]);
  Serial.print("UID 3: "); Serial.println(mfrc522.uid.uidByte[2]);
  Serial.print("UID 4: "); Serial.println(mfrc522.uid.uidByte[3]);

  short doOpen = 0, i;
  for(i = 0; i < NUMBER_OF_KEYS; i++){
    if(mfrc522.uid.uidByte[0]==code[i][0] && mfrc522.uid.uidByte[1] == code[i][1] && mfrc522.uid.uidByte[2] == code[i][2] && mfrc522.uid.uidByte[3] == code[i][3]){
      doOpen = 1;
      Serial.println("Code akzeptiert!");
      break;
    }
  }

  mfrc522.PICC_HaltA();
  return doOpen;

}

long microsecondsToInches(long microseconds) {
  
  return microseconds / 74 / 2;
  
}

long microsecondsToCentimeters(long microseconds) {

  return microseconds / 29 / 2;
  
}

void opendoor(){
  
  while(begin <= 180){
      servoBase.write(begin);
      begin ++;
      delay(27);
    }
  
}

void closedoor(){
  
  while(begin >= 0){
      servoBase.write(begin);
      begin --;
      delay(27);
    }
  
}
