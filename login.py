import webapp2
from webapp2_extras import sessions
import os
from google.appengine.ext.webapp import template
import sessions_module;


def render_template(handler, template_name, template_values):
    path = os.path.join(os.path.dirname(__file__), 'templates/' + template_name)
    html = template.render(path, template_values)
    handler.response.out.write(html)

class MainHandler(sessions_module.BaseSessionHandler):

    def get(self):
        print("yo")
        if self.session.get('counter'):
            self.response.out.write('Session is in place')
            counter = self.session.get('counter')
            self.session['counter'] = counter + 1
            self.response.out.write('Counter = ' + str(self.session.get('counter')))
        else:
            self.response.out.write('Fresh Session')
            self.session['counter'] = 1
            self.response.out.write('Counter = ' + str(self.session.get('counter')))
    #post to login will receive:
    #username="username"
    #password="password"
    #should give user session
    def post(self):
        print "word"

app = webapp2.WSGIApplication([('/login', MainHandler)], config=sessions_module.myconfig_dict, debug=True)