file = open(r"input.txt", "r")
lines = file.readlines()
input_file = [line.strip() for line in lines]

class Process:
    MNT = {}
    MDT = {}
    KPDTAB = {}
    PNTAB = []
 
    MNT_counter = 1
    KPDTAB_counter = 0
    MDTP_counter = 1

    got_header = False

    def main(self):
        for instruction in input_file:

            if instruction == "MACRO":
                got_header = True
            
            elif instruction == "MEND":
                self.process_mend()
            
            elif got_header == True:
                got_header = False
                self.process_mnt(instruction)
            else:
                self.process_body(instruction)
                
    def process_mnt(self,ins):
        definition = ins.split()
        name, parameters = definition[0], definition[1].split(',')

        current_kpdtp_index = self.KPDTAB_counter + 1
        keyword = 0
        positional = 0
        for i in parameters:
            if "=" in i:
                keyword += 1
                self.PNTAB.append(i)
                self.process_kpdtab(i)
            else:
                positional += 1
                self.PNTAB.append(i)
        
        kpdtp = "-"  #if no keyword parameters
        if keyword != 0:
            kpdtp = current_kpdtp_index
        
        self.MNT[self.MNT_counter] = {
            'Name' : f'{name}',
            '#PP' : f"{positional}",
            '#KP' : f"{keyword}",
            'MDTP' : f"{self.MDTP_counter}",
            'KPDTP' : f"{current_kpdtp_index}"
        }
        self.MNT_counter += 1

    def process_kpdtab(self,parameter):

        parameter = parameter.split("=")
        value = "No default value"
        if parameter[1] != "":
            value = parameter[1]
        
        self.KPDTAB[self.KPDTAB_counter + 1] = {
            'Name' : f'{parameter[0]}',
            'Value' : f'{value}'
        }
        self.KPDTAB_counter += 1
    
    def process_body(self, word):
        instruction = word.split()[0]
        params = word.split()[1].split(',')
        ins_line = instruction + " "
        param_references = []
        
        for param in params:
            index = self.PNTAB.index(param) + 1
            param_references.append("(P," + str(index) + ")")

        ins_line += " ".join(param_references)
        self.MDT[self.MDTP_counter] = ins_line
        self.MDTP_counter += 1

    def process_mend(self):
        self.MDT[self.MDTP_counter] = "MEND"
        self.MDTP_counter += 1

    def show_Result(self):
        counter = 0
        print("Sr.No\tName \t#PP\t#KP\tMDTP\tKPDTP")
        for entry in self.MNT.values():
            counter += 1
            print(counter, end="\t")
            print(entry['Name'], end=" \t")
            print(entry['#PP'], end="\t")
            print(entry['#KP'], end="\t")
            print(entry['MDTP'], end="\t")
            print(entry['KPDTP'], end="\n")
        
        print("\nMDT")
        print("Sr.No\tInstruction")
        for sr_no, instruction in self.MDT.items():
            print(f"{sr_no}\t{instruction}")

        print("\nKPDTAB")
        print("Sr.No\tName\t\tValue")
        for sr_no, entry in self.KPDTAB.items():
            print(f"{sr_no}\t{entry['Name']:10}\t{entry['Value']}")

def start():
    obj = Process()
    obj.main()
    obj.show_Result()
    file.close()

start()








        



