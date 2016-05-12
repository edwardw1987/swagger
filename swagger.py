# -*- coding: utf-8 -*-
# @Author: edward
# @Date:   2016-05-12 14:11:21
# @Last Modified by:   edward
# @Last Modified time: 2016-05-12 17:29:48
from functools import partial

# api = swagger.docs(Api(app), apiVersion='0.1',
#                    basePath='http://localhost:5000',
#                    resourcePath='/',
#                    produces=["application/json", "text/html"],
#                    api_spec_url='/api/spec',
#                    description='A Basic API')

class _APIs:
    def __init__(self):
        self.apis = []
        self.make_docs()
    def add_api(self, method, **kw):
        self.apis.append(self.pre_api(method, **kw))

    def operation(self, **kw):
        return partial(self.add_api, **kw)

    def pre_api(self, fn, **kw):
         d = dict(
                method=fn.__name__,
            )
         d.update(kw)
         return d

    def get_spec(self):
        return self.apis 

    def make_docs(self, apiVersion='1.0', swaggerVersion='1.2',
             basePath='http://localhost:9999',
             resourcePath='/',
             produces=["application/json"],
             api_spec_url='/api/spec',
             description='Auto generated API docs by swagger'):
        self.API_VERSION = apiVersion
        self.SWAGGER_VERSION = swaggerVersion
        self.BASE_PATH = basePath
        self.RESOURCE_PATH = resourcePath
        self.PRODUCES = produces
        self.API_SPEC_URL = api_spec_url
        self.DESCRIPTION = description


apis = _APIs()
operation = apis.operation
docs = apis.make_docs
get_api_spec = apis.get_spec


def main():
    class Handler:
        @operation(
            nickname="get something from api"
        )
        def get(self):
            """this is get notes """
            print 'get'

        def post(self):
            print 'post'

    for i in apis.apis:
        print i


if __name__ == '__main__':
    main()


