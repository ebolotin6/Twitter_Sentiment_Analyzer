# Eli Bolotin
# Nov 4 2018
# DS710: Final Project

from textblob import TextBlob as tb
from profanity import profanity
import csv
import json
import re
import math
import statistics
# import pprint
import dateutil.parser
from difflib import SequenceMatcher
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.metrics import accuracy_score

def clean_tweets(tweets_json, tweets_type = "stream"):
	file_name = tweets_json.split(".")[0]

	# load up json file
	try:
		with open(tweets_json, 'r') as file:
			tweets = json.load(file)
	except Exception as e:
		print(e)
		return False

	# remove all links in tweets and get text length
	for tweet in tweets:
		text = tweet.pop(3)
		text = re.sub(r'http\S+', '', text, flags=re.MULTILINE)
		text_len = len(text)
		tweet.append(text)
		tweet.append(text_len)

	# regex pattern to remove other invalid qualifiers
	if tweets_type == 'stream':
		regex = re.compile(r'^(\d)+|^(#\w\b)+|^\"|^\*|^[A-Z]{5, }|[A-Z]$|^How|^The\s\d+|^Photos|(\'\')+|(free|buy|get|class|connect|discount|now|read|job|video|news|follow|added|review|publish|clubs|manager|study|success|limited|release|help|gift|ideas|massage|schedule|services|check|join|pain|therapy|alternative|new\schallenge|product|need|learn|for\smen|for\swomen|revolution|leadership|weight\sloss|diet\splan|ebay|click|promo|certified|store|pick|sign|log-in|login|tips|meet|secret|improve|listen|(\w+)for(\w+)|trainer)|(\$|\+|\@|\?|\?$)|(\.\n\.)|^$', re.IGNORECASE)
	else:
		regex = re.compile(r'[^\u0000-\u007F]{5,}|^\s*$|\W{7,}|^(\d)+|^(#\w\b)+|^\"|^\*|^[A-Z]{5, }|[A-Z]$|^How|^The\s\d+|^Photos|(\'\')+|(top\s\d+|free|buy|class|discount|job|review|publish|clubs|manager|study|success|limited|release|help|gift|massage|schedule|services|check|join|pain|therapy|alternative|new\sproduct|learn|for\smen|for\swomen|revolution|leadership|ebay|click|promo|certified|store|pick|sign|log-in|login|tips|meet|secret|(\w+)for(\w+)|trainer)|(\$)|(\.\n\.)', re.IGNORECASE)


	# get all indices for tweets list, and set excluded indices
	all_indices = [i for i in range(len(tweets))]
	excluded_indices = []

	# get median hashtag count
	median, hashtag_counts = get_median_hashtags(tweets)
	
	# if median is 0, then use mean
	if median == 0:
		median = math.ceil(statistics.mean(hashtag_counts))

	# loop through tweets and remove near duplicate pairs
	if tweets_type != "stream":
		for i in range(1, len(tweets)):
			current_tweet = tweets[i][3]
			previous_tweet = tweets[i-1][3]
			test = percent_same(current_tweet, previous_tweet)

			if test >= .5:
				excluded_indices.append(i)
	
	# loop through tweets and hashtag counts and build exclusion index
	for i, values in enumerate(zip(tweets, hashtag_counts)):
		tweet = values[0][3]
		hashtag_count = values[1]
		# print(f"{i + 1} --- {tweet} --- {hashtag_count} --- {median}")

		# exclude tweets that have profanity or high(er) hashtag_count
		if profanity.contains_profanity(tweet) == True or hashtag_count > median:
			excluded_indices.append(i)
		else:
			match = regex.search(tweet)
			if match:
				excluded_indices.append(i)
			else:
				pass

	# filter all_indices to exclude excluded_indices
	excluded_indices = set(excluded_indices)
	filtered_indices = list(filter(lambda x:  x not in excluded_indices, all_indices))
	filtered_tweets = [tweets[index] for index in filtered_indices]

	try:
		# print to csv
		output_filename_csv = file_name + "_clean.csv"

		with open(output_filename_csv, 'w') as new_file:
			field_names = ['index','screen_name','user_id','tweet_text','length']
			writer = csv.writer(new_file, delimiter=',')
			writer.writerow(field_names)
			writer.writerows(filtered_tweets)

		# print to json if tweets_type is full data and not a stream
		if tweets_type == "full":
			output_filename_json = file_name + "_clean.json"
			with open(output_filename_json, 'w') as new_file:
				new_file.write(json.dumps(filtered_tweets))

			print("Successfully cleaned tweets. Returning json file for analysis.")
			return output_filename_json
		else:
			print("Successfully cleaned tweets. Returning csv file for review.")
			return output_filename_csv

	except Exception as e:
		print("Error: ", e)
		return False

def percent_same(str1, str2):
	return SequenceMatcher(None, str1, str2).ratio()

def get_median_hashtags(tweets):
	n = len(tweets)
	
	hashtag_counts = []

	for i, tweet in enumerate(tweets):
		tweet = tweet[3]
		num_hashtags = tweet.count("#")
		# print(f"{i} --- {tweet} --- {num_hashtags}")
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

def analyze_tweets(tweets_json):
	with open(tweets_json, 'r') as file:
		full_tweets = json.load(file)

	full_tweets_index = []
	index = 0

	# ordering the full_tweets list with an index
	for user in full_tweets:
		for tweet in user:
			tup = tuple((index, tweet))
			full_tweets_index.append(tup)
			index += 1

	file_name = tweets_json.split(".")[0]
	# open the filtered version of the full tweets list
	with open(file_name + "_truncated_clean.json", 'r') as file:
		filtered_tweets = json.load(file)

	# filter the full list of tweets
	filtered_tweets = [full_tweets_index[tweet[0]-1] for tweet in filtered_tweets]

	tweets_list = []
	sid = SentimentIntensityAnalyzer()
	index = 0

	for tweet in filtered_tweets:
		tweet = tweet[1]
		index += 1
		user_id = tweet['user']['id']
		user_screenname = tweet['user']['screen_name']
		user_des = tweet['user']['description']
		tweet_id = tweet['id']
		tweet_date = dateutil.parser.parse(tweet['created_at']).date()
		tweet_text = tweet['text']
		tweet_text = re.sub(r'http\S+', '', tweet_text, flags=re.MULTILINE)
		tweet_len = len(tweet_text)
		followers_count = tweet['user']['followers_count']
		friends_count = tweet['user']['friends_count']
		favorites_count = tweet['user']['favourites_count']
		ss = sid.polarity_scores(tweet_text)
		sentiment_vader = ss['compound']
		sentiment_tb = tb(tweet_text).sentiment[0]
		hashtags = tweet['entities']['hashtags']
		hashtags_str = ''

		for hashtag in hashtags:
			try:
				if len(hashtags) == 1:
					hashtags_str += hashtag['text'] + ', '
				else:
					for hashtag in hashtags:
						hashtags_str += hashtag['text'] + ', '
			except Exception as e:
				pass

		current_tweet = (index, user_id, user_screenname, user_des, tweet_id, tweet_date, tweet_text, tweet_len, followers_count, friends_count, favorites_count, round(sentiment_vader,2), round(sentiment_tb,2), hashtags_str)
		tweets_list.append(current_tweet)

	try:
		output_filename_csv = file_name + "_analysis.csv"

		with open(output_filename_csv, 'w') as file: 
			field_names = ['index', 'user_id', 'user_screenname','user_des','tweet_id','tweet_date','tweet_text','tweet_len','followers_count','friends_count','favorites_count','sentiment_vader','sentiment_tb','hashtags']
			writer = csv.writer(file, delimiter=',')
			writer.writerow(field_names)
			writer.writerows(tweets_list)	

		print(f"{file_name}_analysis.csv created.")
		return output_filename_csv
	except Exception as e:
		print("Error: ", e)

def stream_json_to_csv(json_file_input, output, stream = True):
	# this function is for already truncated data (list of 4 element lists)
	with open(json_file_input + ".json", 'r') as file:
		file = json.load(file)

	# write to csv
	with open(output + ".csv", 'w') as new_file:
		field_names = ['index','screen_name','user_id','tweet_text']
		writer = csv.writer(new_file, delimiter=',')
		writer.writerow(field_names)
		writer.writerows(file)

	print("CSV created.")
