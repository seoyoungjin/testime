import sys
from os import path
import dbus

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))) + "/testime")
from ibus_config import IBus_Address

bus = dbus.connection.Connection(IBus_Address())
ibus = bus.get_object('org.freedesktop.IBus', '/org/freedesktop/IBus')

ctx_path = ibus.CreateInputContext("Test", dbus_interface='org.freedesktop.IBus')
ctx = bus.get_object('org.freedesktop.IBus', ctx_path)
iface = dbus.Interface(ctx, dbus_interface='org.freedesktop.IBus.InputContext')

e = ctx.GetEngine(dbus_interface='org.freedesktop.IBus.InputContext')
print("Engine = ", e[2])

iface.SetCapabilities(9)
iface.FocusIn()
iface.SetEngine('hangul')

e = iface.GetEngine()
print("Engine = ", e[2])
