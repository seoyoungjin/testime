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

FCTIX_SERVICE         = "org.fcitx.Fcitx"
FCITX_IM_PATH         = "/inputmethod"
FCITX_IC_PATH         = "/inputcontext_%D"
FCITX_IM_INTERFACE    = "org.fcitx.Fctix.InputMethod"
FCITX_IC_INTERFACE    = "org.fcitx.Fctix.InputContext"


# LATER class Driver(dbus.service.Object):
class FcitxDriver(QtCore.QObject):

    commitText = QtCore.Signal(str)
    preeditChaned = QtCore.Signal(str)

    def __init__(self, name):
        super().__init__()
        self.bus = dbus.get_session_bus(private = True)
        try:
            # Get the remote object
            self.ibus = self.bus.get_object(FCITX_SERVICE, FCTIX_IM_PATH)
            # Get the remote interface for the remote object
            ic_path = self.ibus.CreateInputContext(name, dbus_interface=FCITX_IM_INTERFACE)
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

    # LATER
    def preedit(self):
        return self.__preedit;

    # LATER
    def preeditVisible(self):
        return self.__preedit_visible;

    def __commit_text_cb(self, text):
        qDebug("< CommitText : %s" % text[2])
        self.commitText.emit(text[2])

    def __update_preedit_text_cb(self, text, cursor_pos, visible):
        assert(text[0] == 'IBusText')
        qDebug("< UpdatePreeditText : text = %s cursor_pos = %d visible = %d" %
                (text[2], cursor_pos, visible))
        self.__preedit = text[2]
        self.__preedit_visible = visible

    def __show_preedit_text_cb(self):
        qDebug("< ShowPreeditText")
        if self.__preedit_visible:
            return
        self.__preedit_visible = True

    def __hide_preedit_text_cb(self):
        qDebug("< HidePreeditText")
        if not self.__preedit_visible:
            return
        self.__preedit_visible = False

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
