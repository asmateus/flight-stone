void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  delay(2000);
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.write("Hello, World! From the dirty Arduino\n");
  delay(1000);
}
