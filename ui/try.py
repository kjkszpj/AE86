import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from total import Ui_total

class widow(QtGui.QMainWindow):

    def __init__(self):
        super(widow, self).__init__()
        self.ui=Ui_total()
        self.ui.setupUi(self)
        self.show()
        self.connect(self.ui.action_dec2hex, QtCore.SIGNAL('triggered()'), tryevent)

def tryevent():
    print 'gogogo'

def main():
    app = QtGui.QApplication(sys.argv)
    ex = widow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()