from textblob import TextBlob
from elasticsearch import Elasticsearch
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import tweepy

consumer_key=""
consumer_secret=""

access_token=""
access_token_secret=""

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

class StdOutListener(StreamListener):

    def on_data(self, data):
        try:
            allData = json.loads(data)
            tweetText = TextBlob(allData["text"])

            print tweetText
            print tweetText.sentiment.polarity
            #print allData['entities']['hashtags']
            #print allData['user']['location']
            #print allData['user']['followers_count']
            #print allData['favorite_count']
            #print allData['place']['country']


            #print allData['coordinates']

            # tweetText.word_counts   for later
            if tweetText.sentiment.polarity > 0:
                sentiment = "positive"
            elif tweetText.sentiment.polarity == 0:
                sentiment = "netural"
            else: sentiment = "negative"

            es.index(index="sentiment3",
                     doc_type="test",
                     body={
                           "author": allData["user"]["screen_name"],
                           "date": allData["created_at"],
                           "message": allData["text"],
                           "polarity": tweetText.sentiment.polarity,
                            "sentiment":sentiment,
                           }

                      )
        except KeyError:

            return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    api = tweepy.API(auth)

    trends1 = api.trends_place(1)
    # trends1 is a list with only one element in it, which is a dict
    #print trends1
    data = trends1[0]
    # grab the trends
    trends = data['trends']
    # grab T.T
    trend = (trends[0])
    print trend['name']
    #get name
    name = str(trend['name'])

    #start stream
    stream.filter(languages=["en"],track = [name])

