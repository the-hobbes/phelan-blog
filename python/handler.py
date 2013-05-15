# Created 3MAR2013 
# Authors:
# 	Phelan
# 
# This base handler provides much of the basic libraries used by the other handlers, as well as a Handler class which 
# facilitates an easier method for rendering content to jinja templates. 
# This is done so you can just import this handler file instead of writing the import, template, and Handler information each
# time.

# also, this has a bunch of the default methods that handlers may use as well as some small handlers themselves

import webapp2
import os
import jinja2
import re
from google.appengine.ext import db
import logging
import hashing
from datastore import *

from google.appengine.api import memcache # import memcache
import pickle
import time

#set templating directory with jinja. NOTE that jinja escapes html because autoescape = True
template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Handler(webapp2.RequestHandler):
	'''
		Class Handler 
		This class inherits from RequestHandler. It is used to simplify writing and rendering to templates by providing
		simpler methods to use in order to do such operations. 
		For example, in other classes which implement this Handler, rendering data to a template can be accomplished by 
		the following statement:
			self.render(template, keyvalue pairs)
		as opposed to the following: 
			self.write(self.render_str(template, keyvalue pairs))
		params: inherits from RequestHandler

		Also, it provides other methods commonly used by page handlers, like form validation and cookie operations.
	'''
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def renderStr(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		logging.info("template directory")
		logging.info(template_dir)

		#called by render_front in MainPage class
		self.write(self.renderStr(template, **kw))

	# Validation functions
	USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
	PASS_RE = re.compile(r"^.{3,20}$")
	EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')

	def valid_username(self, username):
		return username and self.USER_RE.match(username)

	def valid_password(self, password):
		return password and self.PASS_RE.match(password)

	def valid_email(self, email):
		return not email or self.EMAIL_RE.match(email)

	def validateInput(self, request):
		# validate the form input
		username = request.get('username')
		password = request.get('password')
		verify = request.get('verify')
		email = request.get('email')

		params = dict(username = username, email = email)

		if not self.valid_username(username):
			params['error_username'] = "That's not a valid username."
			return True, params

		if not self.valid_password(password):
			params['error_password'] = "That wasn't a valid password."
			return True, params

		elif password != verify:
			params['error_verify'] = "Your passwords didn't match."
			return True, params

		if not self.valid_email(email):
			params['error_email'] = "That's not a valid email."
			return True, params

		return False, params

	# cookie specific functions
	def set_secure_cookie(self, name, val):
		# sets a cookie whose name is name and whose value is val
		h = hashing.Hasher()
		cookie_val = h.makeSecureVal(val)
		self.response.headers.add_header(
		'Set-Cookie',
		'%s=%s; Path=/' % (name, cookie_val))

	def read_secure_cookie(self, name):
		# reads a secure cookie (make sure its secure, otherwise nothing gets returned)
		h = hashing.Hasher()
		cookie_val = self.request.cookies.get(name)
		# if cookie val and check secure val return true
		return cookie_val and h.checkSecureVal(cookie_val)

	# login and logout functions
	def login(self, user):
		self.set_secure_cookie('user_id', str(user.key().id()))

	def logout(self):
		# keeping the same path lets us destroy the right cookie
		self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

	def initialize(self, *a, **kw):
		'''
			this gets called before every request, and it checks for the user cookie (user_id).
			basically checks to see if the user is logged in or not
			called by the appengine framework

			NOTE ON THIS:
			Steve's wanted to check for a user cookie each time the webserver receives a request from a client (browser), but 
			instead of overriding the webapp2.RequestHandler.__init__ method as described in the docs, he overrides the initalize 
			method which he knows is called by __init__, and then makes sure to call the superclass' (webapp2.RequestHandler) 
			initialize. (In Python, a class's __init__ method is automatically called when a class instance is created.) The rest of
			the handler code can then just check self.user to see if a user is logged in, which should be more efficient and cleaner 
			retrieving the cookie, repeating the hash validity check, etc. each time.
		'''
		webapp2.RequestHandler.initialize(self, *a, **kw)
		uid = self.read_secure_cookie('user_id')
		# if the cookie exists, store the user object in the self.user variable, whose value is read from the datastore by the id
		self.user = uid and User.by_id(int(uid[0]))

class PerspectiveHandler(Handler):
	'''
		simple handler to render the perspective template
	'''
	def get(self):
		self.render("perspectiveTest.html")

# caching methods
def updateCache(update = False):
	'''
		updateCache
		Used to retrieve the blog posts from the datastore, most recent first. Updates the cache when it needs to. 
		Parameters:
			update, a boolean value indicating whether or not the cache needs to be updated. 
			If update is True, we update the cache- we run the query and update the cache with the result
			If update is False, then we just pull from the cache, no query is run.
		Return:
			posts, a list of the blog posts
	'''
	# caching algorimth
	key = 'top'
	posts = memcache.get(key)

	# if posts isn't in the database, or we need to update the cache...
	if posts is None or update:
		logging.error("DB QUERY") # to show if you've made a database hit

		# get all the posts in the datastore by timestamp
		posts = db.GqlQuery("SELECT * from Posts ORDER BY time DESC") #remember, posts is a cursor- a pointer to the results in the database.

		# make a list out of the cursor from the query so it is less wasteful
		# basically caching the result of the query as a list, which actually runs the query
		posts = list(posts)
		memcache.set(key, posts) 

		# TODO: print the age of the query out on the front page (current time - the time it was updated in the cache)

	return posts