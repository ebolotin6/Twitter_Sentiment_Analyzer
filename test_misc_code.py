# from textblob import TextBlob
import json
import pprint
# from nltk.sentiment.vader import SentimentIntensityAnalyzer
# from sklearn.metrics import accuracy_score
# import dateutil.parser

# from textblob import TextBlob as Textblob
# import re
# from GetTweets import *

#############

# blob = TextBlob("Analytics Vidhya is a great platform to learn data science.")
# print(blob.sentiment[0])

#############

with open("streamed_tweets_athletic.json", 'r') as file:
	file = json.load(file)
	pprint.pprint(len(file))

#############

# with open("streamed_tweets_workout_clean_full.json", 'r') as file:
# 	file = json.load(file)
# 	users = file

# all_indices = []
# all_tweets = []
# index = 0

# for user in users:
# 	for tweet in user:
# 		all_indices.append(index)
# 		all_tweets.append(tweet)
# 		index += 1

# print(all_indices, end="\n\n")

# with open("streamed_tweets_workout_clean_full_truncated_clean.json", 'r') as file:
# 	file = json.load(file)
# 	filtered_tweets = file

# filtered_excel_indices = []

# for tweet in filtered_tweets:
# 	filtered_excel_indices.append(tweet[0])

# filtered_tweets = [all_tweets[excel_index-1] for excel_index in filtered_excel_indices]

#############

# with open("streamed_tweets_movies_clean_full.json", 'r') as file:
# 	file = json.load(file)
# 	pprint.pprint(len(file))

#############

# hashtag_dict = {}
# tweets_list = []

# for tweet in file:
# 	user_id = tweet['user']['id']
# 	screen_name = tweet['user']['screen_name']
# 	tweet_id = tweet['id']
# 	tweet_text = tweet['extended_tweet']['full_text']
# 	tweet_len = len(tweet_text)
# 	sentiment = Textblob(tweet_text).sentiment[0]
# 	followers_count = tweet['user']['followers_count']
# 	friends_count = tweet['user']['friends_count']
# 	favorites_count = tweet['user']['favourites_count'] 

# 	for hashtag in tweet['extended_tweet']['entities']['hashtags']:
# 		hashtag = hashtag['text']
# 		if hashtag in hashtag_dict:
# 			hashtag_dict[hashtag] += 1
# 		else:
# 			hashtag_dict[hashtag] = 1
	
# 	current_tweet = (user_id, screen_name, tweet_id, tweet_text, tweet_len, sentiment, hashtag_dict)
# 	tweets_list.append(current_tweet)

#############

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

#############

# with open("users_mediagroup" + ".json", "r") as file:
# with open("users_workoutgroup.json", "r") as file:
# with open("users_workoutgroup.json", "r") as file:
# 	try:
# 		file = json.load(file)
# 		print(len(file), end="\n")
# 		# for i, row in enumerate(file):
# 		# 	print(f'{i} ---- {row[3]}')
# 	except Exception as e:
# 		print(e)

#############

# line = '#GrandOpeningSale Shop https://t.co/EEO3NThR1X #Follow us to see a #NEW #DESIGN EVERY DAY! #nyc #newyork #love discount.com @ + - $... https://t.co/VN5xAEmUJ5'

# line1 = 'Do it while you can, please'
# line2 = 'The Backlund house is #haunted, but no one knows why - In The House Of In Between by @JDBuffington is available at… https://t.co/FTYkxX0bz2'
# line3 = 'Check out #NYCMetroFandom for upcoming #comics and #prowrestling events!'
# line4 = 'https://t.co/dH3yEfMWqG  As  for  you overpaid pieces of... #30rock #30rockefellerplaza #showrunner #sitcom #pilot… https://t.co/SBly2FYl4T'
# line5 = 'Meet Hope &amp; Tess! How much will these teleporting twins impact the fate of the Universe? Read the FINDERS KEEPERS… https://t.co/KeQRTtlPoz'
# line6 = 'Great book and you should order yourself a copy:)'
# line7 = '"Permission To Come Aboard Sir" Scene In American Comedy Movie Ace Ventura: Pet Detective (1994) - Jim Carrey As Ac… https://t.co/l3Qog5gS0G'
# line8 = 'Check out the new website!'
# line9 = 'Ski Magazine Subscription 1 Yr  $4.69 https://t.co/9twKxYzdaT #skiing #magazine #paris #model #fitness #fashion… https://t.co/fpOi3Txuol'

# line = 'Like so many, I leaned a lot about the life of veterans after watching The West Wing. Yet when I chatted with… https://t.co/EQQQFvGevF'

# match = re.findall(r'^(\d)+|^(#\w\b)+|^\"|^\*|^[A-Z]{5, }|[A-Z]$|^How|^The\s\d+|^Photos|(\'\')+|(\.org|\.net|\.com)|(free|buy|get|class|connect|discount|now|read|job|video|news|follow|added|review|publish|clubs|manager|study|success|limited|release|help|gift|ideas|massage|schedule|services|check|join|pain|therapy|alternative|new\schallenge|product|need|learn|for\smen|for\swomen|revolution|leadership|ebay|pick|sign|log-in|login|tips|meet|secret|improve|listen|(\w+)for(\w+)|trainer)|(\$|\+|\@|\?|\?$)|(\.\n\.)', line, flags = re.MULTILINE | re.IGNORECASE)

# regex = re.compile(r'^(\d)+|^(#\w\b)+|^\"|^\*|^[A-Z]{5, }|[A-Z]$|^How|^The\s\d+|^Photos|(\'\')+|(\.org|\.net|\.com)|(free|buy|get|class|connect|discount|now|read|job|video|news|follow|added|review|publish|clubs|manager|study|success|limited|release|help|gift|ideas|massage|schedule|services|check|join|pain|therapy|alternative|new\schallenge|product|need|learn|for\smen|for\swomen|revolution|leadership|ebay|pick|sign|log-in|login|tips|meet|secret|improve|listen|(\w+)for(\w+)|trainer)|(\$|\+|\@|\?|\?$)|(\.\n\.)', re.IGNORECASE)

# match = regex.search(line)

# print(match)
 	
#############

# sentences = ["VADER is smart, handsome, and funny.","VADER is smart, handsome, and funny!","VADER is very smart, handsome, and funny.", "VADER is VERY SMART, handsome, and FUNNY.", "VADER is VERY SMART, handsome, and FUNNY!!!", "VADER is VERY SMART, really handsome, and INCREDIBLY FUNNY!!!", "The book was good.", "The book was kind of good.","The plot was good, but the characters are uncompelling and the dialog is not great.", "A really bad, horrible book.","At least it isn't a horrible book.",":) and :D","","Today sux","Today sux!","Today SUX!", "Today kinda sux! But I'll get by, lol"]

# sid = SentimentIntensityAnalyzer()

# for sentence in sentences:
# 	ss = sid.polarity_scores(sentence)	
# 	print(f"{sentence}: {ss['compound']}")


