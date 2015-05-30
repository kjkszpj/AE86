# -*- coding: cp936 -*-
def ALU(aluA=1, aluB=1, aluFun=0):
    if (aluFun == 0):   return aluA + aluB;
    elif (aluFun == 1): return aluB - aluA; #order right? aluB-aluA / aluA-aluB
    elif (aluFun == 2): return aluA & aluB;
    elif (aluFun == 3): return aluA ^ aluB;
    #what about condition code? implement here/new function
    
    print "aluFun error: %d" %(aluFun);
    return 0;

if __name__ == "__main__":
    print ALU(1, 1, 1);
