from google.appengine.ext import ndb

class MyUser(ndb.Model):
    email_address = ndb.StringProperty()
    username = ndb.StringProperty()
    followers = ndb.StringProperty(repeated = True)
    following = ndb.StringProperty(repeated = True)
    full_name = ndb.StringProperty()
    description = ndb.StringProperty()
    userid = ndb.StringProperty()
    no_of_tweets = ndb.IntegerProperty(default = 0)

class TweetModel(ndb.Model):
    tweet_id = ndb.IntegerProperty()
    tweet_text = ndb.StringProperty()
    tweet_time = ndb.DateTimeProperty()
    tweet_username = ndb.StringProperty()
