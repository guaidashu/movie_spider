"""
author songjie
"""


def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    url = environ['PATH_INFO']
    return '<h1>Hello, web!</h1>'
