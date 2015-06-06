from PyQt4 import QtGui
from PyQt4 import QtCore
import memory
from memory import read_reg

def combine(name1, name2):
    return (read_reg(name1) << 4) + read_reg(name2)

def refresh_pipe(ui, addr, value):
    if addr in memory.mem_alias.values():
        prpr = memory.mem_alias.keys()[memory.mem_alias.values().index(addr)]
        value_len = 0
        tb = None
        if prpr[1] != '_':
            #   not interested
            return
        stage = prpr[0]
        pr_head = prpr[2]
        pr_name = prpr[2:]
        #   format define(head & value)
        if pr_head == 'i':
            if stage == 'W': head = 'icode'; value_len = 1; value = read_reg('W_icode')
            elif stage == 'M': head = 'icode:Cnd'; value_len = 2; value = combine('M_icode', 'M_Cnd')
            else: head = 'icode:ifun'; value_len = 2; value = combine(stage + '_icode', stage + '_ifun')
        elif pr_head == 'C': head = 'icode:Cnd'; value_len = 2; value = combine('M_icode', 'M_Cnd')
        elif pr_head == 'v': head = prpr[2:]; value_len = 8
        elif pr_head == 'p': head = 'predPC'; value_len = 4
        elif pr_head == 'd': head = 'dstE:dstM'; value_len = 2; value = combine(stage + '_dstE', stage + '_dstM')
        elif pr_head == 's': head = 'srcA:srcB'; value_len = 2; value = combine('E_srcA', 'E_srcB')
        elif pr_head == 'r': head = 'rA:rB'; value_len = 2; value = combine('D_rA', 'D_rB')

        #   get textBrowser object
        #   FETCH
        if prpr == 'F_predPC': tb = ui.text_F_predPC
        #   DECODE
        elif prpr in ['D_icode', 'D_ifun']: tb = ui.text_D_icode_ifun
        elif prpr in ['D_ra', 'D_rB']: tb = ui.text_D_rA_rB
        elif prpr == 'D_valC': tb = ui.text_D_valC
        elif prpr == 'D_valP': tb = ui.text_D_valP
        #   EXECUTE
        elif prpr in ['E_icode', 'E_ifun']: tb = ui.text_E_icode_ifun
        elif prpr == 'E_valC': tb = ui.text_E_valC
        elif prpr == 'E_valA': tb = ui.text_E_valA
        elif prpr == 'E_valB': tb = ui.text_E_valB
        elif prpr in ['E_dstE', 'E_dstM']: tb = ui.text_E_dstE_dstM
        elif prpr in ['E_srcA', 'E_srcB']: tb = ui.text_E_srcA_srcB
        #   MEMORY
        elif prpr in ['M_icode', 'M_Cnd']: tb = ui.text_M_icode_Cnd
        elif prpr == 'M_valE': tb = ui.text_M_valE
        elif prpr == 'M_valA': tb = ui.text_M_valA
        elif prpr in ['M_dstE', 'M_dstM']: tb = ui.text_M_dstE_dstM
        #   WRITE BACK
        elif prpr == 'W_icode': tb = ui.text_W_icode
        elif prpr == 'W_valE': tb = ui.text_W_valE
        elif prpr == 'W_valM': tb = ui.text_W_valM
        elif prpr in ['W_dstE', 'W_dstM']: tb = ui.text_W_dstE_dstM

        if tb != None:
            if value_len == 1: value = '%01x' % value
            elif value_len == 2: value = '%02x' % value
            elif value_len == 4: value = '0x%04x' % value
            elif value_len == 8: value = '0x%08x' % value
            value = value.upper()
            QtGui.QTextBrowser.setText(tb, head + '\n' + value)
            tb.repaint()
    else:
        pass