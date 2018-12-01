# Twitter Sentiment Analyzer
### Notes on Regex filter in clean_tweets() method of TwitterProgram class
#### Author: Eli Bolotin



This regex filter is designed to filter out specifc tweets (and users) from the streamed tweets file. Below is a breakdown of exactly what is filtered out:

**[^\u0000-\u007F]{5,}** 
- Str begins with 5 or more non-ASCII letters. Meant to filter out non-English tweets.

**^\\s\*$**
- Str begins and ends with 0 or more spaces

**\W{7,}**
- Str contains 7 or more non-word characters

**^(\d)+**
- Str begins and ends with one or more decimal digits

**^(#\\w\\b)+**
- Str begins with one or more words followed by non-words

**^\\"**
- Str begins with quotes

**^\***
- Str begins with astericks

**^[A-Z]{5, }**
- Str begins with 5 or more capital characters

**[A-Z]$**
- Str ends with capital characters

**^How**
- Str starts with "How"

**^The\\s\\d+**
- Str starts with the word "the" followed by a space and a number

**^Photos**
- Str begins with the word "Photos"

**(\\'\\')+**
- Str begins with one or more backslashes

**(top\s\d+|free|buy|get|class|connect|discount|now|read|job|video|news|follow|added|review|publish|clubs|manager|study|success|limited|sex|release|help|gift|ideas|massage|schedule|services|check|join|pain|therapy|alternative|new\schallenge|product|need|learn|
for\smen|for\swomen|revolution|leadership|weight\sloss|diet\splan|ebay|click|promo|certified|store|pick|sign|log-in|login|tips|meet|secret|improve|listen|**
- Str contains any one of these words or phrases

**(\\w+)for(\\w+)**
- Str contains one or more words followed by for followed by one or more words

**trainer)**
- Str contains the word trainer

**\\$**
- Str contains a $ symbol

**\+**
- Str contains a + symbol

**\\@**
- Str contains an @ symbol

**\\?**
- Str contains a ? symbol

**\\?$**
- Str ends with a question mark

**(\.\n\.)**
- Str contains a period followed by a new line followed by a period

**^\$**
- Str starts with $


Copyright 2018 Eli Bolotin, All Rights Reserved.