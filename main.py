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
picam = picam2cv()

import crf

last = Image()
current = Image()
shutdown = False

def threadCamLoop():
	while not shutdown:
		last = current
		current = picam.getRaspiCamImage()

		motionDetected, blobsDetected = crf.detectMovement(last, current)
		numberOfPeople, currentAnon = crf.anonymize(current)

		sDateTimeFile = datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
		sDateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

		filenameCurrent = config['filenameNow'].format(sDateTimeFile)
		filenameDetect = config['filenameMovement'].format(sDateTimeFile)

		filesToUpload = []
		imgCurrent = crf.drawText(currentAnon, config['titleNow'].format(sDateTime))
		imgCurrent.save(filenameCurrent)
		filesToUpload.append(filenameCurrent)

		if motionDetected:
			imgMovement = crf.drawMovement(currentAnon, blobsDetected)
			imgMovement = crf.drawText(currentAnon, config['titleMovement'].format(sDateTime))
			imgMovement.save(filenameDetect)
			filesToUpload.append(filenameDetect)

		crf.sendSFTP(filesToUpload)

def signal_handler(signal, frame):
	print('SIGINT detected. Prepareing to shut down.')
	global shutdown
		shutdown = True

if __name__ == '__main__':
	print("Starting cam")

	#Start listening for SIGINT (Ctrl+C)
	signal.signal(signal.SIGINT, signal_handler)

	t = threading.Thread(target=threadCamLoop, args=())
	t.start()

	#Cause the process to sleep until a signal is received
	signal.pause()

	print("Exit")
	sys.exit(0)

