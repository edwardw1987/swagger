# -*- coding: utf-8 -*-
# @Author: edward
# @Date:   2016-05-12 10:19:03
# @Last Modified by:   edward
# @Last Modified time: 2016-05-12 11:00:04
from tornado.web import (
    RequestHandler, Application, url, HTTPError,authenticated)
from tornado.ioloop import IOLoop
from tornado.options import define
import tornado
import os

from jinja2 import Template
from jinja2 import Environment, FileSystemLoader

def render_template(template_name, **context):
    extensions = context.pop('extensions', [])
    globals = context.pop('globals', {})

    jinja_env = Environment(
        loader=FileSystemLoader(
            os.path.join(os.path.dirname(__file__), 'templates')),
        extensions=extensions,
    )
    jinja_env.globals.update(globals)

    # jinja_env.update_template_context(context)
    return jinja_env.get_template(template_name).render(context)

class HomeHandler(RequestHandler):
    def get(self):
        # raise Exception(self.request.full_url()) 
        # http://localhost:8888/
        self.write("Hello,world")

class ApiDocs(RequestHandler):
	def get(self):
		# self.write('test')
		r = render_template('docs.html')
		self.write(r)
class ApiSpec(RequestHandler):
	def get(self):
		self.write(open('spec.json').read())
# tornado资源配置
settings = {
    'template_path': os.path.join(os.path.dirname(__file__), 'static'),
    'static_path': os.path.join(os.path.dirname(__file__),'static'),
    'login_url': '/login',
    'autoreload': True,
    'debug': True,
    'cookie_secret': 'abcdefg',
}

Application([
    (r'/?', HomeHandler),
    (r'/docs/?', ApiDocs),
    (r'/api/spec.json?', ApiSpec),
    ], default_host="0.0.0.0", **settings).listen(8888)

IOLoop.current().start()