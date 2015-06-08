from PyQt4 import QtGui
from PyQt4 import QtCore
from time import sleep
import sys
sys.path.append('C:\\Users\\You\\Documents\\GitHub\\AE86\\core\\pipe')
import memory
import main


def init_status(ui):
    ui.showMessage('CYCLE\t%d | ZF:0 SF:0 OF: 0' %0)
    return 'CYCLE\t%d | ZF:0 SF:0 OF: 0' %0


def refresh_status(ui, addr, value, sim):
    if addr not in memory.mem_alias.values(): return None
    reg_name = memory.mem_alias.keys()[memory.mem_alias.values().index(addr)]
    if reg_name in ['CYCLE', 'CC', '']:
        tcc = memory.read_reg('CC')
        text = 'CYCLE\t%d   |' % memory.read_reg('CYCLE')
        text += '   ZF:%d SF:%d OF:%d   |  ' % ((tcc >> 2) & 1, (tcc >> 1) & 1, tcc & 1)
        if sim.f_stall:
            text += ' F:stall'
        if sim.f_bubble:
            text += ' F:bubble'
        if sim.d_stall:
            text += ' D:stall'
        if sim.d_bubble:
            text += ' D:bubble'
        if sim.e_stall:
            text += ' E:stall'
        if sim.e_bubble:
            text += ' E:bubble'
        if sim.m_stall:
            text += ' M:stall'
        if sim.m_bubble:
            text += ' M:bubble'
        if sim.w_stall:
            text += ' W:stall'
        if sim.w_bubble:
            text += ' W:bubble'
        if text[-1] != ' ':
            text += '   |  '
        if sim.ts_exc:
            text += ' exception,'
        if sim.ts_luh:
            text += ' load use hazard,'
        if sim.ts_ret:
            text += ' return encounter,'
        if sim.ts_mis:
            text += ' mispredict branch,'
        if text[-1] == ',': text = text[:-1] + '.'
        ui.showMessage(text)