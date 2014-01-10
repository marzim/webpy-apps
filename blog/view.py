from blog import render, model

class View:
    def GET(self, id):
        """View single post"""
        post = model.get_post(int(id))
        return render.view(post)