# vim:set et sts=4 sw=4:
#
# python -m testime.batch

import unittest

from PySide2.QtCore import QObject, qDebug, QEventLoop
from PySide2.QtWidgets import QApplication
from testime.FcitxDriver import FcitxDriver
from testime.keyboard import KeynameToKeysym, KeynameToKeycode

class TestObject(QObject):
    def __init__(self, name):
        QObject.__init__(self)

        if name == 'Fcitx':
            self.driver = FcitxDriver(name)
        else:
            self.driver = IBusDriver(name)
        self.text = ""
        self.preedit = True
        self.driver.commitText.connect(self.onCommitText)
        self.driver.preeditChanged.connect(self.onPreeditChanged)
        self.driver.iface.FocusIn()

    def __del__(self):
        del self.driver

    def onCommitText(self, text):
        qDebug("SLOT(commitText) : %s" % text)
        self.text += text
        self.preedit = False

    def onPreeditChanged(self):
        #qDebug("SLOT(preeditChanged) : %s" % self.driver.preedit())
        #self.updateTextRect()
        pass

    def keyPressEvent(self, key, mod):
        keysym = KeynameToKeysym[key]
        keycode = KeynameToKeycode[key]
        ret = self.driver.ProcessKeyEvent(keysym, keycode, mod)
        qDebug("keyPress : %s(%d) returns %d" % (key, keysym, ret))

    def clear(self):
        self.preedit = True
        self.text = ""


class BatchTestCase(unittest.TestCase):

    def setUp(self):
        self.obj = TestObject("Fcitx")

    def tearDown(self):
        del self.obj

    def test_batch(self):
		# control+space
        self.obj.keyPressEvent('space', 4)

        self.obj.keyPressEvent('k', 0)
        self.obj.keyPressEvent('f', 0)
        self.obj.keyPressEvent('Return', 0)

        self.obj.driver.bus.flush()
        while self.obj.preedit:
            QEventLoop().processEvents(QEventLoop.AllEvents, 1)
        self.assertEqual(self.obj.text, u"가")

        self.obj.clear()
        self.obj.keyPressEvent('k', 0)
        self.obj.keyPressEvent('f', 0)
        self.obj.keyPressEvent('s', 0)
        self.obj.keyPressEvent('Return', 0)

        while self.obj.preedit:
            QEventLoop().processEvents(QEventLoop.AllEvents, 1)
        self.assertEqual(self.obj.text, u"간")


if __name__ == '__main__':
    import sys
    import dbus

    # Enable glib main loop support
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    app = QApplication(sys.argv)

    suite = unittest.TestSuite()
    suite.addTest(unittest.defaultTestLoader.loadTestsFromName('testime.batch_test'))
    unittest.TextTestRunner().run(suite)
    #unittest.main()
