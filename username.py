import webapp2
import jinja2
import os
import logging
from google.appengine.ext import ndb
from google.appengine.api import users

from myuser import MyUser

JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ['jinja2.ext.autoescape'],
    autoescape = True
)

class UsernamePage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template = JINJA_ENVIRONMENT.get_template('username.html')
        user=users.get_current_user()
        myuser_key = ndb.Key('MyUser',user.user_id())
        myuser = myuser_key.get()
        template_values = {
        'myuser' : myuser
        }
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        template = JINJA_ENVIRONMENT.get_template('username.html')
        user=users.get_current_user()
        action = self.request.get('button')
        if action=='Submit':
            edit = self.request.get('edit')

            full_name = self.request.get('full_name')
            description = self.request.get('description')
            myuser_key = ndb.Key('MyUser',user.user_id())
            myuser = myuser_key.get()
            if edit == 'yes' :
                myuser.full_name = full_name
                myuser.description = description
                myuser.put()
                self.redirect('/')

            elif edit == 'no':
                username = self.request.get('username')
                username_query = MyUser.query(MyUser.username == username).fetch()
                if not username_query:
                    if myuser==None:
                        myuser = MyUser(id = user.user_id(),userid=user.user_id(), email_address = user.email(), username = username, full_name=full_name, description=description)
                        myuser.put()
                        self.redirect('/')
                else :
                    error = 'Username already exists'
                    template_values = {
                    'error' : error,
                    'myuser':myuser
                    }
                    self.response.write(template.render(template_values))
