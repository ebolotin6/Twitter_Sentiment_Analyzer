# Eli Bolotin
# Nov 4 2018
# DS710: Final Project

import tweepy
import csv
import json
import jsonpickle
from textblob import TextBlob
from twitter_credentials import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
 
# auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
# api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

def get_followers(screen_name1, screen_name2):
	with open('walmart_followers.json', 'w') as f:
		walmart_followers = api.followers_ids(screen_name = screen_name1)
		f.write(jsonpickle.encode(walmart_followers, unpicklable=False) + '\n')

	with open('wholefoods_followers.json', 'w') as f:
		wholefoods_followers = api.followers_ids(screen_name = screen_name2)
		f.write(jsonpickle.encode(wholefoods_followers, unpicklable=False) + '\n')

	print(f"Created files of both follower sets.")

def process_to_list(walmart_json, wholefoods_json):
	# open files with followers and convert them to lists of json
	followers_walmart = []
	with open(walmart_json, 'r') as file:
		for line in file:
			followers_walmart.append(json.loads(line))

	followers_wholefoods = []
	with open(wholefoods_json, 'r') as file:
		for line in file:
			followers_wholefoods.append(json.loads(line))

	# get user_ids from combined lists of Walmart and Wholefoods followers
	followers = followers_walmart + followers_wholefoods
	follower_ids = []
	
	for follower in followers:
		f_id = follower['id']
		follower_ids.append(str(f_id))

	return follower_ids

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

# approach 1: get list of walmart and whole foods followers (REST) and then track their political tweets (Streaming)

# file1, file2 = get_followers("followers_walmart_v1.json","followers_wholefoods_v1.json")
# follower_ids = process_to_list("followers_walmart_v1.json", "followers_wholefoods_v1.json")
# myStreamListener = MyStreamListener()
# myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
# # query = "%23vote OR %23midterms OR %23RockTheVote OR %23democrat OR %23republican"
# query = ['vote', 'midterms', 'RockTheVote', 'democrat', 'republican']
# myStream.filter(follow=follower_ids, track=query, is_async=True)
