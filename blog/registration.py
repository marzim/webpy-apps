#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      mc185104
#
# Created:     13/12/2013
# Copyright:   (c) mc185104 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import web
from web import form
import hashlib
from web.template import render

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
