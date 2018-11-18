# Eli Bolotin
# Nov 4 2018
# DS710: Final Project

from GetTweets import *
from ProcessTweets import *

keywords1 = ['watching','watching show','greatest show','watch season','netflix','favorite show','best show','greatest movie','great acting','new season','watching tv','binge watching','newseries','binging','new episode','prime video','bestshowever','dvr','worst show','worst movie','love the movie','oscar worthy','movie sucks','atthemovies','film','horror','comedy','shortfilm']

keywords2 = ['#watchingshow','#greatestshow','#watchseason','#favoriteshow','#bestshow','#greatestmovie','#greatacting','#newseason','#watchingtv','#bingewatching','#newepisode','#primevideo','#worstshow','#worstmovie','#lovethemovie','#oscarworthy','#moviesucks']

keywords = keywords1 + keywords2

########################
#	Manual Execution   
########################

### step 1
# stream_tweets(keywords, option = 'user_info', file_name = 'streamed_tweets_movies', max_tweets = 2000)

### step 2 (returns file appended with _clean)
# clean_tweets("streamed_tweets_movies.json")

### step 3 (returns file appended with _truncated)
# get_full_tweets("streamed_tweets_movies_clean.csv")

### step 4 (returns file appended with _clean)
# clean_tweets("streamed_tweets_movies_clean_full_truncated.json", tweets_type="full")

### step 5 - produce sentiment analysis of cleaned tweets. Remember, we are cleaning the full file, not the truncated version (which is the same as the full file, only less columns for readability).
# analyze_tweets("streamed_tweets_movies_clean_full.json")