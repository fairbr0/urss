#script to get user locations based on self reported location

import pymongo
from pymongo import MongoClient
import json
import re
from string import punctuation

england = [
    (-5.812, 49.937, 1.527, 51.337),
    (-3.013, 51.337, 1.527, 51.504),
    (-2.686, 51.504, 1.785, 52.706),
    (-3.181, 52.706, 1.780, 54.005),
    (-3.680, 54.005, -0.022, 55.031),
    (-3.340, 55.037, -1.406, 55.826)
]

class TweetLocationIdentifier():

    client = MongoClient()
    db = client.towns_db
    punc = list(punctuation)
    punc.remove('-')
    punc.remove('\'')

    def checkTweetLocation(self, tweet):
        if tweet['lang'] != 'en':
            return None
        locU = self.getTweetLocationByUserLocal(tweet['user'])
        if locU:
            return locU
        locP = self.getTweetLocationByPlace(tweet['place'])
        if locP:
            return locP

        locC = self.getTweetLocationByGeo(tweet['coordinates'])
        if locC:
            return locC
        return None

    def checkDb(self, parts):
        query = ' '.join(c for c in parts).lower()

        obj = self.db.towns.find_one({'town':query})
        if obj:
            return obj
        obj = self.db.counties.find_one({'county':query})
        if obj:
            return obj
        return None

    def removePunc(self, location):
        chars = list(location)
        out = []
        for char in chars:
            if char in self.punc:
                out.append(" ")
            else:
                out.append(char)
        out = "".join(c for c in out)
        return out

    def getTweetLocationByUserLocal(self, user):
        #method checks against mongodb for location
        if user['location'] == None:
            return None
        location = user['location']
        loc = self.removePunc(location)
        parts = loc.split()
        if len(parts) <= 0:
            return None
        for i in range(0, len(parts) + 1):
            for j in range(len(parts) + 1 ):
                sub = parts[i:j]
                if len(sub) != 0:
                    res = self.checkDb(sub)
                    if res:
                        return res
        return None

    def getTweetLocationByGeo(self, coordinates):
        #method checks against UK bounding box
        if coordinates == None:
            return None

        coordinates = coordinates['coordinates']
        for area in england:
            if coordinates[0] > area[0] and coordinates[0] < area[2] and coordinates[1] > area[1] and coordinates[1] < area [3]:
                return coordinates
        return None

    def getTweetLocationByPlace(self,place):
        if place == None:
            return None
        if place['country'] == 'United Kingdom':
            res = self.db.towns.find_one({'town':place['name'].lower()})
            if res:
                return res
        return None

#locaIdentifier = TweetLocationIdentifier()

t2 = {u'user': {
    'location':'manchester/leeds'
}}

tweet = {u'contributors': None, u'truncated': False, u'text': u'Arthritis now &gt; apocalypse now #makeAmovieUnwell', u'is_quote_status': False, u'in_reply_to_status_id': None, u'id': 889180731590795268, u'favorite_count': 0, u'source': u'<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', u'retweeted': False, u'coordinates': None,
u'timestamp_ms': u'1500832181247', u'entities': {u'user_mentions': [], u'symbols': [], u'hashtags': [{u'indices': [34, 51], u'text': u'makeAmovieUnwell'}], u'urls': []}, u'in_reply_to_screen_name': None, u'id_str': u'889180731590795268',
u'retweet_count': 0, u'in_reply_to_user_id': None, u'favorited': False, u'user': {u'follow_request_sent': None, u'profile_use_background_image': True, u'default_profile_image': False, u'id': 787016459386052612, u'verified': False, u'profile_image_url_https': u'https://pbs.twimg.com/profile_images/884043707749629953/L1Yatsuc_normal.jpg', u'profile_sidebar_fill_color': u'DDEEF6', u'profile_text_color': u'333333', u'followers_count': 34, u'profile_sidebar_border_color': u'C0DEED', u'id_str': u'787016459386052612', u'profile_background_color': u'F5F8FA', u'listed_count': 1, u'profile_background_image_url_https': u'', u'utc_offset': None, u'statuses_count': 125, u'description': None, u'friends_count': 53, u'location': u'Liverpool, England', u'profile_link_color': u'1DA1F2', u'profile_image_url': u'http://pbs.twimg.com/profile_images/884043707749629953/L1Yatsuc_normal.jpg', u'following': None, u'geo_enabled': True, u'profile_banner_url': u'https://pbs.twimg.com/profile_banners/787016459386052612/1498669508', u'profile_background_image_url': u'', u'name': u'Rocco Richards', u'lang': u'en-gb', u'profile_background_tile': False, u'favourites_count': 195, u'screen_name': u'Roccojrichards', u'notifications': None, u'url': u'http://www.pitchero.com/clubs/propugnatoreathleticfootballclub/', u'created_at': u'Fri Oct 14 19:45:20 +0000 2016', u'contributors_enabled': False, u'time_zone': None, u'protected': False, u'default_profile': True, u'is_translator': False}, u'geo': None, u'in_reply_to_user_id_str': None, u'lang': u'en', u'created_at': u'Sun Jul 23 17:49:41 +0000 2017', u'filter_level': u'low', u'in_reply_to_status_id_str': None, u'place': {u'full_name': u'Liverpool, England', u'url': u'https://api.twitter.com/1.1/geo/id/151b9e91272233d1.json', u'country': u'United Kingdom', u'place_type': u'city', u'bounding_box': {u'type': u'Polygon', u'coordinates': [[[-3.008791, 53.36489], [-3.008791, 53.474867], [-2.822063, 53.474867], [-2.822063, 53.36489]]]}, u'country_code': u'GB', u'attributes': {}, u'id': u'151b9e91272233d1', u'name': u'Liverpool'}}

#locaIdentifier.checkTweetLocation(tweet)
