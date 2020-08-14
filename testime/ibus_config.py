import os
import configparser

# 
# libdbus - get_local_machine_id()
#
# bus = dbus.SessionBus()
# ibus = bus.get_object("org.freedesktop.IBus", "/org/freedesktop/IBus")
# ibus.GetMachineId(dbus_interface='org.freedesktop.DBus.Peer')
# dbus.String('6209f12f15ce4b16bcd09203f6e97ecf')

def get_machine_id():
    try:
        with open("/etc/machine-id") as f:
            return f.read().strip()
    except:
        pass
    try:
        with open("/var/lib/dbus/machine-id") as f:
            return f.read().strip()
    except:
        pass
    return "" 


def IBus_AddressFilename():
    if 'IBUS_ADDRESS' in os.environ:
        return os.environ["IBUS_ADDRESS"]

    if 'DISPLAY' in os.environ:
        display = os.environ["DISPLAY"]
    else:
        display = ":0.0"
    host, disp_num  = display.split(':')
    if not host:
        host = 'unix'
    disp_num  = disp_num.split('.')[0]

    if 'XDG_CONFIG_HOME' in os.environ:
        config_dir = os.environ["XDG_CONFIG_HOME"]
    else:
        if not 'HOME' in os.environ:
            return None
        config_dir = os.environ['HOME'] + '/.config'

    key = get_machine_id()
    return format("%s/ibus/bus/%s-%s-%s" % (config_dir, key, host, disp_num))


def IBus_Address():
    config_path = IBus_AddressFilename()
    with open(config_path, 'r') as f:
        config_string = '[dummy]\n' + f.read()
    config = configparser.ConfigParser()
    config.read_string(config_string)
    return config.get('dummy', 'IBUS_ADDRESS')


if __name__ == "__main__":
	print(get_machine_id())
	print(IBus_AddressFilename())
	print(IBus_Address())

