# Twitter Sentiment Analysis Program
# Eli Bolotin
# Copyright 2018

import tweepy
import os.path
import json
import csv
import dill
import re
import math
import statistics
import requests
from os import makedirs
from twitter_credentials import *
from textblob import TextBlob as tb
from profanity import profanity
from difflib import SequenceMatcher
import dateutil.parser
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.metrics import accuracy_score

# authenticate with Twitter API and set arguments for dealing with rate_limiting
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# Save and load instances of TweetProgram class to/from local storage. 
# Details: This program is class-based to allow for data persistence. Data persistence allows us to create an object once, run a method (or more), end the program, and then come back and start from where we left off. Said differently, this allows the user to run a method on the same object between program executions. To achieve this end (save an object's state outside program execution), we use serialization. Specifically, the 'dill' package (serialization) is employed in this program.
def StreamedTweets(file_name_json, sub_dir):
	file_name = file_name_json.split(".")[0]

	try:
		abs_file_path, abs_sub_dir = get_abs_path(file_name, sub_dir)
		file_name_pkl = abs_file_path + '.pkl'

		if os.path.exists(file_name_pkl):
			with open(file_name_pkl, 'rb') as f:
				obj = dill.load(f)
				message = f"Loaded '{file_name_json}' into memory."

		else:
			abs_file_name_json = abs_file_path + '.json'

			if os.path.exists(abs_file_name_json):
				with open(file_name_pkl, 'wb') as f:
					obj = TweetProgram(abs_file_name_json)
					dill.dump(obj, f)
					message = f"Created '{file_name_json}' stream to work on."
			else:
				print(f"JSON file '{file_name_json}' does not exist.")
				return False
		
		print(f"--------------------------------------------------------------\n {message} \n--------------------------------------------------------------")

		return(obj)

	except Exception as e:
		print("Error: ", e)
		return False

# decorator for TwitterProgram class methods that prints the activity of a given method.
def print_status(func):
	def wrapper(self, **kwargs):
		if func.__name__ == 'clean_tweets':
			print("\t - Cleaning ... ", end="")

		elif func.__name__ == 'get_full_tweets':
			print("\t - Fetching full tweets ... ", end="")

		elif func.__name__ == 'get_sentiment':
			print("\t - Analyzing tweet sentiment ... ", end="")

		obj = func(self, **kwargs)
		return obj
	return wrapper

# function to get abs_path of files in sub directories
def get_abs_path(file_name, sub_dir):
	cwd = os.path.dirname(__file__)

	if os.path.exists(sub_dir):
		rel_file_path = sub_dir + "/" + file_name
		abs_file_path = os.path.join(cwd, rel_file_path)
		abs_sub_dir = os.path.join(cwd, sub_dir)
		return(abs_file_path, abs_sub_dir)
	else:
		print("Incorrect directory.")
		return False

# get list of banned (profane) words
def get_profanity_list():
	try:
		r = requests.get('https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/master/en')
		profanity_words = r.content.decode("utf-8") 
		profanity_list = profanity_words.split("\n")
		return profanity_list

	except Exception as e:
		print("Error: ", e)

# class for tweet stream json objects that need to be cleaned, fetched in full, and analyzed for sentiment.
class TweetProgram:
	def __init__(self, file_name, tweets_type = "stream"):
		# set file names at various stages of tweet stream processing
		self.sub_dir = os.path.split(file_name)[1]
		self.streamed_tweets_json = file_name
		self.streamed_tweets_filename = os.path.splitext(self.streamed_tweets_json)[0]
		self.cleaned_streamed_tweets_csv = self.streamed_tweets_filename + "_clean.csv"
		self.full_tweets_json = self.cleaned_streamed_tweets_csv.split(".")[0] + "_full.json"
		self.full_tweets_trunc_json = self.full_tweets_json.split(".")[0] + "_trunc.json"
		self.full_tweets_trunc_csv = self.full_tweets_json.split(".")[0] + "_trunc.csv"
		self.full_tweets_trunc_clean_json = self.full_tweets_trunc_json.split(".")[0] + "_clean.json"
		self.full_tweets_trunc_clean_csv = self.full_tweets_trunc_csv.split(".")[0] + "_clean.csv"
		self.full_tweets_analysis_csv = self.full_tweets_json.split(".")[0] + "_analysis.csv"
		
		self.step_1_streamed_tweets_present = 1
		
		if os.path.exists(self.cleaned_streamed_tweets_csv):
			self.step_2_cleaned_streamed_tweets = 1
		else:
			self.step_2_cleaned_streamed_tweets = 0
		
		if os.path.exists(self.full_tweets_trunc_json):
			self.step_3_fetched_full_tweets = 1
		else:
			self.step_3_fetched_full_tweets = 0

		if os.path.exists(self.full_tweets_trunc_clean_json):
			self.step_4_cleaned_full_tweets = 1
		else:
			self.step_4_cleaned_full_tweets = 0

		if os.path.exists(self.full_tweets_analysis_csv):
			self.step_5_analyzed_full_tweets = 1
		else:
			self.step_5_analyzed_full_tweets = 0

		# set filename for pickled object (self)
		self.obj_name = self.streamed_tweets_filename + ".pkl"
		
		# tweet stream settings
		self.max_tweets = 20
		self.max_users = 100
		self.tweets_type = tweets_type

		# containers for messages. currently unused.
		error_messages = {}
		success_messages = {}
	
	# save instance to local storage
	def save_obj(self):
		with open(self.obj_name, 'wb') as f:
			dill.dump(self, f)

	# load instance from local storage
	def load_obj(self):
		with open(self.obj_name, 'rb') as f:
			dill.load(self, f)

	def reset_obj(self):
		self.step_1_streamed_tweets_present = 1
		self.step_2_cleaned_streamed_tweets = 0
		self.step_3_fetched_full_tweets = 0
		self.step_4_cleaned_full_tweets = 0
		self.step_5_analyzed_full_tweets = 0

		self.save_obj()

	# Clean_tweets method. This method cleans & filters a json dict of tweets and returns both json and csv files of the tweets data.
	@print_status
	def clean_tweets(self, tweets_type = None):
		# identify the type of tweet
		if tweets_type == None:
			self.tweets_type = "stream"
		else:
			self.tweets_type = tweets_type

		# if streamed tweets have not been cleaned before, then open the streamed tweets.
		if self.step_2_cleaned_streamed_tweets == 0 and self.tweets_type == "stream":
			try:
				with open(self.streamed_tweets_json, 'r') as file:
					tweets = json.load(file)
			
			except Exception as e:
				print(f"Message: Streamed tweets file not found: '{os.path.relpath(self.streamed_tweets_json)}'")
				return False
		
		# check if streamed tweets have already been cleaned before.
		elif self.step_2_cleaned_streamed_tweets == 1 and self.tweets_type == "stream":
			print(f"Message: You already cleaned your tweet stream. Csv file here: '{os.path.relpath(self.cleaned_streamed_tweets_csv)}'")
			return False

		# check if full tweets have already been cleaned before.
		elif self.step_4_cleaned_full_tweets == 1 and self.tweets_type == "full":
			print(f"Message: You already cleaned the full tweets for this stream. Truncated file here: '{os.path.relpath(self.full_tweets_trunc_clean_csv)}'")
			return False
		
		# if full tweets data is available, then open it.
		elif self.step_3_fetched_full_tweets == 1 and self.tweets_type == "full":
			try:
				with open(self.full_tweets_trunc_json, 'r') as file:
					tweets = json.load(file)
			
			except Exception as e:
				print(f"Message: Full tweets file not found: '{os.path.relpath(self.full_tweets_trunc_json)}'")
				return False

		# for every tweet, remove all links and get text length
		for tweet in tweets:
			text = tweet.pop(3)
			text = re.sub(r'http\S+', '', text, flags=re.MULTILINE)
			text_len = len(text)
			tweet.append(text)
			tweet.append(text_len)

		# regex pattern to filter out invalid tweets from streamed data. See Regex_README.md for details.
		regex = re.compile(r'[^\u0000-\u007F]{5,}|^\s*$|\W{7,}|^(\d)+|^(#\w\b)+|^\"|^\*|^[A-Z]{5, }|[A-Z]$|^How|^The\s\d+|^Photos|(\'\')+|(top\s\d+|free|buy|get|class|connect|discount|now|read|job|video|news|follow|added|review|publish|clubs|manager|study|success|limited|sex|release|help|gift|ideas|massage|schedule|services|check|join|pain|therapy|alternative|new\schallenge|product|need|learn|for\smen|for\swomen|revolution|leadership|weight\sloss|diet\splan|ebay|click|promo|certified|store|pick|sign|log-in|login|tips|meet|secret|improve|listen|(\w+)for(\w+)|trainer)|(\$|\+|\@|\?|\?$)|(\.\n\.)|^$', re.IGNORECASE)

		# get all users in tweet list and create list to hold excluded users
		all_users = set([tweet[2] for tweet in tweets])
		excluded_users = []

		# get median hashtag count and also a list of hashtag counts
		median, hashtag_counts = self._get_median_hashtags(tweets)

		# get stdev of hashtag count
		stdev = math.ceil(statistics.stdev(hashtag_counts))
		
		# if median is 0, then use mean
		if median == 0:
			median = math.ceil(statistics.mean(hashtag_counts))

		# get list of profanities and load it
		profanity_list = get_profanity_list()		
		profanity.load_words(profanity_list)

		# loop through tweets and hashtag counts and build exclusion index
		for i, values in enumerate(zip(tweets, hashtag_counts)):
			tweet = values[0][3]
			user_id = values[0][2]
			hashtag_count = values[1]
			mid_68 = median + stdev

			# testing for spammy tweets
			current_tweet = tweets[i][3]
			past_tweet = tweets[i-1][3]
			test = self._percent_same(current_tweet, past_tweet)

			# testing for profanity
			profanity_test = profanity.contains_profanity(tweet)

			# exclude authors/users of spammy tweets, or tweets that have profanity, or a hashtag_count above the median + 1 stdev
			if test >= .5 or profanity_test == True or hashtag_count > mid_68:
				excluded_users.append(user_id)
			else:
				match = regex.search(tweet)
				if match:
					excluded_users.append(user_id)
				else:
					pass

		# filter out excluded_users from all_users and return filtered tweets
		excluded_users = set(excluded_users)
		filtered_users = list(filter(lambda x:  x not in excluded_users, all_users))
		filtered_tweets = [tweet for tweet in tweets if tweet[2] in filtered_users]

		try:
			# print to csv
			if self.tweets_type == "stream":
				output_filename_csv = self.cleaned_streamed_tweets_csv
			else:
				output_filename_csv = self.full_tweets_trunc_clean_csv

			with open(output_filename_csv, 'w') as new_file:
				field_names = ['index','screen_name','user_id','tweet_text','length']
				writer = csv.writer(new_file, delimiter=',')
				writer.writerow(field_names)
				writer.writerows(filtered_tweets)

			# print to json if tweets_type is full data and not a stream
			if self.tweets_type == "full":
				output_filename_json = self.full_tweets_trunc_clean_json
				
				with open(output_filename_json, 'w') as new_file:
					new_file.write(json.dumps(filtered_tweets))

				self.step_4_cleaned_full_tweets = 1
				self.save_obj()
				print(f"Successfully cleaned tweets. See csv file for review: '{os.path.relpath(output_filename_csv)}'")
				return output_filename_json

			else:
				self.step_2_cleaned_streamed_tweets = 1
				self.save_obj()
				print(f"Successfully cleaned tweets. See csv file for review: '{os.path.relpath(output_filename_csv)}'")
				return output_filename_csv
		
		except Exception as e:
			print("Error: ", e)
			return False

	def _percent_same(self, str1, str2):
		return SequenceMatcher(None, str1, str2).ratio()

	def _get_median_hashtags(self, tweets):
		n = len(tweets)
		
		hashtag_counts = []

		for i, tweet in enumerate(tweets):
			tweet = tweet[3]
			num_hashtags = tweet.count("#")
			hashtag_counts.append(num_hashtags)

		hashtag_counts_sorted = sorted(hashtag_counts)

		if n % 2 == 0:
			first_half_max_index = round(n / 2)
			second_half_first_index = first_half_max_index + 1
			first_half_max_value = hashtag_counts_sorted[first_half_max_index - 1] # -1 because list indices start at 0
			second_half_first_value = hashtag_counts_sorted[second_half_first_index - 1]
			median = (first_half_max_value + second_half_first_value) / 2

		elif n % 2 != 0:
			median_index = math.ceil(n / 2) - 1 # - 1 to account for list index starting at 0
			median = hashtag_counts_sorted[median_index]

		median = round(median, 2)
		return(median, hashtag_counts)

	def _write_tweets(self, file_name = None, tweets_list = None):
		if file_name != None and tweets_list != None:
			try:
				with open(file_name, 'a') as file:
					file.seek(0)
					file.truncate()
					file.write(json.dumps(tweets_list))

				return True
			except Exception as e:
				print(e)
				return False
		else:
			print("Pass proper arguments, please.")

	@print_status
	def get_full_tweets(self, tweets_cleaned = "yes", max_tweets = None, max_users = None):
		# if streamed tweets have been fetched in full before, return false
		if self.step_3_fetched_full_tweets == 1:
			print(f"Message: You already fetched full (other) tweets for this stream. Truncated file here: '{os.path.relpath(self.full_tweets_trunc_csv)}'")
			return False

		# default is 20 most recent tweets per user
		if max_tweets != None:
			self.max_tweets = max_tweets

		# default is 100 (first from top) users in streamed tweets file
		if max_users != None:
			self.max_users = max_users

		# Determine whether to accept a csv or json as input based on if the input tweets have been cleaned before.
		if tweets_cleaned == "yes":
			# this takes a csv instead of json to allow the user to manually clean tweets if necessary.
			try:
				with open(self.cleaned_streamed_tweets_csv, 'r') as tweets:
					tweets = csv.reader(tweets)
					tweets_list = list(tweets)[1:] # skip header
			except Exception as e:
				print(e)
		else:
			try:
				with open(self.streamed_tweets_json, 'r') as tweets:
					tweets_list = json.load(tweets) # skip header
			except Exception as e:
				print(e)

		user_ids = []
		
		for tweet in tweets_list:
			user_id = int(tweet[2])
			
			# filter to get only unique users
			if user_id not in user_ids:
				user_ids.append(user_id)

		# select top 100 user_ids from streamed data
		if isinstance(self.max_users, int):
			user_ids = user_ids[:self.max_users]

		all_tweets = []
		
		for user_id in user_ids:
			user_tweets = []

			try:
				# search user timeline of top [max_users] users from streamed tweet data, and pull 20 tweets max for each user.
				for tweet in tweepy.Cursor(api.user_timeline, user_id = user_id,  include_entities = True).items(self.max_tweets):
					data = tweet._json

					# define some columns to filter out of the API request.
					try:
						reply_to1 = data['in_reply_to_status_id']
						reply_to2 = data['in_reply_to_user_id']
						quote_status = data['is_quote_status']
						sensitive = data['possibly_sensitive']
						retweeted = data['retweeted']

						# filter out invalid tweets for each user and append the valid ones the user_tweets list.
						if not 'RT @' in data['text'] and reply_to1 == None and reply_to2 == None and quote_status == False and sensitive == False and retweeted == False:
							user_tweets.append(tweet._json)

					except Exception as e:
						# print("Error: ", e)
						pass
				
				all_tweets.append(user_tweets)

			# Passing on the error because 401 response codes can happen if a user's tweets are private.
			except tweepy.TweepError as e:
				# print("Error: ", e)
				# return False
				pass

			if len(all_tweets) % 10 == 0:
				self._write_tweets(self.full_tweets_json, all_tweets)

		# for readability, create a truncated version of the full json file in both json and csv format.
		else:
			write_tweets = self._write_tweets(self.full_tweets_json, all_tweets)
			len_tweets = len(all_tweets)

			if write_tweets == True:
				try:
					output_filename_json = self._truncate_and_transform(self.full_tweets_json)
					print(f"Successfully collected {len_tweets} tweets. See csv: '{os.path.relpath(self.full_tweets_trunc_csv)}'")
					return(output_filename_json)

				except Exception as e:
					print("Error: ", e)
					return False

	def _truncate_and_transform(self, input_json):
		# this function truncates a json list of (complete) tweet data to a readable csv (with only 4 columns) and also to json format.
		try:
			with open(input_json, 'r') as file:
				file = json.load(file)

		except Exception as e:
			print(e)

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
		with open(self.full_tweets_trunc_json, 'w') as f:
			f.write(json.dumps(tweets))

		# write to csv
		with open(self.full_tweets_trunc_csv, 'w') as new_file:
			field_names = ['index','screen_name','user_id','tweet_text']
			writer = csv.writer(new_file, delimiter=',')
			writer.writerow(field_names)
			writer.writerows(tweets)

		self.step_3_fetched_full_tweets = 1
		self.save_obj()
		return(self.full_tweets_trunc_json)

	@print_status
	def get_sentiment(self, use_cleaned_tweets = False):
		# make sure that tweets have not already been analyzed
		if self.step_5_analyzed_full_tweets != 1:
			# make sure that tweets are full and cleaned
			if self.step_3_fetched_full_tweets == 1:
				try:
					with open(self.full_tweets_json, 'r') as file:
						full_tweets = json.load(file)
				except Exception as e:
					return False
			else:
				print("Message: to analyze tweets for sentiment you need to get_full_tweets and clean them.")
				return False
		else:
			print(f"Message: tweets already analyzed. Csv name: '{os.path.relpath(self.full_tweets_analysis_csv)}'")
			return False

		full_tweets_index = []
		index = 0

		# ordering the full_tweets list with an index
		for user in full_tweets:
			for tweet in user:
				tup = tuple((index, tweet))
				full_tweets_index.append(tup)
				index += 1

		if use_cleaned_tweets == True:
			# open the filtered version of the full tweets list
			with open(self.full_tweets_trunc_clean_json, 'r') as file:
				filtered_tweets = json.load(file)

			# filter the full list of tweets
			tweets = [full_tweets_index[tweet[0]-1] for tweet in filtered_tweets]
		else:
			tweets = full_tweets_index

		tweets_list = []
		sid = SentimentIntensityAnalyzer() # create senitment analysis object
		index = 0

		# define fields that we want to pull from tweet data
		for tweet in tweets:
			tweet = tweet[1]
			index += 1
			user_id = tweet['user']['id']
			user_screenname = tweet['user']['screen_name']
			user_des = tweet['user']['description']
			tweet_id = tweet['id']
			tweet_date = dateutil.parser.parse(tweet['created_at']).date() # get date
			tweet_text = tweet['text']
			tweet_text = re.sub(r'http\S+', '', tweet_text, flags=re.MULTILINE) # remove links
			tweet_len = len(tweet_text)
			followers_count = tweet['user']['followers_count']
			friends_count = tweet['user']['friends_count']
			favorites_count = tweet['user']['favourites_count']
			ss = sid.polarity_scores(tweet_text) # sentiment analyzer object
			sentiment_vader = ss['compound'] # NLTK vader sentiment
			sentiment_tb = tb(tweet_text).sentiment[0] # Textblob sentiment
			hashtags = tweet['entities']['hashtags']
			hashtags_str = ''

			# get hashtags
			for hashtag in hashtags:
				try:
					if len(hashtags) == 1:
						hashtags_str += hashtag['text'] + ', '
					else:
						for hashtag in hashtags:
							hashtags_str += hashtag['text'] + ', '
				except Exception as e:
					pass

			# create tuple of fields
			current_tweet = (index, user_id, user_screenname, user_des, tweet_id, tweet_date, tweet_text, tweet_len, followers_count, friends_count, favorites_count, round(sentiment_vader,2), round(sentiment_tb,2), hashtags_str)
			tweets_list.append(current_tweet)

		try:
			# write to csv
			with open(self.full_tweets_analysis_csv, 'w') as file: 
				field_names = ['index', 'user_id', 'user_screenname','user_des','tweet_id','tweet_date','tweet_text','tweet_len','followers_count','friends_count','favorites_count','sentiment_vader','sentiment_tb','hashtags']
				writer = csv.writer(file, delimiter=',')
				writer.writerow(field_names)
				writer.writerows(tweets_list)	

			print(f"Successfully analyzed tweet sentiment: '{os.path.relpath(self.full_tweets_analysis_csv)}' created.")
			self.step_5_analyzed_full_tweets = 1
			self.save_obj()
			return self.full_tweets_analysis_csv
		
		except Exception as e:
			print("Error: ", e)

# create class that inherits (tweepy's) parent class
class MyStreamListener(tweepy.StreamListener):
	def __init__(self, option, file_name, sub_dir, max_tweets):
		self.file_name = file_name
		self.sub_dir = sub_dir
		self.option = option
		self.max_tweets = max_tweets
		self.tweets = []
		self.user_ids = []
		self.count_users = 0
		self.cwd = os.path.dirname(__file__)
		self.rel_path = self.sub_dir + self.file_name
		self.abs_file_path = os.path.join(self.cwd, self.rel_path)

		super()

	def on_data(self, data):
		# check that max_tweet number has not been exceeded
		if len(self.user_ids) < self.max_tweets and len(self.tweets) < self.max_tweets:
			data = json.loads(data)
			
			try:
				# define fields to filter on
				user_id_len = len(str(data['user']['id']))
				reply_to1 = data['in_reply_to_status_id']
				reply_to2 = data['in_reply_to_user_id']
				quote_status = data['is_quote_status']
				sensitive = data['possibly_sensitive']
				retweeted = data['retweeted']
	
				# eliminate retweets, bots, replies, quotes, and sensitive material
				if not 'RT @' in data['text'] and user_id_len < 18  and reply_to1 == None and reply_to2 == None and quote_status == False and sensitive == False and retweeted == False:
					
					# pull just user data for each tweet
					if self.option == 'user_info':
						self.count_users += 1
						self.screen_name = data['user']['screen_name']
						self.user_id = data['user']['id']
						self.tweet = data['text']
						self.tup = tuple((self.count_users, self.screen_name, self.user_id, self.tweet))
						self.user_ids.append(self.tup)

						if len(self.user_ids) % 10 == 0:
							try:
								with open(self.abs_file_path + ".json", 'a') as f:
									f.seek(0)
									f.truncate()
									f.write(json.dumps(self.user_ids))
							
							except Exception as e:
								print(e)
			
			except Exception as e:
				pass

		# if reached max tweet count, write to csv
		elif len(self.user_ids) == self.max_tweets:
			try:
				output_filename_csv = self.abs_file_path + '.csv'
				output_filename_json = self.abs_file_path + '.json'

				with open(output_filename_csv, 'w') as csv_output:
					field_names = ['index','screen_name','user_id','tweet_text']
					writer = csv.writer(csv_output, delimiter=',')
					writer.writerow(field_names)
					writer.writerows(self.user_ids)
				
				print(f"--> Successfully captured {self.max_tweets} tweets for '{self.file_name}'. Ending this stream now. The output is in json and csv format:\n\t- JSON file: {os.path.relpath(output_filename_json)}\n\t- CSV file: {os.path.relpath(output_filename_csv)}\n")
				return False
			
			except Exception as e:
				print(e)
				return False

	def on_error(self, status_code):
		print(status_code)
		return False

# wrapper to open stream listener, stream and then filter stream
def stream_tweets(query, option = 'user_info', file_name = 'user_ids', max_tweets = 150):
	try:
		index = 1

		# Create new directory to store stream and sample data in.
		while True:
			sub_dir = "Samples_Round_" + str(index)
			
			if os.path.exists(sub_dir):
				index += 1
			else:
				os.makedirs(sub_dir, exist_ok=False)
				break

		sub_dir = sub_dir + "/"
		
		print(f"Created directory '{sub_dir}' to store data. Streaming tweets for '{file_name}' ...")
		myStreamListener = MyStreamListener(option, file_name, sub_dir, max_tweets)
		myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
		myStream.filter(track=query, languages=['en'], is_async=True)
	
	except Exception as e:
		print("Error: ", e)


