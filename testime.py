#!/usr/bin/env python
# -'''- coding: utf-8 -'''-

import sys
from traceback import print_exc

# import python dbus module and GLib mainloop support
import dbus
import dbus.mainloop.glib

from PySide2 import QtCore
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from testime import IBusDriver
from testime import FcitxDriver
from testime.keyconv import KeysymConv, ModConv

# Enable glib main loop support
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)


class DrawingArea(QWidget):
    def __init__(self, name):
        QWidget.__init__(self)

        self.__text = ""
        #self.driver = IBusDriver.IBusDriver(name)
        self.driver = FcitxDriver.FcitxDriver(name)
        self.driver.commitText.connect(self.commitText)

        self.setBackgroundRole(QPalette.Base);
        self.setAutoFillBackground(True)

    def commitText(self, text):
        self.__text += text

    def updateTextRect(self):
        qDebug("SetCursorLocation")
        # TODO x, y, w, h
        self.driver.iface.SetCursorLocation(0, 0, 5, 5)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setFont(QFont("Arial",18))
        painter.drawText(0, 30, self.__text)
        # drw preedit text with diffrent color
        if self.driver.preeditVisible() and self.driver.preedit():
            rect = painter.boundingRect(self.rect(), self.__text)
            painter.setPen(Qt.red)
            painter.drawText(rect.width(), 30, self.driver.preedit())

    def keyPressEvent(self, event):
        keysym = KeysymConv(event.key())
        mod = ModConv(event.modifiers())
        ret = self.driver.iface.ProcessKeyEvent(keysym, event.nativeScanCode(), mod)
        qDebug("keyPress : %s (%d) returns %d" %
                (QKeySequence(event.key()).toString(), event.key(), ret))
        if not ret:
            if event.text().isprintable():
                self.__text += event.text()
            elif event.key() == Qt.Key_Backspace:
                # TODO ibus-hangul handles this
                if not self.driver.preedit():
                    self.__text = self.__text[:-1]
            elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                self.__text = ""
        self.updateTextRect()

    def mousePressEvent(self, event):
        qDebug('mousePress')
        self.setFocus()

    def focusInEvent(self, event):
        self.driver.iface.FocusIn()
        qDebug("focusIn : Engine = %s" % self.driver.iface.GetEngine()[2])

    def focusOutEvent(self, event):
        qDebug('focusOut')
        self.driver.iface.FocusOut()

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

    canvas = DrawingArea("TestIME")
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
        if mode == QtCore.QtInfoMsg:
            text = 'I'
        elif mode == QtCore.QtWarningMsg:
            text = 'W'
        elif mode == QtCore.QtCriticalMsg:
            text = 'C'
        elif mode == QtCore.QtFatalMsg:
            text = 'F'
        else:
            text = 'D'
        print('%s: %s' % (text, message))

        # to prevent Qt or pyside2 warning
        if mode == QtCore.QtWarningMsg:
            return
        item = QListWidgetItem(message)
        if message[0] == '<':
            item.setText(message[2:])
            item.setBackground(QColor('#ffff99'))
        log.addItem(item)
        log.scrollToBottom()

    QtCore.qInstallMessageHandler(qt_message_handler)
    app.exec_()
