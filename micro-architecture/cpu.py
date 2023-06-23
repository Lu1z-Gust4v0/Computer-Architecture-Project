from firmware import firmware
from memory import memory
from IFU import ifu

alu_operations = {
    0b000000: lambda A, B: 0,
    0b011000: lambda A, B: A, 
    0b010100: lambda A, B: B,
    0b011010: lambda A, B: ~A, 
    0b101100: lambda A, B: ~B, 
    0b111100: lambda A, B: A + B, 
    0b111101: lambda A, B: A + B + 1, 
    0b111001: lambda A, B: A + 1, 
    0b110101: lambda A, B: B + 1,
    0b111111: lambda A, B: B - A, 
    0b110110: lambda A, B: B - 1, 
    0b111011: lambda A, B: -A,
    0b001100: lambda A, B: A & B, 
    0b011100: lambda A, B: A | B, 
    0b010000: lambda A, B: 0, 
    0b110001: lambda A, B: 1, 
    0b110010: lambda A, B: -1, 
}
                                                                                                                 
shifts = {
    0b00: lambda A: A,
    0b01: lambda A: A << 1,
    0b10: lambda A: A >> 1,
    0b11: lambda A: A << 8,
}

# next address | jmp | alu | C | write read fetch | A | B | 
# 000000000_000_00000000_00000000_000_000_000
#     9      3     8        8      3   3   3

registers = {
    "MPC": 0,
    "MIR": 0,

    "MAR": 0,
    "MDR": 0,
    "PC": 0,

    "MBR1": 0,
    "MBR2": 0,

    "X1": 0,
    "X2": 0,
    "X3": 0,
    "H": 0, 

    # Alu's output registers
    "N": 0,
    "Z": 1,
}

reg_code = {
    0: "MAR",
    1: "MDR",
    2: "MBR1", 
    3: "MBR2",
    4: "X1",
    5: "X2",
    6: "X3",
    7: "H"
}

class CPU: 
    def __init__(self, registers=registers, memory=memory, firmware=firmware, ifu=ifu):
        self.memory = memory
        self.registers = registers
        self.firmware = firmware
        self.ifu = ifu
        self.BUS_A = 0
        self.BUS_B = 0
        self.BUS_C = 0

    def read_mbr1(self):
        mbr1 = self.registers["MBR1"]
        self.ifu.consume_mbr1()
        self.ifu.load(self)

        self.registers["PC"] += 1 
        
        return mbr1

    def read_mbr2(self):
        mbr2 = self.registers["MBR2"]
        self.ifu.consume_mbr2()
        self.ifu.load(self)
        
        self.registers["PC"] += 2

        return mbr2

    def fetch_word(self):
        self.ifu.fetch(self.memory)
        self.ifu.load(self) 

    def update_pc(self, value):
        # print(f"PC IS BEING UPDATED {value}")
        self.registers["PC"] = value 
        self.ifu.update_imar(value)
        # print(f"IMAR VALUE {self.ifu.IMAR}")

    # Write selected registers into BUS_A and BUS_B (ALU's inputs)
    def read_regs(self, mir):
        register_a = (mir & 0b111000) >> 3
        register_b = mir & 0b111
        
        # self.ifu.shift_register.print_queue()
        # print("length", self.ifu.shift_register.length)
        # print(f"A: {register_a} B: {register_b}")

        self.BUS_A = self.registers[reg_code[register_a]]
        self.BUS_B = self.registers[reg_code[register_b]]

        # Consume MBRs 
        if reg_code[register_a] == "MBR1":
            self.BUS_A = self.read_mbr1()

        if reg_code[register_a] == "MBR2":
            self.BUS_A = self.read_mbr2()

        if reg_code[register_b] == "MBR1":
            self.BUS_B = self.read_mbr1()

        if reg_code[register_b] == "MBR2":
            self.BUS_B = self.read_mbr2()

    # Write BUS_C value into a register
    def write_regs(self, mir):
        write_bits = (mir & 0b11111111000000000) >> 9

        if write_bits & 0b10000000:
            self.registers["MAR"] = self.BUS_C
            
        if write_bits & 0b01000000:
            self.registers["MDR"] = self.BUS_C
            
        if write_bits & 0b00100000:
            self.update_pc(self.BUS_C)

        if write_bits & 0b00010000:
            self.registers["X1"] = self.BUS_C
            
        if write_bits & 0b00001000:
            self.registers["X2"] = self.BUS_C

        if write_bits & 0b00000100:
            self.registers["X3"] = self.BUS_C

        if write_bits & 0b00000010:
            self.registers["H"] = self.BUS_C

    # Emulates the behavior of an ALU
    def alu(self, mit):
        control_bits = (mit >> 17) & 0b11111111

        INPUT_A = self.BUS_A 
        INPUT_B = self.BUS_B
        OUTPUT = 0
        
        shift_bits = (control_bits & 0b11000000) >> 6        
        operation_bits = control_bits & 0b00111111

        OUTPUT = alu_operations[operation_bits](INPUT_A, INPUT_B)
            
        print("ALU output", OUTPUT)

        if OUTPUT == 0:
            self.registers["N"] = 0
            self.registers["Z"] = 1
        else:
            self.registers["N"] = 1
            self.registers["Z"] = 0
            
        OUTPUT = shifts[shift_bits](OUTPUT)
            
        self.BUS_C = OUTPUT

    # Calculate the next instruction
    def next_instruction(self, mir):
        next_instruction = mir >> 28
        jam = (mir >> 25) & 0b111

        if jam == 0b000:
            self.registers["MPC"] = next_instruction
            return
        if jam & 0b001:                 # JAMZ
            next_instruction = next_instruction | (self.registers["Z"] << 8)
            
        if jam & 0b010:                 # JAMN
            next_instruction = next_instruction | (self.registers["N"] << 8)

        if jam & 0b100:                 # JMPC
            next_instruction = next_instruction | self.read_mbr1()
        
        self.registers["MPC"] = next_instruction

    # Operations with memory
    def memory_io(self, mir):
        memory_bits = (mir & 0b111000000) >> 6
        
        if memory_bits & 0b001:                # FETCH
            self.fetch_word()
        
        if memory_bits & 0b010:                # READ
            self.registers["MDR"] = self.memory.read_word(self.registers["MAR"])
        
        if memory_bits & 0b100:                # WRITE
           self.memory.write_word(self.registers["MAR"], self.registers["MDR"])

    # Emulates one cpu 'step'
    def step(self):
        self.registers["MIR"] = self.firmware.get_instruction(self.registers["MPC"])
        # print("instruction:", bin(self.registers["MIR"]))
        # print("state before", self.registers)

        if self.registers["MIR"] == 0:
            return False    
        
        self.read_regs(self.registers["MIR"])
        self.alu(self.registers["MIR"])
        self.write_regs(self.registers["MIR"])
        self.memory_io(self.registers["MIR"])
        self.next_instruction(self.registers["MIR"])

        # print("state after:", self.registers)
        # print()

        return True

cpu = CPU()
