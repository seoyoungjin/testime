# vim:set et sts=4 sw=4:
# -*- coding: utf-8 -*-

# TODO
# list engines

from gi import require_version as gi_require_version
gi_require_version('GLib', '2.0')
gi_require_version('GdkX11', '3.0')
gi_require_version('Gio', '2.0')
gi_require_version('Gtk', '3.0')

from gi.repository import Gtk
from gi.repository import GLib
from gi.repository import GObject

import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop

IBUS_SERVICE          = "org.freedesktop.IBus"
IBUS_PATH             = "/org/freedesktop/IBus"
IBUS_INTERFACE        = "org.freedesktop.IBus"

# change in ibus_bus_call_sync()
IBUS_SERVICE_PORTAL   = "org.freedesktop.portal.IBus"
IBUS_INTERFACE_PORTAL = "org.freedesktop.portal.IBus"

IBUS_INPUT_CONTEXT  = "org.freedesktop.IBus.InputContext"


CLIENT = "TestIME"

bus = dbus.SessionBus()
# Get Interface via Bus_Name and Object_Path.
service = bus.get_object(IBUS_SERVICE, IBUS_PATH)
interface = dbus.Interface(service, IBUS_INTERFACE)

p_service = bus.get_object(IBUS_SERVICE_PORTAL, IBUS_PATH)
p_interface = dbus.Interface(p_service,
		dbus_interface='org.freedesktop.DBus.Properties')

# list engines


# set capabilities

def IBusSetFocus(val):
    IBusSimpleMessage("FocusIn")
    IBusSimpleMessage("FocusOut")

def IBusReset():
    IBusSimpleMessage("Reset")

