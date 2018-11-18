# Eli Bolotin
# Nov 4 2018
# DS710: Final Project

import tweepy
import csv
from twitter_credentials import *

# OAuth process, using the keys and tokens
# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)
 
# Creation of the actual interface, using authentication
# api = tweepy.API(auth)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
 
id_cocacola = api.get_user(screen_name = "CocaCola").id
id_pepsi = api.get_user(screen_name = "pepsi").id
climate_tweets = api.search(q = "%23climate OR %23environment", count = 100)
climate_user_ids = [tweet.user.id for tweet in climate_tweets]
coke_fans = []

for user_id in climate_user_ids:
	following_coke = api.show_friendship(source_id = user_id, target_id = id_cocacola)[0].following
	following_pepsi = api.show_friendship(source_id = user_id, target_id = id_pepsi)[0].following
	user_following = tuple((user_id, following_coke, following_pepsi))
	coke_fans.append(user_following)
 
with open('preferredsoda.csv', 'w') as file: 
	field_names = ['user_id', 'following_coke','following_pepsi']
	writer = csv.writer(file, delimiter=',')
	writer.writerow(field_names)
	writer.writerows(coke_fans)


