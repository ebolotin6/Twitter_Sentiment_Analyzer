# Eli Bolotin
# Nov 4 2018
# DS710: Final Project

import tweepy
from twitter_credentials import *

# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
 
# Creation of the actual interface, using authentication
api = tweepy.API(auth)
# api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
 
coke_followers = api.followers(screen_name = "CocaCola")
# coke_followers = api.followers_ids(screen_name = "CocaCola")

statuses = []

for i, follower in enumerate(coke_followers):
	i += 1
	try:
		status = follower._json['status']['text']
		statuses.append(tuple((i, status)))
	except:
		pass

print(len(coke_followers))
print(statuses)

# cf_tweets = coke_followers._json['status']['text']
# pepsi_followers = api.followers(screen_name = "pepsi")
# count_coke_followers = len(coke_followers)
# count_pepsi_followers = len(pepsi_followers)
# climate_users = api.search_user(q='#climatechange OR #climate OR #climatechangeisreal')
# tweet_list = api.search(q='#%23datascience') #%23 is used to specify '#'
# print(len(coke_followers))
# print(users_list)
# print(statuses)