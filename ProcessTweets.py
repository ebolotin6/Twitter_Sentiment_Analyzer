# Twitter Sentiment Analysis Program
# Eli Bolotin
# Copyright 2018, All Rights Reserved.

from TwitterProgram import StreamedTweets, TweetProgram

######### Group 1 #########

### step 1 and 2: stream tweets (using StreamTweets.py)
### step 3: instantiate object and clean tweets
group_1 = StreamedTweets("streamed_tweets_media.json", sub_dir="Samples_Round_2")
group_1.clean_tweets()

### step 4: fetch other tweets
group_1.get_full_tweets(max_users = 3000)

### step 5 - produce sentiment analysis of cleaned tweets. Remember, we are cleaning the full file, not the truncated version (which is the same as the full file, only less columns for readability).
group_1.get_sentiment()

######### Group 2 #########

### step 1 and 2: stream tweets (using StreamTweets.py)
### step 3: instantiate object and clean tweets
group_2 = StreamedTweets("streamed_tweets_fitness.json", sub_dir="Samples_Round_2")
group_2.clean_tweets()

### step 4: fetch other tweets
group_2.get_full_tweets(max_users = 3000)

### step 5 - produce sentiment analysis of cleaned tweets. Remember, we are cleaning the full file, not the truncated version (which is the same as the full file, only less columns for readability).
group_2.get_sentiment()
