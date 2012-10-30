#include <TM1638.h>

#define MODULES 4

// define a modules
TM1638 modules[] = {
	TM1638(8, 9, 7),
	TM1638(8, 9, 6),
	TM1638(8, 9, 5),
	TM1638(8, 9, 4)
};

void setup() {
      Serial.begin(57600);
      bootup();
}

char string[4][8];
int k = 0;
byte buttons;

void loop() {

    if(Serial.available() && Serial.available()>2) {
        int type = 0;
        k = 0;

        char ctype = char(Serial.read());
        char cmod = char(Serial.read());
        int mod = atoi(&cmod);
        
        if(ctype==76) { // 76 = "L" : "LED"
            char color = 1;
            int led = -1;
            if(Serial.available()) {
                char ccolor = Serial.read();
                color = atoi(&ccolor);
            }
            if(Serial.available()) {
                char cled = Serial.read();
                led = atoi(&cled);
            }
            if(led>=0) {
                modules[mod].setLED(color, led);
            }
        } else { // 84 = "T" : "TEXT"
            while(Serial.available() > 0) {
                if(k<8) {
                    string[mod][k] = Serial.read();
                } else {
                    break;
                }
                k++;
            }
            modules[mod].clearDisplay();
            modules[mod].setDisplayToString(string[mod]);
        }
        
    }

    for (int i = 0; i < MODULES; i++) {
        buttons = modules[i].getButtons();
        if(buttons!=0) {
            Serial.print("B");
            Serial.print(i);
            Serial.println(buttons);
        }
    }
    delay(200);
}

void clearDisplay() {
    modules[0].clearDisplay();
    modules[1].clearDisplay();
    modules[2].clearDisplay();
    modules[3].clearDisplay();
}

void bootup() {
    clearDisplay();
    modules[0].setDisplayToString("BOOT UP ");
    modules[1].setDisplayToString("BOOT UP ");
    modules[2].setDisplayToString("BOOT UP ");
    modules[3].setDisplayToString("BOOT UP ");
    delay(200);
    clearDisplay();
    delay(200);
    modules[0].setDisplayToString("BOOT UP ");
    modules[1].setDisplayToString("BOOT UP ");
    modules[2].setDisplayToString("BOOT UP ");
    modules[3].setDisplayToString("BOOT UP ");
    delay(200);
    clearDisplay();
    delay(200);
    modules[0].setDisplayToString("PANEL 1 ");
    modules[1].setDisplayToString("PANEL 2 ");
    modules[2].setDisplayToString("PANEL 3 ");
    modules[3].setDisplayToString("PANEL 4 ");
    delay(2000);
    clearDisplay();
    
}

