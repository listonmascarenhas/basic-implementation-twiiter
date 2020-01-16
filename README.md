# basic-implementation-twitter
In this task, we build a basic replica of Twitter which provides basic facilities like creating and searching through tweets and users. We will be using Google App Engine, Python, Jinja and a NoSQL database,

Methods
1.	Main Page
	The get method of MainPage in main.py initially allows the user to login to the application. If the authentication is successful, the application checks if the user is a new user. A new user 	is redirected to another page where he can fill up various details. If an existing user logs in, 	an input field is displayed where the user can post a tweet along with displaying a list of the 	last 50 tweets posted by the current user and the users he is following. If the tweets are of 	the current user, he is allowed to edit them. The sorting function of the last 50 tweets is 	carried 	out in main.html using the jinja2 template. A user can also edit tweets posted by him 	and also post tweets with images. A user can search for other users, view their profile, edit 	his profile details and logout of the application.  
	The post method of MainPage in main.py allows the user to post a tweet and redirects the 	user to the same page to display the changes.
	In main.py we also define the application object that is responsible for this application. The 	routing table is specified in this object.
2.	Username Page
The UsernamePage in username.py is called either when a new user is logged into the application or when a user wants to edit his profile. The check is done in username.html using the jinja2 template. If a user wants to edit his profile, previously stored values are populated on the form and the username input is kept as read only.
The get method of UsernamePage in username.py retrieves the users key and sends it to username.html and checks if the user’s details exists using jinja2.
The post method of UsernamePage in username.py stores the values that the user has entered on the form. If the user is new, a check is kept seeing if a username already exists and username.html is rendered again. If the username is unique, all the user’s values are stored into the datastore. If the user is editing his profile, other than username, the edited values are stored into the datastore and redirected to the main page.

3.	Search
The get method of Search in search.py renders search.html
The post method of Search in search.py searches for words in a tweet and also for usernames. The search functionality is case sensitive. If a username exists, the username is displayed. If the tweet exists, the entire tweet along with the username of the user who posted is displayed. If the username is clicked, it takes to the user’s page.

4.	User
The get method of User in view_user.py displays the users full name, their description, their followers and following count and also display the users past 50 tweets. The current user can follow or unfollow the user as well. The post method of User in view_user.py checks if the follow or unfollow button is clicked. 	If the follow button is clicked, the username is appended to the current users following list 	and the current user’s username is appended to the user’s followers list. If the unfollow 	button is clicked, the username is removed from the current users following list and the 	current user’s username is removed from the user’s followers list. The current user is then 	redirected to the same page to update the values.
	
5.	Tweet Edit
The get method of TweetEdit in tweet_edit.py retrieves the id of the tweet from the url and displays the tweet text in the form which is rendered in tweet_edit.html using jinja2 template. The user can also delete a tweet.
The post method of TweetEdit in tweet_edit.py checks if the Edit or Delete button is clicked. If the Edit button is clicked, the tweet text and the current time are stored. If the Delete button is clicked, the tweet is deleted.


6.	app.yaml
app.yaml is responsible for informing Google App Engine about the runtimes and libraries needed for the application. Python version 2.7 is used as the runtime. We also state that the application is threadsafe so multiple instances can be allowed on the same server. In libraries we state that we will be using Jinja2 running on its latest version. In handlers, we state that all URLs with /css will be redirected to the static directory css. We also state that all other requests will be redirected to the app variable which is defined in main.py. 

Models and data structures

7.	MyUser:
myuser.py contains the class MyUser which uses ndb.Model to store the email address, username, followers, following, full name, description, user id and the no of tweets. This is possible by importing ndb from google.appengine.ext. email_address, username, full_name, description and userid are specified as StringProperty() since they are of ASCII format. no_of_tweets is specified as an IntegerProperty() with default as 0 because it is a counter and needs to be incremented. followers and following are specified as StringProperty() with repeated being True because they might need to store more than one value.

8.	TweetModel
myuser.py contains the class TweetModel which uses ndb.Model to store the tweets text, the time the tweet was posted, the posters username and the tweets url. This is possible by importing ndb from google.appengine.ext. tweet_text, tweet_username and tweet_url are specified as StringProperty() since they are of ASCII format. tweet_time is specified as DateTimeProperty() since we will be storing the current time at which the tweet is posted.
