import sys
from os import path
import dbus

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))) + "/testime")
from ibus_config import IBus_Address

bus = dbus.connection.Connection(IBus_Address())

ibus = bus.get_object('org.freedesktop.IBus', '/org/freedesktop/IBus')
context_path = ibus.CurrentInputContext(dbus_interface='org.freedesktop.IBus')
context = bus.get_object('org.freedesktop.IBus', context_path)
context.Introspect(dbus_interface="org.freedesktop.DBus.Introspectable")

# iface = dbus.Interface(ibus, dbus_interface='org.freedesktop.IBus')
# engines = iface.ListEngines()
engines = ibus.ListEngines(dbus_interface='org.freedesktop.IBus')

print(engines[0])

ctx2_path = ibus.CreateInputContext("Test", dbus_interface='org.freedesktop.IBus')
ctx2 = bus.get_object('org.freedesktop.IBus', ctx2_path)
ctx2.GetEngine(dbus_interface='org.freedesktop.IBus.InputContext')
