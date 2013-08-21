#!/usr/bin/python2

import os
import sys
import time
import serial
import termios
import threading

EXIT_CHAR = '\x1d' # CTRL-]

class Console(object):

  def __init__(self):
    self.fd = sys.stdin.fileno()
    self.old = termios.tcgetattr(self.fd)
    new = termios.tcgetattr(self.fd)
    new[3] = new[3] & ~termios.ICANON & ~termios.ECHO & ~termios.ISIG
    new[6][termios.VMIN] = 1
    new[6][termios.VTIME] = 0
    termios.tcsetattr(self.fd, termios.TCSANOW, new)

  def getChar(self):
    return os.read(self.fd, 1)

  def cleanup(self):
    termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old)

class MicroTerm:

  def __init__(self):

    self.tty = serial.Serial()

    self.tty.close()

    self.tty.port = '/dev/ttyUSB0'
    self.tty.baudrate = 9600
    self.tty.stopbits = serial.STOPBITS_ONE
    self.tty.party = serial.PARITY_NONE
    self.tty.timeout = 1

    self.tty.open()

    self.console = Console()

  def _start_reader(self):
    self.receiver = threading.Thread(target=self.readThread)
    self.receiver.setDaemon(True)
    self.receiver.start()

  def _start_writer(self):
    self.transmitter = threading.Thread(target=self.writeThread)
    self.transmitter.setDaemon(True)
    self.transmitter.start()

  def start(self):
    self.alive = True;
    self._start_reader()
    self._start_writer()

  def join(self):
    self.receiver.join()
    self.transmitter.join()

  def stop(self):
    self.alive = False;
    self.join()

  def close(self):
    self.stop()
    self.tty.close()
    self.console.cleanup()

  def readThread(self):

    try:
      self.reader()
    except:
      self.alive = False
      raise

  def reader(self):

    while self.alive:

      raw_line = self.tty.readline()

      if len(raw_line) < 5: continue

      formatted_time = str(time.asctime(time.localtime(time.time())))

      print formatted_time + ", " + str(raw_line.split(' ')[4].rstrip())

  def writeThread(self):

    try:
      self.writer();
    except:
      self.alive = False;
      raise

  def writer(self):

    while self.alive:

      c = self.console.getChar()

      if c == EXIT_CHAR: self.alive = False

      self.tty.write(c)


def main():

  print "--starting--"

  term = MicroTerm()

  term.start()

  term.join()

  term.close()

  print "--exiting--"

if __name__ == '__main__':
  main()
