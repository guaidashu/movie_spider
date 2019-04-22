"""
author songjie
"""
import web

urls = (
    '/(.*)', 'hello'
)

app = web.application(urls, globals())


class hello:
    def GET(self, name):
        if not name:
            name = 'world'
        return '<h1>hello %s!</h1>' % name
