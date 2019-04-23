import webapp2
import jinja2
import os
import logging
from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.api import search
from datetime import datetime

from myuser import MyUser
from myuser import TweetModel
from username import UsernamePage
from search import Search
from view_user import User
from tweet_edit import TweetEdit
JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ['jinja2.ext.autoescape'],
    autoescape = True
)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        url = ''
        url_string = ''
        tweet_list =[]
        user=users.get_current_user()
        username = ''
        if user:
            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'

            myuser_key = ndb.Key('MyUser',user.user_id())
            myuser = myuser_key.get()
            if myuser == None:
                self.redirect('/userName')

            else:
                username = myuser.username
                following_list = myuser.following
                following_list.append(username)
                for following in following_list:
                    display_query = TweetModel.query(TweetModel.tweet_username == following).fetch()
                    for tweet in display_query:
                        tweet_list.append(tweet)

        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'

        template_values = {
            'url': url,
            'url_string':url_string,
            'user': user,
            'tweet_list' : tweet_list,
            'username' : username
        }
        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        template = JINJA_ENVIRONMENT.get_template('main.html')
        user=users.get_current_user()
        action = self.request.get('button')
        if action=='Post':
            tweet_text = self.request.get('tweet_text')
            myuser_key = ndb.Key('MyUser',user.user_id())
            myuser = myuser_key.get()
            myuser.no_of_tweets +=1
            tweet_key = TweetModel(tweet_id=myuser.no_of_tweets,tweet_text = tweet_text,tweet_time = datetime.now(),tweet_username = myuser.username)
            tweet_key.put()
            myuser.put()
            self.redirect('/')

app = webapp2.WSGIApplication([
    ('/',MainPage),
    ('/userName',UsernamePage),
    ('/search',Search),
    ('/user',User),
    ('/editTweet',TweetEdit),
], debug =True)
