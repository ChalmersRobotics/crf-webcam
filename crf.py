from SimpleCV import Image
imgEmma = Image('emma.jpg')
imgBackground = Image('bg.jpg')
p1 = Image('people1.jpg')
p2 = Image('people2.jpg')
p3 = Image('people3.jpg')
p4 = Image('people4.jpg')
p5 = Image('people5.jpg')
p6 = Image('people6.jpg')

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

def testHaar(img, listHaar):
	outList = []
	for haarFile in listHaar:
		tmpImg = img.copy()
		tmpHaar = tmpImg.grayscale().findHaarFeatures(haarFile)
		tmpImg.draw(tmpHaar, width=3)
		tmpImg.save('tmp.png')
		tmpImg2 = Image('tmp.png')
		outList.append(tmpImg2)
	return(outList)

def anonymize(img):
	print("hejhejhej")
	return(img)

def drawCRFHeader(name, img):
	return(img)

