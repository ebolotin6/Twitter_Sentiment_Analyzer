# Eli Bolotin
# Nov 4 2018
# DS710: Final Project

import csv
import json
from textblob import TextBlob

def get_user_ids(tweets_stream_json):
	with open(tweets_stream_json, 'r') as file:
		file = json.load(file)

	user_ids_list = []
	for tweet in file:
		user_id = tweet['user']['id']	
		user_ids_list.append(user_id)

	with open('user_ids_list.json', 'w') as file:
		file.write(json.dumps(user_ids_list))

	print("User_ds saved.")

def clean_and_analyze(tweets_json, walmart_followers, wholefoods_followers):
	with open(tweets_json, 'r') as file:
		file = json.load(file)

	hash_dict = {}
	tweets_list = []

	for tweet in file:
		user_id = tweet['user']['id']
		screen_name = tweet['user']['screen_name']
		tweet_id = tweet['id']
		tweet_text = tweet['extended_tweet']['full_text']
		tweet_len = len(tweet_text)
		sentiment = Textblob(tweet_text).sentiment[0]

		for hashtag in tweet['extended_tweet']['entities']['hashtags']:
			hashtag = hashtag['text']
			if hashtag in hash_dict:
				hash_dict[hashtag] += 1
			else:
				hash_dict[hashtag] = 1
		
		current_tweet = (user_id, screen_name, tweet_id, tweet_text, tweet_len, sentiment, hash_dict)
		tweets_list.append(current_tweet)

	with open('collected_data.csv', 'w') as file: 
		field_names = ['user_id','screen_name','tweet_id','tweet_text','tweet_len','sentiment','hashtag']
		writer = csv.writer(file, delimiter=',')
		writer.writerow(field_names)
		writer.writerows(processed)	

	print(f"collected_data.csv created.")

walmart_followers_list, wholefoods_followers_list = process_to_list("followers_walmart.json", "followers_wholefoods.json")
# print(walmart_followers, end="\n")
# print(wholefoods_followers, end="\n")

clean_and_analyze('tweet_stream.json', walmart_followers_list, wholefoods_followers_list)



