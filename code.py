import web
from web.contrib import template

render = template.render_genshi(['./templates/'])

urls = (
    '/', 'index'
)

class index:
    def GET(self):
        #i = web.input(name=None)
        name = 'Bob'
        return render.index(name=name)


if __name__ =="__main__":
    app = web.application(urls, globals())
    app.run()