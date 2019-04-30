import webapp2
import jinja2
import os
import logging
from google.appengine.ext import ndb
from google.appengine.api import users


from myuser import MyUser
from myuser import TweetModel

JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ['jinja2.ext.autoescape'],
    autoescape = True
)

class Search(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template = JINJA_ENVIRONMENT.get_template('search.html')
        self.response.write(template.render())

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        template = JINJA_ENVIRONMENT.get_template('main.html')
        action = self.request.get('button')
        if action == 'Search':
            tweet_username_list = []
            tweet_text_list = []


            tweet_search = self.request.get('tweet_search')
            if tweet_search == '':
                    tweet_username_list = []
                    tweet_text_list = []
            else:
                username_query = MyUser.query().fetch()
                tweet_content_query = TweetModel.query().fetch()

                for user in username_query:
                    if any(word in user.username for word in tweet_search.split()):
                        tweet_username_list.append(user.username)
                        tweet_text_list.append("")

                for tweet in tweet_content_query:
                    if all(word in tweet.tweet_text for word in tweet_search.split()):
                        tweet_username_list.append(tweet.tweet_username)
                        tweet_text_list.append(tweet.tweet_text)
            template_values = {
                'tweet_username_list' : tweet_username_list,
                'tweet_text_list' : tweet_text_list
            }
            template = JINJA_ENVIRONMENT.get_template('search.html')
            self.response.write(template.render(template_values))
        if action == 'Back':
            self.redirect('/')
