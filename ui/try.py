# -*- coding: cp936 -*-

import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from total import Ui_total


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
        dialog = QtGui.QDialog(parent = self)
        #   TODO font
        dialog.setWindowTitle('AE86')
        about_info = QtGui.QLabel(u'Brought to you by: 游沛杰\n'
                                  u'Email: 13307130325@fudan.edu.cn\n'
                                  u'View on Github:https://github.com/kjkszpj/AE86\n')
        button_ok = QtGui.QPushButton(u'确认')
        #   TODO connect button_ok
        #   TODO 设置确认键的大小
        #   构造layout
        about_info.move(50, 50)
        button_ok.move(233, 233)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(about_info)
        layout.addWidget(button_ok)
        layout.setMargin(33)
        #   显示框框
        dialog.setLayout(layout)
        dialog.exec_()


def main():
    app = QtGui.QApplication(sys.argv)
    ex = Widow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()