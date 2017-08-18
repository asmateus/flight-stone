char a[9] = "00000000";
 
  void setup()
{
    Serial.begin(115200);
    delay(100);
}

void loop()
{
    if (Serial.available() > 0) {
        Serial.readBytes(a, 8);
        Serial.println(a);
    }
}
