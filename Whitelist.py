import json
import time
import datetime

class Whitelist:
    filename = "whitelist.json"

    @classmethod	
    def GetWhitelist():
        global filename
        with open(filename) as json_data:
            d = json.load(json_data)
            return d

    @classmethod	
    def isUserExpired(name, whitelist):
        if name in whitelist:
            currentTime = int(time.time())
            expiry = whitelist[name]["Expiry"]

            #get time difference and convert to minutes
            timeDiff = (currentTime - whitelist[name]["TimeRegistered"]) / 60
            if timeDiff > expiry:
                return True
        return False

    @classmethod	
    def isUserWithinTimeFrame(name, whitelist):
        epoch = int(time.time())
        currentDay = time.strftime('%A', time.localtime(epoch))
        currentHour= datetime.datetime.now().hour  

        if name in whitelist and currentDay in whitelist[name]["Time"]:
            for timespan in whitelist[name]["Time"][currentDay]:
                if currentHour > timespan[0] and currentHour <= timespan[1]:
                    return True
        return False

    @classmethod	
    def isUserAllowed(name, whitelist):
        if user in whitelist:
            return True
        else:
            return False

    @classmethod	
    def addNewUser(name, whitelist):
        if name in whitelist:
                print "Name already exists. Please enter another name"
                return
        whitelist[name] = {}
        print "You have added " + name + " to the whitelist"
        saveWhitelist(whitelist)

    @classmethod	
    def saveWhitelist(whitelist):
        global filename
        with open(filename, 'w') as json_file:
            json.dump(whitelist, json_file)
