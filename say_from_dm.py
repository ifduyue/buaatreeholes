#codgin: utf8

from sina import Sina
import lib
import conf
from time import sleep
import os

def get_n():
    path = lib.get_timed_path('toweiqun') + "-n"
    if os.path.exists(path):
        return int(lib.readfrom(path))
    else:
        lib.writeto(path, "0")
        return 0

def set_n(n):
    path = lib.get_timed_path('toweiqun') + "-n"
    lib.writeto(path, str(n))

o = lib.get_api()


sina = Sina(conf.username, conf.password)
sina.login()
t = 16

while t:
    t -= 1
    sleep(30)

    for uid, msg in sina.direct_messages():
        if lib.statuses_update(msg):
            print uid, msg
            sina.del_direct_message(uid)
        sleep(5)
    
    path = lib.get_timed_path('toweiqun')
    if not os.path.exists(path): continue
    n = get_n()
    i = 1
    for line in file(path):
        if i > n:
            print i, line
            sina.update_q(conf.weiqun_id, line.strip())
            set_n(i)
            sleep(5)
        i += 1
 
    
    
