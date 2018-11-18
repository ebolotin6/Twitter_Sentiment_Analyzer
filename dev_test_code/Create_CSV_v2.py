# Eli Bolotin
# Nov 4 2018
# DS710: Final Project

import csv
import json
from textblob import TextBlob

def process_to_list(walmart_json, wholefoods_json):
	followers_walmart = []
	with open(walmart_json, 'r') as file:
		for line in file:
			followers_walmart.append(json.loads(line))

	followers_wholefoods = []
	with open(wholefoods_json, 'r') as file:
		for line in file:
			followers_wholefoods.append(json.loads(line))
	
	followers_ids_walmart = []
	followers_ids_wholefoods = []

	for follower in followers_walmart:
		f_id = follower['id']
		followers_ids_walmart.append(str(f_id))

	for follower in followers_wholefoods:
		f_id = follower['id']
		followers_ids_wholefoods.append(str(f_id))		

	return(followers_ids_walmart, followers_ids_wholefoods)

def clean_and_analyze(tweets_json, walmart_followers, wholefoods_followers):
	tweets = []
	with open(tweets_json, 'r') as file:
		for line in file:
			tweets.append(json.loads(line))

	preprocessed = [(tweet['user']['id'], len(tweet['text']), TextBlob(tweet['text']).sentiment[0], 1) for tweet in tweets]
	all_unique_user_ids = set([tweet['user']['id'] for tweet in tweets])
	processed = []

	for user_id in all_unique_user_ids:
		count_tweets = 0
		tweet_len_list = []
		sentiment_list = []
		
		if user_id in walmart_followers:
			follows_walmart = True
		elif user_id not in walmart_followers:
			follows_walmart = False
		
		if user_id in wholefoods_followers:
			follows_wholefoods = True
		elif user_id not in wholefoods_followers:
			follows_wholefoods = False

		for row in preprocessed:
			user_id_c = row[0]
			
			if user_id == user_id_c:
				tweet_len_list.append(row[1])
				sentiment_list.append(row[2])
				count_tweets += 1

		tweet_len_avg = round(sum(tweet_len_list) / count_tweets, 1)
		sentiment_avg = round(sum(sentiment_list) / count_tweets, 1)
		row = tuple((user_id, tweet_len_avg, sentiment_avg, count_tweets, follows_walmart, follows_wholefoods))
		processed.append(row)
	 
	with open('tweepy_analysis.csv', 'w') as file: 
		field_names = ['user_id', 'tweet_len_avg','sentiment_avg','count_tweets','follows_walmart','follows_wholefoods']
		writer = csv.writer(file, delimiter=',')
		writer.writerow(field_names)
		writer.writerows(processed)	

	print(f"Tweepy_analysis.csv created.")

walmart_followers_list, wholefoods_followers_list = process_to_list("followers_walmart.json", "followers_wholefoods.json")
# print(walmart_followers, end="\n")
# print(wholefoods_followers, end="\n")

clean_and_analyze('tweet_stream.json', walmart_followers_list, wholefoods_followers_list)



