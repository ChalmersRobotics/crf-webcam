#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, signal, threading, datetime

sys.path.append('SimpleCVHelper')
from SimpleCVHelper import *

import json
try:
	with open("cam.conf") as json_data_file:
		config = json.load(json_data_file)
except:
	e = sys.exc_info()[0]
	print(e)
	print("Failed to read config file cam.conf")
	global shutdown
	shutdown = True

from picam2cv import picam2cv
picam = None

import webcamFunctions

last = Image()
current = webcamFunctions.c0
shutdown = False

def threadCamLoop():
	global last, current
	while not shutdown:
		sDateTimeFile = datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
		sDateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		print("Cam loop {}".format(sDateTime))

		last = current
		current = picam.getRaspiCamImage()

		motionDetected, blobsDetected = webcamFunctions.detectMovement(last, current)
		numberOfPeople, currentAnon = webcamFunctions.anonymize(current)

		filenameCurrent = config['filenameNow'].format(sDateTimeFile)
		filenameDetect = config['filenameMovement'].format(sDateTimeFile)

		filesToUpload = []
		if motionDetected:
			webcamFunctions.drawCRFHeader(currentAnon, config['titleMovement'].format(sDateTime))
		else:
			webcamFunctions.drawCRFHeader(currentAnon, config['titleNow'].format(sDateTime))
		currentAnon.show()
		#imgCurrent.save(filenameCurrent)
		#filesToUpload.append(filenameCurrent)

		#if motionDetected:
		#	imgMovement = webcamFunctions.drawMovement(currentAnon, blobsDetected)
		#	imgMovement = webcamFunctions.drawText(currentAnon, config['titleMovement'].format(sDateTime))
		#	imgMovement.save(filenameDetect)
		#	filesToUpload.append(filenameDetect)

		#webcamFunctions.sendSFTP(filesToUpload)
	print("Thread exit")

def signal_handler(signal, frame):
	print('SIGINT detected. Prepareing to shut down.')
	global shutdown
	shutdown = True

if __name__ == '__main__':
	print("Starting")

	print("Init raspicam")
	global picam
	picam = picam2cv()

	#Start listening for SIGINT (Ctrl+C)
	signal.signal(signal.SIGINT, signal_handler)

	t = threading.Thread(target=threadCamLoop, args=())
	t.start()

	#Cause the process to sleep until a signal is received
	signal.pause()

	print("Exit")
	sys.exit(0)

