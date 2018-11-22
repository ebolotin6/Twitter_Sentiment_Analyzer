# Eli Bolotin
# Twitter Sentiment Analysis Program
# Copyright 2018, All Rights Reserved.

from TwitterProgram import MyStreamListener, stream_tweets

keywords_m1 = ['watching show','watch season','netflix','movie','new season','watching tv','binge watching','newseries','new episode','prime video','dvr','atthemovies','film','horror','comedy','thriller','shortfilm','firstseason','secondseason','thirdseason','fourthseason','fithseason','lastseason']

keywords_m2 = ['#watchingshow','#watchseason','#newseason','#watchingtv','#bingewatching','#newepisode','#primevideo','#edgeofmyseat','#nbc','#abc','#disney','#cnbc','#cbs','#primetime','#waitedsolong','#comedycentral']

keywords_f1 = ['health fitness','fitness','legday','workoutwednesday','treadmill','pilates','yoga','gym time','deadlift','squats','FitnessFriday','gymlife','workouts','fitness training','postgym','armday','shoulderday','fitnessgoals','runner','workout','workout motivation','lift hard','lift weight','go running','crossfit','morning workout','muscle','six pack','lunges','cardio','elliptical','cycling']

keywords_f2 = ['#health','#gymtime','#fitnesstraining','#workoutmotivation','#lifthard','#liftweight','#gorunning','#sweatforit','#morningworkout','#sixpack','#triathlon']

keywords_m = keywords_m1 + keywords_m2
keywords_f = keywords_f1 + keywords_f2

########################
#	 Execution   
########################

### step 1: media group
file_name_m = stream_tweets(keywords_m, option = 'user_info', file_name = 'streamed_tweets_media', max_tweets = 4000)

### step 1: athletic group
file_name_a = stream_tweets(keywords_f, option = 'user_info', file_name = 'streamed_tweets_fitness', max_tweets = 4000)