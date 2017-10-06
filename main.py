#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('SimpleCVHelper')
from SimpleCVHelper import *

from picam2cv import picam2cv
picam = picam2cv()

import crf

last = Image()
current = picam.getRaspiCamImage()

motionDetected, blobsDetected = crf.detectMovement(last, current)
numberOfPeople, currentAnon = crf.anonymize(current)

roomName = config['name']
sDate = Now(ISO8601)
sDateTime = Now(ISO8601)

filenameCurrent = '{}_current_{}.jpg'.format(roomName, sDate)
filenameDetect = '{}_detect_{}.jpg'.format(roomName, sDate)
titleCurrent = 'CRF {} {}'.format(roomName, sDateTime)
titleDetect = 'CRF {} {}.jpg'.format(roomName, sDateTime)

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

