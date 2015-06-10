# -*- coding: cp936 -*-

from PyQt4 import QtGui
from PyQt4 import QtCore


class AboutDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        #   TODO font
        super(AboutDialog, self).__init__(parent)
        self.setWindowTitle('AE86')
        #   component
        self.about_info = QtGui.QLabel(u'Brought to you by: 游沛杰\n'
                                       u'Email: 13307130325@fudan.edu.cn\n'
                                       u'View on Github:https://github.com/kjkszpj/AE86\n')
        self.button_ok = QtGui.QPushButton(u'确认')
        self.about_info.move(50, 50)
        self.button_ok.move(233, 233)
        #   layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.about_info)
        layout.addWidget(self.button_ok)
        layout.setMargin(33)
        self.setLayout(layout)
        #   connect
        self.connect(self.button_ok, QtCore.SIGNAL('clicked()'), QtCore.SLOT('close()'))
        #   run
        self.show()
        self.exec_()


def main():
    import sys
    app = QtGui.QApplication(sys.argv)
    AboutDialog()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
