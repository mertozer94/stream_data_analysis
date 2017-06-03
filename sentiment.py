from textblob import TextBlob
import bot
from elasticsearch import Elasticsearch
from tweepy.streaming import StreamListener
from tweepy import Stream
import json

es = Elasticsearch()
class MyStreamListener(StreamListener):

    def on_data(self, data):
        try:
            allData = json.loads(data)
            tweetText = TextBlob(allData["text"])

            print tweetText
            print tweetText.sentiment.polarity
            print allData['entities']['hashtags']
            print allData['user']['location']
            print allData['user']['followers_count']
            print allData['favorite_count']
            #print allData['geo']

            #latitude = (allData["geo"]["coordinates"][0])
            #longitude = (allData["geo"]["coordinates"][1])

            if tweetText.sentiment.polarity > 0:
                sentiment = "positive"
            elif tweetText.sentiment.polarity == 0:
                sentiment = "netural"
            else:
                sentiment = "negative"

            es.index(index="elastic",
                     doc_type="myType",
                     body={
                           "author": allData["user"]["screen_name"],
                           "date": allData["created_at"],
                           "message": allData["text"],
                           "polarity": tweetText.sentiment.polarity,
                           "sentiment":sentiment,
                           "hastags": allData['entities']['hashtags'],
                           "followers_count": allData['user']['followers_count'],
                           #"location": str(latitude) + "," + str(longitude) #for later
                           }

                      )
        except KeyError:
            return False

        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    myBot = bot.TwitterBot()

    l = MyStreamListener()
    auth = myBot.getAuth()
    stream = Stream(auth, l)

    trend = myBot.getTrend()

    #start stream
    stream.filter(languages=["en"],track = [trend])

