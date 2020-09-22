import pyaudio
import os
import struct
import numpy as np
import time

# constants
CHUNK = 1024 * 2             # samples per frame
FORMAT = pyaudio.paInt16    # audio format (bytes per sample?)
CHANNELS = 1                 # single channel for microphone
RATE = 44100                 # samples per second

import sys
import serial

serialPort = '/dev/cu.usbmodem14301'
baudRate = 115200
usbConnection = serial.Serial(serialPort, baudRate)

def commandArduino(string):
    outputStr = string + '\n'
    outputStr = bytes(outputStr, 'utf-8')
    usbConnection.write(outputStr)
    usbConnection.reset_input_buffer()

# pyaudio class instance
p = pyaudio.PyAudio()

# stream object to get data from microphone
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=True,
    frames_per_buffer=CHUNK
)

while True:
  try:
    data = stream.read(CHUNK, exception_on_overflow = False)
    data_np = np.frombuffer(data, dtype=np.int16)
    
    # volume
    delta = np.max(data_np) - np.min(data_np)
    delta_mod = int(np.abs(delta) ** 0.7)
    delta_bounded = min(max(delta_mod, 0), 128)

    commandArduino(f'vibrate,{delta_bounded}')
    print(delta, delta_bounded)

  except:
      p.close(stream)