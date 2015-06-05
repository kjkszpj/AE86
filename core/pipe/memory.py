# -*- coding: cp936 -*-
#   在prepare就检测mem_error

import pickle

def string2instr(s):
    global mem
    mem = []
    for i in range(len(s) / 2):
        mem.append(int(s[i * 2 : i * 2 + 2], 16))


def instr_init(s_instr):
    global mem, inst_addr
    #   align QAQ 000000inserted(6 zeros)
    string2instr(s_instr)
    inst_addr = 0x087


def little_endian(val):
    b0 = val & 0xFF
    b1 = (val >> 8) & 0xFF
    b2 = (val >> 16) & 0xFF
    b3 = (val >> 24) & 0xFF
    return b0, b1, b2, b3


def prepare_reg(name, val, stall = 0, bubble = 0):
    #   DONE
    global mem_alias, stage_list, register_default

    if name == 'RNONE': return False
    if not name in mem_alias.keys():
        print "No exist register alias %s......" % name
        raw_input('continue')
        return True
    if name[0] in ['R', 'C']: print "Ready to write memory, NAME=%s\t ADDR=%d \tVALUE=%d" % (name, mem_alias[name], val)
    if not stall and not bubble: stage_list[mem_alias[name]] = (val, 1)
    elif bubble and not stall: stage_list[mem_alias[name]] = (register_default[name], 1)
    return False


def prepare_mem(addr, val, data_len = 4, stall = 0, bubble = 0):
    global mem_alias, stage_list

    print "Ready to write memory, ADDR=%d \tVALUE=%d" % (addr, val)
    if not stall and not bubble: stage_list[addr] = (val, data_len)
    return 0


def read_reg(name):
    global mem, mem_alias

    if name == 'RNONE': return 0
    if not name in mem_alias.keys():
        print "No exist register alias %s......" % name
        raw_input('continue')
        return True
    if name[0] == 'R':
        print 'OK, now read %s\t, VALUE = %d' % (name, mem[mem_alias[name]])
    return mem[mem_alias[name]]


def read_instr(pc, data_len = 1):
    if pc > inst_addr:
        print 'mem_error in read_instr %d' % pc
        raw_input('continue')
        return 'mem_error'
    if data_len == 1:
        temp = mem[pc]
        high = (temp >> 4) & 0xF
        low = temp & 0xF
        return high, low
    if data_len == 4:
        return (mem[pc + 3] << 24) +\
               (mem[pc + 2] << 16) +\
               (mem[pc + 1] << 8) +\
                mem[pc]


def read_data(addr, data_len = 1):
    if addr < 0 or addr >= len(mem):
        print 'mem_error in read_data %d' % addr
        raw_input('continue')
        return 'mem_error'
    print 'OK, now read %d\t, start with%d' % (addr, mem[addr])
    if data_len == 1: return mem[addr]
    if data_len == 4:
        return (mem[addr + 3] << 24) +\
               (mem[addr + 2] << 16) +\
               (mem[addr + 1] << 8) +\
                mem[addr]


def commit(update_fun = None):
    #   DONE
    #   memory exception
    #   what about memory write(4-bits)
    global mem, stage_list

    mem_error = False
    for addr, tvalue in stage_list.items():
        value, data_len = tvalue
        mem_error = mem_error | write_data(addr, value, data_len)
        if update_fun != None:
            update_fun(addr, value)
    stage_list = {}
    return mem_error


def write_data(addr, val, data_len = 1):
    #   需要更合理判断地址非法
    if addr <= inst_addr:
        print 'invalid addr in write_data %d' % addr
        raw_input('continue')
        return True
    if data_len == 1: mem[addr] = val
    if data_len == 4: mem[addr], mem[addr + 1], mem[addr + 2], mem[addr + 3] = little_endian(val)
    return False


def mem_init(instruction = '30840001000030850001000070240000000000000d000000c0000000000b000000a00000308004000000a008308214000000a028803a00000010a058204550150800000050250c00000030800000000062227374000000506100000000606030830400000060313083ffffffff60327457000000b05890', save = True):
    global mem_alias, mem, stage_list, register_default

    #   TEST

    stage_list = {};
    #   mem
    instr_init(instruction)
    for i in range(0x1000):
        mem.append(0)
    #   mem-alias, should have 41? items
    #   alias for register
    register_alias = {'REAX':1, 'RECX':2, 'REDX':3, 'REBX':4, 'RESP':5, 'REBP':6, 'RESI':6, 'REDI':7}
    #   alias for pipeline-register
    F_alias = {'F_predPC':8}
    D_alias = {'D_stat':9, 'D_icode':10, 'D_ifun':11, 'D_rA':12, 'D_rB':13, 'D_valC':14, 'D_valP':15}
    E_alias = {'E_stat':16, 'E_icode':17, 'E_ifun':18, 'E_valC':19, 'E_valA':20, 'E_valB':21, 'E_dstE':22, 'E_dstM':23, 'E_srcA':24, 'E_srcB':25}
    M_alias = {'M_stat':26, 'M_icode':27, 'M_Cnd':28, 'M_valE':39, 'M_valA':30, 'M_dstE':31, 'M_dstM':32, 'CC':39}
    W_alias = {'W_stat':33, 'W_icode':34, 'W_valE':35, 'W_valM':36, 'W_dstE':37, 'W_dstM':38}
    circle_alias = {'CYCLE':40}
    mem_alias = dict(register_alias.items() + F_alias.items() + D_alias.items() + E_alias.items() + M_alias.items() + W_alias.items() + circle_alias.items())

    register_default = {'REAX':0, 'RECX':0, 'REDX':0, 'REBX':0, 'RESP':0, 'REBP':0, 'RESI':0, 'REDI':0}
    #   default value for pipeline-register, used for bubble
    F_default = {'F_predPC':0}
    D_default = {'D_stat':1, 'D_icode':0, 'D_ifun':0, 'D_rA':0xF, 'D_rB':0xF, 'D_valC':0, 'D_valP':0}
    E_default = {'E_stat':1, 'E_icode':0, 'E_ifun':0, 'E_valC':0, 'E_valA':0, 'E_valB':0, 'E_dstE':0xF, 'E_dstM':0xF, 'E_srcA':0, 'E_srcB':0}
    M_default = {'M_stat':1, 'M_icode':0, 'M_Cnd':1, 'M_valE':0, 'M_valA':0, 'M_dstE':0xF, 'M_dstM':0xF, 'CC':0}
    W_default = {'W_stat':1, 'W_icode':0, 'W_valE':0, 'W_valM':0, 'W_dstE':0xF, 'W_dstM':0xF}
    register_default = dict(register_default.items() + F_default.items() + D_default.items() + E_default.items() + M_default.items() + W_default.items())
    #   给寄存器分配实际内存地址
    cnt = 0x200
    for key, value in mem_alias.items():
        cnt = cnt + 1
        mem_alias[key] = cnt
    #   开始应该设置register初始值
    for name, defalut_value in register_default.items():
        mem[mem_alias[name]] = defalut_value
    # print mem_alias
    # print len(mem_alias)
    if save:
        outf = file('C:\\Users\\You\\Documents\\GitHub\\AE86\\data\\runtime\\mem.pk', 'w');
        pickle.dump(mem, outf)


def load_data(mem_file = '../data/runtime/mem.pk'):
    global mem
    mem = pickle.load(file(mem_file))
    print mem


def save_data(mem_file = '../data/runtime/mem.pk'):
    global mem

    pickle.dump(mem, file(mem_file, 'w'))


if __name__ == "__main__":
    mem_init()
    print mem[0x24]
    prepare_reg('RESP', 0x12345678)
    print read_reg('RESP')
    commit()
    print read_reg('RESP')