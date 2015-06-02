# -*- coding: cp936 -*-

from memory import *
#   以下是小函数
#   ---about FETCH stage---

#   ---bug free---
def need_regids(f_icode):
    #   DONE
    return f_icode in [IRRMOVL, IOPL, IPUSHL, IPOPL, IIRMOVL, IRMMOVL, IMRMOVL]

def need_valC(f_icode):
    #   DONE
    return f_icode in [IIRMOVL, IRMMOVL, IMRMOVL, IJXX, ICALL]

def f_predPC(f_icode, f_valC, f_valP):
    #   DONE
    #   what about RET? stall until memory done(before write back)
    if f_icode in [IJXX, ICALL]: return f_valC
    else: return f_valP

def f_pc(F_predPC, M_icode, M_valA, W_icode, W_valM, M_Cnd):
    #   DONE
    if M_icode == IJXX and not M_Cnd: return M_valA
    if W_icode == IRET: return W_valM
    return F_predPC

def instr_valid(f_icode):
    #   DONE
    return f_icode in [INOP, IHALT, IRRMOVL, IIRMOVL, IRMMOVL, IMRMOVL, IOPL, IJXX, ICALL, IRET, IPUSHL, IPOPL]

def f_stat(f_icode, imem_error):
    #   DONE
    #   有优先级？
    if imem_error: return SADR
    if not instr_valid(f_icode): return SINS
    if f_icode == IHALT: return SHLT
    return SAOK

#   ---about DECODE stage---

def d_srcA(D_icode, D_rA):
    #   DONE
    if D_icode in [IRRMOVL, IRMMOVL, IOPL, IPUSHL]: return D_rA
    if D_icode in [IPOPL, IRET]: return RESP
    return RNONE

def d_srcB(D_icode, D_rB):
    #   DONE
    if D_icode in [IOPL, IRMMOVL, IMRMOVL]: return D_rB
    if D_icode in [IPUSHL, IPOPL, ICALL, IRET]: return RESP;
    return RNONE;

def d_dstE(D_icode, D_rB):
    #   DONE
    #   是指在write back阶段的r[dstE]=valE
    if D_icode in [IRRMOVL, IIRMOVL, IOPL]: return D_rB
    if D_icode in [IPUSHL, IPOPL, ICALL, IRET]: return RESP
    return RNONE;

def d_dstM(D_icode, D_rA):
    #   DONE
    if D_icode in [IMRMOVL, IPOPL]: return D_rA
    return RNONE

def d_valA(D_icode, d_valA, srcA, D_valP, e_dstE, M_dstM, M_dstE, W_dstM, W_dstE, e_valE, m_valM, M_valE, W_valM, W_valE):
    #   DONE
    #   可能有两种，valA, valP, 还可以forward
    if D_icode in [ICALL, IJXX]: return D_valP
    if srcA == e_dstE: return e_valE
    if srcA == M_dstM: return m_valM
    if srcA == M_dstE: return M_valE
    if srcA == W_dstM: return W_valM
    if srcA == W_dstE: return W_valE
    return d_valA

def d_valB(srcB, d_valB, e_dstE, M_dstM, M_dstE, W_dstM, W_dstE, e_valE, m_valM, M_valE, W_valM, W_valE):
    #   DONE
    if srcB == e_dstE: return e_valE
    if srcB == M_dstM: return m_valM
    if srcB == M_dstE: return M_valE
    if srcB == W_dstM: return W_valM
    if srcB == W_dstE: return W_valE
    return d_valB

#   ---about EXECUTE stage---

def aluA(E_icode, E_valA, E_valC):
    #   DONE
    if E_icode in [IRRMOVL, IOPL]: return E_valA
    if E_icode in [IIRMOVL, IRMMOVL, IMRMOVL]: return E_valC
    if E_icode in [ICALL, IPUSHL]: return -4
    if E_icode in [IRET, IPOPL]: return 4
    return 0

def aluB(E_icode, E_valB):
    #   DONE
    #   12个指令, 9个要alu, 还有HALT, NOP, JXX, JXX只要set pc
    if E_icode in [IRMMOVL, IMRMOVL, IOPL, ICALL, IPUSHL, IRET, IPOPL]: return E_valB
    if E_icode in [IRRMOVL, IIRMOVL]: return 0
    return 0

def alufun(E_icode, E_ifun):
    #   DONE
    if E_icode == IOPL: return E_ifun
    return ALUADD

def set_CC(E_icode, m_stat, W_stat):
    #   DONE
    return E_icode == IOPL and not m_stat in [SADR, SINS, SHLT] and not W_stat in [SADR, SINS, SHLT]

def e_valA(E_valA):
    #   应该单独开一个函数么...
    return E_valA

def e_dstE(E_icode, e_Cnd, E_dstE):
    #   DONE
    if E_icode == IRRMOVL and not e_Cnd: return RNONE
    return E_dstE

def e_Cnd(E_icode, E_ifun, CC):
    #   CHECK
    ZF, SF, OF = (CC & 4) >> 2, (CC & 2) >> 1, CC & 1
    if E_ifun == 0: return 1
    if E_ifun == 1: return (SF ^ OF) | ZF
    if E_ifun == 2: return SF ^ OF
    if E_ifun == 3: return ZF
    if E_ifun == 4: return ~ZF
    if E_ifun == 5: return ~(SF ^ OF)
    if E_ifun == 6: return ~(SF ^ OF) & ~ZF

#   ---about MEMORY stage---

def mem_addr(M_icode, M_valA, M_valE):
    #   DONE
    if M_icode in [IRMMOVL, IPUSHL, ICALL, IMRMOVL]: return M_valE
    if M_icode in [IPOPL, IRET]: return M_valA
    return 0

def mem_read(M_icode):
    #DONE
    return M_icode in [IMRMOVL, IPOPL, IRET]

def mem_write(M_icode):
    #   DONE
    return M_icode in [IRMMOVL, IPUSHL, ICALL]

def m_stat(dmem_error, M_stat):
    #   DONE
    if dmem_error: return SADR
    return M_stat

#   以下是功能模块

def alu(aluA=1, aluB=1, aluFun=0):
    #   DONE
    #   alu result
    if aluFun not in [0, 1, 2, 3]: print "alu_fun error! %d" % aluFun
    if aluFun == 0:   result = aluA + aluB
    elif aluFun == 1: result = aluB - aluA
    elif aluFun == 2: result = aluA & aluB
    elif aluFun == 3: result = aluA ^ aluB

    #   condition code, ZF|SF|OF
    ZF = result == 0
    SF = result < 0
    OF = (aluA < 0 == aluB < 0) and ((result < 0) != (aluA < 0))
    CC = (ZF << 2) | (SF << 1) | OF

    return result, CC

def decode(pc=0):
    #   TODO debug decode here
    #   icode, ifun, rA, rB, valC, valP
    #   get icode & ifun
    valP = pc
    if read_instr(valP) == 'mem_error': return 0, 0, 0, 0, 0, 0, True
    icode, ifun = read_instr(valP)
    valP += 1

    #   get rA & rB
    if need_regids(icode):
        if read_instr(valP) == 'mem_error': return 0, 0, 0, 0, 0, 0, True
        rA, rB = read_instr(valP)
        valP += 1
    else: rA, rB = 0xF, 0xF

    #   get valC
    if need_valC(icode):
        if read_instr(valP) == 'mem_error': return 0, 0, 0, 0, 0, 0, True
        valC = read_instr(valP, 4)
        valP = valP + 4
    else: valC = 0

    #   invalid instruction detection
    #   invalid icode
    imem_error = not instr_valid(icode)
    #   invalid ifun
    imem_error = imem_error or ifun < 0
    if icode in [IOPL]: imem_error = imem_error or ifun > 3
    elif icode in [IRRMOVL, IJXX]: imem_error = imem_error or ifun > 6
    else: imem_error = imem_error or (ifun != 0)
    #   invalid rA, rB
    imem_error = imem_error or not rA in register_name.keys()
    imem_error = imem_error or not rB in register_name.keys()
    return icode, ifun, rA, rB, valC, valP, imem_error

def rf_read(srcA, srcB):
    global register_name

    return read_reg(register_name[srcA]), read_reg(register_name[srcB])

def rf_write(dstM, valM, dstE, valE):
    #   CHECK valM优先
    global register_name

    prepare_reg(register_name[dstM], valM)
    if dstE != dstM:
        prepare_reg(register_name[dstE], valE)

def dm_read(addr):
    return read_data(addr, 4)

def dm_write(addr, val):
    prepare_mem(addr, val)

def sim_main():
    cnt = 0
    while cnt < 15:
        #   TODO debug sim_main here
        cnt = cnt + 1

        if cnt == 14:
            print 'good'
        #   出现两次的表达式基本上用临时变量存储
        #   ---FETCH connection---
        tf_pc = f_pc(read_reg('F_predPC'), read_reg('M_icode'), read_reg('M_valA'), read_reg('W_icode'), read_reg('W_valM'), read_reg('M_Cnd'))
        tf_icode, tf_ifun, tf_rA, tf_rB, tf_valC, tf_valP, timem_error = decode(tf_pc)

        prepare_reg('D_icode', tf_icode)
        prepare_reg('D_ifun', tf_ifun)
        prepare_reg('D_rA', tf_rA)
        prepare_reg('D_rB', tf_rB)
        prepare_reg('D_valC', tf_valC)
        prepare_reg('D_valP', tf_valP)
        prepare_reg('F_predPC', f_predPC(tf_icode, tf_valC, tf_valP))
        prepare_reg('D_stat', f_stat(tf_icode, timem_error))

        #   ---DECODE connection---
        td_valA = 0
        td_valB = 0
        srcA = d_srcA(read_reg('D_icode'), read_reg('D_rA'))
        srcB = d_srcB(read_reg('D_icode'), read_reg('D_rB'))
        prepare_reg('E_stat', read_reg('D_stat'))
        prepare_reg('E_icode', read_reg('D_icode'))
        prepare_reg('E_ifun', read_reg('D_ifun'))
        prepare_reg('E_valC', read_reg('D_valC'))
        prepare_reg('E_dstE', d_dstE(read_reg('D_icode'), read_reg('D_rB')))
        prepare_reg('E_dstM', d_dstM(read_reg('D_icode'), read_reg('D_rA')))
        prepare_reg('E_srcA', srcA)
        prepare_reg('E_srcB', srcB)

        #   ---EXECUTE connection---
        taluA = aluA(read_reg('E_icode'), read_reg('E_valA'), read_reg('E_valC'))
        taluB = aluB(read_reg('E_icode'), read_reg('E_valB'))
        te_valE, tCC = alu(taluA, taluB, alufun(read_reg('E_icode'), read_reg('E_ifun')))
        te_Cnd = e_Cnd(read_reg('E_icode'), read_reg('E_ifun'), read_reg('CC'))

        prepare_reg('M_stat', read_reg('E_stat'))
        prepare_reg('M_icode', read_reg('E_icode'))
        prepare_reg('M_valE', te_valE)
        prepare_reg('M_valA', read_reg('E_valA'))
        if set_CC(read_reg('E_icode'), m_stat, read_reg('W_stat')): prepare_reg('CC', tCC)
        prepare_reg('M_Cnd', te_Cnd)
        prepare_reg('M_dstE', e_dstE(read_reg('E_icode'), te_Cnd, read_reg('E_dstE')))
        prepare_reg('M_dstM', read_reg('E_dstM'))

        #   ---MEMORY connection---
        tm_stat = m_stat(False, read_reg('M_stat'))
        tm_addr = mem_addr(read_reg('M_icode'), read_reg('M_valA'), read_reg('M_valE'))

        prepare_reg('W_stat', tm_stat)
        prepare_reg('W_icode', read_reg('M_icode'))
        prepare_reg('W_valE', read_reg('M_valE'))
        if mem_read(read_reg('M_icode')):
            tm_valM = dm_read(tm_addr)
            dmem_error = tm_valM == 'mem_error'
        else: tm_valM = 0
        prepare_reg('W_valM', tm_valM)
        if mem_write(read_reg('M_icode')): dm_write(tm_addr, read_reg('M_valA'))
        prepare_reg('W_dstE', read_reg('M_dstE'))
        prepare_reg('W_dstM', read_reg('M_dstM'))

        #   ---WRITE BACK connection---
        rf_write(read_reg('W_dstM'), read_reg('W_valM'), read_reg('W_dstE'), read_reg('W_valE'))

        #   forward comes at last
        #   valA
        tvalA, tvalB = rf_read(srcA, srcB)
        td_valA = d_valA(read_reg('D_icode'), tvalA, srcA,
                         read_reg('D_valP'), e_dstE(read_reg('E_icode'), te_Cnd, read_reg('E_dstE')),
                         read_reg('M_dstM'), read_reg('M_dstE'), read_reg('W_dstM'), read_reg('W_dstE'),
                         te_valE, tm_valM, read_reg('M_valE'), read_reg('W_valM'), read_reg('W_valE'))
        #   valB
        td_valB = d_valB(srcB, tvalB, e_dstE(read_reg('E_icode'), te_Cnd, read_reg('E_dstE')),
                         read_reg('M_dstM'), read_reg('M_dstE'), read_reg('W_dstM'), read_reg('W_dstE'),
                         te_valE, tm_valM,  read_reg('M_valE'), read_reg('W_valM'), read_reg('W_valE'))
        prepare_reg('E_valA', td_valA)
        prepare_reg('E_valB', td_valB)
        #   OK to change
        commit()
        if cnt > 0:
            my_print(cnt)
    return 0

def my_print(cnt):
    #   NO stat here
    print '------cycle\t%d!------' % cnt
    print "FETCH:"
    print '\tF_predPC 	= 0x%x' % read_reg('F_predPC')

    print 'DECODE:'
    print '\tD_icode  	= 0x%x' % read_reg('D_icode')
    print '\tD_ifun   	= 0x%x' % read_reg('D_ifun')
    print '\tD_rA     	= 0x%x' % read_reg('D_rA')
    print '\tD_rB     	= 0x%x' % read_reg('D_rB')
    print '\tD_valC   	= 0x%x' % read_reg('D_valC')
    print '\tD_valP   	= 0x%x' % read_reg('D_valP')

    print 'EXECUTE:'
    print '\tE_icode  	= 0x%x' % read_reg('E_icode')
    print '\tE_ifun   	= 0x%x' % read_reg('E_ifun')
    print '\tE_valC   	= 0x%x' % read_reg('E_valC')
    print '\tE_valA   	= 0x%x' % read_reg('E_valA')
    print '\tE_valB   	= 0x%x' % read_reg('E_valB')
    print '\tE_dstE   	= 0x%x' % read_reg('E_dstE')
    print '\tE_dstM   	= 0x%x' % read_reg('E_dstM')
    print '\tE_srcA   	= 0x%x' % read_reg('E_srcA')
    print '\tE_srcB   	= 0x%x' % read_reg('E_srcB')

    print 'MEMORY:'
    print '\tM_icode  	= 0x%x' % read_reg('M_icode')
    print '\tM_Cnd    	= %d'   % read_reg('M_Cnd')
    print '\tM_valE   	= 0x%x' % read_reg('M_valE')
    print '\tM_valA   	= 0x%x' % read_reg('M_valA')
    print '\tM_dstE   	= 0x%x' % read_reg('M_dstE')
    print '\tM_dstM   	= 0x%x' % read_reg('M_dstM')

    print 'WRITE BACK:'
    print '\tW_icode  	= 0x%x' % read_reg('W_icode')
    print '\tW_valE   	= 0x%x' % read_reg('W_valE')
    print '\tW_valM   	= 0x%x' % read_reg('W_valM')
    print '\tW_dstE   	= 0x%x' % read_reg('W_dstE')
    print '\tW_dstM   	= 0x%x' % read_reg('W_dstM')

def init():
    #   double check this function
    global INOP, IHALT, IRRMOVL, IIRMOVL, IRMMOVL, IMRMOVL, IOPL, IJXX, ICALL, IRET, IPUSHL, IPOPL
    global FNONE, RNONE, RESP, ALUADD, SAOK, SADR, SINS, SHLT
    global register_name
    global CC_mask, CC_result

    mem_init();
    INOP = 0x0
    IHALT = 0x1
    IRRMOVL = 0x2
    IIRMOVL = 0x3
    IRMMOVL = 0x4
    IMRMOVL = 0x5
    IOPL = 0x6
    IJXX = 0x7
    ICALL = 0x8
    IRET = 0x9
    IPUSHL = 0xA
    IPOPL = 0xB

    #   在pipeline里面用到的常量
    FNONE = 0x0
    RESP = 0x4
    RNONE = 0xF
    ALUADD = 0x0

    #   status code
    SAOK = 0x1; SADR = 0x2; SINS = 0x3; SHLT = 0x4;

    #   id-name index for register
    register_name = {0:'REAX', 1:'RECX', 2:'REDX', 3:'REBX', 4:'RESP', 5:'REBP', 6:'RESI', 7:'REDI', 0xF:'RNONE'}

if __name__ == "__main__":
    init()
    sim_main()
    print read_reg('RESP')