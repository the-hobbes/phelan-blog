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

from python.handler import *

class LogoutHandler(Handler):
	def get(self):
		# get the login cookie user_id and set it to nothing, then redirect to the signup page

		if self.request.cookies.get('user_id'):
			# the way you log someone out is to delete their cookie, or in this case set it to an empty string
			# newCookieVal = ""
			# self.response.headers.add_header("Set-Cookie", "user_id=%s; Path=/" % newCookieVal)
			self.logout()

		self.redirect("/")