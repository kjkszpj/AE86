from PyQt4 import QtGui
from PyQt4 import QtCore
import sys
sys.path.append('C:\\Users\\You\\Documents\\GitHub\\AE86\\core\\pipe')
import memory


def init_stack_frame(tb):
    global vesp, vebp

    vesp = 4
    vebp = 0
    tb.resizeRowsToContents()
    tb.resizeColumnsToContents()
    tb.setRowCount(0)


def refresh_stack_frame(tb, addr, value, color = True):
    global vesp, vebp

    if addr in [memory.mem_alias['RESP'], memory.mem_alias['REBP']]:
        new_vesp = memory.read_reg('RESP') - 4
        t_vebp = memory.read_reg('REBP')
        new_vebp = t_vebp
        if value == 0:
            vesp = 4
            vebp = 0
            tb.setRowCount(0)
        if new_vebp > 0:
            new_vebp = max(memory.read_data(new_vebp, 4), new_vebp)
            cnt = 0
            for i in range(vesp, vebp + 1, 4):
                if i not in range(new_vesp, new_vebp + 1):
                    tb.removeRow(cnt)
                else:
                    s = '0x' + ('%04x' % i).upper()
                    if i == t_vebp: s = '>' + s
                    if i == new_vesp + 4: s = '<' + s
                    item = QtGui.QTableWidgetItem(s)
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    item.setTextAlignment(QtCore.Qt.AlignRight)
                    tb.setItem(cnt, 0, item)
                    cnt += 1
            for i in range(new_vesp, new_vebp + 1, 4):
                if i in range(vesp, vebp + 1): continue
                tb.insertRow((i - new_vesp) / 4)
                s = '0x' + ('%04x' % i).upper()
                if i == t_vebp: s = '>' + s
                if i == new_vesp + 4: s = '<' + s
                item = QtGui.QTableWidgetItem(s)
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                item.setTextAlignment(QtCore.Qt.AlignRight)
                tb.setItem((i - new_vesp) / 4, 0, item)

                s = '0x' + ('%08x' % memory.read_data(i, 4)).upper()
                item = QtGui.QTableWidgetItem(s)
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                tb.setItem((i - new_vesp) / 4, 1, item)
            # raw_input()
            vesp = new_vesp
            vebp = new_vebp
            tb.repaint()
    if addr in range(vesp, vebp + 1, 4):
        i = ((addr - vesp) >> 2) + 1
        s = ('%08x' % value).upper()
        item = QtGui.QTableWidgetItem('0x' + s)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        if color:
            item.setBackgroundColor(QtGui.QColor(0xFF, 0xAA, 0x77))
        tb.setItem(i, 1, item)
        tb.repaint()
        return cool_down_stack_frame, (tb, i, 1)
    return None


def cool_down_stack_frame(args):
    item = args[0].item(args[1], args[2])
    if item == None: return
    item.setBackgroundColor(QtGui.QColor(0xFF, 0xFF, 0xFF))
    args[0].repaint()
