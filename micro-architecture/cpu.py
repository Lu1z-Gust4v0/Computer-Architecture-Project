from firmware import firmware
from memory import memory

alu_operations = {
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

registers = {
    "MPC": 0,
    "MIR": 0,

    "MAR": 0,
    "MDR": 0,
    "PC": 0,
    "MBR": 0,
    "X": 0,
    "Y": 0,
    "H": 0,

    # Alu's output registers
    "N": 0,
    "Z": 1,
}

class CPU: 
    def __init__(self, registers=registers, firmware=firmware):
        self.registers = registers
        self.firmware = firmware
        BUS_A = 0
        BUS_B = 0
        BUS_C = 0

    # Write selected registers into BUS_A and BUS_B (ALU's inputs)
    def read_regs(self, reg_num):
        self.BUS_A = self.registers["H"]
    
        if reg_num == 0:
            self.BUS_B = self.registers["MDR"]
        elif reg_num == 1:
            self.BUS_B = self.registers["PC"]
        elif reg_num == 2:
            self.BUS_B = self.registers["MBR"]
        elif reg_num == 3:
            self.BUS_B = self.registers["X"]
        elif reg_num == 4:
            self.BUS_B = self.registers["Y"]
        else:
            self.BUS_B = 0

    # Write BUS_C value into a register
    def write_regs(self, reg_bits):
        if reg_bits & 0b100000:
            self.registers["MAR"] = self.BUS_C
            
        if reg_bits & 0b010000:
            self.registers["MDR"] = self.BUS_C
            
        if reg_bits & 0b001000:
            self.registers["PC"] = self.BUS_C
            
        if reg_bits & 0b000100:
            self.registers["X"] = self.BUS_C
            
        if reg_bits & 0b000010:
            self.registers["Y"] = self.BUS_C
            
        if reg_bits & 0b000001:
            self.registers["H"] = self.BUS_C

    # Emulates the behavior of an ALU
    def alu(self, control_bits):
        
        INPUT_A = self.BUS_A 
        INPUT_B = self.BUS_B
        OUTPUT = 0
        
        shift_bits = (control_bits & 0b11000000) >> 6        
        operation_bits = control_bits & 0b00111111
        
        OUTPUT = alu_operations[operation_bits](INPUT_A, INPUT_B)
            
        if OUTPUT == 0:
            self.registers["N"] = 0
            self.registers["Z"] = 1
        else:
            self.registers["N"] = 1
            self.registers["Z"] = 0
            
        OUTPUT = shifts[shift_bits](OUTPUT)
            
        self.BUS_C = OUTPUT

    # Calculate the next instruction
    def next_instruction(self, instruction, jam):
        next_instruction = instruction
    
        if jam == 0b000:
            self.registers["MPC"] = next_instruction
            return
        if jam & 0b001:                 # JAMZ
            next_instruction = next_instruction | (self.registers["Z"] << 8)
            
        if jam & 0b010:                 # JAMN
            next_instruction = next_instruction | (self.registers["N"] << 8)

        if jam & 0b100:                 # JMPC
            next_instruction = next_instruction | self.registers["MBR"]
        
        self.registers["MPC"] = next_instruction

    # Operations with memory
    def memory_io(self, mem_bits):
        
        if mem_bits & 0b001:                # FETCH
            self.registers["MBR"] = memory.read_byte(self.registers["PC"])
        
        if mem_bits & 0b010:                # READ
            self.registers["MDR"] = memory.read_word(self.registers["MAR"])
        
        if mem_bits & 0b100:                # WRITE
           memory.write_word(self.registers["MAR"], self.registers["MDR"])

    # Emulates one cpu 'step'
    def step(self):
        self.registers["MIR"] = firmware.get_instruction(self.registers["MPC"])
    
        if self.registers["MIR"] == 0:
            return False    
        
        self.read_regs(self.registers["MIR"] & 0b00000000000000000000000000000111)
        self.alu((self.registers["MIR"] & 0b00000000000011111111000000000000) >> 12)
        self.write_regs((self.registers["MIR"] & 0b00000000000000000000111111000000) >> 6)
        self.memory_io((self.registers["MIR"] & 0b00000000000000000000000000111000) >> 3)
        self.next_instruction(
            (self.registers["MIR"] & 0b11111111100000000000000000000000) >> 23,
            (self.registers["MIR"] & 0b00000000011100000000000000000000) >> 20
        )
        
                        
        return True

cpu = CPU()