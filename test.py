import sys,getopt,datetime,codecs
if sys.version_info[0] < 3:
    import got
else:
    import got3 as got

tweetCriteria = got.manager.TweetCriteria().setQuerySearch('Hello')
print(tweetCriteria)
tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]
print(tweet[0])
#for t in tweet:
#	print(t.text)