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
import hashlib
from web import form
### Url mappings
web.config.debug = False
urls = (
'/', 'Index',
'/login','Login',
'/register', 'Register',
'/view/(\d+)', 'View',
'/new', 'New',
'/delete/(\d+)', 'Delete',
'/edit/(\d+)', 'Edit',
)

### Templates
t_globals = {
 'datestr': web.datestr
 }

render = web.template.render('/home/marzim83/myblog/webpy-apps/blog/templates', base='base', globals=t_globals)

class Index:
    def GET(self):
        """Show page"""
        posts = model.get_posts()
        return render.index(posts)

class View:
    def GET(self, id):
        """View single post"""
        post = model.get_post(int(id))
        return render.view(post)

class Login:
    def GET(self):
        """Login page"""
        return render.login()

class Register:
    vpass = form.regexp(r".{3,20}$", 'must be between 3 and 20 characters')
    vemail = form.regexp(r".*@.*", "must be a valid email address")
    vuser_req = form.Validator("Username not provided.", bool)
    vuser_length = form.regexp(r".{3,20}$", 'must be between 3 and 20 characters')
    vuser_exist = form.Validator("Username already exist.", lambda u: u is None or model.get_user(u.username) is None)
    vpass_match = form.Validator("Password didn't match", lambda i: i.password == i.password2)

    register_form = form.Form(
    form.Textbox("username", vuser_req, vuser_length, description="Username"),
    form.Textbox("email", vemail, description="E-Mail"),
    form.Password("password", vpass, description="Password"),
    form.Password("password2", vpass, description="Repeat password"),
    form.Button("submit", type="submit", description="Register"),
    validators = [vpass_match, vuser_exist],
    )

    def GET(self):
        # do $:f.render() in the template
        f = self.register_form()
        return render.registration(f)

    def POST(self):
        f = self.register_form()

        if not f.validates():
            return render.registration(f)
        else:
            # TODO: should show the home page
            encrypt_pass = hashlib.sha1("sAlT754-"+f.d.password).hexdigest()
            model.new_user(f.d.username, encrypt_pass, f.d.email)
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
        form = self.form()
        return render.new(form)

    def POST(self):
        form = self.form()
        if not form.validates():
            return render.new(form)
        model.new_post(form.d.title, form.d.content)
        raise web.seeother('/')

class Delete:
    def POST(self, id):
        model.del_post(int(id))
        raise web.seeother('/')

class Edit:
    def GET(self, id):
        post = model.get_post(int(id))
        form = New.form()
        form.fill(post)
        return render.edit(post, form)

    def POST(self, id):
        form = New.form()
        post = model.get_post(int(id))
        if not form.validates():
            return render.edit(post, form)
        model.update_post(int(id), form.d.title, form.d.content)
        raise web.seeother('/')

app = web.application(urls, globals())
application = app.wsgifunc()

