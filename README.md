# Twitter Sentiment Analyzer
### Create sentiment analysis for Twitter data
#### Author: Eli Bolotin

### Program Description -

The purpose of this program is to collect, clean, and perform sentiment analysis on Twitter data (tweets).

* Type of sentiment analysis performed:
	* NLTK VADER
	* TextBlob

* Program consists of 3 files:
	* **TwitterProgram.py** - core program
	* **StreamTweets.py** - executes steps 1, 2
	* **ProcessTweets.py** - executes steps 3, 4, 5

### Example experiment -

This program was originally designed to answer the following question:
* Are people that talk about fitness happier than people that talk about media (tv, movies, youtube, etc.)?
* This is an experiment in which we are comparing 2 different groups.

Consider 2 groups (example): people that tweet about fitness and people that tweet about media. To conduct the experiment, follow the steps below:

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
	- **TwitterProgram.py** is a program that conducts the pre-work for a statistics experiment. In 4 methods, data is collected, cleaned, and analyzed for sentiment. This requires various packages that take time to load.
2. Make sure your Twitter credentials are valid. See instructions.
3. High-volume requests to Twitter's (free) API may result in a ban. Be careful.

### Sources on sentiment analysis

* NLTK Vader
	* (VADER Sentiment Analysis Explained)[http://datameetsmedia.com/vader-sentiment-analysis-explained/]
	* (Tutorial)[https://nlpforhackers.io/sentiment-analysis-intro/]
	* (Source code)[https://www.nltk.org/_modules/nltk/sentiment/vader.html]

* TextBlob
	* (Documentation)[https://textblob.readthedocs.io/en/dev/]

Copyright 2018 Eli Bolotin