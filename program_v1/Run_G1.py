# Eli Bolotin
# Nov 4 2018
# DS710: Final Project

from GetTweets import *
from ProcessTweets import *

keywords1 = ['health fitness','get fit','fitness','legday','workoutwednesday','treadmill','pilates','yoga','gym time','deadlift','squats','FitnessFriday','gymlife','workouts','fitness training','postgym','armday','shoulderday','fitnessgoals','runner','workout','workout motivation','lift hard','lift weight','go running','sweat forit','crossfit','morning workout','muscle','six pack','lunges','cardio','elliptical','cycling']

keywords2 = ['#health','#gymtime','#fitnesstraining','#workoutmotivation','#lifthard','#liftweight','#gorunning','#sweatforit','#morningworkout','#sixpack','#triathlon']

keywords = keywords1 + keywords2

########################
#	Manual Execution   
########################

### step 1
stream_tweets(keywords, option = 'user_info', file_name = 'streamed_tweets_workout', max_tweets = 10)

### step 2 (returns file appended with _clean)
# clean_tweets("streamed_tweets_workout.json") 

### step 3 (returns file appended with _truncated)
# get_full_tweets("streamed_tweets_workout_clean.csv")

### step 4 (returns file appended with _clean)
# clean_tweets("streamed_tweets_workout_clean_full_truncated.json", tweets_type="full")

### step 5 - produce sentiment analysis of cleaned tweets. Remember, we are cleaning the full file, not the truncated version (which is the same as the full file, only less columns for readability).
# analyze_tweets("streamed_tweets_workout_clean_full.json")
