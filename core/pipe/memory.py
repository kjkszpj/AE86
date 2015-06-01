# -*- coding: cp936 -*-
#   在prepare就检测mem_error

def little_endian(val):
    b0 = val & 0xFF
    b1 = (val >> 8) & 0xFF
    b2 = (val >> 16) & 0xFF
    b3 = (val >> 24) & 0xFF
    return b0, b1, b2, b3


def prepare_reg(name, val, data_len = 1):
    #   DONE
    global mem_alias, stage_list

    if name == 'RNONE': return False
    if not name in mem_alias.keys():
        print "No exist register alias %s......" % name
        n = raw_input()
        return True
    print "Ready to write memory, NAME=%s\t ADDR=%d \tVALUE=%d" % (name, mem_alias[name], val)
    stage_list[mem_alias[name]] = (val, data_len)
    return False


def prepare_mem(addr, val, data_len = 4):
    global mem_alias, stage_list

    print "Ready to write memory, NAME=%s\t ADDR=%d \tVALUE=%d" % (name, mem_alias[name], val)
    stage_list[addr] = (val, data_len)
    return 0


def read_reg(name):
    global mem, mem_alias

    if not name in mem_alias.keys():
        print "No exist register alias %s......" % name
        n = raw_input()
        return True
    return mem[mem_alias[name]]


def read_instr(pc, data_len = 1):
    if addr > inst_addr: return 'mem_error'
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
    #   TODO, exception
    if addr <= inst_addr: return 'mem_error'
    if data_len == 1: return mem[addr]
    if data_len == 4:
        return (mem[addr + 3] << 24) +\
               (mem[addr + 2] << 16) +\
               (mem[addr + 1] << 8) +\
                mem[addr]


def commit():
    #   DONE
    #   TODO, memory exception
    #   what about memory write(4-bits)
    global mem, stage_list

    mem_error = False
    for addr, tvalue in stage_list.items():
        value, data_len = tvalue
        mem_error = mem_error | write_data(addr, value, data_len)
    stage_list = {}
    return mem_error


def write_data(addr, val, data_len = 1):
    #   需要更合理判断地址非法
    if addr <= inst_addr: return True
    if data_len == 1: mem[addr] = val
    if data_len == 4: mem[addr], mem[addr + 1], mem[addr + 2], mem[addr + 3] = little_endian(val)
    return False


def mem_init():
    global mem_alias, mem, stage_list, inst_addr

    #   TEST

    stage_list = {};
    #   mem
    mem = [0x30, 0x84, 0x00, 0x01, 0x00, 0x00, 0x30, 0x85, 0x00, 0x01, 0x00, 0x00]
    inst_addr = 0x00C
    for i in range(200):
        mem.append(0)

    #   mem-alias, should have 40? items
    #   alias for register
    register_alias = {'REAX':1, 'RECX':2, 'REDX':3, 'REBX':4, 'RESP':5, 'REBP':6, 'RESI':6, 'REDI':7}
    #   alias for pipeline-register
    F_alias = {'F_predPC':8}
    D_alias = {'D_stat':9, 'D_icode':10, 'D_ifun':11, 'D_rA':12, 'D_rB':13, 'D_valC':14, 'D_valP':15}
    E_alias = {'E_stat':16, 'E_icode':17, 'E_ifun':18, 'E_valC':19, 'E_valA':20, 'E_valB':21, 'E_dstE':22, 'E_dstM':23, 'E_srcA':24, 'E_srcB':25}
    M_alias = {'M_stat':26, 'M_icode':27, 'M_Cnd':28, 'M_valE':39, 'M_valA':30, 'M_dstE':31, 'M_dstM':32, 'CC':39}
    W_alias = {'W_stat':33, 'W_icode':34, 'W_valE':35, 'W_valM':36, 'W_dstE':37, 'W_dstM':38}
    mem_alias = dict(register_alias.items() + F_alias.items() + D_alias.items() + E_alias.items() + M_alias.items() + W_alias.items())
    #   assign mem address
    cnt = 100
    for key, value in mem_alias.items():
        cnt = cnt + 1
        mem_alias[key] = cnt
    print mem_alias
    print len(mem_alias)

if __name__ == "__main__":
    mem_init()
    prepare_reg('RESP', 0x12345678)
    print read_reg('RESP')
    commit()
    print read_reg('RESP')