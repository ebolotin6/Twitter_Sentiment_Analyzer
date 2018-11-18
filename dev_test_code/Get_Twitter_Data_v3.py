# Eli Bolotin
# Nov 4 2018
# DS710: Final Project

import tweepy
import json
from twitter_credentials import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

def get_past_tweets(query, max_tweets):
	query = ' OR '.join(query)
	# query.replace("#","%23")
	tweets = []
	with open('past_tweets.json', 'a') as file:
		for tweet in tweepy.Cursor(api.search, q=query, rpp=100, lang="en").items(max_tweets):
			tweets.append(tweet._json)
			if len(tweets) % 100 == 0:
				file.seek(0)
				file.truncate()
				file.write(json.dumps(tweets))

def tweets_of_followers(followers_ids, max_tweets):
	tweets = []
	with open('past_tweets.json', 'a') as file:
		for tweet in tweepy.Cursor(api.statuses_lookup, screen_name=followers_id, include_entities=True).items(max_tweets):
			tweets.append(tweet._json)
			if len(tweets) % 100 == 0:
				file.seek(0)
				file.truncate()
				file.write(json.dumps(tweets))

class MyStreamListener(tweepy.StreamListener):
	def __init__(self, file):
		self.file = file
		self.tweets = []
		super()

	def on_data(self, data):
		data = json.loads(data)
		self.tweets.append(data)
		with open(self.file, 'a') as file:
			if len(self.tweets) % 10 == 0:
				file.seek(0)
				file.truncate()
				file.write(json.dumps(self.tweets))

def stream_tweets(query, file = 'tweet_stream.json'):
	myStreamListener = MyStreamListener(file)
	myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
	myStream.filter(track=query, is_async=True)

query = ['#Sprite', '#Cocacola', '#Pepsi', '#Coffee', '#Tea', '#GreenTea', '#Earlgrey', '#espresso', '#Nestle', '#DietCoke', '#Dietpepsi', '#nespresso', '#keurig', '#rootbeer', '#fanta', '#soda', '#cola', '#7up','#MountainDew', '#Caffeine','#drpepper','#Cappuccino','#Latte','#Mocha']

# stream_tweets(query, 'new_stream.json')
# get_past_tweets(query, 15000)