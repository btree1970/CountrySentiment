import tweepy
import json
import os
import re

from dotenv import load_dotenv
load_dotenv()


CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)


api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)




with open('stateAbbrev.json', "r") as states:
     stateID = json.load(states)

# #Twitter id for each other, the 
# index = 0
# for state in stateID:
#      if index > 10:
#           geostates = api.geo_search(query=state, granularity="city")
#           for geostate in geostates:
#                if geostate.name == stateID[state]:
#                     print(geostate.name, geostate.id)
#      index += 1

with open('data/stateID.json', "r") as states:
     stateCodes = json.load(states)

def getTweets():
     tweetsByState = {}
     for state in stateCodes:
          tweetsByState[state] = []
          
     for state in stateCodes:
          stateCode = stateCodes[state]
          tweets = api.search(q="place:{} lang:en trump".format(stateCode), result_type="mixed", count=200)
     
          for tweet in tweets:
               if len(tweet.text) > 10:
                    tweetsByState[state].append(preprocess(tweet.text))
     
     with open('data/tweetState.txt', 'w') as outfile:
          json.dump(tweetsByState, outfile, ensure_ascii=False, indent=4)

     return tweetsByState


def preprocess(tweet):
     # remove urls and non-ascii characters
      return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

getTweets()





