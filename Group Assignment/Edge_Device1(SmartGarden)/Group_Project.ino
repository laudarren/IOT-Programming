#define echoPin 8
#define trigPin 7
#define echoPin3 4
#define trigPin3 3

long duration;
long distance;

long duration3;
long distance3;

int LED_Red = 13;
int LED_Yellow = 12;
int LED_Green = 11;

int MSpin = A0;
int MSpin2 = A1;
int moistureValue;
int moistureValue2;
int moistureLimit=30;
float moisturePercent;
float moisturePercent2;

bool red = false;
bool yellow =false;
bool green = false;
bool servo = false;

#include <Servo.h>

Servo myservo;
int Servo_Pin = 9;
int pos = 0;

#include "DHT.h"

#define DHTPIN 6
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

unsigned long start_time; 
unsigned long timed_event;
unsigned long current_time; // millis() function returns unsigned long

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  
  timed_event = 3000; // after 1000 ms trigger the event
  current_time = millis();
  start_time = current_time;

  myservo.attach(Servo_Pin);
  
  pinMode(MSpin,INPUT);
  pinMode(MSpin2, INPUT);
  pinMode(LED_Red,OUTPUT);
  pinMode(LED_Yellow,OUTPUT);
  pinMode(LED_Green,OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(trigPin, OUTPUT);

  pinMode(echoPin3, INPUT);
  pinMode(trigPin3, OUTPUT);

  dht.begin();
}

void loop() {
  
  //Ultrasonic sensor 1
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);

  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH);

  distance = duration/58.2;

  delay(50);


  //Ultrasonic sensor 2
  digitalWrite(trigPin3, LOW);
  delayMicroseconds(2);

  digitalWrite(trigPin3, HIGH);
  delayMicroseconds(10);

  digitalWrite(trigPin3, LOW);

  duration3 = pulseIn(echoPin3, HIGH);

  distance3 = duration3/58.2;
  
  delay(50);


  // Write serial communication to RPI(grass detection)
  if(distance < 15 || yellow == true)
  {
    Serial.write(18);
  }
  else
  {
    digitalWrite(LED_Yellow,HIGH);
  }

  if(distance3 < 15 || green == true)
  {
    Serial.write(19);
  }
  else
  {
    digitalWrite(LED_Green,HIGH);
  }

  //Soil moisture sensors
  moistureValue = analogRead(MSpin);
  moisturePercent = (100-
  ((moistureValue/1023.00)*100));

  if(moisturePercent<moistureLimit || servo == true)
   {
    if( pos == 0){
      Serial.write(20);
      pos = 180;
    }
   }
   else
   {
    if(pos != 0){
       for (pos = 180; pos >= 0; pos -= 1) { 
       myservo.write(pos);              
       delay(15);                       
      }
     pos = 0;
    }
   }

   moistureValue2 = analogRead(MSpin2);
   moisturePercent2 = (100-
   ((moistureValue2/1023.00)*100));

  if(moisturePercent2<moistureLimit || red == true)
   {   
    Serial.write(21); 
   }
   else
   {
    digitalWrite(LED_Red,LOW);
   }

   

  //DHT11 sensor(Temperature)
  float h = dht.readHumidity();
  // Read temperature as Celsius
  float t = dht.readTemperature();
  // Read temperature as Fahrenheit
  float f = dht.readTemperature(true);
  
  //Print output/Serial from arduino to RPI
  current_time = millis(); // update the timer every cycle

  if (current_time - start_time >= timed_event) {
      Serial.print(0);
      Serial.print(", ");
      Serial.print(moisturePercent);
      Serial.print(", ");
      Serial.print(moisturePercent2);
      Serial.print(", ");
      Serial.print(distance);
      Serial.print(", ");
      Serial.print(distance3);
      Serial.print(", ");
      Serial.print(t);
      Serial.println();
    start_time = current_time;  // reset the timer
  }

  
  // Read serial communication from RPI
  if (Serial.available() > 0) {
    int pin_num = Serial.read() - '0';
    
    switch (pin_num) {
      case 1:
        digitalWrite(LED_Yellow,LOW);
        break;
      case 2:
        digitalWrite(LED_Green,LOW);
        break;
      case 3:
        for (pos = 0; pos <= 180; pos += 1) { 
          myservo.write(pos);              
          delay(15);                       
        }
        break;
      case 4:
        digitalWrite(LED_Red,HIGH);          
        break;
      case 5:
        servo = true;
        break;
      case 6:
        red = true;
        break;
      case 7:
        servo = false;
        break;
      case 8:
        red = false;
        break;
      default:
        break;      
    }
      
  }
}
