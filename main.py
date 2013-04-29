#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from python.handler import *
from python.signupHandler import *
from python.welcomeHandler import *
from python.loginHandler import *
from python.logoutHandler import *
from python.newpostHandler import *
from python.permalinkHandler import *
from python.datastore import *
import re
import logging

class MainHandler(Handler):
	def get(self):
		# display options based on if a user is logged in
		cookieStr = self.request.cookies.get('user_id')
		# get all the posts in the datastore by timestamp
		p = db.GqlQuery("SELECT * from Posts ORDER BY timestamp DESC")

		# self.prepareData(p)

		if cookieStr:
			self.render("index.html", logout="logout", newpost="New Post", posts=p)
		else:
			self.render("index.html", posts=p)	

	def prepareData(self, p):
		# used to prepare the post data for display on the webpage
		for post in p:
			logging.info(post['ID'])
			logging.info(post.username)
			logging.info(post.timestamp)
			logging.info(post.subject)
			logging.info(post.content)


app = webapp2.WSGIApplication([ ('/', MainHandler),
								('/signup',SignupHandler),
								('/welcome', WelcomeHandler),
								('/login', LoginHandler),
								('/logout', LogoutHandler),
								('/newpost', NewpostHandler),
								(r'/permalink/(\d+)', PermalinkHandler) #(\d+)indicates a parameter is passed to the get method. The "\d+" will accept all the links that have 1 or more digit after "/blog/post/" path.
								 ], debug=True)
