#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      mc185104
#
# Created:     10/01/2014
# Copyright:   (c) mc185104 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import web
from web import form
from blog import render, logged, model, session
import hashlib

class Login:

    vuser_req = form.Validator("Username not provided.", bool)
    vpass_req = form.Validator("Password not provided.", bool)
    vuser_exist = form.Validator("Username doesn't exist.", lambda u: u is None or model.get_user(u.username.strip()) is not None)
    vpass_exist = form.Validator("Password didn't match", lambda i: hashlib.sha1("sAlT754-"+i.password).hexdigest() == model.get_user(i.username.strip())['pwd'])

    login_form = form.Form(
        form.Textbox("username", vuser_req, description="Username"),
        form.Password("password", vpass_req, description="Password"),
        form.Button("submit", type="submit", description="Login"),
        validators = [vuser_exist, vpass_exist],
        )
    def GET(self):
        """Login page"""
        f = self.login_form()
        if not logged():
            return render.login(f)
        else:
            raise web.seeother('/')

    def POST(self):

        f = self.login_form()
        if not f.validates():
            return render.login(f)
        else:
            session.login = 1
            session.privilege = 1
            session.user = f.d.username.strip()
            raise web.seeother('/')


