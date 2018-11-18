# Eli Bolotin
# Nov 4 2018
# DS710: Final Project

import tweepy
import csv
import jsonpickle
from twitter_credentials import *

# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)
 
# api = tweepy.API(auth)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
 
max_tweets = 20
query = "%23vote OR %23midterms OR %23RockTheVote OR %23democrat OR %23republican"

with open('tweets2.json', 'w') as f:
	for tweet in tweepy.Cursor(api.search,q=query).items(max_tweets):         
		f.write(jsonpickle.encode(tweet._json, unpicklable=False) + '\n')