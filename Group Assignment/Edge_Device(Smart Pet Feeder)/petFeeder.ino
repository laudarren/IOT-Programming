 #include <Servo.h>
#include <MFRC522.h>
#include <SPI.h>

Servo foodServo;
int buzzerPin = 8; // Change this to the actual pin number for your buzzer
int servoPin = 6;
int foodTrigPin = 5; // Trig pin for the food sensor
int foodEchoPin = 4; // Echo pin for the food sensor
int petTrigPin = 3; // Trig pin for the pet sensor
int petEchoPin = 2; // Echo pin for the pet sensor

#define NUMBER_OF_KEYS 4
static unsigned short code[NUMBER_OF_KEYS][4] = {{100,200,300,400},{111,222,333,444},{26,166,189,174},{5,106,45,197}};

MFRC522 mfrc522(10, 9); // Define the RFID module pins (SS, RST)

int maxFoodCapacity = 100; // Maximum food capacity in grams
int foodDispensed = 0;

void setup() {
  foodServo.attach(servoPin); // Initialize the servo
  pinMode(buzzerPin, OUTPUT);
  pinMode(foodTrigPin, OUTPUT);
  pinMode(foodEchoPin, INPUT);
  pinMode(petTrigPin, OUTPUT);
  pinMode(petEchoPin, INPUT);
  Serial.begin(9600);

  SPI.begin();      // Initiate  SPI bus
  mfrc522.PCD_Init(); // Initiate MFRC522

  Serial.println(F("This code scan the MIFARE Classsic NUID."));
  Serial.print(F("Using the following key:"));
}

void loop() {

  if(Serial.available()>0){
    int command = Serial.parseInt(); 
    if (command == 1){
    openServo();
   } else if (command == 2){
    closeServo();
   }
  }

  // UltrasSonic sensor code for food level
  int foodLevel = measureDistance(foodTrigPin, foodEchoPin);
  


  // Ultrasonic sensor code for pet distance
  int petDistance = measureDistance(petTrigPin, petEchoPin);


  

  // Dispense food logic
  int dispensedAmount = 0;
  if (petDistance < 30) {
    if (foodDispensed < maxFoodCapacity) {
      dispensedAmount = 5; // Adjust the amount as needed
      foodDispensed += dispensedAmount;
      foodServo.write(0); // Open the food funnel
      delay(2000); // Adjust the duration as needed
      foodServo.write(90); // Close the food funnel
    }
  }
  delay(500);


    if (readRFIDCard()) {
    openServo();
    delay(2000); // Adjust the duration as needed
    closeServo();
  }


  
}

int measureDistance(int trigPin, int echoPin) {
  const int numReadings = 5;
  long duration;
  int distance;

  // Take multiple readings and average them
  long totalDuration = 0;
  for (int i = 0; i < numReadings; ++i) {
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);

    // Use timeout to prevent waiting indefinitely
    duration = pulseIn(echoPin, HIGH, 20000); // 20,000 microseconds timeout
    totalDuration += duration;
  }

  // Calculate the average duration
  long averageDuration = totalDuration / numReadings;

  // Calculate the distance
  distance = (averageDuration / 2) / 29.1;

  // Check if the distance is within a reasonable range
  if (distance >= 2 && distance <= 400) {
    return distance;
  } else {
    // Return a special value (e.g., -1) to indicate an error
    return -1;
  }
}

bool readRFIDCard() {
  // Look for new cards
  if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
    return true;
  }
  return false;
}

unsigned short checkID() {
  if (!mfrc522.PICC_ReadCardSerial()) {
    return 0;
  }

  Serial.print("Groesse: "); Serial.println(mfrc522.uid.size);
  Serial.print("UID 1: "); Serial.println(mfrc522.uid.uidByte[0]);
  Serial.print("UID 2: "); Serial.println(mfrc522.uid.uidByte[1]);
  Serial.print("UID 3: "); Serial.println(mfrc522.uid.uidByte[2]);
  Serial.print("UID 4: "); Serial.println(mfrc522.uid.uidByte[3]);

  short doOpen = 0, i;
  for (i = 0; i < NUMBER_OF_KEYS; i++) {
    if (mfrc522.uid.uidByte[0] == code[i][0] && mfrc522.uid.uidByte[1] == code[i][1] && mfrc522.uid.uidByte[2] == code[i][2] && mfrc522.uid.uidByte[3] == code[i][3]) {
      doOpen = 1;
      Serial.println("Code akzeptiert!");
      break;
    }
  }

  mfrc522.PICC_HaltA();
  return doOpen;
}




void openServo() {
  foodServo.write(0); // Open the servo by setting it to 0 degrees
}

void closeServo() {
  foodServo.write(90); // Close the servo by setting it to 90 degrees
}
