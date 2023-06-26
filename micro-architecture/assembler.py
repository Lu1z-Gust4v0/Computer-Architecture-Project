import sys

FOUR_BYTES_LIMIT = 4294967296
ONE_BYTE_LIMIT = 256

instructions = [
    "add", "add2", "add3",
    "sub", "sub2", "sub3",
    "mov", "mov2", "mov3",
    "jz", "jz2", "jz3",
    "jzh", "cmp", "goto",
    "halt", "wb", "ww",
    "inc", "inc2", "inc3",
    "dec", "dec2", "dec3"
]

one_operand_instructions = [
    "inc", "inc2", "inc3",
    "dec", "dec2", "dec3",
    "cmp",
]

two_operand_instructions = [
    "add", "add2", "add3",
    "sub", "sub2", "sub3",
    "mov", "mov2", "mov3",
    "jz", "jz1", "jz3", "jzh"
]

instruction_set = {
    "add":  0x01,
    "add2": 0x0A,
    "add3": 0x12,
    "sub":  0x03,
    "sub2": 0x0C,
    "sub3": 0x14,
    "mov":  0x05,
    "mov2": 0x0E,
    "mov3": 0x22,
    "goto": 0x07,
    "jz":   0x08,
    "jz2":  0x10,
    "jz3":  0x18,
    "jzh":  0x1C,
    "cmp":  0x1A,
    "inc":  0x1E,
    "inc2": 0x1F,
    "inc3": 0x20,
    "dec":  0x21,
    "dec2": 0x22,
    "dec3": 0x23,
    "halt": 0xFF
}


class Assembler:
    def __init__(self, instructions, instruction_set):
        self.instruction_set = instruction_set
        self.instructions = instructions
        self.lines = []
        self.lines_bin = []
        self.tokens = []

    def is_instruction(self, instruction):
        if instruction in self.instructions:
            return True

        return False

    def is_token(self, operand):
        for token in self.tokens:
            if token[0] == operand:
                return True

        return False

    def encode_two_op_instruction(self, instruction, operands):
        line_bin = []

        if len(operands) < 2:
            return line_bin

        if not self.is_token(operands[1]):
            return line_bin

        line_bin.append(self.instruction_set[instruction])
        line_bin.append(operands[1])

        return line_bin

    def encode_one_op_instruction(self, instruction):
        return [self.instruction_set[instruction]]

    def encode_goto(self, operand):
        line_bin = []

        if len(operand) < 1:
            return line_bin

        if not self.is_token(operand[0]):
            return line_bin

        line_bin.append(self.instruction_set["goto"])
        line_bin.append(operand[0])

        return line_bin

    def encode_halt(self):
        return [self.instruction_set["halt"]]

    def encode_write_byte(self, operands):
        line_bin = []

        if len(operands) < 1:
            return line_bin

        value = operands[0]
        if not value.isnumeric() or int(value) >= ONE_BYTE_LIMIT:
            return line_bin

        line_bin.append(int(value))

        return line_bin

    def encode_write_word(self, operands):
        line_bin = []

        if len(operands) < 1:
            return line_bin

        value = operands[0]
        if not value.isnumeric() or int(value) >= FOUR_BYTES_LIMIT:
            return line_bin

        line_bin.append(int(value) & 0xFF)
        line_bin.append((int(value) & 0xFF00) >> 8)
        line_bin.append((int(value) & 0xFF0000) >> 16)
        line_bin.append((int(value) & 0xFF000000) >> 24)

        return line_bin

    def encode_instruction(self, instruction, operands):
        if instruction in two_operand_instructions:
            return self.encode_two_op_instruction(instruction, operands)

        if instruction in one_operand_instructions:
            return self.encode_one_op_instruction(instruction)

        if instruction == "goto":
            return self.encode_goto(operands)

        if instruction == "halt":
            return self.encode_halt()

        if instruction == "wb":
            return self.encode_write_byte(operands)

        if instruction == "ww":
            return self.encode_write_word(operands)

        return []

    def line_to_bin(self, line):
        if self.is_instruction(line[0]):
            return self.encode_instruction(line[0], line[1:])

        return self.encode_instruction(line[1], line[2:])

    def lines_to_bin(self):
        for line in self.lines:
            line_bin = self.line_to_bin(line)

            if line_bin == []:
                print(f"Syntax Error at line {self.lines.index(line)}")
                return False

            self.lines_bin.append(line_bin)

        return True

    def find_tokens(self):
        for i in range(len(self.lines)):
            token = self.lines[i][0]
            is_label = True

            if self.is_instruction(token):
                is_label = False

            if is_label:
                self.tokens.append((token, i))

    def count_bytes(self, line_number):
        bytes = 1
        for line in range(line_number):
            bytes += len(self.lines_bin[line])

        return bytes

    def get_token_byte(self, _token):
        # print("token", _token)
        for token in self.tokens:
            if token[0] == _token:
                return token[1]

    def resolve_tokens(self):
        for i in range(len(self.tokens)):
            self.tokens[i] = (
                self.tokens[i][0],
                self.count_bytes(self.tokens[i][1])
            )

        for line in self.lines_bin:
            # print("line bin", line)
            for i in range(len(line)):
                if self.is_token(line[i]):
                    if (
                        line[i - 1] == self.instruction_set["add"] or
                        line[i - 1] == self.instruction_set["sub"] or
                        line[i - 1] == self.instruction_set["mov"]
                    ):
                        line[i] = self.get_token_byte(line[i]) // 4
                    else:
                        line[i] = self.get_token_byte(line[i])

    def remove_end_of_line(self, line):
        return line.replace("\n", "")

    def remove_commas(self, line):
        return line.replace(",", "")

    def remove_empty_strings(self, raw_tokens):
        tokens = []
        for token in raw_tokens:
            if token != "":
                tokens.append(token)

        return tokens

    def compile(self, input_file, output_file):
        with open(input_file, "r") as input:
            for raw_line in input:
                line = self.remove_end_of_line(raw_line)
                line = self.remove_commas(line)
                raw_tokens = line.lower().split(" ")
                tokens = self.remove_empty_strings(raw_tokens)

                if len(tokens) > 0:
                    self.lines.append(tokens)

        # print("bin", self.lines_bin)
        # print("tokens", self.tokens)
        self.find_tokens()
        # print("bin", self.lines_bin)
        # print("tokens", self.tokens)

        if self.lines_to_bin():
            self.resolve_tokens()
            # print("bin", self.lines_bin)

            byte_array = [0]

            for line in self.lines_bin:
                for byte in line:
                    byte_array.append(byte)

            print(byte_array)
            with open(output_file, "wb") as output:
                output.write(bytearray(byte_array))


def main():
    if len(sys.argv) != 3:
        print("Error: You must provide only two arguments")
        print("Usage: python assembler.py [input].asm [output].bin")
        return 1

    assembler = Assembler(instructions, instruction_set)
    assembler.compile(sys.argv[1], sys.argv[2])

    return 0


main()
