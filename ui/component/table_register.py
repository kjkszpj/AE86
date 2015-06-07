from PyQt4 import QtGui
from PyQt4 import QtCore
from time import sleep
import sys
sys.path.append('C:\\Users\\You\\Documents\\GitHub\\AE86\\core\\pipe')
import main
import memory


def init_table_register(tb):
    tb.resizeRowsToContents()
    tb.resizeColumnsToContents()
    for i in range(8):
        item = QtGui.QTableWidgetItem(main.register_name[i])
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        tb.setItem(i, 0, item)
        value = '%08x' % memory.mem[memory.mem_alias[main.register_name[i]]]
        value = '0x' + value.upper()
        item = QtGui.QTableWidgetItem(value)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        tb.setItem(i, 1, item)
    tb.resizeRowsToContents()
    tb.resizeColumnsToContents()


def refresh_reg(tb, addr, value, color = True):
    value = '%08x' % value
    value = '0x' + value.upper()
    for i in range(8):
        if memory.mem_alias[main.register_name[i]] == addr:
            QtGui.QTableWidgetItem.setText(tb.item(i, 1), value)
            if color:
                tb.item(i, 1).setBackgroundColor(QtGui.QColor(0xFA, 0xD3, 0xD3))
                tb.repaint()
                return (cool_down_reg, (tb, i, 1))
    return None


def cool_down_reg(args):
    args[0].item(args[1], args[2]).setBackgroundColor(QtGui.QColor(0xFA, 0xFF, 0xFF))
    args[0].repaint()