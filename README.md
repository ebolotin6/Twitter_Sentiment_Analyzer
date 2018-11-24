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

### Directions -

See Directions.ipynb

Copyright 2018, All Rights Reserved.