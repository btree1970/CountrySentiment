from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types


with open('tweetState.txt', 'r') as newTweets:
    tweet = json.load(newTweets)

print(tweet)

# text_list = []
# for tweet in fetched_tweet:
#     tweetTxt = tweet.text
#     document=types.Document(
#          content = tweetTxt,
#          type = enums.Document.Type.PLAIN_TEXT
#     )
#     sentiment = client.analyze_sentiment(document=document).document_sentiment
#     text_list.append([tweet.text, sentiment.score, sentiment.magnitude])
