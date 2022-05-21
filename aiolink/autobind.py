import sys
from threading import Lock

lock_call = Lock()
lock_proxy = Lock()

re_enter = False

try:del sys.modules['socket']
except:pass

import socket

old_bind = socket.socket.bind

def auto_bind(s,*argv,**kw):
    global lock, re_enter
    with lock_call:
        if not re_enter:
            with lock_proxy:
                re_enter = True
                addr,port = argv[0]
                print("{}.auto_bind( {}:{},**{})".format((__name__), (addr), (port), (kw)))
                runcmd ="{} -i -mwebsockify {}:{} 127.0.0.1:{}".format((sys.executable), (addr), (port+20000), (port))
                print(runcmd)
                try:
                    return old_bind(s,*argv,**kw)
                finally:
                    os.system('xterm -e "{}" &'.format((runcmd)))
        else:
            print('binding {}'.format((argv)))
        return old_bind(s,*argv,**kw)

socket.socket.bind = auto_bind


from websockify.websocketproxy import *
