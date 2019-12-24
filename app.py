import tweepy
import os

from dotenv import load_dotenv
load_dotenv()

#load gcloud nlp libraries
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types


CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)


api = tweepy.API(auth)
client = language.LanguageServiceClient()

fetched_tweet  = api.search('donald trump', result_type='recent', count = '10')

text_list = []
for tweet in fetched_tweet:
    tweetTxt = tweet.text
    # get sentiment
    document=types.Document(
         content = tweetTxt,
         type = enums.Document.Type.PLAIN_TEXT
    )
    sentiment = client.analyze_sentiment(document=document).document_sentiment
    text_list.append([tweet.text, sentiment.score, sentiment.magnitude])

