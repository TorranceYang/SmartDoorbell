from picamera.array import PiRGBArray
from picamera import PiCamera
from datetime import datetime
from twilio.rest import Client
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

account_sid = 'AC93e7bbc2852f37e60a5dadaa85b48f7'
auth_token = '41949b0e6ef825cc9500f47f16eda0e0'

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
                                savedFilePath = saveImage(predictionImage);
                                handleUserApproval(userinfo, whitelist, savedFilePath)         
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
        return outfile

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

#
def callEndpoint(img):
	#URLs for Custom Vision
	#test_url = 'https://southcentralus.api.cognitive.microsoft.com/customvision/v2.0/Prediction/50373955-41d0-4ee0-87f2-b9c381552603/image?iterationId=298f99c2-c74b-450d-b775-88de52bf5050'
	#test_url = 'https://southcentralus.api.cognitive.microsoft.com/customvision/v2.0/Prediction/50373955-41d0-4ee0-87f2-b9c381552603/image?'

	#URL for Face API
	test_url = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'	
	test_url2 = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/identify'	
	

	#Used for Custom Vision
	content_type = 'application/octet-stream'
	content_type2 = 'application/json'
	#prediction_key = '5f42222ba70e4b80911f93788355e5e7'	

	#Used for Face API
	subscription_key = 'ad4f221bdc5d4f9cbda2b41a62c66f1e'	
	params = {
		'returnFaceId': 'true',
		'returnFaceLandmarks': 'false',
		'returnFaceAttributes': ''
	}

	#Header for Custom Vision
	#headers = {'content-type': content_type, 'Prediction-Key': prediction_key}
	
	#Header for Face API
	headers = {'content-type': content_type, 'Ocp-Apim-Subscription-Key': subscription_key}
	headers2 = {'content-type': content_type2, 'Ocp-Apim-Subscription-Key': subscription_key}
	headers3 = {'Ocp-Apim-Subscription-Key': subscription_key}
	
	img_encoded = cv2.imencode('.jpg', img)[1].tostring()

	#response = requests.post(test_url, data=img_encoded, headers=headers)
	response = requests.post(test_url, params=params, headers=headers, data=img_encoded)
	
	#return parseCustomVisionJson(response.text)
	print 'PRAYING'
	returnedFaces = parseFaceAPIJson(response.text)

	params2 = '{{"personGroupId": "14ac938c-bb57-40ea-9c68-1665c33da400", "faceIds":["{0}"], "maxNumOfCandidatesReturned": 1, "confidenceThreshold":0.5}}'.format(returnedFaces[0])

	#Identify Faces
	response2 = requests.post(test_url2, headers=headers2, data=params2)
	print 'PRAYING HARDER'
	response2Json = json.loads(response2.text)
	print response2Json
	print response2Json[0]['candidates']
	print response2Json[0]['candidates'][0]['personId']

	personId = response2Json[0]['candidates'][0]['personId']

	test_url3 = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/persongroups/14ac938c-bb57-40ea-9c68-1665c33da400/persons/{0}'.format(personId)	
	response3 = requests.get(test_url3, headers=headers2)
	response3Json = json.loads(response3.text)

	print response3Json['name']

	return parseFaceAPIJson(response.text)


def parseFaceAPIJson(json_):
	parsed = json.loads(json_)

	returnedFaces = []

	print '---------------------------------------------------'
	for person in parsed:
		personResult = person['faceId']
		returnedFaces.append(personResult)
		print personResult
		print '---------------------------------------------------'
	print '\n'

	return returnedFaces

def parseCustomVisionJson(json_):
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

def handleUserApproval(userinfo, whitelist, savedFilePath):
    	global setThreshold

        client = Client(account_sid, auth_token)
        mesasge = ""
        
    	if userinfo != None:
        	if userinfo["name"] in whitelist and userinfo["threshold"] >= setThreshold:
            		print "Door unlocked"
                        message = '{0} is at the door!'.format(userInfo["name"])
                else:
            		print "Sending alert to user about unknown user"
                        message = 'There was an unkown face at the door'

        client.messages \
              .create(
                      body = message,
                      from_ = '+14259797389',
                      to = '+19106168328',
                      #THIS URL WILL NEED TO BE CHANGED BASED ON THE NGROK SERVER
                      media_url = 'http://2a2c9c14.ngrok.io/uploads/{}'.format(savedFilePath))

#TODO
#Whitelist logic
#Take the top probability response (should be the first entry in the json -> Check if it's above a given threshold (0 for now)
#If it's above that threshold, check the whitelist and see if they are whitelisted
#If they are, let them in (just print something out for now)
#If they are not, don't let them in and print something out still

main()
