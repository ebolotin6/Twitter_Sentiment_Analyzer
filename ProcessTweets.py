# Eli Bolotin
# Twitter Sentiment Analysis Program
# Copyright 2018, All Rights Reserved.

from TwitterProgram import StreamedTweets, TweetProgram

########################
#	Auto Execution   
########################

######### Group 1 #########

# ### step 1 stream tweets
# ### step 2 instantiate object and clean tweets
# group_1 = StreamedTweets("streamed_tweets_media.json", sub_dir="Experiment_2")
# group_1.clean_tweets()

# ### step 3: fetch other tweets
# group_1.get_full_tweets(max_users = 2000)

# ### step 4: clean the fetched tweets
# group_1.clean_tweets(tweets_type = "full")

# ### step 5 - produce sentiment analysis of cleaned tweets. Remember, we are cleaning the full file, not the truncated version (which is the same as the full file, only less columns for readability).
# group_1.get_sentiment()

######### Group 2 #########

### step 1 stream tweets
### step 2 instantiate object and clean tweets
group_2 = StreamedTweets("streamed_tweets_fitness.json", sub_dir="Experiment_2")
group_2.clean_tweets()

### step 3: fetch other tweets
group_2.get_full_tweets(max_users = 2000)

### step 4: clean the fetched tweets
group_2.clean_tweets(tweets_type = "full")

### step 5 - produce sentiment analysis of cleaned tweets. Remember, we are cleaning the full file, not the truncated version (which is the same as the full file, only less columns for readability).
group_2.get_sentiment()