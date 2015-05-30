# -*- coding: cp936 -*-

#   pipeline寄存器未实现

def alu(aluA=1, aluB=1, aluFun=0):
    #   ------DONE------
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
    #   ------DONE------
    return (data[s + 3] << 24) +\
           (data[s + 2] << 16) +\
           (data[s + 1] << 8) +\
            data[s]

def need_regids(f_icode):
    #   ------DONE------
    return f_icode in [IRRMOVL, IOPL, IPUSHL, IPOPL, IIRMOVL, IRMMOVL, IMRMOVL]

def need_valC(f_icode):
    #   ------DONE------
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
    #   ------DONE------
    #   what about IRET?
    if f_icode in [IJXX, ICALL]: return f_valC
    else: return f_valP

def f_pc(F_predPC, M_icode, M_valA, W_icode, W_valM, M_Cnd):
    #   ------DONE------
    if M_icode == IJXX and not M_Cnd: return M_valA
    if W_icode == IRET: return W_valM
    return F_predPC

def init():
    #   double check this function
    global instruction, INOP, IHALT, IRRMOVL, IIRMOVL, IRMMOVL, IMRMOVL, IOPL, IJXX, ICALL, IRET, IPUSHL, IPOPL, FNONE, RNONE, SAOK, SADR, SINS, SHLT

    instruction = [0x30, 0x84, 0x00, 0x01, 0x00, 0x00]
    #   icode
    INOP = 0x0
    IHALT = 0x1
    IRRMOVL = 0x2
    IIRMOVL = 0x3
    IRMMOVL = 0X4
    IMRMOVL = 0X5
    IOPL = 0X6
    IJXX = 0X7
    ICALL = 0X8
    IRET = 0X9
    IPUSHL = 0XA
    IPOPL = 0XB

    #   ??
    FNONE = 0X0
    RNONE = 0XF

    #   status code
    SAOK = 0X1
    SADR = 0X2
    SINS = 0X3
    SHLT = 0X4

if __name__ == "__main__":
    init()
    print alu(1, 2, 0)
