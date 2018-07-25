from picamera.array import PiRGBArray
from picamera import PiCamera
from datetime import datetime
from Face_API_Image_Recognition import Face_API_Image_Recognition
from Image_Processing import Image_Processing
from face_identifier import FaceIdentifier
from Whitelist import Whitelist
import time
import imutils
import cv2
import requests
import json

# define the path to the face detector
FACE_DETECTOR_PATH = "./haarcascade_frontalface_default.xml"

fileLocation = 'images/testing/'
#Camera init
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

def main():
	#Let the camera warm up
	time.sleep(0.1)

        #Instantiate openCV face recognition
        faceIdentifier = FaceIdentifier('./encodings.pickle')

        #Load the whitelist
        whiteList = Whitelist.GetWhitelist()
        
	avg = None
	detector = cv2.CascadeClassifier(FACE_DETECTOR_PATH)

	#Continually capture images with the camera
	for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
		#Get the current frame as a 'still' image
		image = frame.array
		
		text = "No Face Detected"

		#Resize the image for added performance
		imutils.resize(image, width=500)
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

		#Get a copy of the current frame to send to the ML Model without transformations
		predictionImage = image.copy()
                
		rects = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

		#TODO:
		#Call the openCV face recognition method that takes in a 'bgr' image and rects as input
		#So each frame, see if rects is empty, if it's not, call the method
		if len(rects) > 0:
			#Call openCV face recognition method
			names = faceIdentifier.IdentifyFaces(image, rects)
			openDoor = Whitelist.isUserAllowed(names, whiteList)
			if openDoor:
				break

			#ADD
			#Call to method to unlock the door
			print names

		for (x, y, w, h) in rects:
			cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
			#If the face is too small -> Person is too far away -> Don't process the image
			if w < 100:
				print 'Face is too small, please get closer!'
        
		cv2.putText(image, "Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

		cv2.imshow("Doorbell Feed", image)
	
		key = cv2.waitKey(1) & 0xFF
		if key == ord("q"):
			break
                if key == ord("i"):
			Image_Processing.SaveImage(predictionImage, fileLocation)

		#Clear the current image so a new one can be recorded
		rawCapture.truncate(0)

	cv2.destroyAllWindows()

def openWhiteListOptions():
	global whitelist
	print "commands:"
	print "view"
	print "add <name>"
	print "remove <name>"
	print "exit"
	#loop
	while (True):
		#wait for command
		command = raw_input("Enter command: ")
		#split command and parameter
		cmdarray = command.split()
		#view current users
		if (cmdarray[0] == "view"):
			userArray = getUsers()
			print userArray
		#add user
		if (cmdarray[0] == "add"):
			addUser(cmdarray[1])
		#remove user
		if (cmdarray[0] == "remove"):
			removeUser(cmdarray[1])
		#exit options
		if (cmdarray[0] == "exit"):
			break

def getUsers():
	userList = whitelist.keys()
	return userList

def addUser(userName):
	#prompt user to put face in camera view
	counter = 0
	while (counter < 20):
		#wait for any key press
		raw_input('Press any key to take a picture ('+ 20-counter +' pictures remain)')
		#take picture
		#increment counter
		counter += 1
	Whitelist.addNewUser(username, whitelist)

def removeUser(userName):
	Whitelist.removeUser(username, whitelist)

main()
