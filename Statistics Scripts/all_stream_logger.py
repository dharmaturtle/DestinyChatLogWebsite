# This logs data from the top 100 live streams on Twitch every 3 minutes

import urllib2, json, time, datetime
from pymongo import MongoClient
mongolog = MongoClient('mongodb://localhost:27017/')['testDB2']['logapp_log_streams']

# Rounds to nearest 10 seconds, based on http://stackoverflow.com/a/10854034/625919
def round_time():
	roundTo = 10
	dt = datetime.datetime.now()
	seconds = (dt - dt.min).seconds
	rounding = (seconds+roundTo/2) // roundTo * roundTo
	return dt + datetime.timedelta(0,rounding-seconds,-dt.microsecond)

while True:
	file = urllib2.urlopen('https://api.twitch.tv/kraken/streams?limit=100&offset=0')
	jdata = json.loads(file.read())['streams']
	file.close()
	
	# creates a list of stream-dictionaries
	streams = []
	for x in jdata:
		streamer = {}
		streamer['name']    = x['channel']['display_name']
		streamer['viewers'] = x['viewers']
		streamer['game']    = x['game']
		streamer['status']  = x['channel']['status']
		streams.append(streamer)
	
	# create final dictionary
	final = {}
	final['time'] = round_time()
	final['streams'] = streams
	
	mongolog.insert(final)
	print "Streams logged at: " + str(datetime.datetime.now())
	time.sleep( 180 )