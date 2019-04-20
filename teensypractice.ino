unsigned long s = 0;
void setup(){
    Serial.begin(0);//Not important !(speed 12Mb/s)
    }

void loop(){
    if(Serial.available() > 0){
    while(Serial.available() > 0){//Buffer memory must always be clean !
        char read = Serial.read();
        delay(1);//wait until next_char
        }
    Serial.print("TEST : ");
    Serial.println(s, DEC);
    s++;
    }
}
