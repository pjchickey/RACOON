/*
 * This code handles commands sent from the raspberry pi to the arduino (that controls and reads from sensors)
 * 
 * COMMANDS
 * 3 - Sort to Trash
 * 4 - Sort to Recycling
 * 5 - Read Hinge State (Limit Switch)
 * 6 - Detect if object is in device (load cell)
 * 7 - Read Sensor value
 */

#include <AccelStepper.h>

// Define a stepper and the pins it will use
AccelStepper stepper(AccelStepper::DRIVER, 2, 4); // Defaults to AccelStepper::FULL4WIRE (4 pins) on 2, 3, 4, 5

int command;
String data;
int exitCode = 0; //0 - Task completed successfully; 1 - Task could not complete
int binaryResp = 0; //0 - Default; 1 - Activated
int value = 0;  //Can be any integer value
String stringVal = " ";
int i = 0; //Test counter

void setup(){
  Serial.begin(9600);
}

void loop(){

  if (Serial.available() > 0) {
    
    data = Serial.readStringUntil('\n');
    data.trim();
    command = data.toInt();
    switch(command){
      case 3: //Sort to Trash
        sendToPi("3"); //Acknowledge command
        exitCode = sortObject(0); //Sort to Trash
        stringVal = String(exitCode);
        sendToPi(stringVal);
        break;
      case 4: //Sort to Recycling
        sendToPi("4"); //Acknowledge command
        exitCode = sortObject(1); //Sort to Recycling
        stringVal = String(exitCode);
        sendToPi(stringVal)
        break;
      case 5: //Read Door State (Limit Switch)
        sendToPi("5"); //Acknowledge command
        binaryResp = readDoorState();
        stringVal = "2" + String(binaryResp);
        sendToPi(stringVal) 
        break;
      case 6: //Detect if object is in device (load cell)
        sendToPi("6"); //Acknowledge command
        binaryResp = readLCState();
        stringVal = "2" + String(binaryResp);
        sendToPi(stringVal) 
        break;
       case 7:  //Lock door
        sendToPi("7"); //Acknowledge command
        exitCode = lockDoor();
        stringVal = String(exitCode);
        sendToPi(stringVal)
        break;
       case 8:  //Unlock door
        sendToPi("8"); //Acknowledge command
        exitCode = unlockDoor();
        stringVal = String(exitCode);
        sendToPi(stringVal)
        break;
       case 9: //Dummy read Sensor value
        sendToPi("9"); //Acknowledge command
        value = readSensor();
        stringVal = "2" + String(value);
        sendToPi(stringVal) 
        break;
    }
    sendToPi(stringVal);
 }  
}

void sendToPi(String val){
  int resendAttempts = 10;
  char prefix = val[0];
  if(val == "0"){  //Success exit code
    for(int i = 0; i < resendAttempts;i++){
      Serial.println(0);
    }  
  }else if(prefix == '1' || prefix == '2' || val.toInt() < 8){
    for(int i = 0; i < resendAttempts;i++){   //Error code or Any value
      Serial.println(val.toInt());
    }  
  }else{
    for(int i = 0; i < resendAttempts;i++){   //Any value
      Serial.println(1111);  //Bad input for val
    }  
  }
}

/*
 * Stepper Motor Function
 */
int sortObject(bool direction){ //0 Trash 1 Recycling
  stepper.setMaxSpeed(1500); //1500
  stepper.setAcceleration(500); //500
  stepper.setCurrentPosition(0);
  bool done = false;
  int targetPos = 3100; //3000
  if(direction){  //Recycling
    stepper.moveTo(targetPos);
  }else{    //Trash
    stepper.moveTo(-targetPos);
  }
  while(!done){
      stepper.run();    

    if (stepper.distanceToGo() == 0){
      if(abs(stepper.targetPosition()) == targetPos){
        stepper.moveTo(0); 
      }
      else if(stepper.targetPosition() == 0){
        done = true;
      }

    }
      stepper.run();    
  }

  return 0;
}
/*
 * Get whether door is open or closed
 * 1 - Door closed
 * 0 - Door open
 */
int readDoorState(void){
  int j = i;
  delay(2000);
  i += 1;
  if(i > 1){
    i = 0;
  }
  return  j;   
}

/*
 * Get whether object is detected in device
 * 1 - Object detected
 * 0 - Object not detected
 */
int readLCState(void){
  delay(1000);
  return 1;  
}

/*
 * Lock the object entry door
 */
int lockDoor(void){
  delay(3000);
  return 0;
}

/*
 * Unlock the object entry door
 */
int unlockDoor(void){
  delay(3000);
  return 0;  
}

/*
 * Read an arbitrary sensor
 */
int readSensor(void){
  delay(500);
  return 56;  
}
