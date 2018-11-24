# Eli Bolotin
# Twitter Sentiment Analysis Program
# Copyright 2018, All Rights Reserved.

from TwitterProgram import MyStreamListener, stream_tweets

### Step 1: define keywords and hashtags for media group

keywords_m = ['watching show','watch season','netflix','movie','new season','watching tv','binge watching','newseries','new episode','prime video','dvr','atthemovies','film','horror','comedy','thriller','shortfilm','firstseason','secondseason','thirdseason','fourthseason','fithseason','lastseason','#watchingshow','#watchseason','#newseason','#watchingtv','#bingewatching','#newepisode','#primevideo','#edgeofmyseat','#nbc','#abc','#disney','#cnbc','#cbs','#primetime','#waitedsolong','#comedycentral']

### Step 1: define keywords and hashtags for fitness group

keywords_f = ['health fitness', 'fitness', 'legday', 'workoutwednesday', 'treadmill', 'pilates', 'yoga', 'gym time', 'deadlift', 'squats', 'FitnessFriday', 'gymlife', 'workouts', 'fitness training', 'postgym', 'armday', 'shoulderday', 'fitnessgoals', 'runner', 'workout', 'workout motivation', 'lift hard', 'lift weight', 'go running', 'crossfit', 'morning workout', 'muscle', 'six pack', 'lunges', 'cardio', 'elliptical', 'cycling', '#health', '#gymtime', '#fitnesstraining', '#workoutmotivation', '#lifthard', '#liftweight', '#gorunning', '#sweatforit', '#morningworkout', '#sixpack', '#triathlon']

########################
#	 Execution   
########################


### step 2: stream tweets for media group
file_name_m = stream_tweets(keywords_m, option = 'user_info', file_name = 'streamed_tweets_media', max_tweets = 5000)

### step 2: stream tweets for athletic group
file_name_a = stream_tweets(keywords_f, option = 'user_info', file_name = 'streamed_tweets_fitness', max_tweets = 5000)