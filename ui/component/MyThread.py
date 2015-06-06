from time import sleep
from PyQt4 import QtCore

class MyThread(QtCore.QThread):
    def __init__(self, parent = None):
        QtCore.QThread.__init__(self, parent)
        self.exiting = False
        self.sim = None
        self.interval = 0.1

    def __del__(self):
        self.exiting = True
        self.wait()

    def render(self, sim, interval = 0.1):
        self.sim = sim
        self.interval = interval
        self.start()

    def run(self):
        while self.sim.is_terminated == False:
            self.emit(QtCore.SIGNAL('next()'))
            sleep(self.interval)
        self.emit(QtCore.SIGNAL('terminate()'))

    def setslide(run_thread, interval = 0.1):
        run_thread.interval = interval
