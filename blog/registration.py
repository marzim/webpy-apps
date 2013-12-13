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

render = web.template.render('templates')

vpass = form.regexp(r".{3,20}$", 'must be between 3 and 20 characters')
vemail = form.regexp(r".*@.*", "must be a valid email address")

register_form = form.Form(
form.Textbox("username", description="Username"),
form.Textbox("email", vemail, description="E-Mail"),
form.Password("password", vpass, description="Password"),
form.Password("password2", vpass, description="Repeat password"),
form.Button("submit", type="submit", description="Register"),
validators = [
form.Validator("Password didn't match", lambda i: i.password == i.password2)]
)

class registration:
    def GET(self):
        # do $:f.render() in the template
        f = registration_form()
        return render.registration(f)

    def POST(self):
        f = registration_form()
        if not f.validates():
            return render.registration(f)
        #else:
            # TODO: should show the home page