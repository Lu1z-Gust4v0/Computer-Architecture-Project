from array import array

TOTAL_SIZE = 512


class Firmware:
    def __init__(self, total_size=TOTAL_SIZE):
        self.firmware = array('q', [0]) * total_size

    def set_instruction(self, position, instruction):
        if position >= TOTAL_SIZE:
            return

        self.firmware[position] = instruction

    def get_instruction(self, position):
        if position >= TOTAL_SIZE:
            return

        return self.firmware[position]


# next address | jmp | alu | C | write read fetch | A | B |
# 000000000_000_00000000_00000000_000_000_000
#     9      3     8        8      3   3   3
firmware = Firmware()

# main: PC <- 1; fetch; goto MBR1
firmware.set_instruction(0, 0b000000000_100_00110001_00100000_001_000_000)
# HALT
firmware.set_instruction(255, 0b000000000_000_00000000_00000000_000_000_000)

# add: X1 = X1 + memory[address]
# MAR <- MBR1; read; goto 2
firmware.set_instruction(1, 0b000000010_000_00010100_10000000_010_000_010)
# X1 <- X1 + MDR; fetch; goto MBR1
firmware.set_instruction(2, 0b000000000_100_00111100_00010000_001_100_001)

# sub: X1 = X1 - memory[address]
# MAR <- MBR1; read; goto 4
firmware.set_instruction(3, 0b000000100_000_00010100_10000000_010_000_010)
# X1 <- X1 - MDR; fetch; goto MBR1
firmware.set_instruction(4, 0b000000000_100_00111111_00010000_001_001_100)

# mov: memory[address] = X1
# MAR <- MBR1; goto 6
firmware.set_instruction(5, 0b000000110_000_00010100_10000000_000_000_010)
# MDR <- X1; write; fetch; goto MBR1
firmware.set_instruction(6, 0b000000000_100_00010100_01000000_101_000_100)

# goto address
# PC <- MBR1; fetch; goto MBR1
firmware.set_instruction(7, 0b000000000_100_00010100_00100000_001_000_010)

# if X1 == 0 goto address
# X1 <- X1; if alu = 0 goto 265 else goto 9
firmware.set_instruction(8, 0b000001001_001_00010100_00010000_000_000_100)
# pop MBR1; fetch; goto MBR1
firmware.set_instruction(9, 0b000000000_100_00000000_00000000_001_000_010)
# goto address
firmware.set_instruction(265, 0b000000000_100_00010100_00100000_001_000_010)
