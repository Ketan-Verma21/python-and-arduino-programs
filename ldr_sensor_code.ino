void setup() {
  Serial.begin(9600);
  pinMode(13,OUTPUT);
}
int ldr;
void loop() {
  ldr=analogRead(A1);
  if(ldr<105){
    digitalWrite(13,HIGH);
    }
  else{
    digitalWrite(13,LOW);} 
  delay(100) ; 

}
