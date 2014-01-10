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
from web.template import render

class Login:
    def GET(self):
        """Login page"""
        return render.login()

    def POST(self):
        return
