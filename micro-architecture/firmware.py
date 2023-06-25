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

# main: fetch; goto MBR1
firmware.set_instruction(0, 0b000000000_100_00000000_00000000_001_000_000)
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

# memory[address] = X1
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
# fetch; goto MBR1
firmware.set_instruction(9, 0b000000000_100_00000000_00000000_001_000_000)
# goto address
firmware.set_instruction(265, 0b000000000_100_00010100_00100000_001_000_010)

""" # main: PC <- PC + 1; MBR <- read_byte(PC); goto MBR
firmware.set_instruction(0, 0b000000000_100_00110101_001000_001_001)

# HALT
firmware.set_instruction(255, 0b000000000_000_00000000_000000_000_000)

# X = X + memory[address]

## 2: PC <- PC + 1; fetch; goto 3
firmware.set_instruction(2, 0b000000011_000_00110101_001000_001_001)

## 3: MAR <- MBR; read_word(MAR); goto 4
firmware.set_instruction(3, 0b000000100_000_00010100_100000_010_010)

## 4: H <- MDR; goto 5
firmware.set_instruction(4, 0b000000101_000_00010100_000001_000_000)

## 5: X <- H + X; goto 0
firmware.set_instruction(5, 0b000000000_000_00111100_000100_000_011)


# X = X - memory[address]

## 6: PC <- PC + 1; fetch; goto 7
firmware.set_instruction(6, 0b000000111_000_00110101_001000_001_001)

## 7: MAR <- MBR; read; goto 8
firmware.set_instruction(7, 0b000001000_000_00010100_100000_010_010)

## 8: H <- MDR; goto 9
firmware.set_instruction(8, 0b000001001_000_00010100_000001_000_000)

## 9: X <- X - H; goto 0
firmware.set_instruction(9, 0b000000000_000_00111111_000100_000_011)

# memory[address] = X

## 10: PC <- PC + 1; fetch; goto 11
firmware.set_instruction(10, 0b00001011_000_00110101_001000_001_001)

## 11: MAR <- MBR; goto 12
firmware.set_instruction(11, 0b00001100_000_00010100_100000_000_010)

## 12: MDR <- X; write; goto 0
firmware.set_instruction(12, 0b00000000_000_00010100_010000_100_011)

# goto address

## 13: PC <- PC + 1; fetch; goto 14
firmware.set_instruction(13, 0b00001110_000_00110101_001000_001_001)

## 14: PC <- MBR; fetch; goto MBR
firmware.set_instruction(14, 0b00000000_100_00010100_001000_001_010)

# if X == 0 goto address

## 15: X <- X; if alu = 0 goto 272 else goto 16
firmware.set_instruction(15, 0b00010000_001_00010100_000100_000_011)

## 16: PC <- PC + 1; goto 0
firmware.set_instruction(16, 0b00000000_000_00110101_001000_000_001) """
