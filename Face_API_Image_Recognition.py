from JSON_Parser import JSON_Parser
import cv2
import requests
import json

class Face_API_Image_Recognition:
	subscriptionKey = 'ad4f221bdc5d4f9cbda2b41a62c66f1e'	
	faceAPIDetectFace = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'	
	faceAPIIdentifyFace = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/identify'	
	faceAPIIdentifyPerson = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/persongroups/14ac938c-bb57-40ea-9c68-1665c33da400/persons'

	def DetectFace(cls, img):
	
		content_type = 'application/octet-stream'
		params = {
			'returnFaceId': 'true',
			'returnFaceLandmarks': 'false',
			'returnFaceAttributes': ''
		}
		headers = {'content-type': content_type, 'Ocp-Apim-Subscription-Key': cls.subscription_key}
	
		img_encoded = cv2.imencode('.jpg', img)[1].tostring()

		response = requests.post(faceAPIDetectFace, params=params, headers=headers, data=img_encoded)
		returnedFaces = parseFaceAPIJson(response.text)

		if len(returnedFaces) > 0:
			print 'Face Detected'
			cls.IdentifyFace(returnedFaces[0])
		else:
			print 'No Face Detected'
		
	
	def IdentifyFace(cls, faceId):
		
		content_type = 'application/json'
		headers = {'content-type': content_type2, 'Ocp-Apim-Subscription-Key': cls.subscription_key}
		params = '{{"personGroupId": "14ac938c-bb57-40ea-9c68-1665c33da400", "faceIds":["{0}"], "maxNumOfCandidatesReturned": 1, "confidenceThreshold":0.5}}'.format(faceId)
		response = requests.post(faceAPIIdentifyFace, headers=headers, data=params)
		responseJson = json.loads(response.text)

		personId = 0
		

		cls.IdentifyPerson(personId)

	def IdentifyFaces(cls, faceIds):
		pass

	def IdentifyPerson(cls, personId):
		headers = {'Ocp-Apim-Subscription-Key': cls.subscription_key}
		response = requests.get('{0}/{1}'.format(faceAPIIdentifyPerson, personId), headers=headers)
		responseJson = json.loads(response.text)

		if 'name' in responseJson:
			print 'Name found: {0}'.format(responseJson['name'])
		else:
			print 'Name not found'

	def IdentifyPersons(cls, personIds):
		pass



