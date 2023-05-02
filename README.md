[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/powered-by-electricity.svg)](https://forthebadge.com)

# Awesome-Lime-Scooter-Notifier
Gets list of closest lime scooters to your location, Notifies you if one is close, with other features.

First, run the setup script. You must have a Lime Account in order to do this.
```g++ setup.cpp; ./a.out;```

After you have correctly entered your information, a file titled "LimeUser.txt" will appear in the directory.

Once the file's been generated, you're good to go.
Before you run the program, make sure to set ```currLocation``` on line ```12``` of ```getNearestScooter.py``` to the location where you'd like to look for scooters. And you need to enter the location via latitude and longitude— here is a link that
converts an address to GPS coordinates: [gps-coordinates.net](https://www.gps-coordinates.net/)

```python3 getNearestScooter.py```

There are a few variables that you can tweak to modify the behavior of the program.
Perhaps the most important one is on line ```14```, ```outputAllScooters = False```. Changing the value to ```True``` will only return the list of scooters within ```radius```.
Set ```radius``` to a high value if you'd like to see as many locations as possible.

Since the respository is called "Awesome-Lime-Scooter-Notifier", you're probably wondering what the awesome part is.
getNearestScooter.py, when ```outputAllScooters``` is set to false, will constantly query the Lime API, seeking new scooters.
Taking into account the curvature of the earth, the program detects the distance between two coordinates (your location compared to  the nearest scooter) to determine  
if it's within ```radius```. If it is, then the program will play a ding sound. 

Why is the ding sound important? Say you know you're about to leave for somewhere in an hour, and you'd really like to take a lime scooter. Nobody wants to be constantly checking their phone or walk a long distance to get to a scooter. If you are notified of the presence of a scooter within your ```range```(300m is a good threshold) then you can save a lot of time and effort by using that scooter. Ultimately, the mode where ```outputAllScooters = False``` is quite practical. Thanks for reading this, and please leave a star!
