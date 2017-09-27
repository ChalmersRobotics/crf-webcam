# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
from SimpleCV import Image
from numpy import rot90
import math
import time

class webcamlib:
	def __init__(self, **kwargs):
		self.camera = PiCamera()
		self.imgEmma = Image('emma.jpg')
		self.imgBackground = Image('bg.jpg')

	def getRaspiCamImage(self):
		rawCapture = PiRGBArray(self.camera)
		self.camera.capture(rawCapture, format="rgb")
		image = Image(rot90(rawCapture.array, 1)).flipHorizontal()
		return(image)

