import json
from google.appengine.ext import db
import webapp2
from webapp2_extras import sessions
import os
from google.appengine.ext.webapp import template
import sessions_module
from model.User import User,Session
import uuid
import json

class MainHandler(sessions_module.BaseSessionHandler):

    def post(self):
        loggedIn= False
        username=self.request.headers.get('Username')
        password=self.request.headers.get('Password')
        print("username="+username)
        print("password="+password)
        use = User.all().filter('username',username)
        if use.count() == 1:
            #user found
            user = use.get()
            if(user.password == password):
                print("match")
                i = uuid.uuid1()
                sess = Session(user=user.username,sessId=str(i))
                sess.put()
                self.response.headers['Content-Type'] = 'application/json'
                obj = {
                    'sessKey':str(i)
                }
                self.response.out.write(json.dumps(obj))
            else:
                #no user found/something went wrong
                print("badpass")
        else:
            print("badname")

app = webapp2.WSGIApplication([('/json/login', MainHandler)], config=sessions_module.myconfig_dict, debug=True)