from picamera.array import PiRGBArray
from picamera import PiCamera
from datetime import datetime
import time
import imutils
import cv2
import requests
import json

# define the path to the face detector
FACE_DETECTOR_PATH = "./haarcascade_frontalface_default.xml"

fileLocation = 'images/testing/'

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

timeBetweenCalls = 5
lastCallTime = datetime.now()
setThreshold = 0

def main():
	time.sleep(0.1)

	avg = None
	detector = cv2.CascadeClassifier(FACE_DETECTOR_PATH)

	for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

		image = frame.array
		predictionImage = image.copy()

		text = "No Face Detected"

		imutils.resize(image, width=500)
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

		rects = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

		for (x, y, w, h) in rects:
			cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
			text = "Face detected"
			print 'x: {0}, y: {1}'.format(x, y)
			if x > 100 and y > 100:
				userinfo = faceDetected(predictionImage)
                                whitelist = getWhitelist("test.txt")
                                isUserApproved(userinfo, whitelist)
			else:
				print 'Face is not close enough!'

		cv2.putText(image, "Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
#		cv2.putText(image, datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

		cv2.imshow("Doorbell Feed", image)
	#	cv2.imshow("Grayscale Image", gray)
	
		key = cv2.waitKey(1) & 0xFF
		if key == ord("q"):
			break

		rawCapture.truncate(0)


	cv2.destroyAllWindows()

def saveImage(img):
	print('Saving image')
	outfile = '{0}_{1}.jpg'.format(fileLocation, datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))
	cv2.imwrite(outfile, img)
	print('Image saved')

def faceDetected(img):
	global lastCallTime
	print "Face Detected!"
	currentTime = datetime.now()
	timeDelta = currentTime - lastCallTime
	if timeDelta.seconds > 5:
		print 'CALLING ENDPOINT'
		userinfo = callEndpoint(img)
		lastCallTime = currentTime
                return userinfo

def callEndpoint(img):
	#addr = 'http://smartdoorbell.azurewebsites.net'
	#test_url = addr + '/api/HttpTriggerCSharp1?code=PRLRPIVFL5yswaXPv7uO62oVH/rEGmDFPEPJ9lgGymWxPyAu2QUTSg=='
	#test_url = 'https://southcentralus.api.cognitive.microsoft.com/customvision/v2.0/Prediction/50373955-41d0-4ee0-87f2-b9c381552603/image?iterationId=298f99c2-c74b-450d-b775-88de52bf5050'
	test_url = 'https://southcentralus.api.cognitive.microsoft.com/customvision/v2.0/Prediction/50373955-41d0-4ee0-87f2-b9c381552603/image?'

	#content_type = 'image/jpeg'
	content_type = 'application/octet-stream'
	prediction_key = '5f42222ba70e4b80911f93788355e5e7'	
	
	headers = {'content-type': content_type, 'Prediction-Key': prediction_key}
	#headers = {'content-type': content_type}
	
	img_encoded = cv2.imencode('.jpg', img)[1].tostring()

	#response = requests.post(test_url, data=img_encoded, headers=headers)
	response = requests.post(test_url, data=img_encoded, headers=headers)
	
	return parseJson(response.text)


def parseJson(json_):
	parsed = json.loads(json_)
	predictions = parsed['predictions']
	print '---------------------------------------------------'
	for person in predictions:
		personResult = '{0}: {1}'.format(person['tagName'], person['probability'])
		print personResult
		print '---------------------------------------------------'
	print '\n'
        print predictions[0]['tagName']
        
        userinfo = {"name": predictions[0]['tagName'], "threshold": predictions[0]['probability']}
        return userinfo

def getWhitelist(filename):
    	wlArray = []
    	f = open(filename, "r")
    	for info in f:
        	info = info.rstrip()
        	wlArray.append(info)
    	return wlArray

def isUserApproved(userinfo, whitelist):
    	global setThreshold
    	if userinfo != None:
        	if userinfo["name"] in whitelist and userinfo["threshold"] >= setThreshold:
            		print "Door unlocked"
        	else:
            		print "Send alert to user about unknown user"
        

#TODO
#Whitelist logic
#Take the top probability response (should be the first entry in the json -> Check if it's above a given threshold (0 for now)
#If it's above that threshold, check the whitelist and see if they are whitelisted
#If they are, let them in (just print something out for now)
#If they are not, don't let them in and print something out still

main()
