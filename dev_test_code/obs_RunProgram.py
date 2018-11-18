# Eli Bolotin
# Nov 4 2018
# DS710: Final Project

def run_program(keywords, filename_json, num_users, steps = (1, 2, 3, 4, 5)):
	if isinstance(keywords, list) and isinstance(filename_json, str):
		if 1 in steps:
			### step 1 - stream tweets
			try:
				stream_tweets = stream_tweets(keywords, option = 'user_info', file_name = filename_json, num_users = num_users)
				check_1 = True
			except Exception as e:
				print("Error: ", e)
		
		if 2 in steps and check_1 == True:
			## step 2 - clean streamed tweets (returns file appended with _clean)
			try:
				clean_tweets = clean_tweets(filename_json)
				check_2 = True
			except Exception as e:
				print("Error: ", e)

		# get file name
		filename = filename_json.split(".")[0]

		if 3 in steps and check_2 == True:
			### step 3 - get other tweets for users in streamed tweets (returns file appended with _truncated)
			try:
				get_full_tweets = get_full_tweets(filename + '_clean.csv')
				check_3 = True
			except Exception as e:
				print("Error: ", e)

		if 4 in steps and check_3 == True:
			### step 4 - clean full tweets (returns file appended with _clean)
			try:
				clean_tweets_2 = clean_tweets(filename + "_clean_full_truncated.json", tweets_type="full")
				check_4 = True
			except Exception as e:
				print("Error: ", e)

		if 5 in steps and check_4 == True:
			### step 5 - produce sentiment analysis of cleaned tweets. Remember, we are cleaning the full file, not the truncated version (which is the same as the full file, only less columns for readability)
			try:
				analyze_tweets(filename + "_clean_full.json")
				check_5 = True
			except Exception as e:
				print("Error: ", e)