#!/usr/bin/env python
# -'''- coding: utf-8 -'''-

import sys
from traceback import print_exc

# import python dbus module and GLib mainloop support
import dbus
import dbus.service
import dbus.mainloop.glib

from PySide2 import QtCore
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from testime.ibus_config import IBus_Address
from testime.keyconv import KeysymConv, ModConv

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


class DrawingArea(QWidget):
    def __init__(self, name, session):
        self.bus = session
        self.ibus = bus.get_object(IBUS_SERVICE, IBUS_PATH)
        ic_path = self.ibus.CreateInputContext(name, dbus_interface='org.freedesktop.IBus')
        self.ic = bus.get_object('org.freedesktop.IBus', ic_path)
        self.iface = dbus.Interface(self.ic, IBUS_INPUT_CONTEXT)

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

        self.__is_invalidate = False
        self.__preedit = None
        self.__preedit_visible = False
        self.__aux_string = None
        self.__aux_string_visible = False
        self.__lookup_table = None
        self.__lookup_table_visible = False

        QWidget.__init__(self)

        self.__text = ""
        self.setBackgroundRole(QPalette.Base);
        self.setAutoFillBackground(True)

    def updateTextRect(self):
        qDebug("SetCursorLocation")
        # TODO x, y, w, h
        self.iface.SetCursorLocation(0, 0, 5, 5)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        # TODO commit and preedit different color
        painter.setFont(QFont("Arial",18))
        painter.drawText(0, 30, self.__text)

    def keyPressEvent(self, event):
        keysym = KeysymConv(event.key())
        mod = ModConv(event.modifiers())
        # TODO keycode
        ret = self.iface.ProcessKeyEvent(keysym, event.nativeScanCode(), mod)
        qDebug("key press %s return %d" % (event.key(), ret))
        if not ret:
            self.__text += event.text()
        self.updateTextRect()

    def mousePressEvent(self, event):
        qDebug('mouse press')
        self.setFocus()

    def focusInEvent(self, event):
        self.iface.FocusIn()
        qDebug("focus in : Engine = %s" % self.iface.GetEngine()[2])
        self.updateTextRect()

    def focusOutEvent(self, event):
        qDebug('focus out event')
        self.iface.FocusOut()

    def __commit_text_cb(self, text):
        qDebug("__commit_text_cb : %s" % text[2])
        self.__text += text[2]

    def __update_preedit_text_cb(self, text, cursor_pos, visible):
        assert(text[0] == 'IBusText')
        qDebug("__update_preedit_text_cb text = %s cursor_pos = %d visible = %d" %
                (text[2], cursor_pos, visible))
        self.__preedit = text
        self.__preedit_visible = visible
        self.__invalidate()
        self.updateTextRect()

    def __show_preedit_text_cb(self):
        qDebug("__show_preedit_text_cb")
        if self.__preedit_visible:
            return
        self.__preedit_visible = True
        self.__invalidate()

    def __hide_preedit_text_cb(self):
        qDebug("__hide_preedit_text_cb")
        if not self.__preedit_visible:
            return
        self.__preedit_visible = False
        self.__invalidate()

    def __update_aux_text_cb(self, text, visible):
        qDebug("__update_aux_text_cb")
        self.__aux_string = text
        self.__aux_string_visible = visible
        self.__invalidate()

    def __show_aux_text_cb(self):
        qDebug("__show_aux_text_cb")
        if self.__aux_string_visible:
            return
        self.__aux_string_visible = True
        self.__invalidate()

    def __hide_aux_text_cb(self):
        qDebug("__hide_aux_text_cb")
        if not self.__aux_string_visible:
            return
        self.__aux_string_visible = False
        self.__invalidate()

    def __update_lookup_table_cb(self, lookup_table, visible):
        qDebug("__update_lookup_table_cb")
        self.__lookup_table = lookup_table
        self.__lookup_table_visible = True
        self.__invalidate()

    def __show_lookup_table_cb(self):
        qDebug("__show_lookup_table_cb")
        if self.__lookup_table_visible:
            return
        self.__lookup_table_visible = True
        self.__invalidate()

    def __hide_lookup_table_cb(self):
        qDebug("__hide_lookup_table_cb")
        if not self.__lookup_table_visible:
            return
        self.__lookup_table_visible = False
        self.__invalidate()

    def __invalidate(self):
        self.__is_invalidate = True

    def clear(self):
        self.__text = ""
        self.update()


# main function
if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle("TestIME")
    layout = QGridLayout()

    canvas = DrawingArea("TestIME", bus)
    canvas.setMinimumSize(QSize(400, 40))
    log = QListWidget()

    vlayout = QVBoxLayout()

    ime_combo = QComboBox()
    ime_combo.addItem("IBus")
    ime_combo.addItem("Fcitx")

    testset_combo = QComboBox()
    testset_combo.addItem("2bulsik")
    testset_combo.addItem("3bulsik")

    clear = QPushButton("Clear")

    quit = QPushButton("Quit")
    quit.clicked.connect(app.quit)

    vlayout.addWidget(QLabel("IME"))
    vlayout.addWidget(ime_combo)
    vlayout.addWidget(QLabel("Test Set"))
    vlayout.addWidget(testset_combo)
    vlayout.addStretch()
    vlayout.addWidget(clear)
    vlayout.addWidget(quit)

    layout.addWidget(canvas, 0 ,0)
    layout.addWidget(log, 1, 0)
    layout.addLayout(vlayout, 0, 1, 2 ,1)

    window.setLayout(layout)
    window.show()

    def clear_canvas_log():
        canvas.clear()
        log.clear()

    clear.clicked.connect(clear_canvas_log)

    def qt_message_handler(mode, context, message):
        item = QListWidgetItem(message)
        if message[0] == '_':
            item.setBackground(QColor('#ffff99'))
        log.addItem(item)
        log.scrollToBottom()
        if mode == QtCore.QtInfoMsg:
            mode = 'INFO'
        elif mode == QtCore.QtWarningMsg:
            mode = 'WARNING'
        elif mode == QtCore.QtCriticalMsg:
            mode = 'CRITICAL'
        elif mode == QtCore.QtFatalMsg:
            mode = 'FATAL'
        else:
            mode = 'DEBUG'
        print('%s: %s' % (mode, message))

    QtCore.qInstallMessageHandler(qt_message_handler)

    app.exec_()
