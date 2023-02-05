#Nova Labs
#Bluetooth Commander - Improved receving commands and sending response
#Jan 2023

#OS required
import os
import time
import board
import busio

#USB HID Libraries
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.mouse import Mouse

#Feather RP2040 has integrated LED
#LED required libraries
import neopixel

#Random number library
from random import randint

#AES encryption Module
import easycrypt
from binascii import hexlify, unhexlify

#SD card readfile
import filesdcard

#Creating objects for required libraries
#HID
mouse = Mouse(usb_hid.devices)
keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)
#NeoPixel
pixle = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixle.brightness = 0.3

#Array for reading hexstring.txt file
strfile = []
key_str = filesdcard.hexstringfile(strfile)

#List of Adafruit Keyboard strokes
key_pad = [Keycode.GUI, Keycode.R, Keycode.M, Keycode.UP_ARROW,
           Keycode.ENTER, Keycode.DELETE, Keycode.DOWN_ARROW,
           Keycode.L]

#List of Hex values, for Activating commands
hex_value = ["0A","1A","2A","3A","4A","5A","6A","7A","8A","9A",
             "0B","1B","2B","3B","4B","5B","6B","7B","8B","9B",
             "0C","1C","2C","3C","4C","5C","6C","7C","8C","9C",]

print("HexString File loaded successfully")

#Bluetooth is controlled by UART protocol
uart = busio.UART(tx=board.TX, rx=board.RX, baudrate=9600)

#Dictionary of Pixel LED colors
c_red = (255,0,0)
c_blue = (0,255,0)
c_green = (0,0,255)
c_orange = (255,128,0)
c_pink = (255,51,153)
c_yellow = (255,255,0)
c_aqua = (51,255,255)
c_purple = (153,51,255)
c_white = (255,255,255)
c_black = (0,0,0)
c_magenta = (255,0,255)

#Definition of functions
def decrypt_str():
    keystring = key_str[11].strip()
    hexstring = key_str[4].strip()
    decrypted = easycrypt.decrypt_string(keystring, hexstring)
    return decrypted

def runas_app(colorled, command_str):
    pixle.fill(colorled)
    run_shortcut(1)
    time.sleep(0.5)
    cmd_str = layout.write(command_str)
    time.sleep(1)
    pixle.fill(c_black)

def runas_cmd(colorled, command_pad):
    pixle.fill(colorled)
    keyboard.send(key_pad[0], key_pad[1])
    time.sleep(0.5)
    layout.write(key_str[2])
    time.sleep(1)
    cmd_str = layout.write(command_pad)
    time.sleep(1)
    pixle.fill(c_black)

def run_lock(colorled, keystr1):
    pixle.fill(colorled)
    keyboard.send(key_pad[0], key_pad[keystr1])
    time.sleep(1)
    pixle.fill(c_black)
    
def run_shortcut(keystr2):
    keyboard.send(key_pad[0], key_pad[keystr2])
    time.sleep(0.5)

def unlockdevice():
    pixle.fill(c_blue)
    keyboard.send(key_pad[4])
    time.sleep(1)
    layout.write(decrypt_str())
    keyboard.send(key_pad[4])
    time.sleep(1)
    pixle.fill(c_black)
    
def cmdresponse():
    rsp_string = "Activated command."
    rsp_byte_array = bytearray(rsp_string)
    uart.write(rsp_byte_array)

#MAIN LOOP Process
while True:
    data = uart.read(2)

    if data is not None:
        data_string = ''.join([chr(b) for b in data])
        print("Received HexValue: " + data_string)

        if data_string == hex_value[0]:
            #Open Notepad
            runas_app(c_white, key_str[1])
            cmdresponse()

        elif data_string == hex_value[1]:
            #Restart PC
            runas_cmd(c_orange, key_str[3])
            cmdresponse()

        elif data_string == hex_value[2]:
            #Shutdown PC
            runas_cmd(c_orange, key_str[5])
            cmdresponse()

        elif data_string == hex_value[3]:
            #Lock User
            run_lock(c_blue, 7)
            cmdresponse()

        elif data_string == hex_value[4]:
            unlockdevice()
            cmdresponse()

        elif data_string == hex_value[5]:
            #Open Gmail
            runas_app(c_pink, key_str[6])
            cmdresponse()

        elif data_string == hex_value[6]:
            #Open Facebook
            runas_app(c_aqua, key_str[7])
            cmdresponse()

        elif data_string == hex_value[7]:
            #Open One Note
            runas_app(c_purple, key_str[9])
            cmdresponse()

        elif data_string == hex_value[8]:
            #Open Outlook
            runas_app(c_blue, key_str[8])
            cmdresponse()

        elif data_string == hex_value[9]:
            #Open Microsoft Edge
            runas_app(c_green, key_str[10])
            cmdresponse()

        elif data_string == hex_value[10]:
            runas_app(c_blue, key_str[8]) #Outlook
            time.sleep(10)
            runas_app(c_purple, key_str[9]) #OneNote
            time.sleep(10)
            cmdresponse()
