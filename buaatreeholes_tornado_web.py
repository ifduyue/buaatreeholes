#coding: utf-8
import tornado.web
import tornado.ioloop
from tornado.options import options, define
import tornado.auth
import json


from route import route, routes
import conf
import mixin
from lib import *


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user = self.get_secure_cookie("user")
        try:
            return json.loads(user)
        except: return None
        
@route(r"/")
class MainHandler(BaseHandler):
    def get(self):
        if self.current_user:
            return self.redirect("/say")
        self.render("index.html", notice='')
        
@route(r"/auth")
class AuthHandler(BaseHandler, mixin.SinaMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument('oauth_token', None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authorize_redirect("/auth")
        
    def _on_auth(self, user):
        if user:
            access_token = user.get('access_token')
            access_token['username'] = user['username']
            self.set_secure_cookie("user", json.dumps(access_token))
            return self.redirect("/say")
        
    
@route(r"/authd")
class AuthdHandler(BaseHandler):
    def get(self):
        pass
    
@route(r"/say")
class SayHandler(BaseHandler, mixin.SinaMixin):
    def get(self):
        user = self.current_user
        if not user:
            return self.redirect('/auth')
        self.render('say.html', user=user["username"], notice='')
        
    @tornado.web.asynchronous
    def post(self):
        user = self.current_user
        if not user:
            raise tornado.web.HTTPError(403)
        word = self.get_argument("word", None)
        toweiqu = self.get_argument("toweiqun", None)
        self.sina_request("/statuses/update", self._on_update,
                          access_token=self.settings['buaatreeholes_access_token'],
                          post_args = {
                            'status': mb_code(word),
                          },
                        )
        
    def _on_update(self, body):
        if body is None:
            raise tornado.web.HTTPError(500)
        self.render("say.html", notice="小纸条已经丢进树洞", user=self.current_user['username'])
        

@route(r"/logout")
class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_all_cookies()
        self.redirect("/")
        
        
application = tornado.web.Application(
    routes,
    **conf.settings
)

if __name__ == '__main__':
    define('port', default=8888, type=int)
    
    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
    
    
