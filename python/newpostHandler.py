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
from python.datastore import *
# import datastore
import hashing
import logging
import time

class NewpostHandler(Handler):
	def get(self):
		# check to see if the user is logged in. This is explained in the docstring in hashing.py (the reason why self.user 
		#	can be used to determine if a user is signed in or not).
		
		if self.user:
			# cookie is good, let 'em see newpost
			self.renderNewpost()
		else:
			# cookie is bad, get them out of here
			self.redirect("/")

	def post(self):
		#get the parameters from the post
		subject = self.request.get("subject")
		content = self.request.get("content")

		if subject and content:
			# success, interact with the datastore entity Posts, creating a new row with the right information information
			p = Posts(subject = subject, content = content, username = self.user.name)
			p.put()
			time.sleep(1) # uuugh need this to give the datastore time to catch up, so that when we add stuff to the cache there is stuff to add.

			# get the id of the post you just made
			p_id = p.key().id()

			# update the cache with new information
			posts = updateCache(update = True)
			
			# then redirect to a permalink for the post, in the form of /ID. Note the string substitution for the key, to be
			# 	passed on to the get parameter of permalinkhandler
			self.redirect("/permalink/%s" % str(p.key().id()))
		else:
			# failure
			error = "need both the subject and the content"
			self.renderNewpost(subject, content, error)

	def renderNewpost(self, subject="", content="", error=""):
		#render the new error post page
		self.render("newpost.html", subject=subject, content=content, error=error)