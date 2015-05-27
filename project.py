#!/usr/bin/python

import time
import smbus
import sys
import signal
from Adafruit_I2C import Adafruit_I2C
from Adafruit_ADS1x15 import ADS1x15


if(True):
	try:
		#######################################################################
		#								      #	
		#				SOUND	                              #
		#								      #
		#######################################################################
		def signal_handler(signal, frame):
			print 'You pressed Ctrl+C!'
			sys.exit(0)
		signal.signal(signal.SIGINT, signal_handler)

		ADS1115 = 0x01	# 16-bit ADC
		gain = 4096  # +/- 4.096V
		sps = 800  # 250 samples per second
		adc = ADS1x15(ic=ADS1115)
		volts_adc = adc.readADCSingleEnded(0, gain, sps) / 1000
		adc_thresh = 1.5
#		print "%.6f" % (volts_adc)
		adc_conv = (volts_adc/1.5*adc_thresh)*100	
	

		#######################################################################
		#								      #	
		#				LIGHT	                              #
		#								      #
		#######################################################################
		class TSL2561:
		    i2c = None

		    def __init__(self, address=0x29, debug=0, pause=0.8):
			self.i2c = Adafruit_I2C(address)
			self.address = address
			self.pause = pause
			self.debug = debug
			self.gain = 0 # no gain preselected
			self.i2c.write8(0x80, 0x03)     # enable the device


		    def setGain(self,gain=1):
			""" Set the gain """
			if (gain != self.gain):
			    if (gain==1):
				self.i2c.write8(0x81, 0x02)     # set gain = 1X and timing = 402 mSec
				if (self.debug):
				    print "Setting low gain"
			    else:
				self.i2c.write8(0x81, 0x12)     # set gain = 16X and timing = 402 mSec
				if (self.debug):
				    print "Setting high gain"
			    self.gain=gain;                     # safe gain for calculation
			    time.sleep(self.pause)              # pause for integration (self.pause must be bigger than integration time)


		    def readWord(self, reg):
			"""Reads a word from the I2C device"""
			try:
			    wordval = self.i2c.readU16(reg)
			    newval = self.i2c.reverseByteOrder(wordval)
			    if (self.debug):
				print("I2C: Device 0x%02X returned 0x%04X from reg 0x%02X" % (self.address, wordval & 0xFFFF, reg))
			    return newval
			except IOError:
			    print("Error accessing 0x%02X: Check your I2C address" % self.address)
			    return -1


		    def readFull(self, reg=0x8C):
			"""Reads visible+IR diode from the I2C device"""
			return self.readWord(reg);

		    def readIR(self, reg=0x8E):
			"""Reads IR only diode from the I2C device"""
			return self.readWord(reg);

		    def readLux(self, gain = 0):
			"""Grabs a lux reading either with autoranging (gain=0) or with a specified gain (1, 16)"""
			if (gain == 1 or gain == 16):
			    self.setGain(gain) # low/highGain
			    ambient = self.readFull()
			    IR = self.readIR()
			elif (gain==0): # auto gain
			    self.setGain(16) # first try highGain
			    ambient = self.readFull()
			    if (ambient < 65535):
				IR = self.readIR()
			    if (ambient >= 65535 or IR >= 65535): # value(s) exeed(s) datarange
				self.setGain(1) # set lowGain
				ambient = self.readFull()
				IR = self.readIR()

			if (self.gain==1):
			   ambient *= 16    # scale 1x to 16x
			   IR *= 16         # scale 1x to 16x
				        
			ratio = (IR / float(ambient)) # changed to make it run under python 2

			if (self.debug):
			    print "IR Result", IR
			    print "Ambient Result", ambient

			if ((ratio >= 0) & (ratio <= 0.52)):
			    lux = (0.0315 * ambient) - (0.0593 * ambient * (ratio**1.4))
			elif (ratio <= 0.65):
			    lux = (0.0229 * ambient) - (0.0291 * IR)
			elif (ratio <= 0.80):
			    lux = (0.0157 * ambient) - (0.018 * IR)
			elif (ratio <= 1.3):
			    lux = (0.00338 * ambient) - (0.0026 * IR)
			elif (ratio > 1.3):
			    lux = 0

			return lux

		if __name__ == "__main__":
		    tsl=TSL2561()
		    lux_conv = (tsl.readFull()/6000)*10
		    avg_conv = (lux_conv + adc_conv)/4
		    print "%.2f" % (avg_conv)
#		    print tsl.readLux()
#		    print tsl.readFull()		    
		if (tsl.readFull() >= 65535 or volts_adc > 1.5*adc_thresh):
      			print('Thunder')
#			break
	except ValueError:
		print ('blaj')
