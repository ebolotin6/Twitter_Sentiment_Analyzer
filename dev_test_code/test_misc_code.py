# from textblob import TextBlob
import json
import pprint
from textblob import TextBlob as Textblob

# blob = TextBlob("Analytics Vidhya is a great platform to learn data science.")
# print(blob.sentiment[0])


# with open("new_stream.json", 'r') as file:
# 	file = json.load(file)
# pprint.pprint(file[0])

# hash_dict = {}
# tweets_list = []
# loop = 0
# for tweet in file:
# 	if loop < 1:
# 		user_id = tweet['user']['id']
# 		screen_name = tweet['user']['screen_name']
# 		tweet_id = tweet['id']
# 		tweet_text = tweet['extended_tweet']['full_text']
# 		tweet_len = len(tweet_text)
# 		sentiment = Textblob(tweet_text).sentiment[0]
# 		for hashtag in tweet['extended_tweet']['entities']['hashtags']:
# 			hashtag = hashtag['text']
# 			if hashtag in hash_dict:
# 				hash_dict[hashtag] += 1
# 			else:
# 				hash_dict[hashtag] = 1
		
# 		current_tweet = (user_id, screen_name, tweet_id, tweet_text, tweet_len, sentiment, hash_dict)
# 		tweets_list.append(current_tweet)
# 		loop += 1
# 	else:
# 		break

# print(tweets_list)

# print(hash_dict)

# with open("testfile1.json", "w+") as file:
# 	ls = []
# 	x = 1
# 	while x < 10:
# 		ts = [1, 2, 3]
# 		ls.extend(ts)
# 		file.seek(0)
# 		file.write(json.dumps(ls) + "\n")
# 		x += 1
with open("users_workoutgroup.json", "r") as file:
# with open("users_workoutgroup.json", "r") as file:
	file = json.load(file)
	print(len(file), end="\n")
	for i, row in enumerate(file):
		print(f'{i} ---- {row[1]}')
