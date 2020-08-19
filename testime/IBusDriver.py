#!/usr/bin/env python
# -'''- coding: utf-8 -'''-

import sys
from traceback import print_exc

import dbus
import dbus.service
import dbus.mainloop.glib

from PySide2 import QtCore
from PySide2.QtCore import qDebug

from testime.ibus_config import IBus_Address

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


# LATER class IBusDriver(dbus.service.Object):
class IBusDriver(QtCore.QObject):

    commitText = QtCore.Signal(str)
    preeditChanged = QtCore.Signal()

    def __init__(self, name):
        super().__init__()
        self.bus = dbus.connection.Connection(IBus_Address())
        try:
            # Get the remote object
            self.ibus = self.bus.get_object(IBUS_SERVICE, IBUS_PATH)
            # Get the remote interface for the remote object
            ic_path = self.ibus.CreateInputContext(name, dbus_interface=IBUS_INTERFACE)
            # LATER add_match
            self.ic = self.bus.get_object('org.freedesktop.IBus', ic_path)
            self.iface = dbus.Interface(self.ic, IBUS_INPUT_CONTEXT)
        except dbus.DBusException:
            print_exc()
            sys.exit(1)

        # self.iface.SetCapabilities(255)
        self.iface.SetCapabilities(9)
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

        self.__preedit = None
        self.__preedit_visible = False
        self.__aux_string = None
        self.__aux_string_visible = False
        self.__lookup_table = None
        self.__lookup_table_visible = False

    def __del__(self):
        self.Quit()

    def preedit(self):
        return self.__preedit

    def preeditVisible(self):
        return self.__preedit_visible

    def engine(self):
        return self.iface.GetEngine()[2] 

    def Reset(self):
        self.iface.Reset()

    def Quit(self):
        # LATER
        # connection cloase, unref
        pass

    def ProcessKeyEvent(self, keysym, scancode, mod):
        return self.iface.ProcessKeyEvent(keysym, scancode, mod)

    def __commit_text_cb(self, text):
        qDebug("< CommitText : %s" % text[2])
        self.commitText.emit(text[2])

    def __update_preedit_text_cb(self, text, cursor_pos, visible):
        assert(text[0] == 'IBusText')
        qDebug("< UpdatePreeditText : text = %s cursor_pos = %d visible = %d" %
                (text[2], cursor_pos, visible))
        self.__preedit = text[2]
        self.__preedit_visible = visible
        self.preeditChanged.emit()

    def __show_preedit_text_cb(self):
        qDebug("< ShowPreeditText")
        if self.__preedit_visible:
            return
        self.__preedit_visible = True
        self.preeditChanged.emit()

    def __hide_preedit_text_cb(self):
        qDebug("< HidePreeditText")
        if not self.__preedit_visible:
            return
        self.__preedit_visible = False
        self.preeditChanged.emit()

    def __update_aux_text_cb(self, text, visible):
        qDebug("< UpdateAuxiliaryText")
        self.__aux_string = text
        self.__aux_string_visible = visible

    def __show_aux_text_cb(self):
        qDebug("< ShowAuxiliaryText")
        if self.__aux_string_visible:
            return
        self.__aux_string_visible = True

    def __hide_aux_text_cb(self):
        qDebug("< HideAuxiliaryText")
        if not self.__aux_string_visible:
            return
        self.__aux_string_visible = False

    def __update_lookup_table_cb(self, lookup_table, visible):
        qDebug("< UpdateLookupTable")
        self.__lookup_table = lookup_table
        self.__lookup_table_visible = True

    def __show_lookup_table_cb(self):
        qDebug("< ShowLookupTable")
        if self.__lookup_table_visible:
            return
        self.__lookup_table_visible = True

    def __hide_lookup_table_cb(self):
        qDebug("< HideLookupTable")
        if not self.__lookup_table_visible:
            return
        self.__lookup_table_visible = False
