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
import hashing
import logging

# handle requests for the resource
class SignupHandler(Handler):
	def get(self):
		self.renderLanding()

	def renderLanding(self):
		self.render("signupForm.html")

	def post(self):
		# form validation section
		uname = str(self.request.get('username'))
		pword = str(self.request.get('password'))
		have_error, params = self.validateInput(self.request)

		if have_error:
			# do this if there is an error
			self.render('signupForm.html', **params)
		else:
			# if there isn't an error, hash the password, make the cookie and redirect to the right page
			# make cookie heeere!!!
			h = hashing.Hasher()
			newCookieVal = h.makePwHash(uname, pword)
			# set the set-cookie header to set the cookie
			self.response.headers.add_header("Set-Cookie", "user_id=%s; Path=/" % newCookieVal)
			self.redirect('/welcome', uname)
