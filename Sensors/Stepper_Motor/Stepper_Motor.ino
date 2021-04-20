// Bounce.pde
// -*- mode: C++ -*-
//
// Make a single stepper bounce from one limit to another
//
// Copyright (C) 2012 Mike McCauley
// $Id: Random.pde,v 1.1 2011/01/05 01:51:01 mikem Exp mikem $

#include <AccelStepper.h>

// Define a stepper and the pins it will use
AccelStepper stepper(AccelStepper::DRIVER, 2, 4); // Defaults to AccelStepper::FULL4WIRE (4 pins) on 2, 3, 4, 5
int rasp = 0; //recycle 1 trash 0
bool done = false;
int targetPos = 3000; //3000
//int constspeed = 500;

void setup()
{  
  // Change these to suit your stepper if you want
  //stepper.setMinPulseWidth(10);
  stepper.setMaxSpeed(1500); //1500
  stepper.setAcceleration(500); //500
  stepper.setCurrentPosition(0); 
  if(rasp){
    stepper.moveTo(targetPos);
  }else{
    stepper.moveTo(-targetPos);
  }
  //stepper.setSpeed(1500);
  Serial.begin(9600);
  //delay(7000);
}

void loop()
{
  /*
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    Serial.print("You sent me: ");
    Serial.println(data);

    rasp = data.toInt();
    
    if(rasp){
      Serial.println("Sorting to Recycling...");
    }else{
      Serial.println("Sorting to Trash...");
    }
  }
  */
  
  if (stepper.distanceToGo() == 0){
    if(abs(stepper.targetPosition()) == targetPos){
      stepper.moveTo(0);
      //stepper.setSpeed(-constspeed);  
    }
    else if(stepper.targetPosition() == 0){
      done = true;
    }
      
  }
  if(!done){
    //stepper.runSpeed();
    stepper.run();    
  }

  Serial.println(stepper.distanceToGo());
  

}
