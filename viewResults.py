from google.appengine.ext import db
import webapp2
import os
from google.appengine.ext.webapp import template
import sessions_module
from model.User import User,Session
from model.Jirga import Jirga, ModVote
from model.Question import Question
from model.Vote import Vote

def render_template(handler, template_name, template_values):
    path = os.path.join(os.path.dirname(__file__), 'templates/' + template_name)
    html = template.render(path, template_values)
    handler.response.out.write(html)


def calculateJirga(votes,jirga):
    votes2 = []
    for vote in votes:
        sum = 0;
        voters = User.get(vote.users)
        modVotes = ModVote.get(jirga.modVotes)
        for voter in voters:
            for modVote in modVotes:
                if voter.username == modVote.user:
                    print("woo")
                    sum += int(str(modVote.reward)) + 1
        votes2.append(sum)
    return votes2


class MainHandler(sessions_module.BaseSessionHandler):

    def get(self, jirgaId, qId):
        user = self.getuser()
        if(user is not None):
            question = Question.all().filter('qId',qId).get()
            jirga = Jirga.all().filter('jirgaId',jirgaId).get()
            votes = Vote.get(question.votes)
            votes2 = calculateJirga(votes,jirga)
            template_params = {
                'question':question,
                'votes':votes,
                'user':user,
                'jirga':jirga,
                'votes2':votes2
            }
            render_template(self,"viewResults.html",template_params)
        else:
            self.response.write("FAIL - you need to be logged in for this")

app = webapp2.WSGIApplication([('/viewResults/(.*?)/(.*?)', MainHandler)], config=sessions_module.myconfig_dict, debug=True)