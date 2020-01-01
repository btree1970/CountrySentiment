import json
import time
import logging
import os

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from google.api_core import retry
from google.api_core.retry import if_transient_error
from google.api_core.exceptions import ResourceExhausted

logger = logging.getLogger('google.api_core.retry')

#transient_error
# google.api_core.exceptions.InternalServerError - HTTP 500, gRPC
# google.api_core.exceptions.TooManyRequests - HTTP 429
# google.api_core.exceptions.ServiceUnavailable - HTTP 503
# google.api_core.exceptions.ResourceExhausted - gRPC


client = language.LanguageServiceClient()
   
                  
def getSenimentScoreForTopic (topic):
      with open('data/twitterData/tweetState_{}.txt'.format(topic), 'r') as newTweets:
            fetched_tweet = json.load(newTweets)
      sentimentScore = {}
      numRequest = 0
      for state in fetched_tweet:
            totalSentiment, tweetCount = 0, 0
            tweetsByState = fetched_tweet[state]
            print(state)
            for tweets in tweetsByState:
                  document=types.Document(
                  content = tweets,
                  type = enums.Document.Type.PLAIN_TEXT
                  )

                  #use exponential back-off to adjust for resource exhaustion
                  exp_retry =  retry.Retry(predicate=if_transient_error, initial=1, maximum=240, multiplier=2, deadline=480)
                  
                  sentiment = client.analyze_sentiment(document=document, retry=exp_retry).document_sentiment
                  if abs(sentiment.score) > 0.20:
                        totalSentiment += (sentiment.score * sentiment.magnitude)
                        tweetCount += 1

            if tweetCount == 0:
                  sentimentScore[state] = 0
            else:
                  sentimentScore[state] = totalSentiment/tweetCount

      with open('data/sentiments/tweetSentiments_{}_score.json'.format(topic), 'w') as scores:
            json.dump(sentimentScore, scores,  indent=4)    
                  


# def getSenimentScoreForTopic (topic):
#       with open('data/twitterData/tweetState_{}.txt'.format(topic), 'r') as newTweets:
#             fetched_tweet = json.load(newTweets)
#       sentimentScore = {}
#       numRequest = 0
#       for state in fetched_tweet:
#             totalSentiment, tweetCount = 0, 0
#             tweetsByCountry = fetched_tweet[state]
#             for tweets in tweetsByCountry:
#                   document=types.Document(
#                   content = tweets,
#                   type = enums.Document.Type.PLAIN_TEXT
#                   )
#                   while True:
#                         shouldBreak = False
#                         try:
#                            print('getting sentiment score')
#                            sentiment = client.analyze_sentiment(document=document).document_sentiment
#                            numRequest += 1
#                            print('got sentiment score')
#                            shouldBreak = True
#                         except Exception as inst:
#                               print(inst)
#                         finally:
#                               print(shouldBreak)
#                               if shouldBreak:
#                                     break
#                               print('sleeping for 120 second to mitigate resource exhaustion')
#                               time.sleep(120)
#                   if numRequest > 500:
#                         print('sleeping for 30 sec')
#                         time.sleep(30)
#                   threshold
#                   if abs(sentiment.score) > 0.3:
#                         totalSentiment += (sentiment.score * sentiment.magnitude)
#                         tweetCount += 1

#             if tweetCount == 0:
#                   sentimentScore[state] = 0
#             else:
#                   sentimentScore[state] = totalSentiment/tweetCount

#       with open('data/sentiments/tweetSentiments_{}_score.json'.format(topic), 'w') as scores:
#             json.dump(sentimentScore, scores,  indent=4)    
                  
