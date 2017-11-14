#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, signal, threading, datetime, time, getopt

configFile = "cam.conf"
config = None
import json

from picam2cv import picam2cv
picam = None

import webcamFunctions

last = None
current = None
shutdown = False
debugMode = False

def threadCamLoop():
	global last, current
	current = picam.getRaspiCamImage()
	while not shutdown:
		sDateTimeFile = datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
		sDateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		if debugMode:
			print("Cam loop {}".format(sDateTime))

		last = current
		current = picam.getRaspiCamImage()

		motionDetected, blobsDetected = webcamFunctions.detectMovement(last, current)
		numberOfPeople, currentAnon = webcamFunctions.anonymize(current)

		filenameCurrent = config['filenameNow'].format(sDateTimeFile)
		filenameDetect = config['filenameMovement'].format(sDateTimeFile)

		filesToUpload = []
		imgCurrent = currentAnon.copy()
		webcamFunctions.drawCRFHeader(imgCurrent, config['titleNow'].format(sDateTime))
		if debugMode:
			imgCurrent.show()
		imgCurrent.save(filenameCurrent)
		filesToUpload.append(filenameCurrent)

		if motionDetected:
			imgMovement = currentAnon.copy()
			webcamFunctions.drawMovement(imgMovement, blobsDetected)
			webcamFunctions.drawCRFHeader(imgMovement, config['titleMovement'].format(sDateTime))
			if debugMode:
				imgMovement.show()
			imgMovement.save(filenameDetect)
			filesToUpload.append(filenameDetect)

		webcamFunctions.upload(filesToUpload, config)

		time.sleep(10)
	if debugMode:
		print("Exit cam thread")

def signal_handler(signal, frame):
	if debugMode:
		print('SIGINT detected. Prepareing to shut down.')
	global shutdown
	shutdown = True

if __name__ == '__main__':
	if debugMode:
		print("Starting")
	try:
		opts, args = getopt.getopt(sys.argv[1:],"c:d",["config=","debug"])
		for o, a in opts:
			if o in ("-c", "--config"):
				global configFile
				configFile = a
			if o in ("-d", "--debug"):
				global debugMode
				debugMode = True
	except getopt.GetoptError as err:
		if debugMode:
			print(err)

	try:
		if debugMode:
			print("Config file: {}".format(configFile))
		with open(configFile) as json_data_file:
			global config
			config = json.load(json_data_file)
	except:
		e = sys.exc_info()[0]
		if debugMode:
			print(e)
			print("Failed to read config file cam.conf")
		global shutdown
		shutdown = True

	if debugMode:
		print("Init raspicam")
	global picam
	picam = picam2cv()

	#Start listening for SIGINT (Ctrl+C)
	signal.signal(signal.SIGINT, signal_handler)

	t = threading.Thread(target=threadCamLoop, args=())
	t.start()

	#Cause the process to sleep until a signal is received
	signal.pause()

	if debugMode:
		print("Exit")
	sys.exit(0)

