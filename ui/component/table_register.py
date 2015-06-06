from PyQt4 import QtGui
from PyQt4 import QtCore
from time import sleep
import sys
sys.path.append('C:\\Users\\You\\Documents\\GitHub\\AE86\\core\\pipe')
import main
import memory

def init_table_register(tb):
    global treg
    tb.resizeRowsToContents()
    tb.resizeColumnsToContents()
    tb.verticalHeader().setVisible(False)
    for i in range(8):
        item = QtGui.QTableWidgetItem(main.register_name[i])
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        tb.setItem(i, 0, item)
        item = QtGui.QTableWidgetItem('0x%08x' % memory.mem[memory.mem_alias[main.register_name[i]]])
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        tb.setItem(i, 1, item)
    tb.resizeRowsToContents()
    tb.resizeColumnsToContents()

def refresh_reg(tb, addr, value, color = True):
    value = '0x%08x' % value
    for i in range(8):
        if memory.mem_alias[main.register_name[i]] == addr:
            QtGui.QTableWidgetItem.setText(tb.item(i, 1), value)
            if color:
                tb.item(i, 1).setBackgroundColor(QtGui.QColor(0xFA, 0xD3, 0xD3))
                tb.repaint()
                sleep(0.2)
                tb.item(i, 1).setBackgroundColor(QtGui.QColor(0xFA, 0xFF, 0xFF))
                tb.repaint()