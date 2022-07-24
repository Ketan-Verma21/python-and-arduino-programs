int irs=12 , buzz=7;
void setup() {
  Serial.begin(9600);
  pinMode(irs,INPUT);
  pinMode(buzz,OUTPUT);
  
}

void loop() {
  int out=digitalRead(irs);
  if(out==0){
    digitalWrite(buzz,HIGH);
    }
  else{
    digitalWrite(buzz,LOW);
    }  

}
