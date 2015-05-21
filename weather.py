#!python

# from urllib.request import urlopen

import urllib2

import json

url="http://api.wunderground.com/api/e6a1c41fc03c0ca9/forecast/q/Belgium/Leuven.json"

#response = urlopen(url)
response = urllib2.urlopen(url)   
weather = json.load(response)
detail = weather['forecast']['simpleforecast']['forecastday']

forecast = []

for day in detail:
	weatherdate = day['date']['weekday']
	weatherhigh = day['high']['celsius'] + u'\xb0' + "C"
	weatherlow = day['low']['celsius'] + u'\xb0' + "C"
	weatherpop = str(day['pop']) + "%"
	
	forecast.append(weatherpop)
	# print(weatherdate)
	# print("\tHigh:\t\t%s" % weatherhigh)
	# print("\tLow:\t\t%s" % weatherlow)
	# print("\tChance of rain:\t%s" % weatherpop)
	# print("-----------------------------")

#chance of rain for today
print(forecast[0])
