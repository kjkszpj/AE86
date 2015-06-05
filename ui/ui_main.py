# -*- coding: cp936 -*-

import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from total import Ui_total
from component.AboutDialog import *
from component.load_instruction import *
from component.ips import *
from component.pause_fun import *

import sys
sys.path.append('C:\\Users\\You\\Documents\\GitHub\\AE86\\core\\pipe')
from main import *

class Widow(QtGui.QMainWindow):

    def __init__(self):
        super(Widow, self).__init__()
        self.ui=Ui_total()
        self.ui.setupUi(self)

        self.ui.table_register.setRowCount(8)
        self.ui.table_register.setRowHeight(5, 5)
        self.ui.table_register.resizeRowsToContents()
        self.ui.table_register.resizeColumnsToContents()
        treg = ['REAX', 'RECX', 'REDX', 'REBX', 'RESP', 'REBP', 'RESI', 'REDI']
        self.ui.table_register.verticalHeader().setVisible(False)
        for i in range(8):
            item = QtGui.QTableWidgetItem(treg[i])
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.ui.table_register.setItem(i, 0, item)
            item = QtGui.QTableWidgetItem('0x00000000')
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.table_register.setItem(i, 1, item)

        self.ui.table_register.resizeRowsToContents()
        self.ui.table_register.resizeColumnsToContents()

        self.show()
        #   connect here
        self.connect(self.ui.action_about, QtCore.SIGNAL('triggered()'), self.run_about)
        self.connect(self.ui.action_load_file, QtCore.SIGNAL('triggered()'), self.run_load_instruction)
        self.connect(self.ui.action_1_IPS, QtCore.SIGNAL('triggered()'), self.run_1_IPS)

    #   about
    def run_about(self):
        AboutDialog(parent = self)

    def run_load_instruction(self):
        load_instruction(self)

    def run_1_IPS(self):
        self.sleep_fun = ips8
        self.pause_fun = pause_no
        self.update_fun = self.update
        init()
        load_data()
        sim_main(self.sleep_fun, self.pause_fun, self.update_fun)

    def update(self, addr, value):
        if addr == 533:
            self.ui.test_reax.setText('%d' % value)
            self.ui.test_reax.repaint()


def main():
    app = QtGui.QApplication(sys.argv)
    u = Widow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
