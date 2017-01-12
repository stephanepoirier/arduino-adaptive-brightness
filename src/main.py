# Adaptive brightness for Linux using the Arduino and a photocell sensor.
#
# Author: Stephane Poirier <stephane.poirier01@gmail.com>
# URL: https://github.com/stephanepoirier/arduino-adaptive-brightness

import argparse
import logging
from subprocess import check_output
import threading

import numpy
import serial.tools.list_ports


MIN_BACKLIGHT = 0;
MAX_BACKLIGHT = 100;

def main():
	"""Main program."""
	
	logging.basicConfig(level=logging.WARN, format='%(asctime)s %(message)s')
	
	args = parseArgs()
	
	port = initSerial(args.device, args.baudrate)
	stopEvent = threading.Event()
	adjustBacklightThread = threading.Thread(name='adjustBacklight', target=adjustBacklightLoop, args=(port, stopEvent))
	adjustBacklightThread.start()
	
	print('Press Return to exit.')
	raw_input()
	logging.debug('Exit requested by user.')
	stopEvent.set()
	adjustBacklightThread.join()
			
	port.close()
	

def parseArgs():
	"""Parses program input arguments."""
	
	parser = argparse.ArgumentParser(description='Adjusts screen brightness.')
	
	# Device name arg
	knownPorts = serial.tools.list_ports.comports();
	defaultDev = knownPorts[0].device if knownPorts else ''
	devHelp = 'Serial port device name. Default: {0}.'.format(defaultDev)
	parser.add_argument('--device', type=str, default=defaultDev, help=devHelp)
	
	# Baudrate arg
	defaultBR = 9600
	brHelp = 'Serial baud rate. Default: {0}.'.format(defaultBR)
	parser.add_argument('--baudrate', type=int, default=defaultBR, help=brHelp)

	return parser.parse_args()


def initSerial(device, baudrate):
	"""Opens a serial connection with a given device and baudrate."""
	
	logging.debug('Initializing serial port (device: {0}, Baud rate: {1}).'.format(device, baudrate))

	return serial.Serial(device, baudrate)


def executeCommand(command):
	"""Executes the specified shell command."""
	
	return check_output(command, shell=True)


def setBacklight(value):
	"""Sets the display backlight value."""
	
	logging.debug('Setting backlight to: {0}'.format(value))
	
	command = 'xbacklight -set ' + str(value)
	executeCommand(command)
	
	
def getBacklight():
	"""Returns the display backlight value."""
	
	return executeCommand('xbacklight -get')


def byteToRatio(byteValue):
	"""Interpolates a byte value [0-255] to a [0, 1] ratio."""
	
	return byteValue / 255.0;


def mapArduinoValue(arduinoValue, newMin, newMax):
	"""
	Interpolates an Arduino value (byte) to the specified range.
	
	Keyword arguments:
		arduinoValue -- Arduino value (byte)
		newMin       -- Output lower bound
		newMax       -- Output upper bound
	"""
	
	ratio = byteToRatio(arduinoValue);
	fullRange = newMax - newMin;
	newValue = newMin + (fullRange * ratio);

	return newValue;


def adjustBacklightLoop(port, stopEvent):
	"""
	Repetively reads Arduino photocell sensor input and adjusts the display 
	backlight accordingly.
	
	For robustness, the median value is selected out of a block of readings.
	
	Keyword arguments:
		port      -- Serial port instance
		stopEvent -- Thread event to request terminating the function
	"""
	
	oldBacklight = getBacklight();
	while True:
		port.reset_input_buffer()
		sensorValues = port.read(200)
		if stopEvent.isSet():
			break
		
		sensorValues = map(ord, sensorValues)
		median = numpy.median(sensorValues)
		
		backlight = mapArduinoValue(median, MIN_BACKLIGHT, MAX_BACKLIGHT)
		setBacklight(backlight)
	
	logging.debug('Restoring original backlight.')
	setBacklight(oldBacklight);


main()