/*
 * Reads data from an analog pin and writes it to the serial port.
 * The analog value is scaled from 0-1023 to 0-255 for easier reading by the client.
 * 
 * See "USER CONFIGURATION" section below for customizable parameters.
 */

#include <limits.h>

/****************************************************************/
/*                     USER CONFIGURATION                       */
/****************************************************************/
const unsigned int BAUD_RATE = 9600;
const int ANALOG_PIN = A0;
const double TARGET_FREQUENCY = 100; // Hz (max = 1000)


const unsigned int LOOP_DELAY = 1000.0 / TARGET_FREQUENCY; // ms

const int ANALOG_IN_MIN_VALUE = 0;
const int ANALOG_IN_MAX_VALUE = 1023;

const int READY_SIGNAL = 0;

const int ANALOG_OUT_MIN_VALUE = 1;
const int ANALOG_OUT_MAX_VALUE = UCHAR_MAX;

void setup() {
  Serial.begin(BAUD_RATE);
  while (!Serial) {
    // Wait for serial port to connect. Needed for native USB port only
  }
}

void loop() {
  const unsigned int rawSensorValue = analogRead(ANALOG_PIN);
  const byte sensorValue = map(rawSensorValue, ANALOG_IN_MIN_VALUE, ANALOG_IN_MAX_VALUE, ANALOG_OUT_MIN_VALUE, ANALOG_OUT_MAX_VALUE);
  Serial.write(sensorValue);

  delay(LOOP_DELAY);
}

