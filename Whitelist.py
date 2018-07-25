import json
import time
import datetime

class Whitelist:
    filename = "whitelist.json"

    @classmethod	
    def GetWhitelist(self):
        with open(self.filename) as json_data:
            d = json.load(json_data)
            return d

    @classmethod	
    def isUserWithinTimeFrame(self, name, whitelist):
		epoch = int(time.time())
		currentDay = time.strftime('%A', time.localtime(epoch))
		currentHour = datetime.datetime.now().hour

		#No time set, therefore acts as always allowed
		if name in whitelist and "Time" not in whitelist[name]:
			return True

		if name in whitelist and currentDay in whitelist[name]["Time"]:
			for timespan in whitelist[name]["Time"][currentDay]:
				if currentHour > timespan[0] and currentHour <= timespan[1]:
					return True
		return False

    @classmethod	
    def isUserAllowed(self, names, whitelist):
		for name in names:
			timeframe = self.isUserWithinTimeFrame(name, whitelist)
			if name in whitelist and timeframe:
				return True
			else:
				return False

    @classmethod	
    def addNewUser(self, name, whitelist):
		if name in whitelist:
			print "Name already exists. Please enter another name"
			return
		whitelist[name] = {}
		print "You have added " + name + " to the whitelist"
		self.saveWhitelist(whitelist)

    @classmethod	
    def saveWhitelist(self, whitelist):
        with open(self.filename, 'w') as json_file:
            json.dump(whitelist, json_file)
