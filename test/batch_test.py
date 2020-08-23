# vim:set et sts=4 sw=4:
#
# python -m testime.batch

import unittest
import json

from PySide2.QtCore import QObject, qDebug, QEventLoop
from PySide2.QtWidgets import QApplication

from testime.IBusDriver import IBusDriver
from testime.FcitxDriver import FcitxDriver
from testime.keyboard import KeycodeToKeysym
from testime.keyboard import KeynameToKeysym, KeynameToKeycode
from testime.parse_hotkey import parse_hotkey
from test.hangul_compose import get_2bulsik_test, get_3bulsik_test

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
        pass

    def keyPressEvent(self, key):
        # parse_hotkey() also works for simple keystroke
        # check '-' for speed
        # LATER - check speed for large number test case
        if key != '-' and '-' in key:
            ks = parse_hotkey(key)
            keycode = ks.keycode
            modifier = ks.modifier
            keysym = KeycodeToKeysym[ks.keycode]
        else:
            keysym = KeynameToKeysym[key]
            keycode = KeynameToKeycode[key]
            modifier = 0
        ret = self.driver.ProcessKeyEvent(keysym, keycode, modifier)
        qDebug("keyPress : %s(%d) returns %d" % (keycode, keysym, ret))

    def clear(self):
        self.preedit = True
        self.text = ""


class FcitxTestCase(unittest.TestCase):
    def setUp(self):
        self.obj = TestObject("Fcitx")
        # IME key Contaol-space
        self.obj.keyPressEvent('C-space')

    def tearDown(self):
        del self.obj

    def test_sample(self):
        self.obj.clear()
        self.obj.keyPressEvent('k')
        self.obj.keyPressEvent('f')
        self.obj.keyPressEvent('s')
        self.obj.keyPressEvent('Return')

        while self.obj.preedit:
            QEventLoop().processEvents(QEventLoop.AllEvents, 1)
        self.assertEqual(self.obj.text, u"간")

    def __real_test(self, cases):
        for code in cases:
            self.obj.clear()
            key_sequence = cases[code]
            qDebug("KeySequence : %s" % key_sequence)
            for key in key_sequence:
                self.obj.keyPressEvent(key)
            self.obj.keyPressEvent('Return')

            while self.obj.preedit:
                QEventLoop().processEvents(QEventLoop.AllEvents, 1)
            self.assertEqual(self.obj.text, code)

    def test_2bulsik(self):
        with open('test/2bulsik.json', 'r') as handle:
            cases = json.load(handle)
        self.__real_test(cases)

    def test_3bulsik(self):
        with open('test/3bulsik.json', 'r') as handle:
            cases = json.load(handle)
        self.__real_test(cases)

    def test_all_2bulsik(self):
        cases = get_2bulsik_test()
        self.__real_test(cases)

    def test_all_3bulsik(self):
        cases = get_3bulsik_test()
        self.__real_test(cases)

class IBusTestCase(unittest.TestCase):

    def setUp(self):
        self.obj = TestObject("IBus")
        # IME key Contaol-space
        self.obj.keyPressEvent('Shift-space')

    def tearDown(self):
        del self.obj

    def __real_test(self, cases):
        for code in cases:
            self.obj.clear()
            key_sequence = cases[code]
            qDebug("KeySequence : %s" % key_sequence)
            for key in key_sequence:
                self.obj.keyPressEvent(key)
            self.obj.keyPressEvent('Return')

            while self.obj.preedit:
                QEventLoop().processEvents(QEventLoop.AllEvents, 1)
            self.assertEqual(self.obj.text, code)

    def test_2bulsik(self):
        with open('test/2bulsik.json', 'r') as handle:
            cases = json.load(handle)
        self.__real_test(cases)

    def test_3bulsik(self):
        with open('test/3bulsik.json', 'r') as handle:
            cases = json.load(handle)
        self.__real_test(cases)

    def test_all_2bulsik(self):
        cases = get_2bulsik_test()
        self.__real_test(cases)

    def test_all_3bulsik(self):
        cases = get_3bulsik_test()
        self.__real_test(cases)

if __name__ == '__main__':
    import sys
    import dbus

    # Enable glib main loop support
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    app = QApplication(sys.argv)

    suite = unittest.TestSuite()
    #suite.addTest(IBusTestCase('test_all_2bulsik'))
    #suite.addTest(IBusTestCase('test_all_3bulsik'))
    suite.addTest(FcitxTestCase('test_all_2bulsik'))
    #suite.addTest(FcitxTestCase('test_all_3bulsik'))
    runner = unittest.TextTestRunner()
    runner.run(suite)

    #unittest.main()
