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

'''
	This file contains classes for handling requests for json output of the blog. MainJsonHandler outputs json for the whole blog,
	while PermalinkJsonHandler outputs json for a specific permalink request.
'''
import webapp2
from python.handler import *
from python.datastore import *

import json

class MainJsonHandler(Handler):
	'''
		Handles requests for the json for the whole blog
	'''
	def get(self):
		# get posts from datastore
		posts = db.GqlQuery("SELECT * from Posts ORDER BY time DESC")
		posts = list(posts)

		# make a dictionary from the contents of the posts
		i = 0
		d = {}
		for p in posts:
			i +=1
			d['post_' + str(i)] = {'username':p.username, 
							'subject':p.subject, 
							'time':str(p.time), 
							'content':p.content}

		# make that dictionary a json type. set the content type headers and write the json out
		formatted = json.dumps(d)
		self.response.content_type = 'application/json'
		self.write(formatted) 

class PermalinkJsonHandler(Handler):
	'''
		Handles requests for the json from specific posts
	'''
	def get(self, postid):
		blog_entry = Posts.get_by_id(int(postid))
		d = {}
		d['post'] = {'username':blog_entry.username, 
							'subject':blog_entry.subject, 
							'time':str(blog_entry.time), 
							'content':blog_entry.content}

		formatted = json.dumps(d)
		self.response.content_type = 'application/json'
		self.write(formatted)