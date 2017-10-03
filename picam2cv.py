# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
from SimpleCV import Image
from numpy import rot90
import math
import time

class picam2cv:
	def __init__(self, **kwargs):
		self.camera = PiCamera()

	def getRaspiCamImage(self):
		rawCapture = PiRGBArray(self.camera)
		self.camera.capture(rawCapture, format="rgb")
		image = Image(rot90(rawCapture.array, 1)).flipHorizontal()
		return(image)

