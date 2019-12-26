import json

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

client = language.LanguageServiceClient()


with open('tweetState.txt', 'r') as newTweets:
      fetched_tweet = json.load(newTweets)

text_list = []
for state in fetched_tweet:
      totalSentiment = 0
      tweetsByCountry = fetched_tweet[state]
      for tweets in tweetsByCountry:
                document=types.Document(
                content = tweets,
                type = enums.Document.Type.PLAIN_TEXT
                )
                sentiment = client.analyze_sentiment(document=document).document_sentiment
                totalSentiment += sentiment.score

      text_list.append([state, totalSentiment/len(tweetsByCountry)])
      
print(text_list)
