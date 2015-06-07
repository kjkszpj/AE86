from PyQt4 import QtGui
from PyQt4 import QtCore
from time import sleep
import sys
sys.path.append('C:\\Users\\You\\Documents\\GitHub\\AE86\\core\\pipe')
import memory

def init_stack_frame(tb):
    tb.resizeRowsToContents()
    tb.resizeColumnsToContents()
    QtGui.QTableWidget.setRowCount(tb, 0)

def refresh_stack_frame(tb, addr, value, color = True):
    if addr in [memory.mem_alias['RESP'], memory.mem_alias['REBP']]:
        QtGui.QTableWidget.setRowCount(tb, 0)
        vesp = memory.read_reg('RESP')
        vebp = memory.read_reg('REBP')
        if vebp == 0:
            return False
        else:
            vebp = max(memory.read_data(vebp, 4), vebp)
            for i in range(vesp, vebp + 1, 4):
                cnt = QtGui.QTableWidget.rowCount(tb)
                QtGui.QTableWidget.setRowCount(tb, cnt + 1)

                addr = ('%04x' % i).upper()
                item = QtGui.QTableWidgetItem('0x' + addr)
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                QtGui.QTableWidget.setItem(tb, cnt, 0, item)

                addr = ('%08x' % memory.read_data(i)).upper()
                item = QtGui.QTableWidgetItem('0x' + addr)
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                QtGui.QTableWidget.setItem(tb, cnt, 1, item)
            # raw_input()