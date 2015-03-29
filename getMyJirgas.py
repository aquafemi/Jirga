from google.appengine.ext import db
import webapp2
from webapp2_extras import sessions
import os
import sessions_module
from model.User import User,Session
from model.Jirga import Jirga
import json

class MainHandler(sessions_module.BaseSessionHandler):

    def get(self,sessId):
        sess = Session.all().filter('sessId',sessId).get()
        if sess is not None:
            user = User.all().filter('username',sess.user).get()
            print("user" + user.username)
            if(user is not None):
                jirgas = Jirga.get(user.jirgas)
                result = []
                self.response.headers['Content-Type'] = 'application/json'
                for jirga in jirgas:
                    obj2 = {
                        'name': jirga.title,
                        'key': jirga.jirgaId,
                    }
                    result.append(obj2)
                    print(jirga.title)
                self.response.out.write(json.dumps(result))
            else:
                self.response.write("FAIL - not logged in")

app = webapp2.WSGIApplication([('/getMyJirgas/(.*?)', MainHandler)], config=sessions_module.myconfig_dict, debug=True)
