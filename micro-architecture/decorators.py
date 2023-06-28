import functools


def print_cpu_debug(self):
    print(f"""
------------- STEP DEBUG -------------
| NEXT: {bin(self.firmware.get_instruction(self.registers["MPC"]))}
| MPC: {self.registers["MPC"]}
| MAR: {self.registers["MAR"]}
| MDR: {self.registers["MDR"]}
| MBR1: {self.registers["MBR1"]}
| MBR2: {self.registers["MBR1"]} | {(self.registers["MBR2"] & 0xFFFF) >> 8}
| X1: {self.registers["X1"]}
| X2: {self.registers["X2"]}
| X3: {self.registers["X3"]}
| H : {self.registers["H"]}
| IFU QUEUE: {self.ifu.shift_register.get_queue()}
|""")


def debug_alu(function):
    @functools.wraps(function)
    def wrapper(self, mit):
        function(self, mit)

        if self.debug:
            print("------------- ALU DEBUG -------------")
            print(f"| A: {self.BUS_A} B: {self.BUS_B}")
            print(f"| OUTPUT: {self.BUS_C}")
            print(f"""| Z: {self.registers["Z"]} N: {self.registers["N"]}""")
            print("--------------------------------------")

    return wrapper


def debug_step(function):
    @functools.wraps(function)
    def wrapper(self):
        if self.debug:
            print_cpu_debug(self)

        is_success = function(self)

        return is_success
    return wrapper
