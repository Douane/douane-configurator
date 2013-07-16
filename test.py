#!/usr/bin/env python

import gobject
import dbus
from dbus.mainloop.glib import DBusGMainLoop

def handler(*args):
    print args

bus = dbus.SystemBus(mainloop=DBusGMainLoop())
helloservice = bus.get_object("org.zedroot.Douane", "/org/zedroot/Douane")
helloservice.connect_to_signal("NewIncomingActivity", handler)

loop = gobject.MainLoop()
loop.run()
