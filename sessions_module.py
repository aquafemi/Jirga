#Import sessions for session handling
import webapp2
from webapp2_extras import sessions
import os

#This is needed to configure the session secret key
#Runs first in the whole application
import model
from model.User import Session, User

myconfig_dict = {}
myconfig_dict['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key-somemorearbitarythingstosay',
    'session_max_age': 127800
}

#Session Handling class, gets the store, dispatches the request
class BaseSessionHandler(webapp2.RequestHandler):
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)
        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()

    def getuser(self):
        if self.session.get('sessId'):
            i = str(self.session.get('sessId'))
            sess = Session.all().filter('sessId',i).get()
            user = User.all().filter('username',sess.user).get()
            return user
        else:
            return None
#End of BaseSessionHandler Class
