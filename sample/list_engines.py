import dbus
from pprint import pprint

IBUS_ADDRESS='unix:abstract=/home/yjseo/.cache/ibus/dbus-B57AKfRs,guid=284d0ff3d3628d8dff0883545f351e49'

bus = dbus.connection.Connection(IBUS_ADDRESS)

ibus = bus.get_object('org.freedesktop.IBus', '/org/freedesktop/IBus')
context_path = ibus.CurrentInputContext(dbus_interface='org.freedesktop.IBus')
context = bus.get_object('org.freedesktop.IBus', context_path)
context.Introspect(dbus_interface="org.freedesktop.DBus.Introspectable")

# iface = dbus.Interface(ibus, dbus_interface='org.freedesktop.IBus')
# engines = iface.ListEngines()
engines = ibus.ListEngines(dbus_interface='org.freedesktop.IBus')

# >>> context.GetAll('org.freedesktop.IBus.InputContext', dbus_interface='org.freedesktop.DBus.Properties')
# dbus.Dictionary({}, signature=dbus.Signature('sv'))

#>>> ibus.GetEnginesByNames(["hangul"], dbus_interface='org.freedesktop.IBus')
#dbus.Array([dbus.Struct((dbus.String('IBusEngineDesc'), dbus.Dictionary({}, signature=dbus.Signature('sv')), dbus.String('hangul'), dbus.String('Hangul'), dbus.String('Korean Input Method'), dbus.String('ko'), dbus.String('GPL'), dbus.String('Peng Huang <shawn.p.huang@gmail.com>'), dbus.String('ibus-hangul'), dbus.String('kr'), dbus.UInt32(99), dbus.String(''), dbus.String('한'), dbus.String(''), dbus.String('kr104'), dbus.String(''), dbus.String(''), dbus.String(''), dbus.String('')), signature=None, variant_level=1)], signature=dbus.Signature('v'))
