# arduino-adaptive-brightness
Adjusts the display backlight (a.k.a. adaptive brightness) using an Arduino and a photocell sensor. Every few moments, the display backlight is adjusted according to the ambient brightness perceived by the sensor.

Supported OS(es): Linux.


## Prerequisites

Software:
* [Arduino IDE](https://www.arduino.cc/)
* [Python 2.7](https://www.python.org/)
  * [NumPy](http://www.numpy.org/)
  * [pySerial](https://github.com/pyserial/)
* [xbacklight](https://linux.die.net/man/1/xbacklight)

Hardware:
* Arduino board
* 10kΩ Resistor
* Photocell (LDR)


## Installation

1. Get the code:
  ```bash
  git clone https://github.com/stephanepoirier/arduino-adaptive-brightness.git
  ```

2. Install dependencies, for instance:
  ```bash
  sudo pip install numpy pyserial
  sudo apt-get install xbacklight
  ```

3. Perform hardware setup:
  * Breadboard:
    
    <img src="../master/docs/layout_bb.png" alt="Arduino breadboard diagram" width="300">
  * Schematic diagram:
    
    <img src="../master/docs/layout_schem.png" alt="Arduino schematic diagram" width="300">
  * PCB:
    
    <img src="../master/docs/layout_pcb.png" alt="Arduino PCB diagram" width="300">

4. Open the Arduino sketch `./arduino/ArduinoAnalogReceiver/ArduinoAnalogReceiver.ino` and upload it to the Arduino.


## Usage

1. Make sure the Arduino is connected to your PC via USB
2. Run (add `--help` argument for options):
```bash
python ./src/main.py
```

## Contributing

* Bug reports and enhancement requests: please create an issue on GitHub.
* Pull requests: guidelines are not established yet.


## Authors

Stephane Poirier (<stephane.poirier01@gmail.com>)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
