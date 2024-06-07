import os, re

ADDRESSING_MODES = {
    "IMMEDIATE": re.compile("^\#\$[a-zA-Z0-9]{2}$"),
    "ABSOLUTE": re.compile("^\$[a-zA-Z0-9]{4}$"),
    "ABSOLUTEX": re.compile("^\$[a-zA-Z0-9]{4}\,X$"),
    "ABSOLUTEY": re.compile("^\$[a-zA-Z0-9]{4}\,Y$"),
    "ZEROPAGE": re.compile("^\$[a-zA-Z0-9]{2}$"),
    "ZEROPAGEX": re.compile("^\$[a-zA-Z0-9]{2}\,X$"),
    "ZEROPAGEY": re.compile("^\$[a-zA-Z0-9]{2}\,Y$"),
    "INDIRECTX": re.compile("^\(\$[a-zA-Z0-9]{2}\,X\)$"),
    "INDIRECTY": re.compile("^\(\$[a-zA-Z0-9]{2}\)\,Y$"),
    "INDIRECT": re.compile("^\(\$[a-zA-Z0-9]{4}\)$"),
    "RELATIVE": re.compile("^\$[a-zA-Z0-9]{2}$")
}

ERROR_MESSAGES = {
    "BAD_OPCODE": "Bad instruction",
    "BAD_ADDRESS_MODE": "Bad address mode",
    "BAD_BRANCH": "Bad branch",
    "BAD_OPERAND": "Bad operand",
    "DUPLICATE_SYMBOL": "Duplicate symbol",
    "MEMORY_FULL": "Source, object, or symbol are too large"
}

PSUEDO_INSTRUCTIONS = [
    "ORG",
    "CHK",
    "END",
    "EQU"
]

OPCODES = {
    "ADC": {
        "IMMEDIATE": "69",
        "ZEROPAGE": "65",
        "ZEROPAGEX": "75",
        "ABSOLUTE": "6D",
        "ABSOLUTEX": "7D",
        "ABSOLUTEY": "79",
        "INDIRECTX": "61",
        "INDIRECTY": "71"
    },
    "AND": {
        "IMMEDIATE": "29",
        "ZEROPAGE": "25",
        "ZEROPAGEX": "35",
        "ABSOLUTE": "2D",
        "ABSOLUTEX": "3D",
        "ABSOLUTEY": "39",
        "INDIRECTX": "21",
        "INDIRECTY": "31"
    },
    "ASL": {
        "ACCUMULATOR": "0A",
        "ZEROPAGE": "06",
        "ZEROPAGEX": "16",
        "ABSOLUTE": "0E",
        "ABSOLUTEX": "1E"
    },
    "BCC": {
        "RELATIVE": "90"
    },
    "BCS": {
        "RELATIVE": "B0"
    },
    "BEQ": {
        "RELATIVE": "F0"
    },
    "BIT": {
        "ZEROPAGE": "24",
        "ABSOLUTE": "2C"
    },
    "BMI": {
        "RELATIVE": "30"
    },
    "BNE": {
        "RELATIVE": "D0"
    },
    "BPL": {
        "RELATIVE": "10"
    },
    "BRK": {
        "IMPLIED": "00"
    },
    "BVC": {
        "RELATIVE": "50"
    },
    "BVS": {
        "RELATIVE": "70"
    },
    "CLC": {
        "IMPLIED": "18"
    },
    "CLD": {
        "IMPLIED": "D8"
    },
    "CLI": {
        "IMPLIED": "58"
    },
    "CLV": {
        "IMPLIED": "B8"
    },
    "CMP": {
        "IMMEDIATE": "C9",
        "ZEROPAGE": "C5",
        "ZEROPAGEX": "D5",
        "ABSOLUTE": "CD",
        "ABSOLUTEX": "DD",
        "ABSOLUTEY": "D9",
        "INDIRECTX": "C1",
        "INDIRECTY": "D1"
    },
    "CPX": {
        "IMMEDIATE": "E0",
        "ZEROPAGE": "E4",
        "ABSOLUTE": "EC"
    },
    "CPY": {
        "IMMEDIATE": "C0",
        "ZEROPAGE": "C4",
        "ABSOLUTE": "CC"
    },
    "DEC": {
        "ZEROPAGE": "C6",
        "ZEROPAGEX": "D6",
        "ABSOLUTE": "CE",
        "ABSOLUTEX": "DE"
    },
    "DEX": {
        "IMPLIED": "CA"
    },
    "DEY": {
        "IMPLIED": "88"
    },
    "EOR": {
        "IMMEDIATE": "49",
        "ZEROPAGE": "45",
        "ZEROPAGEX": "55",
        "ABSOLUTE": "4D",
        "ABSOLUTEX": "5D",
        "ABSOLUTEY": "59",
        "INDIRECTX": "41",
        "INDIRECTY": "51"
    },
    "INC": {
        "ZEROPAGE": "E6",
        "ZEROPAGEX": "F6",
        "ABSOLUTE": "EE",
        "ABSOLUTEX": "FE"
    },
    "INX": {
        "IMPLIED": "E8"
    },
    "INY": {
        "IMPLIED": "C8"
    },
    "JMP": {
        "ABSOLUTE": "4C",
        "INDIRECT": "6C"
    },
    "JSR": {
        "ABSOLUTE": "20"
    },
    "LDA": {
        "IMMEDIATE": "A9",
        "ZEROPAGE": "A5",
        "ZEROPAGEX": "B5",
        "ABSOLUTE": "AD",
        "ABSOLUTEX": "BD",
        "ABSOLUTEY": "B9",
        "INDIRECTX": "A1",
        "INDIRECTY": "B1"
    },
    "LDX": {
        "IMMEDIATE": "A2",
        "ZEROPAGE": "A6",
        "ZEROPAGEY": "B6",
        "ABSOLUTE": "AE",
        "ABSOLUTEY": "BE"
    },
    "LDY": {
        "IMMEDIATE": "A0",
        "ZEROPAGE": "A4",
        "ZEROPAGEX": "B4",
        "ABSOLUTE": "AC",
        "ABSOLUTEX": "BC"
    },
    "LSR": {
        "ACCUMULATOR": "4A",
        "ZEROPAGE": "46",
        "ZEROPAGEX": "56",
        "ABSOLUTE": "4E",
        "ABSOLUTEX": "5E"
    },
    "NOP": {
        "IMPLIED": "EA"
    },
    "ORA": {
        "IMMEDIATE": "09",
        "ZEROPAGE": "05",
        "ZEROPAGEX": "15",
        "ABSOLUTE": "0D",
        "ABSOLUTEX": "1D",
        "ABSOLUTEY": "19",
        "INDIRECTX": "01",
        "INDIRECTY": "11"
    },
    "PHA": {
        "IMPLIED": "48"
    },
    "PHP": {
        "IMPLIED": "08"
    },
    "PLA": {
        "IMPLIED": "68"
    },
    "PLP": {
        "IMPLIED": "28"
    },
    "ROL": {
        "ACCUMULATOR": "2A",
        "ZEROPAGE": "26",
        "ZEROPAGEX": "36",
        "ABSOLUTE": "2E",
        "ABSOLUTEX": "3E"
    },
    "ROR": {
        "ACCUMULATOR": "6A",
        "ZEROPAGE": "66",
        "ZEROPAGEX": "76",
        "ABSOLUTE": "6E",
        "ABSOLUTEX": "7E"
    },
    "RTI": {
        "IMPLIED": "40"
    },
    "RTS": {
        "IMPLIED": "60"
    },
    "SBC": {
        "IMMEDIATE": "E9",
        "ZEROPAGE": "E5",
        "ZEROPAGEX": "F5",
        "ABSOLUTE": "ED",
        "ABSOLUTEX": "FD",
        "ABSOLUTEY": "F9",
        "INDIRECTX": "E1",
        "INDIRECTY": "F1"
    },
    "SEC": {
        "IMPLIED": "E8"
    },
    "SED": {
        "IMPLIED": "F8"
    },
    "SEI": {
        "IMPLIED": "78"
    },
    "STA": {
        "ZEROPAGE": "85",
        "ZEROPAGEX": "95",
        "ABSOLUTE": "8D",
        "ABSOLUTEX": "9D",
        "ABSOLUTEY": "99",
        "INDRECTX": "81",
        "INDIRECTY": "91"
    },
    "STX": {
        "ZEROPAGE": "86",
        "ZEROPAGEY": "96",
        "ABSOLUTE": "8E"
    },
    "STY": {
        "ZEROPAGE": "84",
        "ZEROPAGEX": "94",
        "ABSOLUTE": "8C"
    },
    "TAX": {
        "IMPLIED": "AA"
    },
    "TAY": {
        "IMPLIED": "A8"
    },
    "TSX": {
        "IMPLIED": "BA"
    },
    "TXA": {
        "IMPLIED": "8A"
    },
    "TXS": {
        "IMPLIED": "9A"
    },
    "TYA": {
        "IMPLIED": "98"
    },
}

class t34Assembler:
    def __init__(self):
        self.file = None
        self.source = ""
        self.code = ""
        self.commentField = ""
        self.symbols = {}
        self.addrTable = {}
        self.startAddress = hex(0x8000).upper()
        self.endAddress = 0
        self.zeropage = range(0x0000, 0x00FF)
        self.errors = 0
        self.bytes = 0
        self.pc = self.startAddress

    def __hex_twos_dec(self, hex):
        # Get decimal value of hex interpreted as twos complement
        b = bin(int(hex,16))
        binStr = str(b)
        twosBin = "0b"
        for bit in binStr[2:]: twosBin += (str(int(not int(bit))))
        return -int(twosBin, 2) + 1

    def __twos_hex(self, val, nbits):
        return hex((val + (1 << nbits)) % (1 << nbits))

    def __inc_pc(self, amount):
        self.pc = hex(int(self.pc, 16) + amount).upper()

    def __reset_pc(self):
        self.pc = self.startAddress.upper()

    def __number_format(self, nstr):
        # Convert from supported number formats to generalized hex
        try:
            # Binary
            if nstr[0] == '%':
                return hex(int(nstr[1:], 2)).upper()
            # Octal
            elif nstr[0] == "O":
                return hex(int(nstr[1:], 8)).upper()
            # String operations not supported currently (too many changes to make)
            elif nstr[0] == '"':
                print("This assembler currently does not support string operands.")
                return None
            # Decimal
            elif nstr.isnumeric():
                return hex(int(nstr)).upper()
            # Hexadecimal
            elif nstr.startswith("0x") or nstr.startswith("0X") or nstr[0] == "$":
                return hex(int(nstr.replace('$', "0x"), 16)).upper()
        except:
            return None
        return None

    def __string_format(self, hstr):
        # Replace a hex string with proper format for handling
        st = hstr.upper().replace("0X", "$")
        if len(st) == 2:
            st = st[:1] + "0" + st[1:]
        return st

    def __extract_address(self, instr, operand, lineNumber):
        r = re.compile("\$[a-zA-Z0-9]{1,4}")
        operand = self.__replace_symbols(operand)
        match = r.search(operand)
        span = match.span()
        addr = operand[span[0]+1:span[1]]

        # If there is a branch instruction
        if instr.startswith("B"):
            # Get the twos complement hex and get proper position of branch
            twosComp = self.__twos_hex(int(addr, 16) - int(self.addrTable[lineNumber+1],16), 8)
            addr = twosComp.upper().replace("0X", "")
            twosDec = self.__hex_twos_dec(addr)
            dest = hex(int(self.addrTable[lineNumber],16) + twosDec)

            # Check if position is in range of start and end addresses of the program
            if int(dest, 16) not in range(int(self.startAddress, 16), int(self.endAddress, 16)):
                print(f"{ERROR_MESSAGES['BAD_BRANCH']} in line: {lineNumber} : {addr}")
                input()
                self.errors += 1
                return ""
        
        # Handle proper output for different length address
        if len(addr) == 4:
            addr = addr[2:] + " " + addr[:2]
        elif len(addr) == 3:
            addr = "0" + addr[2:] + " " + addr[:2]
        elif len(addr) == 1:
            addr = "0" + addr
        return addr

    def __get_addressing_mode(self, instruction, operand):
        # If there is no operand, addressing mode is implied or accumulator
        if operand == None:
            if instruction in OPCODES:
                if "IMPLIED" in OPCODES[instruction]:
                    return "IMPLIED"
                elif "ACCUMULATOR" in OPCODES[instruction]:
                    return "ACCUMULATOR"
        
        # If an operand exists
        else:
            # Operands in symbol tables are relative or zeropage addressing modes
            if operand in self.symbols:
                if "RELATIVE" in OPCODES[instruction]:
                    return "RELATIVE"
                elif "ZEROPAGE" in OPCODES[instruction]:
                    return "ZEROPAGE"
                else:
                    return "ABSOLUTE"
            
            # Use regex to check the syntax to get proper addressing mode
            operand = self.__replace_symbols(operand)
            for mode in ADDRESSING_MODES.keys():
                if ADDRESSING_MODES[mode].match(operand) and mode in OPCODES[instruction]:
                    return mode
        return None

    def __read_format(self, line):
        # We are not handling comments
        label = None
        instr = None
        operand = None

        # Non-label format
        if line.startswith(" "):
            l = line.split()
            if len(l) >= 1:
                instr = l[0]
            if len(l) == 2:
                operand = l[1]

        # Label format
        elif not line.startswith("*"):
            l = line.split()
            label = l[0]
            if len(l) == 3:
                instr = l[1]
                operand = l[2]
            if len(l) == 2:
                instr = l[1]

        return label, instr, operand

    def __do_operations(self, operand):
        supportedOperations = ['+','-','/','*','!','.','&']
        if operand and any(x in supportedOperations for x in operand):
            # Split the operand into pieces to do the operations
            pieces = []
            temp = ""
            for c in operand:
                if c in supportedOperations:
                    pieces.append(temp)
                    pieces.append(c)
                    temp = ""
                    continue
                temp = temp + c
            pieces.append(temp)
            
            # Iterate through the pieces of the operand 
            for i in range(1, len(pieces), 2):
                first = pieces[i-1]
                second = pieces[i+1]
                operation = pieces[i]

                # Replace any known symbols with their values from symbol table
                if first in self.symbols:
                    first = int(self.__number_format(self.symbols[first]),16)
                if second in self.symbols:
                    second = int(self.__number_format(self.symbols[second]), 16)
                
                # Handle supported operations that exist
                if operation == '+':
                    operand = hex(int(first) + int(second))
                elif operation == '-':
                    operand = hex(int(first) - int(second))
                elif operation == '/':
                    operand = hex(int(first) / int(second))
                elif operation == '*':
                    operand = hex(int(first) * int(second))
                elif operation == '!':
                    operand = hex(int(first) ^ int(second))
                elif operation == '.':
                    operand = hex(int(first) | int(second))
                elif operation == '&':
                    operand = hex(int(first) & int(second))
                operand = self.__string_format(str(operand).upper())
                if len(operand) == 2:
                    operand = operand[:1] + '0' + operand[1:]
        # Return the result of the operations
        return operand

    def __replace_symbols(self, operand):
        # Replace all symbols in the symbol table with their associated values
        for symbol in self.symbols.keys():
            if symbol in operand:
                symbolRef = self.__string_format(str(self.symbols[symbol]).upper())
                if len(symbolRef) == 2:
                    symbolRef = symbolRef[:1] + '0' + symbolRef[1:]
                operand = operand.replace(symbol, symbolRef)
        return operand

    def __calc_bytes(self):
        # Iterate through object code to count the total amount of bytes
        for line in self.code.splitlines():
            self.bytes = self.bytes + len(line.split()) - 1

    def __xor_previous_bytes(self):
        checkSum = 0
        # Iterate through the object code and get the checksum hex
        for line in self.code.splitlines():
            for byte in line.split()[1:]:
                checkSum = checkSum ^ int(byte, 16)
        return hex(checkSum).upper()

    def __add_symbol(self, label, operand, lineNumber):
        # Check for duplicate symbols in the symbol table
        if not label in self.symbols:
            # Get proper format and convert different base types
            symbolValue = self.__number_format(operand)

            # Inproper use of the symbol results in bad operand
            if symbolValue == None:
                print(f"{ERROR_MESSAGES['BAD_OPERAND']} in line: {lineNumber}")
                input()
                return False

            # Add to symbol table
            self.symbols[label] = symbolValue
        
        # Label already exists, result in duplicate symbol error
        else:
            print(f"{ERROR_MESSAGES['DUPLICATE_SYMBOL']} in line: {lineNumber}")
            input()
            self.errors += 1
        
        # Memory is full if the symbol table exceeds 255
        if len(self.symbols) > 255:
            print(ERROR_MESSAGES["MEMORY_FULL"])
            input()
            return False

        return True
            
    def assemble(self):
        # Iterate through asm source
        for lineNumber, line in enumerate(self.source):
            lineNumber = lineNumber + 1
            
            # Check if pc is out of valid memory range
            if (int(self.pc, 16)) > 65535:
                print(f'{ERROR_MESSAGES["MEMORY_FULL"]}')
                input()
                return
            
            # Get proper output for the PC and ignore comments
            self.addrTable[lineNumber] = self.pc.replace("0X", "")
            if line.startswith("*"): continue

            # If line is not a comment, read the format of the line of asm
            label, instr, operand = self.__read_format(line)

            # If the instruction is invalid return
            if instr not in OPCODES and instr not in PSUEDO_INSTRUCTIONS:
                print(f'{ERROR_MESSAGES["BAD_OPCODE"]} in line: {lineNumber}')
                input()
                return

            # Handle label first pass symbol creation
            if label:
                if instr == "EQU" and operand:
                    if not self.__add_symbol(label, operand, lineNumber): return
                else:
                    if not self.__add_symbol(label, self.pc, lineNumber): return

                    # Jump instructions increase pc by 3
                    if instr.startswith("J"):
                        self.__inc_pc(3)
                    else:
                        # Get addressing mode for proper pc count update
                        mode = self.__get_addressing_mode(instr, operand)
                        if mode and mode.startswith("ABSOLUTE") or mode == "INDIRECT":
                            self.__inc_pc(3)
                        else:
                            # Operands increase the pc by 2
                            if operand:
                                self.__inc_pc(2)
                            # Default, instructions increment pc by 1
                            else:
                                self.__inc_pc(1)
            # Handle non-labels
            else:
                # Handle the ORG psuedo instruction
                if instr == "ORG":
                    self.startAddress = self.__number_format(operand)
                    if self.startAddress == None:
                        print(f"{ERROR_MESSAGES['BAD_OPERAND']} in line: {lineNumber}")
                        input()
                        return
                    self.pc = self.startAddress

                # Same checks as labels with non-labels for pc count
                elif instr.startswith("J"):
                    self.__inc_pc(3)
                else:
                    mode = self.__get_addressing_mode(instr, operand)
                    if mode and mode.startswith("ABSOLUTE") or mode == "INDIRECT":
                        self.__inc_pc(3)
                    else:
                        if operand:
                            self.__inc_pc(2)
                        else:
                            self.__inc_pc(1)
        self.endAddress = self.pc
        self.__reset_pc()
        self.__assembler_print()

    def __assembler_print(self):
        print("Assembling")

        # Enumerate lines of the source asm
        for lineNumber, line in enumerate(self.source):
            lineNumber = lineNumber + 1

            # Ignore lines starting with comments from source asm
            if line.startswith("*"):
                print(f"{'':<24}{lineNumber:<3}{line.rstrip()}")
            else:
                # If line is not a comment, read the format of the line
                label, instr, operand = self.__read_format(line)

                # If an operand exists, do any logical operations supported
                if operand:
                    operand = self.__do_operations(operand)

                # If a label exists get the correct addressing mode and extract it
                if label:
                    if instr not in PSUEDO_INSTRUCTIONS:
                        opcode = OPCODES[instr]
                        mode = self.__get_addressing_mode(instr, operand)

                        # If the addressing mode does not match a supported format, bad address
                        if mode == None:
                            print(f"{ERROR_MESSAGES['BAD_ADDRESS_MODE']} in line: {lineNumber}")
                            print(f"{'':<24}{lineNumber:<3}{line.rstrip()}")
                            self.errors += 1
                            input()
                            continue
                        prefix = self.addrTable[lineNumber] + ": " + opcode[mode]

                        # If an operand exists, extract the address
                        if operand:
                            prefix = prefix + " " + self.__extract_address(instr, operand, lineNumber)
                        
                        # Print label non psuedo instr output
                        if lineNumber in self.addrTable:
                            print(f"{prefix:<24}{lineNumber:<3}{line.rstrip()}")
                        self.code = self.code + prefix + '\n'
                    else:
                        # Print label psuedo instr output
                        print(f"{'':<24}{lineNumber:<3}{line.rstrip()}")
                # Handle non-label lines
                else:
                    # Handle non psuedo instructions
                    if instr not in PSUEDO_INSTRUCTIONS:
                        opcode = OPCODES[instr]
                        mode = self.__get_addressing_mode(instr, operand)
                        
                        # Repeat same checks as psuedo instructions but with different output
                        if mode == None:
                            print(f"{ERROR_MESSAGES['BAD_ADDRESS_MODE']} in line: {lineNumber}")
                            print(f"{'':<24}{lineNumber:<3}{line.rstrip()}")
                            self.errors += 1
                            input()
                            continue
                        prefix = self.addrTable[lineNumber] + ": " + opcode[mode]

                        if operand:
                            prefix = prefix + " " + self.__extract_address(instr, operand, lineNumber)

                        if lineNumber in self.addrTable:
                            print(f"{prefix:<24}{lineNumber:<3}{line.rstrip()}")
                        else:
                            print(f"{'':<24}{lineNumber:<3}{line.rstrip()}")
                        self.code = self.code + prefix + '\n'

                    # Handle CHK psuedo instruction
                    elif instr == "CHK":
                        # Output the checksum at the position of the ORG instruction
                        chkSum = self.__xor_previous_bytes().replace("0X", "")
                        prefix = self.addrTable[lineNumber] + ": " + chkSum
                        self.code = self.code + prefix + '\n'
                        print(f"{prefix:<24}{lineNumber:<3}{line.rstrip()}")
                    else:
                        print(f"{'':<24}{lineNumber:<3}{line.rstrip()}")

        # Calculate the total bytes and output
        self.__calc_bytes()
        print(f"\n--End assembly, {self.bytes} bytes, Errors: {self.errors}")
        self.__symbol_print()

    def __symbol_print(self):
        count = 0
        # Print alphabetical order symbol table
        print("\nSymbol table - alphabetical order:")
        for label in sorted(self.symbols.keys()):
            if count == 3:
                print()
                count = 0
            print(f"\t{label:<20}=${self.symbols[label].replace('0X',''):<5}", end="")
            count += 1

        # Print numerical order symbol table
        print("\n\nSymbol table - numerical order:")
        for label, value in self.symbols.items():
            if count == 3:
                print()
                count = 0
            print(f"\t{label:<20}=${value.replace('0X',''):<5}", end="")
            count += 1
    
    def fopen(self, path):
        # Open a file handle for reading to get source asm
        if os.path.exists(path):
            self.file = open(path, "r")
            return True
        return False
    
    def fread(self):
        # Use file handle to read source asm
        self.source = self.file.readlines()
        return self.source
    
    def fwrite(self, path):
        # Write object code to file
        file = open(path, "w")
        file.write(self.code)
        file.close()

    def getSymbols(self):
        return self.symbols

    def getCode(self):
        return self.code
    
    def fclose(self):
        # Close the file handle of source asm
        self.file.close()
        self.file = None
