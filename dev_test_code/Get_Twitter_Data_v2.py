# Eli Bolotin
# Nov 4 2018
# DS710: Final Project

import tweepy
import json
from twitter_credentials import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
 
# auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)

def get_followers(screen_name1, screen_name2):
	with open('walmart_followers.json', 'w') as f:
		# walmart_followers = api.followers_ids(screen_name = screen_name1)
		walmart_follower_ids = []
		for page in tweepy.Cursor(api.followers_ids, screen_name=screen_name1).pages():
			walmart_follower_ids.extend(page)
			f.seek(0)
			f.truncate()
			f.write(json.dumps(walmart_follower_ids) + '\n')

	with open('wholefoods_followers.json', 'w') as f:
		wholefoods_follower_ids = []
		for page in tweepy.Cursor(api.followers_ids, screen_name=screen_name2).pages():
			wholefoods_follower_ids.extend(page)
			f.seek(0)
			f.truncate()
			f.write(json.dumps(wholefoods_follower_ids) + '\n')
	
	print(f"Created files of both follower sets.")
	return(screen_name1, screen_name2)

class MyStreamListener(tweepy.StreamListener):
	def __init__(self, file = 'tweet_stream.json'):
		self.file = file
		super()

	def on_data(self, data):
		with open(self.file, 'a') as file:
			file.write(data)

	#disconnect the stream if we receive an error message indicating we are overloading Twitter
	def on_error(self, status_code):
		print(status_code)
		if status_code == 420:
		#returning False in on_data disconnects the stream
			return False

# approach 2 - step 1: track all political tweets
# myStreamListener = MyStreamListener(file = 'tweet_stream_v3.json')
# with myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
# 	query = ['vote', 'midterms', 'RockTheVote', 'democrat', 'republican']
# 	myStream.filter(track=query, is_async=True)

# approach 2 - step 2: get ids of all walmart and wholefoods followers
walmart_followers, wholefoods_followers = get_followers("Walmart","WholeFoods")
