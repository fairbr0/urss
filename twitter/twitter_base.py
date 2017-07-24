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
db = client.food_database
locationIdentifier = TweetLocationIdentifier()

class TweetStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        loc = locationIdentifier.checkTweetLocation(status._json)
        if loc:
            print '*************'
            print status.text
            print loc
            db.tweets.insert_one(status._json)

streamListener = TweetStreamListener()
stream = tweepy.Stream(auth = api.auth, listener=streamListener)

food = ['dinner', 'lunch', 'tea', 'brunch', 'breakfast', 'snack', 'meal', 'supper']
smoking = ['cig', 'cigarette', 'vape', 'vaping', 'e-cig', 'ecig', 'tobacco', 'nicotine']
fitness = ['gym', 'workout', 'fitness', 'gains']

track = food + smoking + fitness
stream.filter(track=track)
