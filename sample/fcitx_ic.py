import dbus

FCITX_SERVICE         = "org.fcitx.Fcitx"
FCITX_IM_PATH         = "/inputmethod"
FCITX_IC_PATH         = "/inputcontext_%d"
FCITX_IM_INTERFACE    = "org.fcitx.Fcitx.InputMethod"
FCITX_IC_INTERFACE    = "org.fcitx.Fcitx.InputContext"

bus = dbus.SessionBus(private = True)
fcitx = bus.get_object(FCITX_SERVICE, FCITX_IM_PATH)
print("GetCurrentIM = ", fcitx.GetCurrentIM())

#ret = fcitx.CreateICv2("Sample", pid)
ret = fcitx.CreateICv2("Sample")

# add_match, add_filter
print("ic_path =", FCITX_IC_PATH % ret[0])
ctx = bus.get_object(FCITX_SERVICE, FCITX_IC_PATH % ret[0])
iface = dbus.Interface(ctx, dbus_interface=FCITX_IC_INTERFACE)

iface.SetCapacity(255)
iface.FocusIn()
iface.ProcessKeyEvent(32, 0, 0, 0, 0)
