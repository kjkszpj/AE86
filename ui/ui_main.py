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
from component.progress import *
from component.MyThread import *
from component.table_stack_frame import *
from component.table_memory_watch import *

sys.path.append('C:\\Users\\You\\Documents\\GitHub\\AE86\\core\\pipe')
from main import *
from memory import *

class Widow(QtGui.QMainWindow):

    def __init__(self):
        init()
        super(Widow, self).__init__()
        self.cd_paint = []
        self.colorful = True
        self.color_interval = 0.2
        self.ui=Ui_total()
        self.ui.setupUi(self)
        init_stack_frame(self.ui.table_stack_frame)
        init_table_register(self.ui.table_register)

        self.show()
        self.run_thread = MyThread()

        self.sim = Simulator()
        self.sim.init()
        self.sim.load_data()
        self.run_thread.render(self.sim)
        sleep(0.01)
        self.reset()

        #   connect here
        self.connect(self.ui.action_load_file, QtCore.SIGNAL('triggered()'), self.run_load_instruction)
        self.connect(self.ui.action_save_progress, QtCore.SIGNAL('triggered()'), self.run_save_progress)
        self.connect(self.ui.action_load_progress, QtCore.SIGNAL('triggered()'), self.run_load_progress)
        self.connect(self.ui.action_about, QtCore.SIGNAL('triggered()'), self.run_about)

        self.connect(self.ui.action_run_direct, QtCore.SIGNAL('triggered()'), self.run_direct)
        self.connect(self.ui.action_1_IPS, QtCore.SIGNAL('triggered()'), self.run_1_IPS)
        self.connect(self.ui.action_2_IPS, QtCore.SIGNAL('triggered()'), self.run_2_IPS)
        self.connect(self.ui.action_4_IPS, QtCore.SIGNAL('triggered()'), self.run_4_IPS)
        self.connect(self.ui.action_8_IPS, QtCore.SIGNAL('triggered()'), self.run_8_IPS)

        self.connect(self.ui.button_continue, QtCore.SIGNAL('clicked()'), self.run_sim)
        self.connect(self.ui.button_pause, QtCore.SIGNAL('clicked()'), self.pause)
        self.connect(self.ui.button_stop, QtCore.SIGNAL('clicked()'), self.stop)
        self.connect(self.ui.button_step, QtCore.SIGNAL('clicked()'), self.run_step)
        self.connect(self.ui.button_reset, QtCore.SIGNAL('clicked()'), self.reset)

        self.connect(self.run_thread, QtCore.SIGNAL('next()'), self.thread_step)
        self.connect(self.run_thread, QtCore.SIGNAL('terminate()'), self.thread_terminate)

    def run_about(self):
        AboutDialog(parent = self)

    def run_load_instruction(self):
        load_instruction(self)

    def run_load_progress(self):
        load_progress(self)
        self.refresh_all()

    def run_save_progress(self):
        save_progress(self)

    def run_sim(self):
        self.ui.button_continue.setEnabled(False)
        self.ui.button_reset.setEnabled(False)
        self.ui.button_step.setEnabled(False)
        self.ui.button_pause.setEnabled(True)
        self.ui.button_stop.setEnabled(True)
        self.run_thread.sim.is_terminated = False
        self.run_thread.start()

    def run_direct(self):
        self.run_thread.interval = 0.01
        self.run_sim()

    def run_1_IPS(self):
        self.run_thread.interval = 1 / 1
        self.run_sim()
        # self.sleep_fun = ips1
        # self.pause_fun = pause_no
        # self.update_fun = self.notify
        # init()
        # load_data()
        # msg = sim_main(self.sleep_fun, self.pause_fun, self.update_fun, self.cd_fun)
        # QtGui.QMessageBox.information(self, u'程序终止了', msg)

    def run_2_IPS(self):
        self.run_thread.interval = 1.0 / 2
        self.run_sim()

    def run_4_IPS(self):
        self.run_thread.interval = 1.0 / 4
        self.run_sim()

    def run_8_IPS(self):
        self.run_thread.interval = 1.0 / 8
        self.run_sim()

    def notify(self, addr, value):
        cd_register = refresh_reg(self.ui.table_register, addr, value, self.colorful)
        cd_pipeline = refresh_pipe(self.ui, addr, value, self.colorful)
        cd_stack_frame = refresh_stack_frame(self.ui.table_stack_frame, addr, value, self.colorful)
        if cd_register != None:
            func, args = cd_register
            self.cd_paint.append((func, args))
        if cd_pipeline != None:
            func, args = cd_pipeline
            self.cd_paint.append((func, args))

    def cd_fun(self):
        time.sleep(self.color_interval)
        for func, args in self.cd_paint: func(args)
        self.cd_paint = []

    def run_step(self):
        self.color_interval = self.run_thread.interval / 1.618
        self.colorful = self.color_interval >= 0.2
        self.thread_step()
        self.ui.button_pause.setEnabled(True)
        self.ui.button_step.setEnabled(True)
        self.ui.button_stop.setEnabled(True)
        self.ui.button_reset.setEnabled(True)
        self.ui.button_continue.setEnabled(True)

    def pause(self):
        self.thread_terminate()
        self.ui.button_pause.setEnabled(False)
        self.ui.button_step.setEnabled(True)
        self.ui.button_stop.setEnabled(True)
        self.ui.button_reset.setEnabled(True)
        self.ui.button_continue.setEnabled(True)

    def stop(self):
        self.thread_terminate()
        self.run_thread.sim.load_data()
        self.ui.button_continue.setEnabled(False)
        self.ui.button_pause.setEnabled(False)
        self.ui.button_step.setEnabled(False)
        self.ui.button_stop.setEnabled(False)
        self.ui.button_reset.setEnabled(True)

    def reset(self):
        self.stop()
        self.refresh_all()
        self.ui.button_stop.setEnabled(False)
        self.ui.button_pause.setEnabled(False)
        self.ui.button_step.setEnabled(True)
        self.ui.button_reset.setEnabled(True)
        self.ui.button_continue.setEnabled(True)

    def thread_step(self):
        self.color_interval = self.run_thread.interval / 1.618
        self.colorful = self.color_interval >= 0.2
        if self.colorful:
            msg = self.run_thread.sim.step(self.notify, self.cd_fun)
        else:
            msg = self.run_thread.sim.step(self.notify)
        # msg = self.run_thread.sim.step()
        if msg != None:
            QtGui.QMessageBox.information(self, u'程序终止了', msg)
            self.stop()

    def thread_terminate(self):
        self.run_thread.sim.is_terminated = True
        self.run_thread.terminate()

    def refresh_all(self):
        #   可以改进一下
        mem_size = len(memory.mem)
        for i in range(mem_size): self.notify(i, memory.mem[i])
        self.cd_fun()

    #   TODO status bar

def main():
    app = QtGui.QApplication(sys.argv)
    u = Widow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
