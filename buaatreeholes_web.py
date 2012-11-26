#!/usr/bin/env python
#-*- coding: utf-8 -*-

from bottle import *
import sys
import lib
import conf
from beaker.middleware import SessionMiddleware
session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 3600 * 24 * 3,
    'session.data_dir': './data',
    'session.key': conf.session_key,
    'session.auto': True,
}
app = SessionMiddleware(app(), session_opts)


def check_formhash():
    post = request.POST
    s = request.environ.get('beaker.session')
    formhash = s.get('formhash', '')
    return formhash == post.get('formhash', None)


def set_formhash(formhash=None):
    if formhash is None:
        formhash = lib.randstr()
    s = request.environ.get('beaker.session')
    s['formhash'] = formhash
    return formhash


def toggle_notice(notice=''):
    s = request.environ.get('beaker.session')
    ret = s.get('notice', '')
    s['notice'] = notice
    return ret

    
@route('/auth')
def auth():
    s = request.environ.get('beaker.session')
    
    o = lib.get_oauth_handler(conf.site_url+'/authd')
    url = o.get_authorization_url()
    
    s['request_token'] = o.request_token
    s.save()
    
    raise HTTPResponse("", status=303, header=dict(Location=url))


@route('/authd')
def authd():
    s = request.environ.get('beaker.session')
    request_token = s.get('request_token', '')
    if not request_token:
        abort(403, 'request token not set') 
    
    token = request.GET.get('oauth_token')
    verifier = request.GET.get('oauth_verifier')
    
    o = lib.get_oauth_handler()
    o.set_request_token(request_token.key, request_token.secret)
    try:
        access_token = o.get_access_token(verifier)
    except Exception, e:
        abort(500, 'check access_token failed')
    
    o = lib.get_user_api(access_token)
    
    try:
        user = o.verify_credentials()
        s['uid'] = str(user.id)
        s['name'] = lib.mb_code(user.name)
    except: abort(500, 'can not get user info')
    
    s['access_token'] = access_token
    s.save()
    
    redirect('/say')


@route('/')
@view('index')
def root():
    s = request.environ.get('beaker.session')
    access_token = s.get('access_token', '')
    if not access_token:
        return {
            'notice': toggle_notice(),
            'uid': s.get('uid', ''),
            'name': s.get('name',''),
        }
    redirect('/say')
        

@route('/static/:path#.+#')
def static(path):
    raise static_file(path, root='./static')


@route('/say', method='POST')
@view('say')
def say():
    s = request.environ.get('beaker.session')
    access_token = s.get('access_token', '')
    if not access_token:
        toggle_notice('还未登录, <a href="/auth"><img src="/static/login240.png" /></a> ')
        redirect('/')
    if not check_formhash():
        abort(403, 'how you get here?')

    o = lib.get_user_api(access_token)
    
    word = request.POST.get('word', '')
    word = " ".join(word.split())
    wordlen = len(lib.mb_code(word, 'utf-8').decode('utf-8'))
    toweiqun = request.POST.get('toweiqun', '')
    if wordlen == 0 or wordlen > 140:
	abort(403, 'invalid status')
		
    try:
        api = lib.get_api()
        api.update_status(word)
        toggle_notice('小纸条已经丢进树洞')
        if toweiqun == 'on':
            lib.appendto(
                lib.get_timed_path('toweiqun'),
                word + "\n",
            )
        return {
            'uid': s.get('uid', ''),
            'name': s.get('name',''),
            'notice': toggle_notice(),
            'formhash': set_formhash(),
        }
    except Exception, e:
        return "error: " + str(e)


@route('/say')
@view('say')
def say():
    s = request.environ.get('beaker.session')
    access_token = s.get('access_token', '')
    if not access_token:
        toggle_notice('还未登录, <a href="/auth"><img src="/static/login240.png" /></a> ')
        redirect('/')
    return {
        'notice': toggle_notice(), 
        'uid': s.get('uid', ''),
        'name': s.get('name',''),
        'formhash': set_formhash(),
    }
    

@route('/follow')
def follow():
    s = request.environ.get('beaker.session')
    access_token = s.get('access_token', '')
    if not access_token:
        redirect('/auth')
        
    try:
        o = lib.get_user_api(access_token)
        o.create_friendship(user_id=2440698035)
    except Exception, e:
        if "already followed" not in getattr(e, "reason", ""):
            abort(500, str(e))
        
    raise HTTPResponse("", status=303, header=dict(Location=conf.weibo_url))


@route('/logout')
def logout():
    s = request.environ.get('beaker.session')
    s.delete()
    s.invalidate()
    redirect('/')


@route('/error')
def error():
    abort(403, 'error page should always return an error')


try:
    port = int(sys.argv[1])
except:
    port = 8080
run(app=app, server=GeventServer, host='127.0.0.1', port=port, quiet=True, fast=True)

