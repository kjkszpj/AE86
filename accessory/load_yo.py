import sys
sys.path.append('C:\\Users\\You\\Documents\\GitHub\\AE86\\core\\pipe')
from memory import *

def load_yo(inf_name):
    inf = file(inf_name)
    data_all = inf.readlines()
    instruction = ['0'] * 0x1000
    for s in data_all:
        s = s[0:s.find('|')]
        s = s.replace(' ', '')
        if s == '' or s.find(':') == -1 or s.find(':') == len(s) - 1: continue
        s = s.split(':')
        s[0] = s[0][s[0].find('x') + 1:]
        st = int(s[0], 16) * 2
        n = len(s[1])
        for i in range(n):
            instruction[st + i] = s[1][i]
    instruction = "".join(instruction)
    mem_init(instruction)
    print instruction

if __name__ == '__main__':
    load_yo('../data/y86_code/fibo.yo')