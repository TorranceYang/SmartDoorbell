import json

class JSON_Parser:
	@staticmethod
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
	
	@staticmethod
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