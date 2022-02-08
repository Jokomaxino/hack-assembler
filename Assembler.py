#!/usr/bin/python

from Parser import Parser
from Code import Code
from SymbolTable import SymbolTable
import sys

filename = sys.argv[1]
assert(filename[-4:] == '.asm')

code = Code()
parser = Parser(filename)
symbolTable = SymbolTable()

f = open(filename[:-4] + '.hack', 'w')

#1st pass
line_number = 0
while parser.hasMoreCommands():
    parser.advance()
    command_type = parser.commandType()
    if command_type == 'L_COMMAND':
        symbolTable.addEntry(parser.symbol(), str(line_number))
    else:
        line_number += 1

parser.reset()

#2nd pass
empty_register = 16
while parser.hasMoreCommands():
    parser.advance()
    command_type = parser.commandType()
    if command_type == 'A_COMMAND':
        symbol = parser.symbol()
        if symbol[0].isnumeric():
            command = str(bin(int(symbol)))[2:]
        else:
            if not symbolTable.contains(symbol):
                symbolTable.addEntry(symbol, empty_register)
                empty_register += 1
            command = str(bin(int(symbolTable.getAddress(symbol))))[2:]
        
        f.write('0' + '0'*(15 - len(command)) + command + '\n')
    elif command_type == 'C_COMMAND':
        dest = parser.dest()
        comp = parser.comp()
        jump = parser.jump()

        dest = code.dest(dest)
        comp = code.comp(comp)
        jump = code.jump(jump)

        f.write('111' + comp + dest + jump + '\n')
        
f.close()