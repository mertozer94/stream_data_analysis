import tweepy
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from tweepy import Stream

class TwitterBot:

    consumer_key = ""
    consumer_secret = ""

    access_token = ""
    access_token_secret = ""

    def __init__(self):



        return
    def getAuth(self):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)

        return auth
    def getApi(self):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)

        return tweepy.API(auth)

    def getTrend(self):

        trends1 = self.getApi().trends_place(1)
        # trends1 is a list with only one element in it, which is a dict
        # print trends1
        data = trends1[0]
        # grab the trends
        trends = data['trends']
        # grab T.T
        trend = (trends[0])
        print "Trend name is ", trend['name']
        # get name
        return  str(trend['name'])

    def getCursor(self):
        return tweepy.Cursor

