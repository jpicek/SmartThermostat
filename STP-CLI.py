# Author: Johnathan Picek
# Term Project - Smart Thermostat Language Prototype
# STP-CLI.py
# CPSC 46000-003 - Programming Languages
# Professor Dr. Eric Chou

# driver program for a CLI to interact with the Smart Thermostat
# using the simple Smart Thermostat Language

import STPLexer, STPParser, STP
from datetime import datetime

if __name__ == "__main__":
    STP = STP.Thermostat()
    print("Smart Thermostat Language CLI\nEnter Commands:")
    while True:
        entry = ""
        string = ""
        now = datetime.now()
        currHour = now.strftime("%H")
        print("current Hour:", currHour, "current Temp:", STP.schedule[int(currHour)])
        entry = input(" > ")
        # accept commands until EXIT is entered
        # entering EXIT ends the program
        if entry == "EXIT":
            break
        STPLexer.lexer.input(entry)
        STPParser.startParser(STP)
        while True:
            # LEX the entire command, Parse it, and perform operations
            tok = STPLexer.lexer.token()
            if not tok:
                break