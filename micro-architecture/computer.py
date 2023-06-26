from cpu import cpu
from memory import memory
from clock import clock

# memory[50] = 20
memory.write_word(50, 21)
# memory[100] = 20
memory.write_word(100, 22)

# X1 <- X1 + memory[50]
memory.write_byte(1, 1)
memory.write_byte(2, 50)
# X2 <- X2 + memory[100]
memory.write_byte(3, 10)
memory.write_byte(4, 100)

# cmp X1, X2
memory.write_byte(5, 26)
# halt
memory.write_byte(6, 255)

clock.start(cpu)

if cpu.registers["H"] == 0:
    print("X2 > X1")
if cpu.registers["H"] == 1:
    print("X1 >= X2")

