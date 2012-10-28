#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import string
import serial


def main():
    ser = serial.Serial('/dev/ttyUSB0', 57600)
    ser.write('T0ABCD1234')    

if __name__ == '__main__':
    main()

