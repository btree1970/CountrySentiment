import tweepy
import json
import logging
import sys
import os
import re
from nlp import getSenimentScoreForTopic
from storageUtils import Storage

from dotenv import load_dotenv
load_dotenv()

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)

consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
consoleHandler.setFormatter(formatter)

_LOGGER.addHandler(consoleHandler)

CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)


# _LOGGER.info('fdksjfksdlfj')


api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

with open('data/stateAbbrev.json', "r") as states:
     stateID = json.load(states)

# index = 0
# for state in stateID:
#      if index > 45:
#           geostates = api.geo_search(query=state, granularity="city")
#           for geostate in geostates:
#                if geostate.name == stateID[state]:
#                     print(geostate.name, geostate.id)
#      index += 1

with open('data/stateID.json', "r") as states:
     stateCodes = json.load(states)

topicsMap = json.load(open('data/topics.json', 'r'))


emoticons_happy = set([
    ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
    ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
    '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
    'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
    '<3'
    ])

emoticons_sad = set([
    ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
    ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
    ':c', ':{', '>:\\', ';('
    ])


def preprocess(tweet):
     # remove urls and mentions
     return ' '.join(re.sub("(@[A-Za-z0-9]+)|(\w+:\/\/\S+)", " ", tweet).split())



emotics = emoticons_happy.union(emoticons_sad)


def getTweetsForTopic(topic):
    
     tweetsByState = {}
     for state in stateCodes:
          tweetsByState[state] = []

     max_queries = 6
     for state in stateCodes:
     
          stateCode = stateCodes[state]
          tweets = tweet_batch = api.search(q="place:{} {} lang:en ".format(stateCode,
                                             topicsMap[topic]), result_type="mixed", count=100)
          count = 1

          #strange twitter search behaviour
          #even though search doesn't exceed count there are more results on subsequent search
          while count < max_queries:
               tweet_batch = api.search(q="place:{} {} lang:en ".format(stateCode, topicsMap[topic]),
                                        result_type="mixed",
                                        count=100,
                                        max_id=tweet_batch.max_id)
               tweets.extend(tweet_batch)
               count += 1
          
          for tweet in tweets:
               if len(tweet.text) > 10:
                    tweetsByState[state].append(
                         {
                            'text': preprocess(tweet.text),
                            'retweet_count': tweet.retweet_count,
                            'favourite_count': tweet.favorite_count
                         })
          _LOGGER.info('state {} has loaded {} for topic: {}'.format(state, len(tweets), topicsMap[topic]))
                    
     fileName = 'data/twitterData/tweetState_{}.txt'.format(topic)
     try:   
           Storage.upload(json.dumps(tweetsByState, ensure_ascii=False, indent=4), fileName)
           _LOGGER.info('tweets for {} have been successfully loaded.'.format(topicsMap[topic]))
     except IOError:
                _LOGGER.error('unable to successfuly load files')

     return tweetsByState


def loadAllTweetsandGetScores():
     #loadAll Tweets

     topicvals = topicsMap.keys()

     if topicvals:
          for topic in topicvals:
               getTweetsForTopic(topic)
               getSenimentScoreForTopic(topic)
     else:
          raise ImportError

 

