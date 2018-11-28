import tornado.ioloop
import tornado.web
import os.path
from tornado import gen,httpserver,options
from tornado_mysql import pools
import tornado.escape
import bcrypt
import concurrent.futures
import tornado.escape



pools.DEBUG = True
POOL = pools.Pool(
    dict(host='127.0.0.1', port=3306, user='root', passwd='', db='tornado'),
    max_idle_connections=1,
    max_recycle_sec=3)
executor = concurrent.futures.ThreadPoolExecutor(2)


class MainHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        username = self.get_argument('username', '')
        full_name = self.get_argument('full_name', '')
        email = self.get_argument('email', '')
        password = self.get_argument('password', '')
        conformpassword = self.get_argument('conformpassword', '')
        print(username,full_name,email,password,conformpassword)




        self.render("signup.html")






settings = {
    "debug":True,
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "template_path": os.path.join(os.path.dirname(__file__), "templates")
                               }
@gen.coroutine
def make_app():
    tornado.options.parse_command_line()
    application= tornado.web.Application([
        (r"/register", MainHandler),
        (r"/(templates)", tornado.web.StaticFileHandler,
         dict(path=settings['template_path'])),
        (r"/(static)", tornado.web.StaticFileHandler,
         dict(path=settings['static_path']))
    ],**settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)

if __name__ == "__main__":
    app = make_app()
    tornado.ioloop.IOLoop.current().start()