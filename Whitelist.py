import json
import time
import datetime

class Whitelist:

    @classmethod	
    def GetWhitelist():
        with open("whitelist.json") as json_data:
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
    def isUserAllowed(name, probability, whitelist):
        thresholdAllowed = 50
        if user in whitelist and probability >= thresholdAllowed:
            return True
        else:
            return False
