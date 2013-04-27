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
import re
from python.hashing import Hasher

# Validation functions
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
	return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
	return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
	return not email or EMAIL_RE.match(email)

# handle requests for the resource
class SignupHandler(Handler):
	def get(self):
		self.renderLanding()

	def renderLanding(self):
		self.render("signupForm.html")

	def validateInput(self, request):
		# validate the form input
		username = request.get('username')
		password = request.get('password')
		verify = request.get('verify')
		email = request.get('email')

		params = dict(username = username, email = email)

		if not valid_username(username):
			params['error_username'] = "That's not a valid username."
			return True, params

		if not valid_password(password):
			params['error_password'] = "That wasn't a valid password."
			return True, params
		elif password != verify:
			params['error_verify'] = "Your passwords didn't match."
			return True, params

		if not valid_email(email):
			params['error_email'] = "That's not a valid email."
			return True, params

		return False, params


	def post(self):
		# form validation section
		have_error, params = self.validateInput(self.request)
		username = self.request.get('username')
		password = self.request.get('password')

		if have_error:
			# do this if there is an error
			self.render('signupForm.html', **params)
		else:
			# if there isn't an error, hash the password, make the cookie and redirect to the right page
			h = Hasher()
			# make cookie heeere!!!
			newCookieVal = h.makeSecureVal(username, password)
			# set the set-cookie header to set the cookie
			self.response.headers.add_header("Set-Cookie", "user_id=%s" % newCookieVal)
			self.render('welcome.html', **params)
