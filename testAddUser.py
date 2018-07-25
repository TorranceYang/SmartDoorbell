from Whitelist import Whitelist

whitelist = Whitelist.GetWhitelist()
username = "AlexKent"

#prompt user to put face in camera view
counter = 0
while (counter < 20):
    #wait for any key press
    raw_input('Press any key to take a picture ({0} pictures remain)'.format(20 - counter))
    #take picture
    #increment counter
    counter += 1
Whitelist.addNewUser(username, whitelist)
