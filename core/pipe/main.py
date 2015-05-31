# -*- coding: cp936 -*-

#   pipeline寄存器未实现

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

def little_endian(data, s):
    #   DONE
    return (data[s + 3] << 24) +\
           (data[s + 2] << 16) +\
           (data[s + 1] << 8) +\
            data[s]

#   ---about FETCH stage---

def need_regids(f_icode):
    #   DONE
    return f_icode in [IRRMOVL, IOPL, IPUSHL, IPOPL, IIRMOVL, IRMMOVL, IMRMOVL]

def need_valC(f_icode):
    #   DONE
    return f_icode in [IIRMOVL, IRMMOVL, IMRMOVL, IJXX, ICALL]

def decode(pc=0):
    #   异常处理没做
    #   icode, ifun, rA, rB, valC, valP

    #   get icode & ifun
    valP = pc
    temp = instruction[valP]
    valP = valP + 1
    icode = (temp >> 4) & 0xF
    ifun = (temp >> 0) & 0xF

    #   get rA & rB
    if need_regids(ifun):
        temp = instruction[valP]
        valP = valP + 1
        rA = (temp >> 4) & 0xF
        rB = (temp >> 0) & 0xF
    else: rA, rB = 0xF, 0xF

    #   get valC
    if need_valC(ifun):
        valC = little_endian(instruction, valP)
        valP = valP + 4
    else: valC = 0
    return icode, ifun, rA, rB, valC, valP

def f_predPC(f_icode, f_valC, f_valP):
    #   DONE
    #   what about IRET?
    if f_icode in [IJXX, ICALL]: return f_valC
    else: return f_valP

def f_pc(F_predPC, M_icode, M_valA, W_icode, W_valM, M_Cnd):
    #   DONE
    if M_icode == IJXX and not M_Cnd: return M_valA
    if W_icode == IRET: return W_valM
    return F_predPC

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

def d_dstM(D_icode, D_ra):
    #   DONE
    if D_icode in [IMRMOVL, IPOPL]: D_ra
    return RNONE

def d_valA(D_icode, D_valP, d_valA, srcA, e_dstE, M_dstM, M_dstE, W_dstM, W_dstE, e_valE, m_valM, M_valE, W_valM, W_valE):
    #   DONE
    #   srcA or d_srcA
    if D_icode in [ICALL, IJXX]: return D_valP
    if srcA == e_dstE: return e_valE
    if srcA == M_dstM: return m_valM
    if srcA == M_dstE: return M_valE
    if srcA == W_dstM: return W_valM
    if srcA == W_dstE: return W_valE
    return d_valA

def d_valB(srcB, d_valB, e_dstE, M_dstM, M_dstE, W_dstM, W_dstE, e_valE, m_valM, M_valE, W_valM, W_valE):
    #   DONE
    #   no bug?
    #   srcB or d_srcB
    if srcB == e_dstE: return e_valE
    if srcB == M_dstM: return m_valM
    if srcB == M_dstE: return M_valE
    if srcB == W_dstM: return W_valM
    if srcB == W_dstE: return W_valE
    return d_valB

#   ---about excure stage---

def aluA(E_icode, E_valA, E_valC):
    #   DONE
    if E_icode in [IRRMOVL, IOPL]: return E_valA
    if E_icode in [IIRMOVL, IRMMOVL, IMRMOVL]: return E_valC
    if E_icode in [ICALL, IPUSHL]: -4
    if E_icode in [IRET, IPOPL]: 4
    return 0

def aluB(E_icode, E_valB):
    #   DONE
    if E_icode in [IRMMOVL, IMRMOVL, IOPL, ICALL, IPUSHL, IRET, IPOPL]: return E_valB
    if E_icode in [IRRMOVL, IIRMOVL]: return 0
    return 0

def alufun(E_icode, E_ifun):
    #   DONE
    if E_icode == IOPL: return E_ifun
    return ALUADD

def set_cc(E_icode, m_stat, W_stat):
    #   DONE
    return E_icode == IOPL and not m_stat in [SADR, SINS, SHLT] and not W_stat in [SADR, SINS, SHLT]

def e_valA(E_valA):
    #   应该单独开一个函数么...
    return E_valA

def e_dstE(E_icode, e_Cnd, E_dstE):
    #   DONE
    if E_icode == IRRMOVL and not e_Cnd: return RNONE
    return E_dstE

#   ---about memory stage---

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



def init():
    #   double check this function
    global instruction, INOP, IHALT, IRRMOVL, IIRMOVL, IRMMOVL, IMRMOVL, IOPL, IJXX, ICALL, IRET, IPUSHL, IPOP0
    global FNONE, RNONE, RESP, ALUADD, SAOK, SADR, SINS, SHLT

    instruction = [0x30, 0x84, 0x00, 0x01, 0x00, 0x00]
    #   icode
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

    #   ??
    FNONE = 0x0
    RESP = 0x4
    RNONE = 0xF
    ALUADD = 0x0

    #   status code
    SAOK = 0x1
    SADR = 0x2
    SINS = 0x3
    SHLT = 0x4

if __name__ == "__main__":
    init()
    print alu(1, 2, 0)
