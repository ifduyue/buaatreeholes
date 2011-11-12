#coding: utf8

from urlfetch import *
import re
from urlparse import parse_qsl, urljoin
import lib
from bot_txt import *

class Sina(object):
    
    def __init__(self, username, password):
        self.cookies = None
        self.username = username
        self.password = password
    
    def login(self):
        
        response = fetch('http://3g.sina.com.cn/prog/wapsite/sso/login_submit.php')
        data = response.body
        vk = re.search(r'''name="vk"\s+?value="(.*?)"''', data).group(1)
        pname = re.search(r'''name="password_(\d+)"''', data).group(1)
        
        post = {
            'mobile': self.username,
            'password_'+pname: self.password,
            'vk': vk,
            'remember': 'on',
            'submit': '1'
        }
        response = fetch(
            'http://3g.sina.com.cn/prog/wapsite/sso/login_submit.php',
            data = post
        )
        
        set_cookie = response.msg.getheaders('set-cookie')
        self.cookies = setcookielist2cookiestring(set_cookie)
        return self.cookies
    
    
    def del_tweets(self):
        while True:
            response = fetch(
                'http://weibo.cn/dpool/ttt/home.php?cat=1',
                headers={'Cookie': self.cookies}
            )
            
            data = re.findall(r'href="mblogDeal\.php\?([^"]+?act=del[^"]+)"', response.body)
            if not data:
                break
            for i in data:
                j = parse_qsl(i)
                qs = dict(j)
                qs['act'] = 'dodel'
                qs = '&'.join(['='.join(k) for k in qs.items()])
                url = 'http://weibo.cn/dpool/ttt/mblogDeal.php?' + qs
                
                try:
                    fetch(
                        url,
                        headers = {'Cookie': self.cookies}
                    )
                    print url
                except:pass
                
    def unfollow(self):
        while True:
            response = fetch(
                'http://weibo.cn/dpool/ttt/attention.php?cat=0',
                headers={'Cookie': self.cookies}
            )
            
            data = re.findall(r'href="attnDeal\.php\?([^"]+?act=del[^"]+)"', response.body)
            if not data:
                break
            for i in data:
                j = parse_qsl(i)
                qs = dict(j)
                qs['act'] = 'delc'
                qs = '&'.join(['='.join(k) for k in qs.items()])
                url = 'http://weibo.cn/dpool/ttt/attnDeal.php?' + qs
                
                try:
                    fetch(
                        url,
                        headers = {'Cookie': self.cookies}
                    )
                    print url
                except:pass
                
    def remove_followers(self, black=False):
        while True:
            response = fetch(
                'http://weibo.cn/dpool/ttt/attention.php?cat=1',
                headers={'Cookie': self.cookies}
            )
            
            data = re.findall(r'href="attnDeal\.php\?([^"]+?act=remove[^"]+)"', response.body)
            if not data:
                break
            for i in data:
                j = parse_qsl(i)
                qs = dict(j)
                qs['act'] = 'removec'
                qs = '&'.join(['='.join(k) for k in qs.items()])
                url = 'http://weibo.cn/dpool/ttt/attnDeal.php?' + qs
                
                try:
                    fetch(
                        url,
                        headers = {'Cookie': self.cookies}
                    )
                    print url
                except:pass
                
    def direct_messages(self):
        response = fetch(
            'http://weibo.cn/dpool/ttt/msg.php?cat=3',
            headers={'Cookie': self.cookies}
        )
    
        def parse_response(data):
            data = txt_wrap_by_all('<div class="c">', '</div>', data)
            for i in data:
                if i.startswith('<span class="kt">[新]</span>'):
                    i = i[len('<span class="kt">[新]</span>'):]
                msg = txt_wrap_by('</span>', '<span', i)
                uid = txt_wrap_by('<a href="home.php?uid=', '"', i)
                if msg and uid:
                    msg = lib.strip_tags(msg)
                    msg = msg.replace('&nbsp;', '')
                    yield (uid, msg)
        
        return list(parse_response(response.body))
        
    def del_direct_message(self, uid):
        response = fetch(
            'http://weibo.cn/dpool/ttt/msgDeal.php?st=3070&act=delchatc&uid=%s&rl=2' % uid,
            headers={'Cookie': self.cookies}
        )
        return response

    def update_q(self, qid, status):
        response = fetch(
            'http://weibo.cn/dpool/ttt/grouphome.php',
            headers={
                'Cookie': self.cookies,
            },
            data = {
                'act': 'addmblog',
                'groupid': qid,
                'from': 'home',
                'rl': 0,
                'content': status
            },
        )
        return response
                
if __name__ == '__main__':
    import sys
    username, password = sys.argv[1:]
    sina = Sina(username, password)
    sina.login()
    #sina.del_tweets()
    #sina.unfollow()
    #sina.remove_followers()
