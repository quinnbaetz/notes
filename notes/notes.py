#!/usr/bin/env python

# Python Imports
import logging as log
import os.path

# Extern Imports
from tornado.options import options
import tornado.web
import inferno.web
import inferno.config

# Project Imports
import config
import model

ROOT_PATH = os.path.dirname(__file__)

class HelloWorld(inferno.web.RequestHandler):
    def get(self):
        self.session['hello'] = 'hello'
        self.render("index.html", **self.tmpl)

    def render(self, template_name, **kwargs):
        self.view_ind = 1
        super(HelloWorld, self).render(template_name, **kwargs)

    def get_member_id(self):
        return None

    def get_current_user(self):
        return None


class ActiveHandler(inferno.web.ActiveHandler, HelloWorld):
    def get(self):
        self.session_end()
        super(ActiveHandler, self).get()


class Authorizor():
    def authorize(self, role):
        #TODO Implement for your app, default raise 405 for all roles
        raise tornado.web.HTTPError(405)


class SettingsHandler(inferno.web.SettingsHandler, Authorizor):
    pass


# Application
cwd = os.path.abspath(os.path.dirname(__file__))
handler_urls = [
    (r'/', HelloWorld),
    (r'/(favicon.ico)$', tornado.web.StaticFileHandler, {"path": cwd + "/static"}),
    (r'/(robots.txt)$', tornado.web.StaticFileHandler, {"path": cwd + "/static"}),
    (r'/static/(.*)', tornado.web.StaticFileHandler, {"path": cwd + "/static"}),
    (r'^/active.*$', ActiveHandler), # used by netscaler
    (r'^/settings/?$', SettingsHandler),
    (r"/(.*\.scss)$", inferno.web.ScssHandler),
]


settings = dict(
        template_path=os.path.join(ROOT_PATH, "templates")
        )


def main():
    if inferno.config.is_local():
        handler_urls.append((r'/client/(.*)', inferno.web.ClientFileHandler, {"path": cwd + "/client"}))
    log.info('Starting %s' % options.app_name)
    app = inferno.web.Application(**settings)
    app.add_handlers('.*$', handler_urls)    # '.*$' required to work with tornado
    inferno.web.Application.start(app)


if __name__ == "__main__":
    inferno.config.initialize(app_env=config.environments)
    main()
