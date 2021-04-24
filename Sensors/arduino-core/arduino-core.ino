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
        break;
      case 5: //Read Hinge State (Limit Switch)
        sendToPi("5"); //Acknowledge command
        delay(1000);
        //binaryResp = readHingeState();
        binaryResp = 1;
        stringVal = "2" + String(binaryResp); 
        break;
      case 6: //Detect if object is in device (load cell)
        sendToPi("6"); //Acknowledge command
        delay(2000);
        //binaryResp = readHingeState();
        binaryResp = 0;
        stringVal = "2" + String(binaryResp); 
        break;
      case 7: //Dummy read Sensor value
        sendToPi("7"); //Acknowledge command
        delay(1000);
        //value = readSensor();
        value = 56;
        stringVal = "2" + String(value); 
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
