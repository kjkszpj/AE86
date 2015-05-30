# -*- coding: cp936 -*-
def alu(alu_a=1, alu_b=1, alu_fun=0):
    #  order right? aluB-aluA / aluA-aluB
    if alu_fun == 0:   return alu_a + alu_b
    elif alu_fun == 1: return alu_b - alu_a
    elif alu_fun == 2: return alu_a & alu_b
    elif alu_fun == 3: return alu_a ^ alu_b

    #  what about condition code? implement here/new function
    print "aluFun error: %d" % alu_fun
    return 0

if __name__ == "__main__":
    print ALU(1, 1, 1)
