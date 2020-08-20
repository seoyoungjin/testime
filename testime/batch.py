# vim:set et sts=4 sw=4:
#
# python -m testime.batch

import unittest

from PySide2.QtCore import QObject, qDebug, QEventLoop
from PySide2.QtWidgets import QApplication
from testime.FcitxDriver import FcitxDriver

class TestObject(QObject):
    def __init__(self, name):
        QObject.__init__(self)

        self.name = name
        self.text = ""
        #self.driver = IBusDriver(self.name)
        self.driver = FcitxDriver(self.name)
        self.driver.commitText.connect(self.onCommitText)
        self.driver.preeditChanged.connect(self.onPreeditChanged)
        self.driver.iface.FocusIn()

    def onCommitText(self, text):
        qDebug("SLOT(commitText) : %s" % text)
        self.text += text

    def onPreeditChanged(self):
        qDebug("SLOT(preeditChanged) : %s" % self.driver.preedit())
        #self.updateTextRect()

    def updateTextRect(self):
        qDebug("updateTestRect")
        # self.driver.iface.SetCursorLocation(0, 0, 5, 5)

    def keyPressEvent(self, keysym, keycode, mod):
        ret = self.driver.ProcessKeyEvent(keysym, keycode, mod)
        qDebug("keyPress : %d returns %d" % (keysym, ret))
        if not ret:
        	self.updateTextRect()


a = [
    ((45, 41), u"가"),
    ((45, 41, 39), u"간")
]
class BatchTestCase(unittest.TestCase):

    def setUp(self):
        self.obj = TestObject("Fcitx")

    def tearDown(self):
        del self.obj

    def test_batch(self):
		# control+space
        self.obj.keyPressEvent(32, 65, 4)
        self.obj.keyPressEvent(107, 45, 0)
        self.obj.keyPressEvent(102, 41, 0)
		# enter
        self.obj.keyPressEvent(65293, 36, 0)
        self.obj.driver.bus.flush()
        QEventLoop().processEvents(QEventLoop.AllEvents, 1)
        assert(self.obj.text == u"가")


if __name__ == '__main__':
    import sys
    import dbus

    # Enable glib main loop support
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    app = QApplication(sys.argv)

    #runner = unittest.TextTestRunner()
    #runner.run(BatchTestCase())
    unittest.main()
