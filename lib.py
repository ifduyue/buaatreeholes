#!/usr/bin/env python
from json import loads as jsonloads
from json import dumps as jsondumps
from weibopy import OAuthHandler, API, WeibopError, oauth
import conf
import re
import random
import string
import os
import time

def get_path(filename=None):
    HERE = os.path.dirname(os.path.abspath(__file__))
    if filename is not None:
        HERE = os.path.join(HERE, filename)
    return HERE

def get_data_path(filename=None):
    data_dir = get_path("data")
    if not os.path.isdir(data_dir):
        os.makedirs(data_dir)
    return os.path.join(data_dir, filename) if filename is not None else data_dir

def make_data_dir(dirname=None):
    path = get_data_path(dirname)
    if not os.path.isdir(path):
        os.makedirs(path)
    return path

def get_timed_path(prefix=None):
    filename = time.strftime('%Y-%m-%d')
    if prefix is None:
        path = get_data_path(filename)
    else:
        path = make_data_dir(prefix)
        path = os.path.join(path, filename)
    return path
    
def mb_code(string, coding="utf-8"):
    if isinstance(string, unicode):
        return string.encode(coding)
    for c in ('utf-8', 'gb2312', 'gbk', 'gb18030', 'big5'):
        try:
            return string.decode(c).encode(coding)
        except:
            pass
    return string

def writeto(path, data):
    fh = open(path, 'w')
    fh.write(data)
    fh.close()
    
def readfrom(path):
    fh = open(path, 'r')
    data = fh.read()
    fh.close()
    return data

def appendto(path, data):
    fh = open(path, 'a+')
    fh.write(data)
    fh.close()
    
def dumpto(path, obj):
    import pickle
    fh = open(path, 'wb')
    pickle.dump(obj, fh)
    fh.close()
    
def loadfrom(path):
    import pickle
    fh = None
    try:
        fh = open(path, 'rb')
        obj = pickle.load(fh)
    except Exception, e:
        obj = None
    finally:
        if fh: fh.close()
    return obj

def strip_tags(html):
    html = re.sub("<.*?>", " ", html)
    return re.sub("\s+", " ", html)
    
def randstr(l=4, h=8):
    import string
    chars = string.ascii_letters + string.digits
    result = ''
    length = random.randint(l, h)
    for i in xrange(length):
        result += random.choice(chars)
    return result
        
def decodeHtmlentities(string):
    entity_re = re.compile("&(#?)(\d{1,5}|\w{1,8});")

    def substitute_entity(match):
        from htmlentitydefs import name2codepoint as n2cp
        ent = match.group(2)
        if match.group(1) == "#":
            return unichr(int(ent))
        else:
            cp = n2cp.get(ent)

            if cp:
                return unichr(cp)
            else:
                return match.group()

    return entity_re.subn(substitute_entity, string)[0]

def get_conf():
    import conf
    confs = {}
    for i in dir(conf):
        if i.startswith('__'):
            continue
        confs[i] = getattr(conf, i)
    return confs

def set_conf(confs):
    import os
    confile = os.path.join(os.path.dirname(__file__), 'conf.py')
    with open(confile, 'w') as f:
        for k, v in confs.items():
            if isinstance(v, int):
                format = "%s = %s\n"
            elif isinstance(v, str):
                format = "%s = '%s'\n"
            else:
                continue
            f.write(format % (k, v))
        return True
    
def get_oauth_handler(callback=None):
    return OAuthHandler(
        conf.consumer_key,
        conf.consumer_secret,
        callback=callback,
    )
    
def get_auth_url(callback=None):
    o = get_oauth_handler(callback)
    ourl = o.get_authorization_url()
    request = oauth.OAuthRequest.from_token_and_callback(
        token = o.request_token,
        callback = callback,
        http_url = ourl,
    )
    return request.to_url()
    

def get_api():
    c = get_conf()
    try:
        o = get_oauth_handler()
        o.setToken(c['access_token_key'], c['access_token_secret'])
    except KeyError, e:
        sys.stderr.write("you should run get_oauthed.py first.\n")
    return API(o)
    
def get_user_api(access_token):
    o = get_oauth_handler()
    o.setToken(access_token.key, access_token.secret)
    return API(o)
    
def statuses_update(status):
    api = get_api()
    try:
        api.update_status(status)
        return True
    except:
        return False
