# Authors:
#   Phelan
# 
# this file collects all of the datastore entities needed by the blog. 
from google.appengine.ext import db
import hashing

class User(db.Model):
    '''
        user entity.
        @classmethod are decorators. This particular one means that you can call these methods on the class itself, not 
        instances (objects) of this class. User.by_id, for example. 

        These are procedural lookups, not GQL ones
    '''
    name = db.StringProperty(required = True)
    pw_hash = db.StringProperty(required = True)
    email = db.StringProperty()

    @classmethod
    def by_id(cls, uid):
        # looks up user by id
        return User.get_by_id(uid, parent = users_key())

    @classmethod
    def by_name(cls, name):
        # looks up user by name. basically select * from user where name == name, and get() returns first instance
        u = User.all().filter('name =', name).get()
        return u

    @classmethod
    def register(cls, name, pw, email = None):
        # this one actually creates a new user object, based on the inputs
        # doesn't actually store it
        h = hashing.Hasher()
        # users_key may not be necessary
        pw_hash = makePwHash(name, pw)
        return User(parent = users_key(),
                            name = name,
                            pw_hash = pw_hash,
                            email = email)

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.pw_hash):
            return u