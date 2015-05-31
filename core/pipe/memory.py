def little_endian(val):
    b0 = val & 0xF
    b1 = (val >> 8) & 0xF
    b2 = (val >> 16) & 0xF
    b3 = (val >> 24) & 0xF
    return b0, b1, b2, b3


def prepare_reg_by_name(name, val):
    print "Ready to write memory, NAME=%s\t ADDR=%d VALUE=%d" % (name, mem_alias[name], val)
    #   TODO, add to towrite log
    return 0


def commit():
    #   TODO, commit all changes
    return 0


def read_instr(pc, data_len):
    #   TODO, instruction exception
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


def read_data(addr, data_len):
    #   TODO, exception
    if data_len == 1: return mem[addr]
    if data_len == 4:
        return (mem[addr + 3] << 24) +\
               (mem[addr + 2] << 16) +\
               (mem[addr + 1] << 8) +\
                mem[addr]


def write_data(addr, data_len, val):
    #   TODO, exception
    if data_len == 1: mem[addr] = val
    if data_len == 4: mem[addr], mem[addr + 1], mem[addr + 2], mem[addr + 3] = little_endian(val);


def init():
    global mem_alias, mem

    #   TODO, mem_alias, init
    #   TODO, mem init
    mem_alias = {}
    mem = []
    return 0

if __name__ == "__main__":
    print "HELLO WORLD"