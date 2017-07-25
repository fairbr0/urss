import tweepy
import pymongo
import json
from pymongo import MongoClient
from tweepy import OAuthHandler
from place_getter import TweetLocationIdentifier

##############Twitter Setup###############
consumer_key='6I2KaONMkwXF9qxn0MaVM3Rmn'
consumer_secret='oz0tecv1khaM4qHRIBfh4YH6ADCWVDO5pFYgtwXJBDZ6MfgnIv'
access_token_key='1109431981-7e1SGl7ohk4XqsoY1znIndsNMxeGdnalm6oUF0n'
access_token_secret='2SPoj0huCDQ53KRouYHLZ5tL1d4D3ByOOMwYQuFSdjP4T'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)

api = tweepy.API(auth)

##############Mongo Setup################

client = MongoClient()
db = client.tweet_database
locationIdentifier = TweetLocationIdentifier()

class TweetStreamListener(tweepy.StreamListener):

    total_streamed = 0
    total_accepted = 0    

    def on_status(self, status):
        if self.total_streamed % 1000 == 0:
            with open('stats.txt', 'a') as f:
		f.write('Total Streamed: ' + str(self.total_streamed) + ' Total Accepted: ' + str(self.total_accepted) + '\n')
		
        loc = locationIdentifier.checkTweetLocation(status._json)
        self.total_streamed += 1
        if loc:
            self.total_accepted += 1
	    '''
            print '*************'
            print status.text
            print loc
            '''
	    db.tweets.insert_one(status._json)

streamListener = TweetStreamListener()

food = ['dinner', 'lunch', 'tea', 'brunch', 'breakfast', 'snack', 'meal', 'supper']
smoking = ['cig', 'cigarette', 'vape', 'vaping', 'e-cig', 'ecig', 'tobacco', 'nicotine']
fitness = ['gym', 'workout', 'fitness', 'gains', 'exercise','run', 'running', 'swim', 'swimming', 'jog', 'jogging', 'cycle', 'cycling', 'bike', 'biking', 'hike']

track = food + smoking + fitness
while True:
    try:
	stream = tweepy.Stream(auth = api.auth, listener=streamListener)
        stream.filter(track=track)
    except KeyboardInterrupt:
	stream.disconnect()
	break
    except:
	continue
