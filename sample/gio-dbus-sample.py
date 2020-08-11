from gi.repository import Gio
 
 
bus = Gio.bus_get_sync(Gio.BusType.SESSION, None)
proxy = Gio.DBusProxy.new_sync(bus, Gio.DBusProxyFlags.NONE, None,
                               'org.freedesktop.DBus',
                               '/org/freedesktop/DBus',
                               'org.freedesktop.DBus', None)
res = proxy.call_sync('ListNames', None, Gio.DBusCallFlags.NO_AUTO_START,
                      500, None)
print(res)
