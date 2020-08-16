import dbus

FCITX_SERVICE         = "org.fcitx.Fcitx"
FCITX_IM_PATH         = "/inputmethod"
FCITX_IC_PATH         = "/inputcontext_%d"
FCITX_IM_INTERFACE    = "org.fcitx.Fctix.InputMethod"
FCITX_IC_INTERFACE    = "org.fcitx.Fctix.InputContext"

bus = dbus.SessionBus(private = True)
fcitx = bus.get_object(FCITX_SERVICE, FCITX_IM_PATH)

#ret = fcitx.CreateICv2("Sample", pid)
ret = fcitx.CreateICv2("Sample")

# add_match, add_filter
print("ic_path =", FCITX_IC_PATH % ret[0])
ctx = bus.get_object(FCITX_SERVICE, FCITX_IC_PATH % ret[0])
iface = dbus.Interface(ctx, dbus_interface=FCITX_IC_INTERFACE)

