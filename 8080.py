# emulator for 8080 architecture
# does not currently support 8085 architecture
import sys

# six 8-bit registers + one 16-bit memory register + one 8-bit accumulator register
# labelled B C D E H L M A
#           V   V   V   V
# pairs:    B   D   H   PSW [paired with special flag register]
reg = []
for i in range(0x8):
    reg.append(0x00)

reg[0] = 0x20
reg[1] = 0x3F

# generate the register pair from the index of the pair
def pair_in(reg, ind):
    return (reg[ind * 2] << 8) | reg[ind * 2 + 1]

# put the new value from the register pair into the registers
def pair_out(reg, ind, pair):
    reg[ind * 2] = pair >> 8
    reg[ind * 2 + 1] = pair & 0xFF

# 65,536 bytes of memory
memory = []
for i in range(0x10000):
    memory.append(0x00)

# program counter
pc = 0x0000

# stack
stk = []

# input/output
inp = range(256)
out = range(256)

# condition bits
carry = False
aux_carry = False
sign = False
zero = False
parity = False

# illegal instruction
def illegal(op):
    print("illegal instruction accessed at 0x{:02X}".format(op))
    exit

# interpreter loop
while True:
    # fetch instruction and increment program counter
    instr = memory[pc]
    pc += 1

    # chopped info
    most = (instr >> 4)
    least = instr & 0xF
    aaa = (instr >> 3) & 0x07
    dd = (instr >> 4) & 0x03
    ddd = (instr >> 3) & 0x07
    sss = instr & 0x07
    d8 = memory[pc + 1]
    d16 = (memory[pc + 1] << 8) | memory[pc + 2]
    a16 = (memory[pc + 1] << 8) | memory[pc + 2]

    # decode/execute
    if instr == 0x00:
        # nop: no operation [1 4]
        pass
    elif most < 0x4 and least == 0x0:
        # illegal operations
        illegal(instr)
    elif instr == 0x31:
        # LXI SP: [3 10] IMPLEMENT LATER
        pass
    elif most < 0x3 and least == 0x1:
        # LXI: [3 10]
        pair = pair_in(reg, dd)
        pass
        pair_out(reg, dd, pair)
    elif most < 0x2 and least == 0x2:
        # STAX: [2 7]
        pass
    elif instr == 0x22:
        # SHLD: [5 16]
        pass
    elif instr == 0x32:
        # STA: [4 13]
        pass
    elif instr == 0x33:
        # INX SP: [1 5]
        pass
    elif most < 0x3 and least == 0x3:
        # INX: [1 5]
        pair = pair_in(reg, dd)
        pair_out(reg, dd, pair)
    elif instr == 0x34:
        # INR M: [3 10]
        pass
    elif most < 0x3 and least == 0x4:
        # INR [BDH]: [1 5]
        pass
    elif instr == 0x35:
        # DCR M: [3 10]
        pass
    elif most < 0x3 and least == 0x5:
        # DCR [BDH]: [1 5]
        pass
    elif instr == 0x36:
        # MVI M: [3 10]
        pass
    elif most < 0x3 and least == 0x6:
        # MVI [BDH]: [2 7]
        pass
    elif instr == 0x07:
        # RLC: [1 4]
        pass
    elif instr == 0x17:
        # RAL: [1 4]
        pass
    elif instr == 0x27:
        # DAA: [1 4]
        pass
    elif instr == 0x37:
        # STC: [1 4]
        pass
    elif most < 0x4 and least == 0x8:
        # illegal operations
        illegal(instr)
    elif instr == 0x39:
        # DAD SP: [3 10]
        pass
    elif most < 0x3 and least == 0x9:
        # DAD: [3 10]
        pass
    elif most < 0x2 and least == 0xA:
        # LDAX: [2 7]
        pair = pair_in(reg, dd)
        pair_out(reg, dd, pair)
    elif instr == 0x2A:
        # LHLD: [5 16]
        pass
    elif instr == 0x3A:
        # LDA: [4 13]
        pass
    elif instr == 0x3B:
        # DCX SP: [1 5]
        pass
    elif most < 0x3 and least == 0xB:
        # DCX: [1 5]
        pass
    elif most < 0x4 and least == 0xC:
        # INR [CELA]: [1 5]
        pass
    elif most < 0x4 and least == 0xD:
        # DCR [CELA]: [1 5]
        pass
    elif most < 0x4 and least == 0xE:
        # MVI [CELA]: [2 7]
        pass
    elif instr == 0x0F:
        # RRC: [1 4]
        pass
    elif instr == 0x1F:
        # RAR: [1 4]
        pass
    elif instr == 0x2F:
        # CMA: [1 4]
        pass
    elif instr == 0x3F:
        # CMC: [1 4]
        pass
    elif instr == 0x76:
        # HLT: halt [1 7]
        pass
    elif instr >> 6 == 0x1:
        # MOV: move from source to dest [1 4], M[2 7]
        pass
    elif most == 0x8 and least < 0x8:
        # ADD: add register value to accumulator [1 4]
        pass
    elif most == 0x8 and least < 0x10:
        # ADC: add register value to accumulator with carry [1 4]
        pass
    elif most == 0x9 and least < 0x8:
        # SUB: subtract register value from accumulator [1 4]
        pass
    elif most == 0x9 and least < 0x10:
        # SBB: subtract register value from accumulator with borrow [1 4]
        pass
    elif most == 0xA and least < 0x8:
        # ANA: & accumulator with register [1 4], M[2 7]
        pass
    elif most == 0xA and least < 0x10:
        # XRA: ^ accumulator with register [1 4], M[2 7]
        pass
    elif most == 0xB and least < 0x8:
        # ORA: | accumulator with register [1 4], M[2 7]
        pass
    elif most == 0xB and least < 0x10:
        # CMP: compare accumulator with register [1 4], M[2 7]
        pass
    elif instr == 0xC0:
        # RNZ: [1/3 5/11]
        pass
    elif instr == 0xD0:
        # RNC: [1/3 5/11]
        pass
    elif instr == 0xE0:
        # RPO: [1/3 5/11]
        pass
    elif instr == 0xF0:
        # RP: [1/3 5/11]
        pass
    elif least == 0x1:
        # POP: [3 10]
        pair = pair_in(reg, dd)
        pair_out(reg, dd, pair)
    elif instr == 0xC2:
        # JNZ: [3 10]
        pass
    elif instr == 0xD2:
        # JNC: [3 10]
        pass
    elif instr == 0xE2:
        # JPO: [3 10]
        pass
    elif instr == 0xF2:
        # JP: [3 10]
        pass
    elif instr == 0xC3:
        # JMP: [3 10]
        pass
    elif instr == 0xD3:
        # OUT: [3 10]
        pass
    elif instr == 0xE3:
        # XTHL: [5 18]
        pass
    elif instr == 0xF3:
        # DI: [1 4]
        pass
    elif instr == 0xC4:
        # CNZ: [3/5 11/17]
        pass
    elif instr == 0xD4:
        # CNC: [3/5 11/17]
        pass
    elif instr == 0xE4:
        # CPO: [3/5 11/17]
        pass
    elif instr == 0xF4:
        # CP: [3/5 11/17]
        pass
    elif least == 0x5:
        # PUSH: [3 11]
        pair = pair_in(reg, dd)
        pair_out(reg, dd, pair)
    elif instr == 0xC6:
        # ADI: [2 7]
        pass
    elif instr == 0xD6:
        # SUI: [2 7]
        pass
    elif instr == 0xE6:
        # ANI: [2 7]
        pass
    elif instr == 0xF6:
        # ORI: [2 7]
        pass
    elif least == 0x7 or least == 0xF:
        # RST: restart subroutine [3 11]
        pass
    elif instr == 0xC8:
        # RZ: [1/3 5/11]
        pass
    elif instr == 0xD8:
        # RC: [1/3 5/11]
        pass
    elif instr == 0xE8:
        # RPE: [1/3 5/11]
        pass
    elif instr == 0xF8:
        # RM: [1/3 5/11]
        pass
    elif instr == 0xC9:
        # RET: return from subroutine [3 10]
        pass
    elif instr == 0xD9:
        # illegal operation
        illegal(instr)
    elif instr == 0xE9:
        # PCHL: [1 5]
        pass
    elif instr == 0xF9:
        # SPHL: [1 5]
        pass
    elif instr == 0xCA:
        # JZ: [3 10]
        pass
    elif instr == 0xDA:
        # JC: [3 10]
        pass
    elif instr == 0xEA:
        # JPE: [3 10]
        pass
    elif instr == 0xFA:
        # JM: [3 10]
        pass
    elif instr == 0xCB:
        # illegal operation
        illegal(instr)
    elif instr == 0xDB:
        # IN: [3 10]
        pass
    elif instr == 0xEB:
        # XCHG: [1 4]
        pass
    elif instr == 0xFB:
        # EI: [1 4]
        pass
    elif instr == 0xCC:
        # CZ: [3/5 11/17]
        pass
    elif instr == 0xDC:
        # CC: [3/5 11/17]
        pass
    elif instr == 0xEC:
        # CPE: [3/5 11/17]
        pass
    elif instr == 0xFC:
        # CM: [3/5 11/17]
        pass
    elif instr == 0xCD:
        # CALL: [5 17]
        pass
    elif instr == 0xDD:
        # illegal operation
        illegal(instr)
    elif instr == 0xED:
        # illegal operation
        illegal(instr)
    elif instr == 0xFD:
        # illegal operation
        illegal(instr)
    elif instr == 0xCE:
        # ACI [2 7]
        pass
    elif instr == 0xDE:
        # SBI [2 7]
        pass
    elif instr == 0xEE:
        # XRI [2 7]
        pass
    elif instr == 0xFE:
        # CPI [2 7]
        pass
    else:
        # something has gone terribly wrong
        exit(0)