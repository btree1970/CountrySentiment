# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_render_template]



import json
import os
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request
from app import loadAllTweetsandGetScores
from storageUtils import Storage



app = Flask(__name__, template_folder="static")


def valid_cron(handler):
    @wraps(handler)
    def check_valid_cron(*args, **kwargs):
        if request.headers.get('X-AppEngine-Cron') is None:
            print(request.headers)
            return "Unauthourized user", 401
        else:
            return handler(*args, **kwargs)
    return check_valid_cron


@app.route("/api/score/<string:topicID>")
def getSenimentScores(topicID):

    fileName = 'data/sentiments/tweetSentiments_{}_score.json'.format(topicID)
    sentimentScores = json.loads(Storage.load(fileName))

    return sentimentScores

@app.route("/api/tweets/<topicID>")
def getTweets(topicID):

    fileName = 'data/twitterData/tweetState_{}.txt'.format(topicID)
    tweets = json.loads(Storage.load(fileName))

    return tweets

@app.route("/api/tags/")
def getPopularTags():

    return json.load(open('data/topics.json', 'r'))


@app.route("/cron" )
@valid_cron
def seceduler():
    loadAllTweetsandGetScores()

    currentTime = datetime.now()
    open('data/lastupdatetime.txt', 'w').write(currentTime.strftime("%Y-%m-%d %H:%M:%S"))

    return 'update successful'

    

@app.route('/')
def root():
   
    #get last update time
    lastUpdateTime = open('data/lastupdatetime.txt', 'r').read().strip()
    return render_template('index.html', lastUpdateTime=lastUpdateTime)


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [START gae_python37_render_template]

