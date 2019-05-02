import requests
import math
import time
import os
#import matplotlib.pyplot as plt
import numpy as np
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" #hide pygame hello message
from pygame import mixer
from vincenty import vincenty
#################################################################
radius = 400 #only show the scooters within [radius] distance of you (meters)
currLocation = (37.8644,-122.2649) #your location in latitude, longitude
zoom = 12 #higher number => more scooters loaded
outputAllScooters = False #if True outputs all found scooters within [radius], then exits
#if False, program will update every [refreshRate] seconds, outputting, first: the nearest scooter.
#Then, if the found scooter(s) is/are within the radius, the program plays a sound and outputs the scooter(s)
refreshRate = 60 #Seconds before we request more scooter data
#################################################################
neBound = (currLocation[0] + 0.001012 ,currLocation[1] + 0.001704)
swBound = (currLocation[0] - 0.001309,currLocation[1]-0.002239)
def distance(p0, p1):
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)
with open('LimeUser.txt', 'r') as file:
    f = file.read()
token = f[f.find("token") + len("token\":\""): f.find("\",\"user")  ] #extract token from LimeUser.txt
webSession = f[f.find("_limebike-web_session")+23:-1] #extract webSession from LimeUser.txt
cookies = {
    '_limebike-web_session': webSession,
}
headers = {
    'authorization': 'Bearer ' + token,
}
while True:
    response = requests.get('https://web-production.lime.bike/api/rider/v1/views/map?ne_lat=' + str(neBound[0]) + '&ne_lng=' + str(neBound[1]) + '&sw_lat='+ str(swBound[0]) + '&sw_lng='+ str(swBound[1]) + '&user_latitude=' + str(currLocation[0]) + '&user_longitude='+ str(currLocation[1]) + '&zoom=' +str(zoom), headers=headers, cookies=cookies)
    try:
        scooters = response.json()['data']['attributes']['bikes']
    except ValueError:
        print('http request failure: please run the setup script.')
        exit()
    locations = []
    batteryLevels = []
    ids = []
    printedScooters = 0
    for scooter in scooters:
        if outputAllScooters:
            if vincenty((scooter["attributes"]["latitude"], scooter["attributes"]["longitude"]),currLocation)*1000 <= radius:
                print((scooter["attributes"]["latitude"], scooter["attributes"]["longitude"]),"ID: ",scooter['attributes']["last_three"] ,"battery level: ", scooter["attributes"]["battery_level"])
                printedScooters += 1
        if scooter["attributes"]["type_name"] != "manual": #I only want electric ones
            batteryLevels.append(scooter["attributes"]["battery_level"])
            locations.append((scooter["attributes"]["latitude"], scooter["attributes"]["longitude"])) #show me where it is
            ids.append(scooter['attributes']["last_three"])
    if outputAllScooters and printedScooters == 0:
        print("No scooters found. Try increasing your radius?")
    if outputAllScooters:
        '''for location in locations: #Graph scooter locations on a scatterplot. uncomment line 5 as well for this
            plt.scatter(location[0],location[1])
        plt.scatter(currLocation[0],currLocation[1],color="black",label="you are here")
        plt.show()'''
        exit()
    smallestDistance = 100000
    index = 0
    for i in range(0,len(locations)):
        d = vincenty(currLocation,locations[i])*1000
        if smallestDistance > d:
            smallestDistance = d
            index = i
    print(locations[index],"is the closest scooter to the location.",vincenty(locations[index],currLocation)*1000,"meters away. ID: " ,ids[index])
    closeScooters = 0
    for i in range(0,len(locations)):
        distance = vincenty(currLocation,locations[i])*1000
        if distance <= radius: #If it's within my specified radius
            #notify me that there is one
            mixer.init()
            mixer.music.load('alert.mp3')
            mixer.music.play()
            #os.system("say scuter " + str(int(distance)) + " meters away")
            print("Close scooter at", locations[i],"battery level " + batteryLevels[i])
            closeScooters += 1
    if closeScooters == 0:
        print("no scooters within the radius.")
    time.sleep(refreshRate) # check every minute
