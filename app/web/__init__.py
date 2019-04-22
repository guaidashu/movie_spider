"""
author songjie
"""
from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.settings')
    app.config.from_object('config.secure')
    register_blueprint(app)
    return app


def register_blueprint(app):
    from app.web.help_spider import help_spider
    app.register_blueprint(help_spider)

# def start():
#     httpd = make_server('', 8080, application)
#     print("Server listen on 8080")
#     httpd.serve_forever()
