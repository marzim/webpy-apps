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
from blog import render, model, logged, New

class Edit:

    def GET(self, id):
        if not logged():
            raise web.seeother('/')

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
