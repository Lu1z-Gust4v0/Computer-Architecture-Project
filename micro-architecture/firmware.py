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

# add: X2 <- X2 + address[memory]
# MAR <- MBR1; read; goto 11
firmware.set_instruction(10, 0b000001011_000_00010100_10000000_010_000_010)
# X2 <- X2 + MDR; fetch; goto MBR1
firmware.set_instruction(11, 0b000000000_100_00111100_00001000_001_101_001)

# sub: X2 <- X2 - address[memory]
# MAR <- MBR1; read; goto 13
firmware.set_instruction(12, 0b000001101_000_00010100_10000000_010_000_010)
# X2 <- X2 - MDR; fetch; goto MBR1
firmware.set_instruction(13, 0b000000000_100_00111111_00001000_001_001_101)

# mov: address[memory] = X2
# MAR <- MBR1; goto 15
firmware.set_instruction(14, 0b000001111_000_00010100_10000000_000_000_010)
# MDR <- X2; write; fetch; goto MBR1
firmware.set_instruction(15, 0b000000000_100_00010100_01000000_101_000_101)

# if X2 == 0 goto address
# X2 <- X2; if alu = 0 goto 273 else goto 17
firmware.set_instruction(16, 0b000010001_001_00010100_00001000_000_000_101)
# pop MBR1; fetch; goto MBR1
firmware.set_instruction(17, 0b000000000_100_00000000_00000000_001_000_010)
# goto address
firmware.set_instruction(273, 0b000000000_100_00010100_00100000_001_000_010)

# add: X3 <- X3 + address[memory]
# MAR <- MBR1; read; goto 19
firmware.set_instruction(18, 0b000010011_000_00010100_10000000_010_000_010)
# X3 <- X3 + MDR; fetch; goto MBR1
firmware.set_instruction(19, 0b000000000_100_00111100_00000100_001_110_001)

# sub: X3 <- X3 - address[memory]
# MAR <- MBR1; read; goto 21
firmware.set_instruction(20, 0b000010101_000_00010100_10000000_010_000_010)
# X3 <- X3 - MDR; fetch; goto MBR1
firmware.set_instruction(21, 0b000000000_100_00111111_00000100_001_001_110)

# mov: address[memory] = X3
# MAR <- MBR1; goto 23
firmware.set_instruction(22, 0b000010111_000_00010100_10000000_000_000_010)
# MDR <- X3; write; fetch; goto MBR1
firmware.set_instruction(23, 0b000000000_100_00010100_01000000_101_000_110)

# if X3 == 0 goto address
# X3 <- X3; if alu = 0 goto 281 else goto 25
firmware.set_instruction(24, 0b000011001_001_00010100_00000100_000_000_110)
# pop MBR1; fetch; goto MBR1
firmware.set_instruction(25, 0b000000000_100_00000000_00000000_001_000_010)
# goto address
firmware.set_instruction(281, 0b000000000_100_00010100_00100000_001_000_010)

# cmp: X1, X2
# H <- X1 - X2; if alu < 0 goto 283 else goto 27
firmware.set_instruction(26, 0b000011011_010_00111111_00000010_000_101_100)
# H <- 1; fetch; goto MBR1
firmware.set_instruction(27, 0b000000000_100_00110001_00000010_001_000_000)
# H <- 0; fetch; goto MBR1
firmware.set_instruction(283, 0b000000000_100_00010000_00000010_001_000_000)

# if H == 0 goto address
# H <- H; if alu = 0 goto 285 else goto 29
firmware.set_instruction(28, 0b000011101_001_00010100_00000010_000_000_111)
# pop MBR1; fetch; goto MBR1
firmware.set_instruction(29, 0b000000000_100_00000000_00000000_001_000_010)
# goto address
firmware.set_instruction(285, 0b000000000_100_00010100_00100000_001_000_010)

# inc X1
# X1 <- X1 + 1; goto MBR1
firmware.set_instruction(30, 0b000000000_100_00110101_00010000_000_000_100)

# inc2 X2
# X1 <- X1 + 1; goto MBR1
firmware.set_instruction(31, 0b000000000_100_00110101_00001000_000_000_101)

# inc3 X3
# X1 <- X1 + 1; goto MBR1
firmware.set_instruction(32, 0b000000000_100_00110101_00000100_000_000_110)

# dec X1
# X1 <- X1 - 1; goto MBR1
firmware.set_instruction(33, 0b000000000_100_00110110_00010000_000_000_100)

# dec2 X2
# X1 <- X1 - 1; goto MBR1
firmware.set_instruction(34, 0b000000000_100_00110110_00001000_000_000_101)

# dec3 X3
# X1 <- X1 - 1; goto MBR1
firmware.set_instruction(35, 0b000000000_100_00110110_00000100_000_000_110)

# del X1
# X1 <- 0; goto MBR1 
firmware.set_instruction(36, 0b000000000_100_00010000_00010000_000_000_000)

# del2 X2
# X1 <- 0; goto MBR1 
firmware.set_instruction(37, 0b000000000_100_00010000_00001000_000_000_000)

# del3 X3
# X1 <- 0; goto MBR1 
firmware.set_instruction(38, 0b000000000_100_00010000_00000100_000_000_000)

# mul: X1 <- X1 * X2
# H <- X1; goto 40
firmware.set_instruction(39, 0b000101000_000_00010100_00000010_000_000_100)
# X2 <- X2 - 1; goto 41
firmware.set_instruction(40, 0b000101001_000_00110110_00001000_000_000_101)
# X2 <- X2; if alu == 0 goto else 298 goto 42
firmware.set_instruction(41, 0b000101010_001_00010100_00001000_000_000_101)
# X1 <- X1 + H; goto 40
firmware.set_instruction(42, 0b000101000_000_00111100_00010000_000_100_111)
# fetch; goto MBR1
firmware.set_instruction(298, 0b000000000_100_00000000_00000000_001_000_000)