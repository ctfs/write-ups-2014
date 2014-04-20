import sys
import struct
import itertools


paris_code = '0000009a33319b00009c00ff9dff0080d88047dfaf0fd7ef3700807e26e626ef4e26b79e0002263f263e80f7dfc626b73e3f5313ff0f0026bf9a00019e21af80d5dd1212c30ff5ef56000fddef3f009b00009a0000a79d4d5a0febef65009b00009a0000a79badde9aefbea7'.decode('hex')


def inst_1byte(code, ip):
    inst = ord(code[ip])
    opcode = inst >> 3
    operand = inst & 7
    return opcode, operand


def inst_2byte(code, ip):
    inst = struct.unpack('>H', code[ip:ip+2])[0]
    opcode = inst >> 6
    op1, op2 = (inst >> 3) & 7, inst & 7
    return opcode, op1, op2


def inst_3byte(code, ip):
    inst = ord(code[ip+1]) + (ord(code[ip+2]) << 8) + (ord(code[ip]) << 16)
    opcode = inst >> 0x13
    op1, op2 = (inst >> 0x10) & 7, inst & 0xffff
    return opcode, op1, op2


def decode(code, ip):
    instructions = [
        (0x00, 1),
        (0x201, 2),
        (0x202, 2),
        (0x203, 2),
        (0x13, 3),
        (0x98, 2),
        (0x99, 2),
        (0x9a, 2),
        (0x9b, 2),
        (0x9, 1),
        (0x15, 1),
        (0x2, 1),
        (0x3f, 2),
        (0x1f, 3),
        (0x1d, 3),
        (0x7, 1),
        (0x18, 1),
        (0x1b, 1),
        (0x0a, 1),
        (0x14, 1)]
    for instopcode, instlen in instructions:
        if instlen == 1:
            opcode, operand = inst_1byte(code, ip)
            if instopcode == opcode:
                return instlen , opcode, [operand]
        elif instlen == 2:
            opcode, op1, op2 = inst_2byte(code, ip)
            if instopcode == opcode:
                return instlen, opcode, [op1, op2]
        elif instlen == 3:
            opcode, op1, op2 = inst_3byte(code, ip)
            if instopcode == opcode:
                return instlen, opcode, [op1, op2]


def reg(x):
    return 'r'+str(x)


def imm(x):
    return hex(x)


def mem(x):
    return 'word ['+str(x)+']'


def disassemble(opcode, operands):
    if opcode == 0x00:
        return 'nop'
    elif opcode == 0x201:
        return 'mov ' + reg(operands[1]) + ', ' + reg(operands[0])
    elif opcode == 0x202:
        return 'mov ' + mem(reg(operands[1])) + ', ' + reg(operands[0])
    elif opcode == 0x203:
        return 'mov ' + reg(operands[1]) + ', ' + mem(reg(operands[0]))
    elif opcode == 0x13:
        return 'mov ' + reg(operands[0]) + ', ' + imm(operands[1])
    elif opcode == 0x98:
        return 'add ' + reg(operands[1]) + ', ' + reg(operands[0])
    elif opcode == 0x99:
        return 'sub ' + reg(operands[1]) + ', ' + reg(operands[0])
    elif opcode == 0x9a:
        return 'xor ' + reg(operands[1]) + ', ' + reg(operands[0])
    elif opcode == 0x9b:
        return 'and ' + reg(operands[1]) + ', ' + reg(operands[0])
    elif opcode == 0x9:
        return 'shr ' + reg(operands[0]) + ', 8'
    elif opcode == 0x15:
        return 'not ' + reg(operands[0])
    elif opcode == 0x2:
        return 'inc ' + reg(operands[0])
    elif opcode == 0x3f:
        return 'cmp ' + reg(operands[1]) + ', ' + reg(operands[0])
    elif opcode == 0x1f:
        return 'jmp ' + imm(operands[1])
    elif opcode == 0x1d:
        return 'jz ' + imm(operands[1])
    elif opcode == 0x7:
        return 'push ' + reg(operands[0])
    elif opcode == 0x18:
        return 'pop ' + reg(operands[0])
    elif opcode == 0x1b:
        return 'bswap ' + reg(operands[0])
    elif opcode == 0xa:
        return 'xor200h ' + reg(operands[0])
    elif opcode == 0x14:
        return 'done'
