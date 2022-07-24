int triggerPin=7;
int echoPin=7;
float distance;
float duration;


void setup()
{
  Serial.begin(9600);
}

void loop()
{
  pinMode(triggerPin,OUTPUT);
  digitalWrite(triggerPin,LOW);
  delayMicroseconds(2);
  
  digitalWrite(triggerPin, HIGH);
  delayMicroseconds(5);
  
  digitalWrite(triggerPin,LOW);
  pinMode(echoPin,INPUT);
  duration=pulseIn(echoPin,HIGH);
  distance=(duration*0.034)/2;
  
  Serial.print("\n Distance: ");
  Serial.print(distance);
  Serial.print(" cm");
  delay(100);
}
