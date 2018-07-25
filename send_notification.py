from Image_Processing import Image_Processing

account_sid = 'AC93e7bbc2852f37e60a5dadaa85b48f7'
auth_token = '41949b0e6ef825cc9500f47f16eda0e0'

client = Client(account_sid, auth_token)

class Notifications:

    @classmethod
    def SendRecognized(self, names, filePath):
        introString = BuildNames(name) + "at the door!"

        self.SendNotification(message, filePath)

    @classmethod
    def SendUnrecognized(self, filePath):
        SendNotification("There is an unrecognized face at the door!")

    @classmethod
    def SendNotification(self, message, filePath):
         client.messages \
              .create(
                      body = message,
                      from_ = '+14259797389',
                      to = '+19106168328',
                      media_url = 'http://d7a77f38.ngrok.io/uploads/{}'.format(filePath))

    @classmethod
    def BuildNames(self, names):
        result = ""

        if len(names == 1):
            result = "{0} is ".format(names[0])
        elif len(names == 2):
            result = "{0} and {1} are ".format(names[0], names[1])
        else:
            for i, name in enumerate(names):
                if(i == length(names) - 1):
                    result += "and {0} are ".format(names[i])
                else:
                    result += result + "{0}, ".format(names[i])

        return result
