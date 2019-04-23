import webapp2
import jinja2
import os
import logging
from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.api import search

from myuser import MyUser
from myuser import TweetModel

from datetime import datetime
JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ['jinja2.ext.autoescape'],
    autoescape = True
)

class TweetEdit(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template = JINJA_ENVIRONMENT.get_template('tweet_edit.html')
        id = self.request.get('id')
        username = self.request.get('username')
        tweet_query = TweetModel.query(ndb.AND(TweetModel.tweet_id==int(id)),
                                        TweetModel.tweet_username==username).fetch()


        #logging.info(tweet_query.key.id())
        template_values = {
            'tweet_query' : tweet_query[0]
        }
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        action = self.request.get('button')
        tweet_key = self.request.get('tweet_key')
        if action == 'Edit':
            tweet_edit = self.request.get('tweet_edit')
            tweet_key = ndb.Key('TweetModel',tweet_key)
            tweet = tweet_key.get()
            tweet.tweet_text = tweet_edit
            tweet.tweet_time = datetime.now()
            tweet.put()

        elif action == 'Delete':
            tweet_key = ndb.Key('TweetModel',int(tweet_key))
            tweet = tweet_key.get()
            # tweet = TweetModel.get_by_id(int(tweet_key))
            tweet.key.delete()
        self.redirect('/')
