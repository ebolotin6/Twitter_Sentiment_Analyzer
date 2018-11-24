# Twitter Sentiment Analyzer
### A program for generating sentiment analysis on Twitter data
#### Author: Eli Bolotin

### Program Description -

1. This program generates (NLTK) sentiment analysis using self-collected and cleaned Twitter data.
2. The TSA program consists of 3 files:
	* TwitterProgram.py - core program
	* StreamTweets.py - executes step 1 
	* ProcessTweets.py - executes steps 2, 3, 4
3. Output: sentiment analysis

### Experiment Description -

The original question that this program was designed to answer was:
* Are people that talk about fitness happier than people that talk about media (tv, movies, youtube, etc.)?
* This is an experiment in which we are comparing 2 different groups (samples).

### Example experiment -

Consider 2 groups (example): people that talk (tweet) about fitness and people that tweet about media. To conduct the experiment, follow the steps below:

1. Create (unbiased) keywords and hashtags that define these groups. 
2. Stream tweets using keywords/hashtags for both groups (Twitter Stream API)
3. Clean the streamed tweets (via program)
4. Fetch other (non-filtered) tweets for users in streamed groups.
5. Run sentiment analysis for fetched tweets.
6. Conduct statistical analysis in R.

### Instructions -

1. Add your twitter credentials to *twitter_credentials.py*
2. See *instructions.ipynb* for instructions on how to execute program.

### Important notes before using:

1. Install any missing packages and be patient when they load.
	- TwitterProgram.py is an entire statistics experiment built into a relatively simple program. In 5 methods, data is collected, cleaned, and analyzed for sentiment.
2. Make sure your Twitter credentials are valid. See instructions.
3. This program is designed to run efficiently and to handle Twitter rate limiting without interruption. However, do not abuse Twitter's API request/access policy, as they will ban you.
4. Use this program responsibly.

Copyright 2018, All Rights Reserved.