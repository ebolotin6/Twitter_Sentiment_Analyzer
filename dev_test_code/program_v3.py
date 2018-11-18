# Eli Bolotin
# Nov 4 2018
# DS710: Final Project

import tweepy
import csv
from textblob import TextBlob
from twitter_credentials import *

# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)
 
# api = tweepy.API(auth)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
 
id_walmart = api.get_user(screen_name = "Walmart").id
id_safeway = api.get_user(screen_name = "Safeway").id
id_wholefoods = api.get_user(screen_name = "WholeFoods").id
id_albertsons = api.get_user(screen_name = "Albertsons").id

tweets = api.search(q = "%23vote OR %23midterms OR %23RockTheVote OR %23democrat OR %23republican", count = 5)

preprocessed = [(tweet.user.id, len(tweet.text), TextBlob(tweet.text).sentiment[0], 1) for tweet in tweets]
all_unique_user_ids = set([tweet.user.id for tweet in tweets])
processed = []

for user_id in all_unique_user_ids:
	count_tweets = 0
	tweet_len_list = []
	sentiment_list = []
	
	for row in preprocessed:
		user_id_c = row[0]
		if user_id == user_id_c:
			tweet_len_list.append(row[1])
			sentiment_list.append(row[2])
			count_tweets += 1
	
	tweet_len_avg = round(sum(tweet_len_list) / count_tweets, 1)
	sentiment_avg = round(sum(sentiment_list) / count_tweets, 1)
	following_walmart = api.show_friendship(source_id = user_id, target_id = id_walmart)[0].following
	following_safeway = api.show_friendship(source_id = user_id, target_id = id_safeway)[0].following
	following_wholefoods = api.show_friendship(source_id = user_id, target_id = id_wholefoods)[0].following
	following_albertsons = api.show_friendship(source_id = user_id, target_id = id_albertsons)[0].following
	row = tuple((user_id, tweet_len_avg, sentiment_avg, count_tweets, following_walmart, following_safeway, following_wholefoods, following_albertsons))
	processed.append(row)
 
with open('tweepy_analysis.csv', 'w') as file: 
	field_names = ['user_id', 'tweet_len_avg','sentiment_avg','count_tweets','following_walmart','following_safeway','following_wholefoods','following_albertsons']
	writer = csv.writer(file, delimiter=',')
	writer.writerow(field_names)
	writer.writerows(processed)


