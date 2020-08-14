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

from testime.ibus_config import IBus_Address
from testime import keysyms, modifier

IBUS_CAP_PREEDIT_TEXT       = 1
IBUS_CAP_AUXILIARY_TEXT     = 1 << 1
IBUS_CAP_LOOKUP_TABLE       = 1 << 2
IBUS_CAP_FOCUS              = 1 << 3
IBUS_CAP_PROPERTY           = 1 << 4
IBUS_CAP_SURROUNDING_TEXT   = 1 << 5

IBUS_SERVICE          = "org.freedesktop.IBus"
IBUS_PATH             = "/org/freedesktop/IBus"
IBUS_INTERFACE        = "org.freedesktop.IBus"
IBUS_INPUT_CONTEXT    = "org.freedesktop.IBus.InputContext"

# Enable glib main loop support
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
bus = dbus.connection.Connection(IBus_Address())

try:
    # Get the remote object
    ibus = bus.get_object(IBUS_SERVICE, IBUS_PATH)
    # Get the remote interface for the remote object
    iface = dbus.Interface(ibus, IBUS_INTERFACE)
except dbus.DBusException:
    print_exc()
    sys.exit(1)

# signal handler
def button_quit():
    pass


class MyCanvas(QWidget):
    def __init__(self, name, session):
        self.bus = session
        self.ibus = bus.get_object(IBUS_SERVICE, IBUS_PATH)
        ic_path = self.ibus.CreateInputContext(name, dbus_interface='org.freedesktop.IBus')
        self.ic = bus.get_object('org.freedesktop.IBus', ic_path)
        self.iface = dbus.Interface(self.ic, IBUS_INPUT_CONTEXT)

        self.iface.SetCapabilities(255)
        self.iface.connect_to_signal("CommitText", self.__commit_text_cb)

        self.iface.connect_to_signal("UpdatePreeditText", self.__update_preedit_text_cb)
        self.iface.connect_to_signal("ShowPreeditText", self.__show_preedit_text_cb)
        self.iface.connect_to_signal("HidePreeditText", self.__hide_preedit_text_cb)

        self.iface.connect_to_signal("UpdateAuxiliaryText", self.__update_aux_text_cb)
        self.iface.connect_to_signal("ShowAuxiliaryText", self.__show_aux_text_cb)
        self.iface.connect_to_signal("HideAuxiliaryText", self.__hide_aux_text_cb)

        self.iface.connect_to_signal("UpdateLookupTable", self.__update_lookup_table_cb)
        self.iface.connect_to_signal("ShowLookupTable", self.__show_lookup_table_cb)
        self.iface.connect_to_signal("HideLookupTable", self.__hide_lookup_table_cb)

        self.__is_invalidate = False
        self.__preedit = None
        self.__preedit_visible = False
        self.__aux_string = None
        self.__aux_string_visible = False
        self.__lookup_table = None
        self.__lookup_table_visible = False

        QWidget.__init__(self)

    def keyPressEvent(self, event):
        print('key press', event)
        self.iface.ProcessKeyEvent(keysyms.space, 0, modifier.SHIFT_MASK)
        self.iface.ProcessKeyEvent(keysyms.K, 0, 0)

    def mousePressEvent(self, event):
        print('mouse press')
        self.setFocus()

    def focusInEvent(self, event):
        print('focus in event')
        self.iface.FocusIn()

    def focusOutEvent(self, event):
        print('focus out event')
        self.iface.FocusOut()

    def __commit_text_cb(self, text):
        print("_commit_text_cb", text)

    def __update_preedit_text_cb(self, text, cursor_pos, visible):
        print("__update_preedit_text_cb", text)
        self.__preedit = text
        self.__preedit_visible = visible
        self.__invalidate()

    def __show_preedit_text_cb(self):
        print("__show_preedit_text_cb")
        if self.__preedit_visible:
            return
        self.__preedit_visible = True
        self.__invalidate()

    def __hide_preedit_text_cb(self):
        print("__hide_preedit_text_cb")
        if not self.__preedit_visible:
            return
        self.__preedit_visible = False
        self.__invalidate()

    def __update_aux_text_cb(self, text, visible):
        print("__update_aux_text_cb")
        self.__aux_string = text
        self.__aux_string_visible = visible
        self.__invalidate()

    def __show_aux_text_cb(self):
        print("__show_aux_text_cb")
        if self.__aux_string_visible:
            return
        self.__aux_string_visible = True
        self.__invalidate()

    def __hide_aux_text_cb(self):
        print("__hide_aux_text_cb")
        if not self.__aux_string_visible:
            return
        self.__aux_string_visible = False
        self.__invalidate()

    def __update_lookup_table_cb(self, lookup_table, visible):
        print("__update_lookup_table_cb")
        self.__lookup_table = lookup_table
        self.__lookup_table_vis 
        self.__invalidate()

    def __show_lookup_table_cb(self):
        print("__show_lookup_table_cb")
        if self.__lookup_table_visible:
            return
        self.__lookup_table_visible = True
        self.__invalidate()

    def __hide_lookup_table_cb(self):
        print("__hide_lookup_table_cb")
        if not self.__lookup_table_visible:
            return
        self.__lookup_table_visible = False
        self.__invalidate()

    def __invalidate(self):
        self.__is_invalidate = True


# main function
if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)

    window = QWidget()
    layout = QVBoxLayout()
    canvas = MyCanvas("TestIME", bus)
    canvas.setFixedSize(300, 300)

    button = QPushButton("Quit")
    button.clicked.connect(app.quit)

    layout.addWidget(canvas)
    layout.addWidget(button)

    window.setLayout(layout)
    window.show()

    app.exec_()
