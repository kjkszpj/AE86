# -*- coding: cp936 -*-

import sys
import time
import thread
from PyQt4 import QtGui
from PyQt4 import QtCore
from total import Ui_total
from component.AboutDialog import *
from component.load_instruction import *
from component.ips import *
from component.pause_fun import *
from component.table_register import *
from component.table_pipe import *

sys.path.append('C:\\Users\\You\\Documents\\GitHub\\AE86\\core\\pipe')
from main import *
from memory import *

class Widow(QtGui.QMainWindow):

    def __init__(self):
        init()
        super(Widow, self).__init__()
        self.cd_paint = []
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
        self.update_fun = self.notify
        init()
        load_data()
        msg = sim_main(self.sleep_fun, self.pause_fun, self.update_fun, self.cd_fun)
        QtGui.QMessageBox.information(self, u'程序终止了', msg)

    def run_2_IPS(self):
        self.sleep_fun = ips2
        self.pause_fun = pause_no
        self.update_fun = self.notify
        init()
        load_data()
        msg = sim_main(self.sleep_fun, self.pause_fun, self.update_fun, self.cd_fun)
        QtGui.QMessageBox.information(self, u'程序终止了', msg)

    def run_4_IPS(self):
        self.sleep_fun = ips4
        self.pause_fun = pause_no
        self.update_fun = self.notify
        init()
        load_data()
        msg = sim_main(self.sleep_fun, self.pause_fun, self.update_fun, self.cd_fun)
        QtGui.QMessageBox.information(self, u'程序终止了', msg)

    def run_8_IPS(self):
        self.sleep_fun = ips8
        self.pause_fun = pause_no
        self.update_fun = self.notify
        init()
        load_data()
        msg = sim_main(self.sleep_fun, self.pause_fun, self.update_fun, self.cd_fun)
        QtGui.QMessageBox.information(self, u'程序终止了', msg)

    def notify(self, addr, value):
        cd_register = refresh_reg(self.ui.table_register, addr, value)
        cd_pipeline = refresh_pipe(self.ui, addr, value)
        if cd_register != None:
            func, args = cd_register
            self.cd_paint.append((func, args))
        if cd_pipeline != None:
            func, args = cd_pipeline
            self.cd_paint.append((func, args))

    def cd_fun(self):
        time.sleep(2)
        for func, args in self.cd_paint:
            func(args)
        self.cd_paint = []

def main():
    app = QtGui.QApplication(sys.argv)
    u = Widow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
