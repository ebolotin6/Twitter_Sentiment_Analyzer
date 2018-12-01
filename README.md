# Twitter Sentiment Analyzer
### Create sentiment analysis for Twitter data
#### Author: Eli Bolotin

### Program Description -

This program serves as an all-in-one method of data collection, cleaning, and sentiment analysis for the purposes of statistical analysis. It is designed for the experiment below.

1. This program creates (NLTK) sentiment analysis using self-collected and cleaned Twitter data.
2. Program consists of 3 files:
	* **TwitterProgram.py** - core program
	* **StreamTweets.py** - executes steps 1, 2
	* **ProcessTweets.py** - executes steps 3, 4, 5
3. Output: sentiment analysis

### Experiment Description -

This program was designed to answer the following question:
* Are people that talk about fitness happier than people that talk about media (tv, movies, youtube, etc.)?
* This is an experiment in which we are comparing 2 different groups.

### Example experiment -

Consider 2 groups (example): people that talk (tweet) about fitness and people that tweet about media. To conduct the experiment, follow the steps below:

1. Create keywords and hashtags that define these groups. 
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
	- TwitterProgram.py is a program that conducts the pre-work for a statistics experiment. In 4 methods, data is collected, cleaned, and analyzed for sentiment. This requires various packages that take time to load.
2. Make sure your Twitter credentials are valid. See instructions.
3. High-volume requests to Twitter's (free) API may result in a ban. Be careful.

Copyright 2018 Eli Bolotin, All Rights Reserved.