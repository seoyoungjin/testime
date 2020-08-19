#!/usr/bin/env python
# -'''- coding: utf-8 -'''-

import sys
from traceback import print_exc

import dbus
import dbus.service
import dbus.mainloop.glib

from PySide2 import QtCore
from PySide2.QtCore import qDebug, QRect

from testime.ibus_config import IBus_Address

CAPACITY_NONE = 0
CAPACITY_CLIENT_SIDE_UI = (1 << 0)
CAPACITY_PREEDIT = (1 << 1)
CAPACITY_CLIENT_SIDE_CONTROL_STATE =  (1 << 2)
CAPACITY_PASSWORD = (1 << 3)
CAPACITY_FORMATTED_PREEDIT = (1 << 4)
CAPACITY_CLIENT_UNFOCUS_COMMIT = (1 << 5)
CAPACITY_SURROUNDING_TEXT = (1 << 6)
CAPACITY_EMAIL = (1 << 7)
CAPACITY_DIGIT = (1 << 8)
CAPACITY_UPPERCASE = (1 << 9)
CAPACITY_LOWERCASE = (1 << 10)
CAPACITY_NOAUTOUPPERCASE = (1 << 11)
CAPACITY_URL = (1 << 12)
CAPACITY_DIALABLE = (1 << 13)
CAPACITY_NUMBER = (1 << 14)
CAPACITY_NO_ON_SCREEN_KEYBOARD = (1 << 15)
CAPACITY_SPELLCHECK = (1 << 16)
CAPACITY_NO_SPELLCHECK = (1 << 17)
CAPACITY_WORD_COMPLETION = (1 << 18)
CAPACITY_UPPERCASE_WORDS = (1 << 19)
CAPACITY_UPPERCASE_SENTENCES = (1 << 20)
CAPACITY_ALPHA = (1 << 21)
CAPACITY_NAME = (1 << 22)
CAPACITY_GET_IM_INFO_ON_FOCUS = (1 << 23)
CAPACITY_RELATIVE_CURSOR_RECT = (1 << 24)

FCITX_SERVICE         = "org.fcitx.Fcitx"
FCITX_IM_PATH         = "/inputmethod"
FCITX_IC_PATH         = "/inputcontext_%d"
FCITX_IM_INTERFACE    = "org.fcitx.Fcitx.InputMethod"
FCITX_IC_INTERFACE    = "org.fcitx.Fcitx.InputContext"


# LATER class Driver(dbus.service.Object):
class FcitxDriver(QtCore.QObject):

    commitText = QtCore.Signal(str)
    preeditChanged = QtCore.Signal()

    def __init__(self, name):
        super().__init__()
        self.bus = dbus.SessionBus(private = True)
        try:
            self.fcitx = self.bus.get_object(FCITX_SERVICE, FCITX_IM_PATH)
            ret = self.fcitx.CreateICv2(name, dbus_interface=FCITX_IM_INTERFACE)
            # print("ret =", ret)
            self.ic = self.bus.get_object(FCITX_SERVICE, FCITX_IC_PATH % ret[0])
            self.iface = dbus.Interface(self.ic, dbus_interface=FCITX_IC_INTERFACE)
        except dbus.DBusException:
            print_exc()
            sys.exit(1)

        #self.iface.SetCapacity(255)
        self.iface.SetCapacity(CAPACITY_PREEDIT)

        self.iface.connect_to_signal("EnableIM", self.__enable_im_cb)
        self.iface.connect_to_signal("CloseIM", self.__close_im_cb)
        self.iface.connect_to_signal("CurrentIM", self.__current_im_cb)

        self.iface.connect_to_signal("CommitString", self.__commit_text_cb)

        self.iface.connect_to_signal("UpdatePreedit", self.__update_preedit_cb)
        self.iface.connect_to_signal("DeleteSurroundingText", self.__delete_surrounding_text_cb)
        self.iface.connect_to_signal("UpdateFormattedPreedit", self.__update_formatted_preedit_cb)
        self.iface.connect_to_signal("UpdateClientSideUI", self.__update_client_side_ui_cb)

        self.iface.connect_to_signal("ForwardKey", self.__forward_key_cb)
        # LATER AddHintCallback

        self.__rect = QRect(-1, -1, 0, 0)
        self.__preedit = None
        self.__aux_string = None
        self.__aux_string_visible = False
        self.__lookup_table = None
        self.__lookup_table_visible = False

    def __del__(self):
        self.Quit()

    def preedit(self):
        return self.__preedit

    def preeditVisible(self):
        return not self.__preedit or len(self.__preedit)

    def engine(self):
        return self.fcitx.GetCurrentIM()

    def Reset(self):
        self.iface.Reset()
        self.iface.CloseIC()

    def Quit(self):
        self.iface.DestroyIC()

    def ProcessKeyEvent(self, keysym, keycode, mod):
        # event = UP or DOWN
        # event_time = 0
        return self.iface.ProcessKeyEvent(keysym, keycode, mod, 0, 0)

    def __enable_im_cb(self):
        qDebug("< EnableIM")

    def __close_im_cb(self):
        qDebug("< CloseIM")

    def __current_im_cb(self, name, uniqueName, langCode):
        qDebug("< CurrentIM : %s %s %s" % (name, uniqueName, langCode))

    def __commit_text_cb(self, text):
        qDebug("< CommitText : %s" % text)
        self.commitText.emit(text)

    def __update_preedit_cb(self, text, cursor_pos):
        qDebug("< UpdatePreeditText : text = %s, cursor_pos = %d" % (text, cursor_pos))
        self.__preedit = text
        self.preeditChanged.emit()

    def __delete_surrounding_text_cb(self, offset, nchar):
        qDebug("< DeleteSurroundingText : %d %d" % (offset, nchar))

    def __update_formatted_preedit_cb(self, text, cursorpos):
        print(text)
        qDebug("< UpdateFormattedPreedit : %s" % cursorpos)

    def __update_client_side_ui_cb(self, auxup, auxdown, preedit, candidateword, imname, cursorpos):
        print("auxup =", auxup)
        print("auxdown =", auxdown)
        print("preedit =", preedit)
        print("candidateword =", candidateword)
        print("imname =", imname)
        qDebug("< UpdateClientSideUI : %s" % imname)

    def __forward_key_cb(self, keyval, state, type_):
        qDebug("< ForwardKey: %d %d %d" % (keyval, state, type_))
