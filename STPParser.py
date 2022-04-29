# Author: Johnathan Picek
# Term Project - Smart Thermostat Language Prototype
# STPParser.py
# CPSC 46000-003 - Programming Languages
# Professor Dr. Eric Chou

# grammar definitions
# and rule matching
# wrote this instead of using yacc

import STPLexer, STP
from STPLexer import tokens

# grammar:
'''
available symbol types:
command
number
target

correct usages:
command                 (ex: CLEAR, _SCHED, _SYSPROPS)
command number          (ex: SET 72)
command target number   (ex: SET SLEEP 68, SET WAKE 72, SET AWAY 66, SET HOME 71, SET ALL 71)
command number number   (ex: BOUNDARY 0 6, BOUNDARY 3 22)

'''

class Stack:
    def __init__(self):
        # Stack class's only data member is a list of items
        self.items = []
    def isEmpty(self):
        # return whether self.items is an empty list or not
        return self.items == []
    def push(self, item):
        # add item to the top of the stack (the end of the list)
        self.items.append(item)
    def pop(self):
        # remove and return the "top" item from the stack
        return self.items.pop()
    def peek(self):
        # return the "top" item from the stack without removing it
        return self.items[len(self.items) - 1]
    def peek2(self):
        # return the 2nd item from the stack without removing it
        if self.size() >= 2:
            return self.items[len(self.items) - 2]
        else:
            return
    def peek3(self):
        # return the 3rd item from the stack without removing it
        if self.size() >= 3:
            return self.items[len(self.items) - 3]
        else:
            return
    def size(self):
        return len(self.items)
    def __str__(self):
        return str(self.items)

def startParser(therm):
    while True:
        tok = STPLexer.lexer.token()
        if not tok:
            break
        # print(tok)
        # print(tok.type)
        # print(tok.value)
        ES.push(tok) ## tok == ES.peek()
        parse(therm)
    # print(ES)

def parse(therm):
    ## check for rule matching
    # single commands
    if ES.peek().type == 'COMMAND':
        if ES.peek().value == '_SCHED':
            therm.displaySchedule()
        elif ES.peek().value == '_SYSPROPS':
            therm.displaySchedule()
            therm.displayBoundaries()
        elif ES.peek().value == 'CLEAR':
            print("System reset to default settings")
            therm.clear()

    # command number
    ## SET command (default target: 'NOW'):
    elif (ES.peek2() and ES.peek2().type == 'COMMAND' and ES.peek().type == 'NUMBER'):
        if ES.peek2().value == 'BOUNDARY':
            # not a SET
            return
        # print("SET rule found")
        if ES.peek().value >= SAFETY_TEMP_MIN and ES.peek().value <= SAFETY_TEMP_MAX:
            therm.run_set(ES.peek().value, 'NOW')  # run_set(temp, target)
        else:
            print("Entry Denied.", ES.peek().value, "is an unsafe temperature.")

    # command number|target number
    elif (ES.peek3() and ES.peek3().type == 'COMMAND'):
        if ES.peek2().type == 'NUMBER' and ES.peek().type == 'NUMBER':
            # command number number
            ## BOUNDARY command:
            # print("boundary rule found")
            therm.run_boundary(ES.peek2().value, ES.peek().value)      # run_boundary(bound ID, time)

        elif ES.peek2().type == 'TARGET' and ES.peek().type == 'NUMBER':
            # command target number
            ## SET TARGET command:
            # print("SET TARGET rule found")
            if ES.peek().value >= SAFETY_TEMP_MIN and ES.peek().value <= SAFETY_TEMP_MAX:
                therm.run_set(ES.peek().value, ES.peek2().value)          # run_set(temp, target)
            else:
                print("Entry Denied.", ES.peek().value, "is an unsafe temperature.")

ES = Stack()    # expression stack
SAFETY_TEMP_MIN = 50
SAFETY_TEMP_MAX = 85