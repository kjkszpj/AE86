# -*- coding: cp936 -*-

import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from total import Ui_total
from component.AboutDialog import *


class Widow(QtGui.QMainWindow):

    def __init__(self):
        super(Widow, self).__init__()
        self.ui=Ui_total()
        self.ui.setupUi(self)
        self.show()

        #   connect here
        self.connect(self.ui.action_about, QtCore.SIGNAL('triggered()'), self.run_about)

    #   about
    def run_about(self):
        AboutDialog(parent = self)


def main():
    app = QtGui.QApplication(sys.argv)
    u = Widow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
