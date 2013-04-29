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
import datastore

class PermalinkHandler(Handler):
	def get(self, entryId):
		# has the id of the entry passed along with the get request so it can be looked up and displayed
		blog_entry = Posts.get_by_id(int(entryId))

		if blog_entry:
			self.render("permalink.html", blog_entry=blog_entry)
		else:
			self.render("permalink.html", blog_entry="", error="Blog post %s not found!" % entryId)

	def post(self):
		# no post
		pass
