from google.appengine.ext import ndb

class MyUser(ndb.Model):
    email_address = ndb.StringProperty()
    username = ndb.StringProperty()
    followers = ndb.StringProperty(repeated = True)
    following = ndb.StringProperty(repeated = True)
    full_name = ndb.StringProperty()
    description = ndb.StringProperty()
    userid = ndb.StringProperty() 

class TweetModel(ndb.Model):
    tweet_id = ndb.StringProperty()
    tweet_text = ndb.StringProperty()
    tweet_time = ndb.DateTimeProperty()
    tweet_username = ndb.StringProperty()
