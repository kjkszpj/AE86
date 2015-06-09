from PyQt4 import QtGui
from PyQt4 import QtCore
from time import sleep
import memory
from memory import read_reg

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

def combine(name1, name2):
    return (read_reg(name1) << 4) + read_reg(name2)

def refresh_pipe(ui, addr, value, color = True):
    if addr in memory.mem_alias.values():
        prpr = memory.mem_alias.keys()[memory.mem_alias.values().index(addr)]
        value_len = 0
        tb = None
        if prpr[1] != '_':
            #   not interested
            return None
        stage = prpr[0]
        pr_head = prpr[2]
        pr_name = prpr[2:]
        #   format define(head & value)
        if pr_head == 'i':
            if stage == 'W': head = 'icode'; value_len = 1; value = read_reg('W_icode')
            elif stage == 'M': head = 'icode Cnd'; value_len = 2; value = combine('M_icode', 'M_Cnd')
            else: head = 'icode ifun'; value_len = 2; value = combine(stage + '_icode', stage + '_ifun')
        elif pr_head == 'C': head = 'icode Cnd'; value_len = 2; value = combine('M_icode', 'M_Cnd')
        elif pr_head == 'v': head = prpr[2:]; value_len = 8
        elif pr_head == 'p': head = 'predPC'; value_len = 4
        elif pr_head == 'd': head = 'dstE dstM'; value_len = 2; value = combine(stage + '_dstE', stage + '_dstM')
        elif pr_head == 's': head = 'srcA srcB'; value_len = 2; value = combine('E_srcA', 'E_srcB')
        elif pr_head == 'r': head = 'rA:rB'; value_len = 2; value = combine('D_rA', 'D_rB')
        else: return None

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
            elif value_len == 4: value = '0x' + ('%04x' % value).upper()
            elif value_len == 8: value = '0x' + ('%08x' % value).upper()
            QtGui.QTextBrowser.setText(tb, head + '\n' + value)
            # what the html
            if color:
                tb.setHtml(_translate("total", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                               "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                               "p, li { white-space: pre-wrap; }\n"
                                               "</style></head><body style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:400; font-style:normal; background-color:aliceblue;\">\n"
                                               "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'courier\';\">%s</span></p>\n"
                                               "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'courier\';\">%s</span></p></body></html>" % (head, value), None))
                tb.repaint()
                return (cool_down_pipe, (tb, head, value))
    else:
        pass
        return None

def cool_down_pipe(args):
    args[0].setHtml(_translate("total", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                   "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                   "p, li { white-space: pre-wrap; }\n"
                                   "</style></head><body style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                   "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'courier\';\">%s</span></p>\n"
                                   "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'courier\';\">%s</span></p></body></html>" % (args[1], args[2]), None))
    args[0].repaint()