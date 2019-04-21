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
class User(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        username = self.request.get('username')
        user=users.get_current_user()
        myuser_key = ndb.Key('MyUser',user.user_id())
        myuser = myuser_key.get()
        same_user=''
        username_query = MyUser.query(MyUser.username == username).fetch()
        full_name=username_query[0].full_name
        tweet_list = []


        if myuser.username == username:
            same_user = 'yes'
        following_list = myuser.following
        follow = 'Follow'
        if username in following_list:
            follow = 'Unfollow'

        tweet_query = TweetModel.query(TweetModel.tweet_username == username).fetch(limit=50)

        for tweet in tweet_query:
            tweet_list.append(tweet.tweet_text)

        template_values = {
        'username': username,
        'full_name' : full_name,
        'follow' : follow,
        'same_user' : same_user,
        'tweet_list' : tweet_list
        }
        template = JINJA_ENVIRONMENT.get_template('view_user.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        action = self.request.get('button')
        user=users.get_current_user()
        myuser_key = ndb.Key('MyUser',user.user_id())
        myuser = myuser_key.get()
        follow = ''
        if action == 'Follow':
            username = self.request.get('username')
            myuser.following.append(username)
            username_query = MyUser.query(MyUser.username == username).fetch()
            logging.info(username_query)
            user_profile_key = ndb.Key('MyUser',username_query[0].userid)
            user_profile=user_profile_key.get()
            user_profile.followers.append(myuser.username)
            follow = 'Follow'
            logging.info(follow)
        elif action== 'Unfollow':
            username = self.request.get('username')
            myuser.following.remove(username)
            username_query = MyUser.query(MyUser.username == username).fetch()
            logging.info(username_query)
            user_profile_key = ndb.Key('MyUser',username_query[0].userid)
            user_profile=user_profile_key.get()
            logging.info(user_profile_key)
            user_profile.followers.remove(myuser.username)
            follow = 'Unfollow'
            logging.info(follow)
        myuser.put()
        user_profile.put()
        self.redirect('/user?username='+username)
