# vim:set et sts=4 sw=4:

from abc import abstractmethod, ABC, ABCMeta
from PySide2 import QtCore

QObjectType = type(QtCore.QObject)

class QABCMeta(QObjectType, ABCMeta):
    pass

# LATER class Driver(dbus.service.Object):
class DBusDriver(QtCore.QObject, metaclass=QABCMeta):

    @abstractmethod
    def engine(self):
        pass

    @abstractmethod
    def preedit(self):
        pass

    @abstractmethod
    def preeditVisible(self):
        pass

    @abstractmethod
    def Reset(self):
        pass

    @abstractmethod
    def Quit(self):
        pass

if __name__ == "__main__":
    class A(DBusDriver):
        pass

    a = A()
