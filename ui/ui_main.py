# -*- coding: cp936 -*-

import os
import sys
sys.path.append(os.path.abspath(sys.argv[0])[0:-13] + 'core\\pipe')
import time
import thread
from PyQt4 import QtGui
from PyQt4 import QtCore
from total import Ui_total
from component.AboutDialog import *
from component.load_instruction import *
from component.pause_fun import *
from component.table_register import *
from component.table_pipe import *
from component.progress import *
from component.MyThread import *
from component.table_stack_frame import *
from component.table_memory_watch import *
from component.table_code import *
from component.table_status import *
from component.output import *
from component.table_memory_watch import *

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
        init_status(self.ui.statusBar)

        self.show()
        self.run_thread = MyThread()

        self.inst_file = 'C:\\Users\\You\\Documents\\GitHub\\AE86\\data\\y86_code\\asum.yo'
        self.sim = Simulator()
        self.sim.init()
        self.sim.load_data()
        self.code = init_code(self.ui.text_code, self.inst_file)
        self.run_thread.render(self.sim)
        sleep(0.01)
        self.reset()

        #   connect here
        self.connect(self.ui.action_load_file, QtCore.SIGNAL('triggered()'), self.run_load_instruction)
        self.connect(self.ui.action_output, QtCore.SIGNAL('triggered()'), self.run_output)
        self.connect(self.ui.action_save_progress, QtCore.SIGNAL('triggered()'), self.run_save_progress)
        self.connect(self.ui.action_load_progress, QtCore.SIGNAL('triggered()'), self.run_load_progress)
        self.connect(self.ui.action_about, QtCore.SIGNAL('triggered()'), self.run_about)

        self.connect(self.ui.action_run_direct, QtCore.SIGNAL('triggered()'), self.run_direct)
        self.connect(self.ui.action_1_IPS, QtCore.SIGNAL('triggered()'), self.run_1_IPS)
        self.connect(self.ui.action_2_IPS, QtCore.SIGNAL('triggered()'), self.run_2_IPS)
        self.connect(self.ui.action_4_IPS, QtCore.SIGNAL('triggered()'), self.run_4_IPS)
        self.connect(self.ui.action_8_IPS, QtCore.SIGNAL('triggered()'), self.run_8_IPS)
        self.connect(self.ui.action_stop, QtCore.SIGNAL('triggered()'), self.stop)
        self.connect(self.ui.action_pause, QtCore.SIGNAL('triggered()'), self.pause)
        self.connect(self.ui.action_step, QtCore.SIGNAL('triggered()'), self.thread_step)

        self.connect(self.ui.action_read_memory, QtCore.SIGNAL('triggered()'), self.run_watch_memory)
        self.connect(self.ui.action_write_memory, QtCore.SIGNAL('triggered()'), self.run_alter_memory)

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

    def run_output(self):
        output(self)

    def run_load_progress(self):
        load_progress(self)
        self.refresh_all()

    def run_save_progress(self):
        save_progress(self)

    def run_watch_memory(self):
        WatchDialog(self)

    def run_alter_memory(self):
        AlterDialog(self)

    def run_sim(self):
        self.ui.button_continue.setEnabled(False)
        self.ui.button_reset.setEnabled(False)
        self.ui.button_step.setEnabled(False)
        self.ui.button_pause.setEnabled(True)
        self.ui.button_stop.setEnabled(True)
        self.run_thread.sim.is_terminated = False
        self.run_thread.start()

    def run_direct(self):
        self.run_thread.interval = 0.02
        self.run_sim()

    def run_1_IPS(self):
        self.run_thread.interval = 1 / 1
        self.run_sim()

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
        cd_code = refresh_code(self.ui.text_code, self.code, addr, value)
        cd_status = refresh_status(self.ui.statusBar, addr, value, self.run_thread.sim)
        if cd_register != None:
            func, args = cd_register
            self.cd_paint.append((func, args))
        if cd_pipeline != None:
            func, args = cd_pipeline
            self.cd_paint.append((func, args))
        if cd_stack_frame != None:
            func, args = cd_stack_frame
            self.cd_paint.append((func, args))
        if cd_code != None:
            func, args = cd_code
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
        self.code = init_code(self.ui.text_code, self.inst_file)
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
