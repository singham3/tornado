import tornado.ioloop
import tornado.web
import os.path
from tornado import gen,httpserver,options
from tornado_mysql import pools
import tornado.escape



pools.DEBUG = True
POOL = pools.Pool(
    dict(host='127.0.0.1', port=3306, user='root', passwd='', db='tornado'),
    max_idle_connections=1,
    max_recycle_sec=3)




class Login(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')
        print(username,password)
        check_login_result = yield self.check_login(username, password)
        print(check_login_result)
        if check_login_result==1:
            self.redirect('/home')
            self.finish()
        elif check_login_result==2:
            self.render("login.html", login=check_login_result, error1="user and password not match")


        elif check_login_result==3:
            self.render("login.html", login=check_login_result, error2="user does not exist")

        else:
            self.render("login.html", login=check_login_result, error3="Please enter the complete")

        self.render("login.html")

    @gen.coroutine
    def check_login(self,username,password):
        p = yield POOL.execute("SELECT * FROM signup")
        all = p.fetchall()
        if username and password:
            if username in [i[1] for i in all]:
                if password in [i[4] for i in all]:
                    return 1
                else:
                    return 2
            else:
                return 3
        else:
            return 4


class Signup(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        username = self.get_argument('username', '')
        full_name = self.get_argument('full_name', '')
        email = self.get_argument('email', '')
        password = self.get_argument('password', '')
        conformpassword = self.get_argument('conformpassword', '')
        print(username, full_name, email, password, conformpassword)
        check_register_result = yield self.check_register(username, full_name, email, password, conformpassword)
        print(check_register_result)
        if check_register_result == 1:
            cur = yield POOL.execute(
                """INSERT INTO signup (username, full_name, email, password, conformpassword) VALUES ('%(username)s', '%(full_name)s', '%(email)s', '%(password)s', '%(conformpassword)s')""" % {
                    "username": username, "full_name": full_name, "email": email, "password": password,
                    "conformpassword": conformpassword})
            cur.fetchall()

            self.redirect('/')
        elif check_register_result == 2:
            self.render('signup.html',result=check_register_result, error2='The mailbox has been registered')
        elif check_register_result == 3:
            self.render('signup.html',result=check_register_result, error3='password does not match')
        elif check_register_result == 4:
            self.render('signup.html',result=check_register_result, error4='User name has been registered')
        else:
            self.render('signup.html',result=check_register_result, error5='Please enter the complete')

        self.render("signup.html",result=check_register_result)
    @gen.coroutine
    def check_register(self, username, full_name, email, password, conformpassword):
        p = yield POOL.execute("SELECT * FROM signup")
        all = p.fetchall()
        if username and full_name and email and password and conformpassword:
            if username not in [i[1] for i in all]:  # Username is not in the database
                if email not in [i[3] for i in all]:
                    if password == conformpassword:
                        return 1  # nothing
                    else:
                        return 3
                else:
                    return 2  # The mailbox exists and the username does not exist.
            else:
                return 4  # The username is in the database and already exists
            # elif:
            #     if username and password: return 4 #Enter email
            #     elif username and email: return 5 #Enter your user name
            #     elif password and email: return 6 #enter password

        else:
            return 5









class Home(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class About(tornado.web.RequestHandler):
    def get(self):
        self.render("about.html")

class Services(tornado.web.RequestHandler):
    def get(self):
        self.render("services.html")


class Contact(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        full_name = self.get_argument('full_name','')
        phone = self.get_argument('phone','')
        email = self.get_argument('email','')
        message = self.get_argument('message','')



        sql = "INSERT INTO tornado ( full_name, phone, email, message) VALUES ( %s,%s, %s, %s);"
        cur =  yield POOL.execute(sql,(full_name,phone,email,message))
        cur.fetchall()

        self.render("contact.html")
        print(full_name, phone, email, message)


class Portfolio_1(tornado.web.RequestHandler):
    def get(self):
        self.render("portfolio-1-col.html")
class Portfolio_2(tornado.web.RequestHandler):
    def get(self):
        self.render("portfolio-2-col.html")
class Portfolio_3(tornado.web.RequestHandler):
    def get(self):
        self.render("portfolio-3-col.html")
class Portfolio_4(tornado.web.RequestHandler):
    def get(self):
        self.render("portfolio-4-col.html")
class Portfolio_item(tornado.web.RequestHandler):
    def get(self):
        self.render("portfolio-item.html")

class Blog_Home_1(tornado.web.RequestHandler):
    def get(self):
        self.render("blog-home-1.html")

class Blog_Home_2(tornado.web.RequestHandler):
    def get(self):
        self.render("blog-home-2.html")
class Blog_Post(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        comment = self.get_argument('comment', '')

        sql = "INSERT INTO comment (comment) VALUES ( %s);"
        cur = yield POOL.execute(sql, (comment))
        cur.fetchall()
        self.render("blog-post.html" ,comment=comment)
class Full_Width(tornado.web.RequestHandler):
    def get(self):
        self.render("full-width.html")
class Sidebar(tornado.web.RequestHandler):
    def get(self):
        self.render("sidebar.html")
class Faq(tornado.web.RequestHandler):
    def get(self):
        self.render("faq.html")
class _404(tornado.web.RequestHandler):
    def get(self):
        self.render("404.html")
class Pricing(tornado.web.RequestHandler):
    def get(self):
        self.render("pricing.html")
settings = {
    "debug": True,
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "template_path": os.path.join(os.path.dirname(__file__), "templates")

}

@gen.coroutine
def make_app():
    tornado.options.parse_command_line()
    application= tornado.web.Application([
        (r"/", Login),
        (r"/register", Signup),
        (r"/home", Home),
        (r"/about", About),
        (r"/services", Services),
        (r"/contact", Contact),
        (r"/portfolio-1", Portfolio_1),
        (r"/portfolio-2", Portfolio_2),
        (r"/portfolio-3", Portfolio_3),
        (r"/portfolio-4", Portfolio_4),
        (r"/portfolio-item", Portfolio_item),
        (r"/blog-home-1", Blog_Home_1),
        (r"/blog-home-2", Blog_Home_2),
        (r"/blog-post", Blog_Post),
        (r"/full-width", Full_Width),
        (r"/sidebar", Sidebar),
        (r"/faq", Faq),
        (r"/404", _404),
        (r"/pricing", Pricing),
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