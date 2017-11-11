from SimpleCV import Image
import cv2

imgEmma = Image('emma.jpg')
imgBackground = Image('bg.jpg')
p1 = Image('people1.jpg')
p2 = Image('people2.jpg')
p3 = Image('people3.jpg')
p4 = Image('people4.jpg')
p5 = Image('people5.jpg')
p6 = Image('people6.jpg')

c0 = Image('crf00.png')
c1 = Image('crf01.png')
c2 = Image('crf02.png')
c3 = Image('crf03.png')
c4 = Image('crf04.png')
c5 = Image('crf05.png')

def detectMovement(last, current):
	diff = (current - last) + (last - current)
	diff2 = diff.erode(4)
	blobs = diff2.findBlobs(minsize=10000)
	if blobs:
		return(True, blobs)
	else:
		return(False, blobs)

def anonymize(img):
	imgOut = img.copy()
	features = imgOut.findHaarFeatures("upper_body.xml")
	anonScale = 20.0
	for feature in features:
		#Pixelate via rescale
		featureImg = feature.crop().resize(	w=int(feature.width()/anonScale),
											h=int(feature.height()/anonScale)
											).scale(anonScale)
		imgOut = imgOut.blit(featureImg, pos=feature.topLeftCorner())
	return(len(features), imgOut)

def drawCRFHeader(img, headerText):
	img.dl().selectFont("ethnocentric")
	img.drawText(text=headerText, x=16, y=8, fontsize=72, color=(0, 0, 0))
	img.drawText(text=headerText, x=8, y=12, fontsize=72, color=(255, 200, 46))

