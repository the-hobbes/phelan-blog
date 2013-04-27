# Class used to provide hashing, salting, and password comparision functionality to a webpage
# phelan vendeville

import hashlib
import hmac
import random
import string

class Hasher():
	# class variables

	def __init__(self):
		'''
			Default Constructor
		'''
		

	# functions related to hashing cookies and checking their veracity
	def hashStr(s):
		'''
			returns the hex digest of a hashed value s
		'''
		# using HMAC
		return hmac.new(SECRET, s).hexdigest()

	def makeSecureVal(s):
		'''
			returns the pair value,hash where value is s, and hash is the hash of s
		'''
		return "%s|%s" % (s, hashStr(s))

	def checkSecureVal(h):
		'''
			takes h, which is a value and its hash in this format: "s,hash".
			checks to make sure that the hash of s is equal to the hash. This is to make sure no one has tampered with s.
		'''
		val = h.split("|")
		if h == makeSecureVal(val[0]):
			return val

	def saltGenerator(size=5):
		'''
			used to generate a series of random characters to be used in a salt.
			Parameters:
				size, an optional length defaulted to 5
			returns
				the series of random characters to be used as a salt
		'''
		return ''.join(random.choice(string.letters) for x in xrange(size) )

	def makePwHash(name, pw, salt= None):
		'''
			returns a hashed password and salt of the format->
				HASH(name + pw + salt),salt using sha256
			Parameters:
				name, the username
				pw, the plaintext password
			returns
				a string of the format (hash, salt)
		'''
		if not salt:
			salt = saltGenerator()	
		
		hashed = hashlib.sha256(name + pw + salt).hexdigest()

		return "%s,%s" % (h, salt)

	def validatePassword(name, pw, h):
		'''
			used to validate a user's password, by comparing the hash of the name+pw+salt with the hash passed in(which has the salt
			added to the end of it).
			Parameters:
				name, the user's name
				pw, the user's password
				h, the hash of the name+pw+salt. Has the form Hash,salt
			returns
				a boolean, true if the password matches, false if it does not
		'''

		salt = h.split(',')[1]
		return h == makePwHash(name, pw, salt)