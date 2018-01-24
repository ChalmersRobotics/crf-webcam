from SimpleCV import Image
import cv2, pysftp

def detectMovement(last, current):
	diff = (current - last) + (last - current)
	diff2 = diff.erode(4)
	blobs = diff2.findBlobs(minsize=2000)
	if blobs:
		return(True, blobs)
	else:
		return(False, blobs)

def anonymize(img):
	imgOut = img.copy()
	scaleFactor = 5.0
	imgReduced = img.copy().scale(1/scaleFactor)

	features = imgReduced.findHaarFeatures("upper_body.xml")

	anonScale = 20.0
	for feature in features:
		#Pixelate via rescale
		featureImg = feature.crop().scale(1/scaleFactor).scale(scaleFactor**2)
		x,y = feature.topLeftCorner()
		imgOut = imgOut.blit(featureImg, pos=(int(x*scaleFactor),int(y*scaleFactor)))
	return(len(features), imgOut)

def drawCRFHeader(img, headerText):
	img.dl().selectFont("ethnocentric")
	img.drawText(text=headerText, x=16, y=8, fontsize=60, color=(0, 0, 0))
	img.drawText(text=headerText, x=8, y=12, fontsize=60, color=(255, 200, 46))

def drawMovement(img, blobs):
	for blob in blobs:
		img.draw(blob, width=5, color=(255,0,0))

def upload(files, config):
	for server in config['uploadPaths']:
		try:
			cnopts = pysftp.CnOpts()
			cnopts.hostkeys = None
			conn = pysftp.Connection(host=server['hostname'], username=server['username'], private_key=server['identify'], cnopts=cnopts)
			conn.cwd(server['uploadPath'])
			for filee in files:
				conn.put(filee)
		except Exception as e:
			print "Exception ({0}): {1}".format(e.errno, e.strerror)
			pass
		conn.close()

