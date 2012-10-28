X-Plane plugin
==============

A plugin for X-Plane 10 to show the data on a homemade cockpit



I'm using 4 7-segment/8 digits displays from dx.com ( any of these: http://dx.com/s/tm1638 ), they use the TM1638 chip, fortunately there's an arduino library for it.

The arduino code will be as simple and dummy as possible, so it could be configured on the python script.A python script could be modified easily, but arduino code has to be compiled and uploaded each time, leaving the hard-work to python will made the plugin more flexible and configurable.

Usage
===
* T{MODULE}{TEXT} : Display the message {TEXT} on the {MODULE} ({MODULE} is an integer from 0 to 3, {TEXT} is a string of length 8, shorter length will cause some problems, any character from position 9 will not be displayed)
* L{MODULE}{COLOR}{LED} : Set/unset the color {COLOR} on the led number {LED} of the module {MODULE} ({MODULE} and {LED} numbers starts from 0), Available colors are RED=1, GREEN=2, RED+GREEN=3, anything else will turn the led off.
* B{MODULE}{BUTTONS} : Sent from the arduino to the serial port telling us which buttons are pressed. {BUTTONS} are the sum of the value of the buttons (buttonX=2^X), for example, buttons 1 + 4 are pressend on the module 0, B034 (2^1 + 2^5 = 2 + 32 = 34)


TODO
===
* Take care of longer/shorter string propertly
* Sending twice the same command for leds, will turn them off, need to improve it.
* Add servos
