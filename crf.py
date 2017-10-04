from SimpleCV import Image
imgEmma = Image('emma.jpg')
imgBackground = Image('bg.jpg')

def detectMovement(last, current):
	diff = (current - last) + (last - current)
	diff2 = diff.erode(4)
	blobs = diff2.findBlobs(minsize=10000)
	changesOut = current
	if blobs:
		for blob in blobs:
			changesOut.drawRectangle(x=blob.minX(), y=blob.minY(), w=blob.minRectWidth(), h=blob.minRectHeight(), width=3)
	#changesOut.show()
	if blobs:
		return(True, changesOut)
	else:
		return(False, changesOut)

def anonymize(img):
	print("hejhejhej")
	return(img)

def drawCRFHeader(name, img):
	return(img)

