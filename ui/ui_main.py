# -*- coding: cp936 -*-

import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from total import Ui_total
from component.AboutDialog import *
from component.load_instruction import *
from component.ips import *
from component.pause_fun import *
from component.table_register import *

import sys
sys.path.append('C:\\Users\\You\\Documents\\GitHub\\AE86\\core\\pipe')
from main import *
from memory import *

class Widow(QtGui.QMainWindow):

    def __init__(self):
        init()
        super(Widow, self).__init__()
        self.ui=Ui_total()
        self.ui.setupUi(self)
        init_table_register(self.ui.table_register)
        self.show()
        #   connect here
        self.connect(self.ui.action_about, QtCore.SIGNAL('triggered()'), self.run_about)
        self.connect(self.ui.action_load_file, QtCore.SIGNAL('triggered()'), self.run_load_instruction)
        self.connect(self.ui.action_1_IPS, QtCore.SIGNAL('triggered()'), self.run_1_IPS)
        self.connect(self.ui.action_2_IPS, QtCore.SIGNAL('triggered()'), self.run_2_IPS)
        self.connect(self.ui.action_4_IPS, QtCore.SIGNAL('triggered()'), self.run_4_IPS)
        self.connect(self.ui.action_8_IPS, QtCore.SIGNAL('triggered()'), self.run_8_IPS)

    #   about
    def run_about(self):
        AboutDialog(parent = self)

    def run_load_instruction(self):
        load_instruction(self)

    def run_1_IPS(self):
        self.sleep_fun = ips1
        self.pause_fun = pause_no
        self.update_fun = self.update
        init()
        load_data()
        sim_main(self.sleep_fun, self.pause_fun, self.update_fun)

    def run_2_IPS(self):
        self.sleep_fun = ips2
        self.pause_fun = pause_no
        self.update_fun = self.update
        init()
        load_data()
        sim_main(self.sleep_fun, self.pause_fun, self.update_fun)

    def run_4_IPS(self):
        self.sleep_fun = ips4
        self.pause_fun = pause_no
        self.update_fun = self.update
        init()
        load_data()
        sim_main(self.sleep_fun, self.pause_fun, self.update_fun)

    def run_8_IPS(self):
        self.sleep_fun = ips8
        self.pause_fun = pause_no
        self.update_fun = self.update
        init()
        load_data()
        sim_main(self.sleep_fun, self.pause_fun, self.update_fun)

    def update(self, addr, value):
        refresh_reg(self.ui.table_register, addr, value)


def main():
    app = QtGui.QApplication(sys.argv)
    u = Widow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
