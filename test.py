from twilio.rest import Client

account_sid = 'AC93e7bbc2852f37e60a5dadaa85b48f75'
auth_token = '41949b0e6ef825cc9500f47f16eda0e0'

setThreshold = 99

def main():
        userinfo = {"name": "torrance", "threshold": 100}
        whitelist = ["torrance"]
        handleUserApproval(userinfo, whitelist, "Profile.jpg");
        
def handleUserApproval(userinfo, whitelist, savedFilePath):
    	global setThreshold

        client = Client(account_sid, auth_token)
        mesasge = ""
        
    	if userinfo != None:
        	if userinfo["name"] in whitelist and userinfo["threshold"] >= setThreshold:
            		print "Door unlocked"
                        message = '{0} is at the door!'.format(userinfo["name"])
                else:
            		print "Sending alert to user about unknown user"
                        message = 'There was an unkown face at the door'

        client.messages \
              .create(
                      body = message,
                      from_ = '+14259797389',
                      to = '+19106168328',
                      media_url = 'http://e8549234.ngrok.io/uploads/{}'.format(savedFilePath))

#TODO
#Whitelist logic
#Take the top probability response (should be the first entry in the json -> Check if it's above a given threshold (0 for now)
#If it's above that threshold, check the whitelist and see if they are whitelisted
#If they are, let them in (just print something out for now)
#If they are not, don't let them in and print something out still

main()
