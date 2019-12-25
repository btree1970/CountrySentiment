import tweepy
import json
import os

from dotenv import load_dotenv
load_dotenv()


CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)


api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
client = language.LanguageServiceClient()


#Twitter id for each other, the 
# for state in stateID:
#      geostates = api.geo_search(query=state, granularity="city")
#      for geostate in geostates:
#           if geostate.name == stateID[state]:
#                print(geostate.name, geostate.id)
#

with open('stateAbbrev.json', "r") as states:
     stateID = json.load(states)

with open('stateID.json', "r") as states:
     stateCodes = json.load(states)

def getTweets():
     tweetsByState = {}
     for state in stateCodes:
          tweetsByState[state] = []
     for state in stateCodes:
          stateCode = stateCodes[state]
          tweets = api.search(q="place:{}".format(stateCode), result_type="mixed", count=100)
     
          for tweet in tweets:
               tweetsByState[state].append(tweet.text)

with open('tweetState.txt', 'w') as outfile:
    json.dump(tweetsByState, outfile,  indent=4)


