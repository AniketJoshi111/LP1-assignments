LC = 0
symbol_names = []
symbol_LC = []
symbol_names.append("TBD")
symbol_LC.append(-1000)

literal_names = []
literal_LC = []
literal_names.append("TBD")
literal_LC.append(-1000)

f = open('input.txt','r')
lines = f.readlines()  # Read all lines into a list
input = [line.strip() for line in lines]

class OPTAB:
    @staticmethod
    def is_IS(opcode):
        l = ['STOP', 'ADD', 'SUB', 'MULT', 'MOVER', 'MOVEM', 'COMP', 'BC', 'DIV', 'READ', 'PRINT']
        for i in range(len(l)):
            if l[i] == opcode:
                return i
            
        return -1

    @staticmethod
    def is_AD(opcode):
        l = ['START', 'END', 'ORIGIN', 'EQU', 'LTORG', 'AD']
        for i in range(len(l)):
            if l[i] == opcode:
                return i + 1
        return -1
    
    @staticmethod
    def is_REG(opcode):
        l = ['AREG', 'BREG', 'CREG', 'DREG']
        for i in range(len(l)):
            if l[i] == opcode:
                return i + 1
        return -1

    @staticmethod
    def is_DC_DS(opcode):
        if opcode == "DC":
            return "DC"
        elif opcode == "DS":
            return "DS"
        return -1

    @staticmethod
    def is_Other(opcode):
        l = ['LT', 'LE', 'EQ', 'GT', 'GE', '  ']
        for i in range(len(l)):
            if opcode == l[i]:
                return i + 1
        return -1

    @staticmethod
    def is_Constant(opcode):
        if OPTAB.is_AD(opcode) != -1:
            return False
        
        elif OPTAB.is_IS(opcode) != -1:
            return False 

        elif OPTAB.is_REG(opcode) != -1 :
            return False
        
        elif OPTAB.is_DC_DS(opcode) != -1:
            return False

        elif OPTAB.is_Other(opcode) != -1:
            return False
        
        else:
            return True


class Process:

    @staticmethod
    def for_start(ins):
        global LC
        LC = int(ins[1]) 
    
    @staticmethod   
    def for_ltorg(ins):
        global LC
        #Assign LC to all those with -1 LC
        for i in range(len(literal_LC)):
            if(literal_LC[i] == -1):
                literal_LC[i] = LC
                LC = LC + 1 

    @staticmethod    
    def for_equ(ins):
        symb1 = ins[0]
        symb2_equation = ins[2]
        if symb1 not in symbol_names:
            symbol_names.append(symb1)
            symbol_LC.append(-1)
        
        # Condtion for simple symbol (might not work in some cases)
        if symb2_equation.isalpha():   
            symb2_index = symbol_names.index(symb2_equation)
            LC_value = symbol_LC[symb2_index]

            symb1_index = symbol_names.index(symb1)
            symbol_LC[symb1_index] = LC_value

        # Is an equation like A+1
        else:
            if '+' in symb2_equation:
                symbol_part, offset_part = symb2_equation.split('+')
                offset = int(offset_part)
                operation = '+'
            elif '-' in symb2_equation:
                symbol_part, offset_part = symb2_equation.split('-')
                offset = int(offset_part)
                operation = '-'
            else:
                print("ERROR IN EQU PARSING")
    
            symb2_index = symbol_names.index(symbol_part)
            LC_value = symbol_LC[symb2_index]

            symb1_index = symbol_names.index(symb1)
            if operation == '+':  
                symbol_LC[symb1_index] = LC_value + offset
            elif operation == '-':
                symbol_LC[symb1_index] = LC_value - offset


    @staticmethod
    def for_origin(ins):
        global LC
        symb_equation = ins[1]

        # Case when symb_equation is a single symbol
        if len(symb_equation) == 1:
            index = symbol_names.index(symb_equation)
            LC = symbol_LC[index]

        # Case when symb_equation is in the form of "L2+1" or "L2-1"
        else:
            # Find the position of '+' or '-'
            if '+' in symb_equation:
                symbol_part, offset_part = symb_equation.split('+')
                offset = int(offset_part)
                operation = '+'
            elif '-' in symb_equation:
                symbol_part, offset_part = symb_equation.split('-')
                offset = int(offset_part)
                operation = '-'
            else:
                print("ERROR IN ORIGIN PARSING")
                return

            # Retrieve LC value of the symbol part
            try:
                index = symbol_names.index(symbol_part)
                LC_value = symbol_LC[index]

                # Update LC based on the operation
                if operation == '+':
                    LC = LC_value + offset
                elif operation == '-':
                    LC = LC_value - offset

            except ValueError:
                print(f"ERROR: Symbol '{symbol_part}' not found in symbol table.")

    @staticmethod
    def for_DS(ins):
        global LC
        if(ins[0] not in symbol_names):
            symbol_names.append(ins[0])
            symbol_LC.append(-1)
        index = symbol_names.index(ins[0])
        symbol_LC[index] = LC

        storage = int(ins[2])
        line_output = f"{LC:03} (DL,2) (C,{storage})"
        LC = LC + storage
        
        return line_output
        

    @staticmethod
    def for_DC(ins):
        global LC
        index = symbol_names.index(ins[0])
        symbol_LC[index] = LC
        

        value_str = ins[2].strip("'")
        const_value = int(value_str)

        line_output = f"{LC:03} (DL,1) (C,{const_value})"
        LC = LC + 1
        return line_output


def main():
    global LC
    output = []  # Store formatted output lines

    for i in input:
        instruction = i.split()
        #formatting for LC
        if(OPTAB.is_AD(instruction[0]) == -1):
            line_output = f"{LC:03} "  # Start each line with the current LC, formatted as 3 digits
        else:
            line_output = f" "          #NOTHING for AD instruction

        # Check if the instruction starts with "START"
        if instruction[0] == "START":
            Process.for_start(instruction)
            continue  # Move to the next instruction in 'input' directly
        
        #Check if the instruction has "DS"
        if "DS" in instruction:   
            ds_line = Process.for_DS(instruction)
            output.append(ds_line)
            continue

        #Check if the instruction has "DC"
        if "DC" in instruction:
            dc_line = Process.for_DC(instruction)
            output.append(dc_line)
            continue
        
        #Check if the instruction has "EQU"
        if "EQU" in instruction:
            Process.for_equ(instruction)
            output.append("  ")
            continue
        
        #Check if the instruction has "ORIGIN"
        if "ORIGIN" in instruction:
            Process.for_origin(instruction)
            output.append("  ")
            continue

        #Check if the instruction has "LTORG"
        if "LTORG" in instruction:
            Process.for_ltorg(instruction)

        for token in instruction:
            if OPTAB.is_Constant(token) == True:
                
                #CHECK if the token is a literal
                if "=" in token:
                    token.strip('=')
                    token.strip("'")
                    literal_names.append(token)
                    literal_LC.append(-1)
                    for i in range(len(literal_names)):
                        if(literal_names[i] == token and literal_LC[i] == -1):
                            index = i
                            break
                    # line_output += f"(L,{literal_names.index(token):02}) "
                    line_output += f"(L,{index:02}) "
                    continue

                # condition for LABEL and its first occurence
                if instruction[0] == token and token not in symbol_names: 
                    symbol_names.append(token)
                    symbol_LC.append(LC)

                # condition for LABEL but not its first occurence
                elif instruction[0] == token and token in symbol_names:
                    index = symbol_names.index(token)
                    symbol_LC[index] = LC
            
                # condition for the NOT label and first occurrence of a symbol
                elif token not in symbol_names:  
                    symbol_names.append(token)
                    symbol_LC.append(-1)
                    line_output += f"(S,{symbol_names.index(token):02}) "
                # condition for the NOT label and and not its first occurrence
                else:                                                  
                    line_output += f"(S,{symbol_names.index(token):02}) "

            #CHECK IF ins is IS and increment LC
            elif OPTAB.is_IS(token) != -1:
                num = OPTAB.is_IS(token)
                line_output += f"(IS,{num:02}) "
                LC += 1

            elif OPTAB.is_REG(token) != -1:
                num = OPTAB.is_REG(token)
                line_output += f"({num}) "

            elif OPTAB.is_Other(token) != -1:
                num = OPTAB.is_Other(token)
                line_output += f"({num}) "

        output.append(line_output.strip())  # Add each formatted line to output list

    # Print final output
    for line in output:
        print(line)
    
    symbol_names.remove("TBD")
    symbol_LC.remove(symbol_LC[0])
    # Printing symbol names and corresponding LC values vertically
    print("Index  Symbol \t LC")
    for i in range(len(symbol_names)):
        print(f"  {i+1} \t {symbol_names[i]} \t {symbol_LC[i]}")

    literal_names.remove("TBD")
    literal_LC.remove(literal_LC[0])
    Process.for_ltorg("")
    print("")
    print("Index  Literal \t LC")
    for i in range(len(literal_LC)):
        print(f"  {i+1} \t {literal_names[i]} \t {literal_LC[i]}")


# Run the main function
main()




    
    # @staticmethod
    # def for_AD(ins):
    #     if "LTORG" in ins:
    #         Process.for_ltorg(ins)
    #     elif "ORIGIN" in ins:
    #         Process.for_origin(ins)
    #     elif "EQU" in ins:
    #         Process.for_equ(ins)
