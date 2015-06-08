from PyQt4 import QtGui
from PyQt4 import QtCore
from time import sleep
import sys
sys.path.append('C:\\Users\\You\\Documents\\GitHub\\AE86\\core\\pipe')
import memory
import re


def init_code(ui, f_name = 'C:\\Users\\You\\Documents\\GitHub\\AE86\\data\\y86_code\\asum.yo'):
    inf = file(f_name, 'r')
    code = inf.readlines()
    result = {}
    for s in code:
        pattern = 'x\w+:'
        if re.search('x[\dabcdefABCDEF]+:.*\S+.*\|', s) == None: continue
        temp = re.search('x[\dabcdefABCDEF]+|', s).group()
        if re.search(pattern, s) == None: continue
        addr = re.search('x[\dabcdefABCDEF]+:', s).group()
        addr = re.search('[\dabcdefABCDEF]+', addr).group()
        addr = int(addr, 16)
        if s.find('#') != -1: s = s[0:s.find('#')]
        result[addr] = s[:-1]
    return result


#   TODO color
def refresh_code(ui, code, addr, value):
    if addr not in memory.mem_alias.values(): return None
    reg_name = memory.mem_alias.keys()[memory.mem_alias.values().index(addr)]
    if reg_name == 'W_PC':
        if value not in code.keys(): return None
        text = '***' + code[value] + '\n'
        #   5 behind and 5 ahead
        pc = value - 2
        cnt = 5
        while cnt:
            cnt -= 1
            while pc not in code.keys() and pc >= 0: pc -= 2
            if pc < 0: break
            text = code[pc] + '\n' + text
            pc -= 2
        pc = value + 2
        cnt = 5
        addr_limit = max(code.keys())
        while cnt:
            cnt -= 1
            while pc not in code.keys() and pc <= addr_limit: pc += 2
            if pc > addr_limit: break
            text = text + code[pc] + '\n'
            pc += 2
        QtGui.QTextBrowser.setText(ui, text)
        ui.repaint()
        return None


#   TODO cd here
def cool_down_code():
    pass


if __name__ == '__main__':
    result = init_code(None)
    for addr, code in result.items():
        print addr, code
    refresh_code(None, result, 10)