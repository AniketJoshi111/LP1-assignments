f = open('input3.txt','r')
lines = f.readlines()
input = [line.strip() for line in lines]

#for test case 1
# symbol_names = ['N','ONE','TERM','AGAIN','TWO','RESULT']
# symbol_LC = [114,116,117,104,118,115]
#for test case 2

symbol_names = ['A','L1','B','C','D','L2']
symbol_LC = [100,103,108,99,101,106]

LC = 0
class Process:

    @staticmethod
    def for_start(ins):
        ins = Process.any_token(ins)

        return int(ins[1])
    
    @staticmethod
    def for_origin(instruction):
        global LC
        if '+' in instruction[1]:
            symbol_part, offset_part = instruction[1].split('+')
            offset = int(offset_part)
            operation = '+'
        elif '-' in instruction[1]:
            symbol_part, offset_part = instruction[1].split('-')
            offset = int(offset_part)
            operation = '-'
        else:
            symbol_part = instruction[1]  # Only the symbol part
            offset = 0
            operation = None

        # Extract the index from the symbol part (e.g., '(S,06)' -> 6)
        symbol_index = int(symbol_part.strip('()').split(',')[1])

        if operation == '+':

            LC = symbol_LC[symbol_index-1] + offset

        elif operation == '-':
            LC = symbol_LC[symbol_index-1] - offset

        else:
            LC = symbol_LC[symbol_index-1]
    @staticmethod
    def any_token(ins):
        ins = ins.strip("(")
        ins = ins.strip(")")
        ins = ins.split(",")
        return ins        #RETURNS an ARRAY
    
    @staticmethod
    def for_DS(token):
        global LC
        token = Process.any_token(token)

        storage = int(token[1])
        line_output = f"{LC:03} 00 0 {storage:03} "

        LC = LC + storage
        return line_output

    @staticmethod
    def for_DC(token):
        global LC
        token = Process.any_token(token)

        storage = int(token[1])
        line_output = f"{LC:03} 00 0 {storage:03} "

        LC = LC + 1
        return line_output
    
output = []
for i in input:

    instruction = i.split()

    # FOR START
    if "(AD,01)" in instruction[0]:
        LC = Process.for_start(instruction[1])
        output.append(" no m/c code ")
        continue
    if "(AD,03)" in instruction[0]:
        Process.for_origin(instruction)
        output.append(" no m/c code ")
        continue


    if "(DL,02)" in instruction[0]:
        line_output = Process.for_DS(instruction[1])
        output.append(line_output)
        continue

    if "(DL,01)" in instruction[0]:
        line_output = Process.for_DC(instruction[1])
        output.append(line_output)
        continue

        
    
    for token in instruction:
        token_arr = Process.any_token(token)

        if(token_arr[0] == "IS"):

            line_output = f"{LC:03} "
            LC = LC + 1
            if(len(instruction) == 3):
                line_output += f"{int(token_arr[1]):02} "
            elif(len(instruction) == 2):
                line_output += f"{int(token_arr[1]):02} 0 "

            elif(len(instruction) == 1):
                line_output += f"{int(token_arr[1]):02} 0 000 "

        
        elif(token_arr[0] == "S"):
            LC_value = symbol_LC[int(token_arr[1]) - 1]
            line_output += f"{LC_value:03} "

        elif(token_arr[0] == "C"):
            value = int(token_arr[1])

            line_output += f"{value:03}"

        elif(len(token_arr[0]) == 1):
            value = int(token_arr[0])
            line_output += f"{value:01} "
    
    output.append(line_output.strip())

for line in output:
    print(line)
    
f.close()