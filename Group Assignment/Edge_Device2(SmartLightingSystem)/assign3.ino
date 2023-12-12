byte lastButtonStateOne = LOW; 
byte ledStateOne = LOW; 

byte lastButtonStateMany = LOW; 
byte ledStateMany = LOW; 

unsigned long debounceDuration = 50; 
unsigned long lastTimeButtonStateChanged = 0; 

unsigned int pinStatus = 0; 

void setup() { 
  pinMode(8, OUTPUT); 
  pinMode(7, INPUT); 
  pinMode(4, OUTPUT); 
  pinMode(12, OUTPUT); 
  pinMode(2, INPUT); 
  pinMode(9, OUTPUT); 
  pinMode(3, OUTPUT); 
  pinMode(5, OUTPUT); 
  pinMode(10, OUTPUT); 
  pinMode(A0, INPUT); 
  pinMode(A1, INPUT); 
  pinMode(A2, INPUT); 
  pinMode(A3, INPUT); 
  pinMode(13, OUTPUT); 
  pinMode(11, OUTPUT); 

  Serial.begin(9600); 

} 

void loop() { 
  // Codes are taken and modified from: https://roboticsbackend.com/arduino-turn-led-on-and-off-with-button/ 
  // One  button to One LED 
  if (millis() - lastTimeButtonStateChanged > debounceDuration){ 
    byte buttonStateOne = digitalRead(7); 
    if (buttonStateOne != lastButtonStateOne){ 
      lastTimeButtonStateChanged = millis(); 
      lastButtonStateOne = buttonStateOne; 
      if (buttonStateOne == LOW){ 
        ledStateOne = (ledStateOne == HIGH) ? LOW : HIGH; 
        digitalWrite(8, ledStateOne); 
      } 
    } 
  } 

  // One button to All LEDs 
  if (millis() - lastTimeButtonStateChanged > debounceDuration){ 
    byte buttonStateMany = digitalRead(2); 
    if (buttonStateMany != lastButtonStateMany){ 
      lastTimeButtonStateChanged = millis(); 
      lastButtonStateMany = buttonStateMany; 
      if (buttonStateMany == LOW){ 
        ledStateMany = (ledStateMany == HIGH) ? LOW : HIGH; 
        digitalWrite(4, ledStateMany); 
        digitalWrite(12, ledStateMany); 
        digitalWrite(8, ledStateMany); 
      } 
    } 
  } 

  int ldrStatus1 = analogRead(A0); 
  int ldrStatus2 = analogRead(A1); 
  int ldrStatus3 = analogRead(A2); 
  int ldrStatus4 = analogRead(A3); 

  Serial.print(ldrStatus1); 
  Serial.print(","); 
  Serial.print(ldrStatus2); 
  Serial.print(","); 
  Serial.print(ldrStatus3); 
  Serial.print(","); 
  Serial.println(ldrStatus4); 

  if (ldrStatus1 < 300) { 
    digitalWrite(9, HIGH); 
  } 
  else { 
    digitalWrite(9, LOW); 
  } 

  if (ldrStatus2 < 300) { 
    digitalWrite(3, HIGH); 
  } 
  else { 
    digitalWrite(3, LOW); 
  } 

  if (ldrStatus3 < 300) { 
    digitalWrite(5, HIGH); 
  } 
  else { 
    digitalWrite(5, LOW); 
  } 

  if (ldrStatus4 < 300) { 
    digitalWrite(10, HIGH); 
  } 
  else { 
    digitalWrite(10, LOW); 
  } 

  delay(1000); 

  if (Serial.available()>0) { 
    pinStatus = Serial.parseInt(); 
    switch(pinStatus){ 
      case 1: 
        digitalWrite(12, HIGH); 
        digitalWrite(4, HIGH); 
        digitalWrite(8, HIGH); 
        break; 
      case 2: 
        digitalWrite(12, LOW); 
        digitalWrite(4, LOW); 
        digitalWrite(8, LOW); 
        break; 
      case 3: 
        digitalWrite(8, HIGH); 
        break; 
      case 4:  
        digitalWrite(8, LOW); 
        break; 
      case 5: 
        digitalWrite(9, LOW); 
        break; 
      case 6: 
        digitalWrite(9, HIGH); 
        break; 
      case 7: 
        digitalWrite(3, LOW); 
        break; 
      case 8: 
        digitalWrite(3, HIGH); 
        break; 
      case 9: 
        digitalWrite(5, LOW); 
        break; 
      case 10: 
        digitalWrite(5, HIGH); 
        break; 
      case 11: 
        digitalWrite(10, LOW); 
        break; 
      case 12: 
        digitalWrite(10, HIGH); 
        break; 
      case 13: 
        digitalWrite(13, HIGH); 
        break; 
      case 14: 
        digitalWrite(13, LOW); 
        break;  
      case 15: 
        digitalWrite(11, HIGH); 
        break;  
      case 16: 
        digitalWrite(11, LOW); 
        break;       
      default: 
        break; 
    } 
  }  
} 
