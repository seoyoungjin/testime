#!/usr/bin/env python
# -'''- coding: utf-8 -'''-
import sys
import dbus
import dbus.mainloop.glib

from PySide2 import QtCore
from PySide2.QtCore import Qt, QObject, QSize, QEventLoop, qDebug
from PySide2.QtGui import QPainter, QFont, QPalette, QColor, QKeySequence
from PySide2.QtWidgets import *

from testime.IBusDriver import IBusDriver
from testime.FcitxDriver import FcitxDriver
from testime.keyboard import KeycodeToKeysym

# Enable glib main loop support
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

MAX_LOG_COUNT = 1000
IMES = ["Fcitx", "IBus"]

class DrawingArea(QWidget):
    def __init__(self, name):
        QWidget.__init__(self)

        self.name = name
        self.driver = None

        self.__text = ""
        self.__textRect = QtCore.QRect()
        self.onActivateIME(IMES[0])
        self.setBackgroundRole(QPalette.Base)
        self.setAutoFillBackground(True)

    def onActivateIME(self, ime):
        assert(ime == "IBus" or ime == "Fcitx")
        if ime == "IBus" and not isinstance(self.driver, IBusDriver):
            del self.driver
            self.driver = IBusDriver(self.name)
        if ime == "Fcitx" and not isinstance(self.driver, FcitxDriver):
            del self.driver
            self.driver = FcitxDriver(self.name)
        self.driver.commitText.connect(self.onCommitText)
        self.driver.preeditChanged.connect(self.onPreeditChanged)

    def onCommitText(self, text):
        #qDebug("SLOT(commitText) : %s" % text)
        self.__text += text
        self.updateTextRect()

    def onPreeditChanged(self):
        #qDebug("SLOT(preeditChanged) : %s" % self.driver.preedit())
        self.updateTextRect()

    def updateTextRect(self):
        qDebug("SetCursorLocation")
        # x, y, w, h
        pos = self.mapToGlobal(self.pos())
        pos.setX(pos.x() + self.__textRect.width())
        pos.setY(pos.y() + self.__textRect.height())
        self.driver.SetCursorLocation(pos.x(), pos.y(), 5, 5)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setFont(QFont("Arial", 18))
        painter.drawText(0, 30, self.__text)
        self.__textRect = painter.boundingRect(self.rect(), self.__text)
        # draw preedit text with diffrent color
        if self.driver.preeditVisible():
            painter.setPen(Qt.red)
            painter.drawText(self.__textRect.width(), 30, self.driver.preedit())

    def keyPressEvent(self, event):
        mod = event.nativeModifiers()
        keycode = event.nativeScanCode()
        keysym = KeycodeToKeysym[keycode][mod & 0x03]
        if not keysym:
            keysym = KeycodeToKeysym[keycode][0]
            print("KeycodeToKeysym", event.key(), mod, QKeySequence(event.key()).toString())
        ret = self.driver.ProcessKeyEvent(keysym, keycode, mod)
        qDebug("keyPress : %d returns %d" % (keycode, ret))
        if not ret:
            QEventLoop().processEvents(QEventLoop.AllEvents, 1)
            if event.text().isprintable():
                self.__text += event.text()
            elif event.key() == Qt.Key_Backspace:
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
        qDebug("focusIn : Engine = %s" % self.driver.engine())

    def focusOutEvent(self, event):
        qDebug('focusOut')
        self.driver.iface.FocusOut()

    def clear(self):
        self.__text = ""
        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = QMainWindow()
    window.setGeometry(200, 200, 500, 500)
    window.setWindowTitle("TestIME")

    central = QWidget()
    layout = QGridLayout()

    canvas = DrawingArea("TestIME")
    canvas.setMinimumSize(QSize(400, 40))
    log = QListWidget()

    vlayout = QVBoxLayout()

    ime_combo = QComboBox()
    for ime in IMES:
        ime_combo.addItem(ime)

    def listTestSet():
        import os
        ts = [os.path.splitext(f)[0] for f in os.listdir('test') if f.endswith('.json')]
        return ts

    testset_combo = QComboBox()
    for testset in listTestSet():
        testset_combo.addItem(testset)

    clear = QPushButton("Clear")
    batch = QPushButton("Batch Test")
    quitb = QPushButton("Quit")
    quitb.clicked.connect(app.quit)

    vlayout.addWidget(QLabel("IME"))
    vlayout.addWidget(ime_combo)
    vlayout.addWidget(QLabel("Test Set"))
    vlayout.addWidget(testset_combo)
    vlayout.addWidget(batch)
    vlayout.addStretch()
    vlayout.addWidget(clear)
    vlayout.addWidget(quitb)

    layout.addWidget(canvas, 0, 0)
    layout.addWidget(log, 1, 0)
    layout.addLayout(vlayout, 0, 1, 2, 1)

    central.setLayout(layout)
    window.setCentralWidget(central)
    window.show()

    def clear_canvas_log():
        canvas.clear()
        log.clear()

    def run_batch_test():
        import unittest
        from test.batch_test import IBusTestCase, FcitxTestCase 

        suite = unittest.TestSuite()
        if ime_combo.currentText() == "Fcitx":
            testDriver = FcitxTestCase
        else:
            testDriver = IBusTestCase
        suite.addTest(testDriver('test_' + testset_combo.currentText()))
        unittest.TextTestRunner().run(suite)

    def activate_ime(ime: str):
        canvas.clear()
        log.clear()
        canvas.onActivateIME(ime)
        window.statusBar().showMessage(ime)

    clear.clicked.connect(clear_canvas_log)
    batch.clicked.connect(run_batch_test)
    ime_combo.activated[str].connect(activate_ime)

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

        # to prevent Qt warning
        if mode == QtCore.QtWarningMsg:
            return
        item = QListWidgetItem(message)
        if message[0] == '<':
            item.setText(message[2:])
            item.setBackground(QColor('#ffff99'))
        if MAX_LOG_COUNT < log.count():
            log.clear()
        log.addItem(item)
        log.scrollToBottom()

    QtCore.qInstallMessageHandler(qt_message_handler)
    app.exec_()
