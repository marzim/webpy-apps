import web
from blog import render, model, session

class View:
    def GET(self, id):
        """View single post"""
        if session.login > 0:
            post = model.get_post(int(id), session.login)
            return render.view(post)
        else:
            raise web.seeother('/')