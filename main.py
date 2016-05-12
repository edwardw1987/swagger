# -*- coding: utf-8 -*-
# @Author: edward
# @Date:   2016-05-12 10:19:03
# @Last Modified by:   edward
# @Last Modified time: 2016-05-12 16:34:37
from tornado.web import (
    RequestHandler, Application, url, HTTPError,authenticated)
from tornado.ioloop import IOLoop
from tornado.options import define
import tornado
from tornado.escape import json_encode
import os
import swagger
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
    @swagger.operation(
        nickname="home nickname"
    )
    def get(self):
        # raise Exception(self.request.full_url()) 
        # http://localhost:8888/
        self.write("Hello,world")

    @swagger.operation(
        nickname="home post"
    )
    def post(self):
        self.write('test post')
        
class Docs(RequestHandler):
	def get(self):
		# self.write('test')
		r = render_template('docs.html')
		self.write(r)


class ApiSpec(RequestHandler):
    def get(self):
        # self.write(open('spec.json').read())
        json_spec = json_encode(swagger.get_api_spec())
        self.write(json_spec)

# tornado资源配置
settings = {
    'template_path': os.path.join(os.path.dirname(__file__), 'static'),
    'static_path': os.path.join(os.path.dirname(__file__),'static'),
    'login_url': '/login',
    'autoreload': True,
    'debug': True,
    'cookie_secret': 'abcdefg',
}
handlers = [
    (r'/?', HomeHandler),
    (r'/docs/?', Docs),
    (r'/api/spec.json', ApiSpec),
]
Application(handlers, default_host="0.0.0.0", **settings).listen(8888)

IOLoop.current().start()