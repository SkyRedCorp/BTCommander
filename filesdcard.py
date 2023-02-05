#Nova Labs
#File SD Card library - used for read specific files on SD
#Jan 2023

#Import OS, Core and SD libraries
import os
import adafruit_sdcard
import board
import busio
import digitalio
import storage

#Check File
from core.checkfile import file_exists

name = "filesdcard"

#Chip Select Port
SD_CS = board.D0

#SPI protocol ports
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)

#Used for Adafruit SD Card library
cs = digitalio.DigitalInOut(board.D5)
sdcard = adafruit_sdcard.SDCard(spi, cs)

#Storage type and mount
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

#strfile = []


#Hex String file function (List of strings to put in Run command)
def hexstringfile(strfile):
    arrfile = []
    if(file_exists("/sd/hexstring.txt")):
        with open("/sd/hexstring.txt", "r") as f:
            lines = f.readlines()
            print("Reading HexString file...")
            for line in lines:
                arrfile.append(line)
        return arrfile

#KeyPad file function (List of Key Strokes - Experimental)
def keypadfile(keyfile):
    arrfile = []
    if(file_exists("/sd/keypad.txt")):
        with open("/sd/keypad.txt", "r") as f:
            lines = f.readlines()
            print("Reading KeyPad file...")
            for line in lines:
                arrfile.append(line)
        return arrfile

#Command list File function (List of Commands to response)
def cmdfile(cmdlistfile):
    arrfile = []
    
    if(file_exists("/sd/keypad.txt")):
        with open("/sd/keypad.txt", "r") as f:
            lines = f.readlines()
            print("Reading KeyPad file...")
            for line in lines:
                arrfile.append(line)
        return arrfile
    
    with open("/sd/cmdfile.txt", "r") as f:
        lines = f.readlines()
        print("Reading CMDFile...")
        for line in lines:
            arrfile.append(line.strip())
    return arrfile