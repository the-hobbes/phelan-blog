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

class MainHandler(Handler):
	def get(self):
		cookieStr = self.request.cookies.get('user_id')

		if cookieStr:
			self.render("index.html", logout="logout")
		else:
			self.render("index.html")	

app = webapp2.WSGIApplication([ ('/', MainHandler),
								('/signup',SignupHandler),
								('/welcome', WelcomeHandler),
								('/login', LoginHandler),
								('/logout', LogoutHandler)
								 ], debug=True)
