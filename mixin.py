from tornado.auth import OAuthMixin
import urllib
from tornado import httpclient
import logging
from tornado import escape

class SinaMixin(OAuthMixin):
    
    _OAUTH_REQUEST_TOKEN_URL = 'http://api.t.sina.com.cn/oauth/request_token'
    _OAUTH_ACCESS_TOKEN_URL = 'http://api.t.sina.com.cn/oauth/access_token'
    _OAUTH_AUTHORIZE_URL = 'http://api.t.sina.com.cn/oauth/authorize'
    _OAUTH_VERSION = '1.0a'
    _OAUTH_NO_CALLBACKS = False


    def authenticate_redirect(self):
        http = httpclient.AsyncHTTPClient()
        http.fetch(self._oauth_request_token_url(), self.async_callback(
            self._on_request_token, self._OAUTH_AUTHENTICATE_URL, None))

    def sina_request(self, path, callback, access_token=None,
                           post_args=None, **args):
        url = "http://api.t.sina.com.cn" + path + ".json"
        if access_token:
            all_args = {}
            all_args.update(args)
            all_args.update(post_args or {})
            method = "POST" if post_args is not None else "GET"
            oauth = self._oauth_request_parameters(
                url, access_token, all_args, method=method)
            args.update(oauth)
        if args: url += "?" + urllib.urlencode(args)
        callback = self.async_callback(self._on_sina_request, callback)
        http = httpclient.AsyncHTTPClient()
        if post_args is not None:
            http.fetch(url, method="POST", body=urllib.urlencode(post_args),
                       callback=callback)
        else:
            http.fetch(url, callback=callback)

    def _on_sina_request(self, callback, response):
        if response.error:
            logging.warning("Error response %s fetching %s", response.error,
                            response.request.url)
            callback(None)
            return
        callback(escape.json_decode(response.body))

    def _oauth_consumer_token(self):
        self.require_setting("sina_consumer_key", "Sina OAuth")
        self.require_setting("sina_consumer_secret", "Sina OAuth")
        return dict(
            key=self.settings["sina_consumer_key"],
            secret=self.settings["sina_consumer_secret"])

    def _oauth_get_user(self, access_token, callback):
        callback = self.async_callback(self._parse_user_response, callback)
        self.sina_request(
            "/users/show/" + access_token["user_id"],
            access_token=access_token, callback=callback)

    def _parse_user_response(self, callback, user):
        if user:
            user["username"] = user["screen_name"]
        callback(user)
