# -*- coding: cp936 -*-

import sys
sys.path.append('C:\\Users\\You\\Documents\\GitHub\\AE86\\core\\pipe')
from main import *
import memory
from PyQt4 import QtGui
from PyQt4 import QtCore

class WatchDialog(QtGui.QDialog):
    def __init__(self, parent = None):
        #   TODO font
        super(WatchDialog, self).__init__(parent)
        self.setWindowTitle(u'想要看内存')
        #   component
        self.text_addr = QtGui.QLineEdit()
        self.button_ok = QtGui.QPushButton(u'确认')
        self.text_addr.move(50, 50)
        self.button_ok.move(233, 233)
        #   layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.text_addr)
        layout.addWidget(self.button_ok)
        layout.setMargin(33)
        self.setLayout(layout)
        #   connect
        self.connect(self.button_ok, QtCore.SIGNAL('clicked()'), self.watch)
        #   run
        self.show()
        self.exec_()

    def watch(self):
        addr = str(QtGui.QLineEdit.text(self.text_addr))
        if addr[0:2] == '0x': addr = int(addr, 16)
        else: addr = int(addr)
        data = memory.read_data(addr, 4)
        self.close()
        addr = '0x' + ('%04x' % addr).upper()
        data = '0x' + ('%08x' % data).upper()
        QtGui.QMessageBox.information(self.parent(), "It works!", u"ADDR: %s,\tVALUE: %s" % (addr, data))


class AlterDialog(QtGui.QDialog):
    def __init__(self, parent = None):
        #   TODO font
        super(AlterDialog, self).__init__(parent)
        self.setWindowTitle(u'想要看内存')
        #   component
        self.text_addr = QtGui.QLineEdit()
        self.text_data = QtGui.QLineEdit()
        self.text_addr.setText(u'地址')
        self.text_data.setText(u'数值')
        self.button_ok = QtGui.QPushButton(u'确认')
        self.text_addr.move(50, 50)
        self.button_ok.move(233, 233)
        #   layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.text_addr)
        layout.addWidget(self.text_data)
        layout.addWidget(self.button_ok)
        layout.setMargin(33)
        self.setLayout(layout)
        #   connect
        self.connect(self.button_ok, QtCore.SIGNAL('clicked()'), self.alter)
        #   run
        self.show()
        self.exec_()

    def alter(self):
        addr = str(self.text_addr.text())
        data = str(self.text_data.text())
        if addr[0:2] == '0x': addr = int(addr, 16)
        else: addr = int(addr)
        if data[0:2] == '0x': data = int(data, 16)
        else: data = int(data)
        memory.write_data(addr, data, 4)
        data = memory.read_data(addr, 4)
        self.close()
        addr = '0x' + ('%04x' % addr).upper()
        data = '0x' + ('%08x' % data).upper()
        QtGui.QMessageBox.information(self.parent(), "It works!", u"ADDR: %s,\tVALUE: %s" % (addr, data))


def main():
    app = QtGui.QApplication(sys.argv)
    u = AlterDialog()
    sys.exit(app.exec_())


if __name__ == '__main__':
    memory.mem_init()
    main()