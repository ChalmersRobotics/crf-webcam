#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, signal, threading

sys.path.append('SimpleCVHelper')
from SimpleCVHelper import *

import json
try:
	with open("cam.conf") as json_data_file:
		config = json.load(json_data_file)


from picam2cv import picam2cv
picam = picam2cv()

import crf

last = Image()
current = Image()
shutdown = False

def threadCamLoop():
	while not shutdown:
		current = picam.getRaspiCamImage()

		motionDetected, blobsDetected = crf.detectMovement(last, current)
		numberOfPeople, currentAnon = crf.anonymize(current)

		roomName = config['name']
		sDate = Now(ISO8601)
		sDateTime = Now(ISO8601)

		filenameCurrent = config['filenameNow'].format(sDate)
		filenameDetect = config['filenameMovement'].format(sDate)
		titleCurrent = config['titleNow'].format(sDateTime)
		titleDetect = config['titleMovement'].format(sDateTime)

		filesToUpload = []
		imgCurrent = crf.drawText(currentAnon, titleCurrent)
		imgCurrent.save(filenameCurrent)
		filesToUpload.append(filenameCurrent)

		if motionDetected:
			imgMovement = crf.drawMovement(currentAnon, blobsDetected)
			imgMovement = imgMovement(imgMovement, titleDetect)
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

