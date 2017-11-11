# -*- coding: utf-8 -*-
import os
import re
import sys,getopt,datetime,codecs
if sys.version_info[0] < 3:
    import got
else:
    import got3 as got
from textblob import TextBlob



psTweets = 0
ngTweets = 0
ntTweets = 0
numTweets = 0

def main(argv):

	os.remove('/Users/ishitasinha/pwcSentimentStocks/GetOldTweets-python/output_got.csv')

	if len(argv) == 0:
		print('You must pass some parameters. Use \"-h\" to help.')
		return

	if len(argv) == 1 and argv[0] == '-h':
		f = open('exporter_help_text.txt', 'r')
		print f.read()
		f.close()

		return

	try:
		opts, args = getopt.getopt(argv, "", ("username=", "near=", "within=", "since=", "until=", "querysearch=", "toptweets", "maxtweets=", "output="))

		tweetCriteria = got.manager.TweetCriteria()
		outputFileName = "output_got.csv"

		for opt,arg in opts:
			if opt == '--username':
				tweetCriteria.username = arg

			elif opt == '--since':
				tweetCriteria.since = arg

			elif opt == '--until':
				tweetCriteria.until = arg

			elif opt == '--querysearch':
				tweetCriteria.querySearch = arg

			elif opt == '--toptweets':
				tweetCriteria.topTweets = True

			elif opt == '--maxtweets':
				tweetCriteria.maxTweets = int(arg)
			
			elif opt == '--near':
				tweetCriteria.near = '"' + arg + '"'
			
			elif opt == '--within':
				tweetCriteria.within = '"' + arg + '"'

			elif opt == '--within':
				tweetCriteria.within = '"' + arg + '"'

			elif opt == '--output':
				outputFileName = arg
				
		outputFile = codecs.open(outputFileName, "a", "utf-8")

		outputFile.write('username;date;retweets;favorites;text;geo;mentions;hashtags;id;permalink')

		print('Searching...\n')

		def receiveBuffer(tweets):
			global numTweets

			for t in tweets:
				analysis = TextBlob(' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])(\w+:\/\/\S+)", " ", t.text).split()))
				# set sentiment
				if analysis.sentiment.polarity > 0:
					global psTweets
					psTweets = psTweets + 1
				elif analysis.sentiment.polarity == 0:
					global ntTweets
					ntTweets = ntTweets + 1
				else:
					global ngTweets
					ngTweets = ngTweets + 1
				outputFile.write(('\n%d\n%s\n%s\n' % (numTweets,t.date.strftime("%Y-%m-%d %H:%M"), t.text)))
				numTweets = numTweets + 1;

			outputFile.flush();
			print('More %d saved on file...\n' % len(tweets))

		got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer)

	except arg:
		print('Arguments parser error, try -h' + arg)
	finally:
		outputFile.close()
		print('Done. Output file generated "%s".' % outputFileName)

	storageFile = open('storeData.json','wa')

	global psTweets
	global ngTweets
	global ntTweets
	psTweets = psTweets/float(numTweets)
	ngTweets = ngTweets/float(numTweets)
	ntTweets = ntTweets/float(numTweets)
	
	print('Number of total tweets: {}'.format(numTweets))
	print('Number of positive tweets: {}'.format(psTweets))
	print('Number of negative tweets: {}'.format(ngTweets))
	print('Number of neutral tweets: {}'.format(ntTweets))

	storageFile.write('Number of total tweets: {}\n'.format(numTweets))
	storageFile.write('Number of positive tweets: {}\n'.format(psTweets))
	storageFile.write('Number of negative tweets: {}\n'.format(ngTweets))
	storageFile.write('Number of neutral tweets: {}\n'.format(ntTweets))
	storageFile.close()
		
if __name__ == '__main__':
	main(sys.argv[1:])


