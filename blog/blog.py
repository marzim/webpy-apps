#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      mc185104
#
# Created:     11/12/2013
# Copyright:   (c) mc185104 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

""" Basic blog using webpy 0.3 """
import web
import model

### Url mappings
web.config.debug = False
urls = (
'/', 'Index',
'/login','login.Login',
'/logout','Logout',
'/register', 'register.Register',
'/view/(\d+)', 'view.View',
'/new', 'New',
'/delete/(\d+)', 'Delete',
'/edit/(\d+)', 'edit.Edit',
)

### Templates
app = web.application(urls, globals())
store = web.session.DiskStore('sessions')
session = web.session.Session(app, store, initializer={'login': 0, 'privilege': 0, 'user': 'anonymous'})

t_globals = {
 'datestr': web.datestr,
 'session': session
 }

render = web.template.render('/home/marzim83/myblog/webpy-apps/blog/templates', base='base', globals=t_globals)

def logged():
    if session.login > 0:
        return True
    else:
        return False

class Index:
    def GET(self):
        """Show page"""
        if logged():
            posts = model.get_posts(session.login)
            return render.index(posts)
        else:
            raise web.seeother('/login')

class Logout:
    def GET(self):
        session.login = 0
        session.kill()
        raise web.seeother('/')


class New:
    form = web.form.Form(
        web.form.Textbox('title', web.form.notnull,
            size=30,
            description="Post title:"),
        web.form.Textarea('content', web.form.notnull,
            rows=30, cols=80,
            description="Post content:"),
        web.form.Button('Post entry'),
    )

    def GET(self):
        if not logged():
            raise web.seeother('/')

        form = self.form()
        return render.new(form)

    def POST(self):
        form = self.form()
        if not form.validates():
            return render.new(form)
        model.new_post(form.d.title, form.d.content, session.login)
        raise web.seeother('/')


class Delete:
    def GET(self, id):
        if not logged():
            raise web.seeother('/')

    def POST(self, id):
        model.del_post(int(id))
        raise web.seeother('/')


application = app.wsgifunc()

