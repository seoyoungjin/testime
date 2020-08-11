#!/usr/bin/env python
# -'''- coding: utf-8 -'''-

import sys
from traceback import print_exc

# import python dbus module and GLib mainloop support
import dbus
import dbus.service
import dbus.mainloop.glib

from PySide2.QtCore import *
from PySide2.QtWidgets import QWidget, QVBoxLayout
from PySide2.QtWidgets import QPushButton, QApplication

IBUS_SERVICE          = "org.freedesktop.IBus"
IBUS_PATH             = "/org/freedesktop/IBus"
IBUS_INTERFACE        = "org.freedesktop.IBus"
IBUS_INPUT_CONTEXT  = "org.freedesktop.IBus.InputContext"

# Enable glib main loop support
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
# Get the session bus
bus = dbus.SessionBus()

try:
    # Get the remote object
    remote_object = bus.get_object(IBUS_SERVICE, IBUS_PATH)
    # Get the remote interface for the remote object
    iface = dbus.Interface(remote_object, IBUS_INTERFACE)
except dbus.DBusException:
    print_exc()
    sys.exit(1)

# signal handler
def button_quit():
    pass
  

def say_hello():
    print("Button clicked, Hello!")

# The adaptor, MUST inherit dbus.service.Object
class DBusWidget(dbus.service.Object):
    def __init__(self, name, session):
        # export this object to dbus
        dbus.service.Object.__init__(self, name, session)

class MyCanvas(QWidget):
    def __init__(self, name, session):
        self.dw = DBusWidget(name, session)
        QWidget.__init__(self)
   
    def mousePressEvent(self, event):
        print('mouse press')
        self.setFocus()

    def focusInEvent(self, event):
        print('focus in event')
        dbus.service.method(IBUS_INPUT_CONTEXT, "FocusIn")

# main function
if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)                                                                    
    window = QWidget()
    layout = QVBoxLayout()
    canvas = MyCanvas(bus, IBUS_PATH)
    canvas.setFixedSize(300, 300)

    button = QPushButton("Quit")
    button.clicked.connect(app.quit)

    layout.addWidget(canvas)
    layout.addWidget(button)

    window.setLayout(layout)
    window.show()

    # connect the DBus signal clicked to the function button_clicked
    #iface.connect_to_signal("clicked", button_clicked)
    #iface.connect_to_signal("lastWindowClosed", app.quit)

    app.exec_()
