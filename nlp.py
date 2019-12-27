import json
import time

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

client = language.LanguageServiceClient()


with open('data/tweetState.txt', 'r') as newTweets:
      fetched_tweet = json.load(newTweets)

sentimentScore = {}

numRequest = 0
for state in fetched_tweet:
      totalSentiment, tweetCount = 0, 0
      tweetsByCountry = fetched_tweet[state]
      for tweets in tweetsByCountry:
               
                document=types.Document(
                content = tweets,
                type = enums.Document.Type.PLAIN_TEXT
                )
                sentiment = client.analyze_sentiment(document=document).document_sentiment
                #threshold
                if abs(sentiment.score) > 0.3:
                    totalSentiment += (sentiment.score * sentiment.magnitude)
                    tweetCount += 1
                numRequest += 1
                 #600 requests per minute
                if numRequest == 599:
                    print("sleeping for 60 sec")
                    time.sleep(61)
                    numRequest = 0
      sentimentScore[state] = totalSentiment/tweetCount

with open('data/tweetSentiments.json', 'w') as scores:
      json.dump(sentimentScore, scores,  indent=4)
      
