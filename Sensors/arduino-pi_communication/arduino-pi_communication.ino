bool first = true;
int var;
const int SUCCESS = 0;

void setup(){
  Serial.begin(9600);
}

void loop(){

  if (Serial.available() > 0) {
    
    String data = Serial.readStringUntil('\n');
    data.trim();
    int command = data.toInt();
    sendToPi(command);
    sendToPi(SUCCESS);
    
    
    
    /*
    if(first){
      var = Serial.read();    // data type: int
      first = false;  
    }
    Serial.print(var);
    */
    /*
    var = Serial.read();    // data type: int
    sendToPi(0);
    if(var == 49){
      sendToPi(3);  //Sorting to Recycling...
      delay(5000);
      sendToPi(3);  //Finished with no errors    
    }else if(var == 48){
      sendToPi(2);  //Sorting to Trash...
      delay(5000);
      sendToPi(1);  //Error - did not finish  
    }
    */
 }  
}

void sendToPi(int code){
  int resendAttempts = 100;
  for(int i = 0; i < resendAttempts;i++){
    Serial.print(code);
  }
}
