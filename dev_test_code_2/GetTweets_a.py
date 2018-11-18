# Eli Bolotin
# Nov 4 2018
# DS710: Final Project

import tweepy
import json
import pprint
import csv
from twitter_credentials import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

def get_full_tweets(clean_streamed_tweets, max_tweets = 20, max_users = 100):
	file_name = clean_streamed_tweets.split(".")[0]
	output_json = file_name + "_full.json"

	with open(clean_streamed_tweets, 'r') as tweets:
		tweets = csv.reader(tweets)
		tweets_list = list(tweets)[1:] # skip header

	user_ids = []
	
	for tweet in tweets_list:
		user_id = int(tweet[2])
		user_ids.append(user_id)

	if isinstance(max_users, int):
		user_ids = user_ids[:max_users]

	all_tweets = []
	
	for user_id in user_ids:
		user_tweets = []

		try:
			for tweet in tweepy.Cursor(api.user_timeline, user_id = user_id,  include_entities = True).items(max_tweets):
				data = tweet._json

				try:
					reply_to1 = data['in_reply_to_status_id']
					reply_to2 = data['in_reply_to_user_id']
					quote_status = data['is_quote_status']
					sensitive = data['possibly_sensitive']
					retweeted = data['retweeted']

					if not 'RT @' in data['text'] and reply_to1 == None and reply_to2 == None and quote_status == False and sensitive == False and retweeted == False:
						user_tweets.append(tweet._json)

				except Exception as e:
					# print("Error: ", e)
					pass
			
			all_tweets.append(user_tweets)

		except tweepy.TweepError as e:
			print("Error: ", e)
			return False

		if len(all_tweets) % 10 == 0:
			with open(output_json, 'a') as file:
				file.seek(0)
				file.truncate()
				file.write(json.dumps(all_tweets))
	
	# for readability, create a truncated version of the full json file in both json and csv format.
	try:
		output_filename_json = truncate_and_transform(output_json)
		print(f"Collected {max_tweets} tweets for {max_users} users. Ending program.")
		return output_filename_json
	
	except Exception as e:
		print("Error: ", e)
		return False

def truncate_and_transform(input_json):
	file_name = input_json.split(".")[0]

	# this function truncates a json list of (complete) tweet data to a readable csv (with only 4 columns) and also to json format.
	try:
		with open(input_json, 'r') as file:
			file = json.load(file)

		users = file
		index = 0
		tweets = []
		
		for user in users:
			for tweet in user:
				index += 1
				screen_name = tweet['user']['screen_name']
				user_id = tweet['user']['id']
				tweet = tweet['text']
			
				ls = [index, screen_name, user_id, tweet]
				tweets.append(ls)

		# write to json
		output_filename_json = file_name + "_truncated.json" 
		with open(output_filename_json, 'w') as f:
			f.write(json.dumps(tweets))

		# write to csv
		output_filename_csv = file_name + "_truncated.csv" 
		with open(output_filename + "_truncated.csv", 'w') as new_file:
			field_names = ['index','screen_name','user_id','tweet_text']
			writer = csv.writer(new_file, delimiter=',')
			writer.writerow(field_names)
			writer.writerows(tweets)

		return output_filename_json
	except Exception as e:
		print(e)
		return False

class MyStreamListener(tweepy.StreamListener):
	def __init__(self, option, file_name, max_tweets):
		self.file_name = file_name
		self.option = option
		self.max_tweets = max_tweets
		self.tweets = []
		self.user_ids = []
		self.count_users = 0
		super()

	def on_data(self, data):
		if len(self.user_ids) < self.max_tweets and len(self.tweets) < self.max_tweets:	
			data = json.loads(data)
			
			try:
				user_id_len = len(str(data['user']['id']))
				reply_to1 = data['in_reply_to_status_id']
				reply_to2 = data['in_reply_to_user_id']
				quote_status = data['is_quote_status']
				sensitive = data['possibly_sensitive']
				retweeted = data['retweeted']
				# hashtag_count = len(data['entities']['hashtags'])
	
				if not 'RT @' in data['text'] and user_id_len < 18  and reply_to1 == None and reply_to2 == None and quote_status == False and sensitive == False and retweeted == False:
					
					if self.option == "all_info":
						self.tweets.append(data)
						try:
							with open(self.file_name + ".json", 'a') as f:
								if len(self.tweets) % 10 == 0:
									f.seek(0)
									f.truncate()
									f.write(json.dumps(self.tweets))
						except Exception as e:
							print(e)
					
					elif self.option == 'user_info':
						self.count_users += 1
						self.screen_name = data['user']['screen_name']
						self.user_id = data['user']['id']
						self.tweet = data['text']
						self.tup = tuple((self.count_users, self.screen_name, self.user_id, self.tweet))
						self.user_ids.append(self.tup)

						if len(self.user_ids) % 10 == 0:
							try:
								with open(self.file_name + ".json", 'a') as f:
									f.seek(0)
									f.truncate()
									f.write(json.dumps(self.user_ids))
			
							except Exception as e:
								print(e)
			
			except Exception as e:
				pass

		elif len(self.user_ids) >= self.max_tweets:
			try:
				output_filename_csv = self.file_name + '.csv'
				output_filename_json = self.file_name + '.json'

				with open(output_filename_csv, 'w') as csv_output:
					field_names = ['index','screen_name','user_id','tweet_text']
					writer = csv.writer(csv_output, delimiter=',')
					writer.writerow(field_names)
					writer.writerows(self.user_ids)
				
				print(f"Captured {self.max_tweets} tweets. Ending program.")
				return output_filename_json
			
			except Exception as e:
				print(e)
				return False

	def on_error(self, status_code):
		print(status_code)
		return False

def stream_tweets(query, option = 'user_info', file_name = 'user_ids', max_tweets = 150):
	myStreamListener = MyStreamListener(option, file_name, max_tweets)
	myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
	myStream.filter(track=query, languages=['en'], is_async=True)
