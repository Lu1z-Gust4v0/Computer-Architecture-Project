from cpu import cpu
from memory import memory
from clock import clock

# memory[50] = 10
memory.write_word(50, 10)
# memory[100] = 5
memory.write_word(100, 5)

# X1 <- X1 + memory[50]
memory.write_byte(1, 1)
memory.write_byte(2, 50)
# X2 <- X2 + memory[100]
memory.write_byte(3, 10)
memory.write_byte(4, 100)

# X1 <- X1 * X2
memory.write_byte(5, 39)

# halt
memory.write_byte(6, 255)

clock.start(cpu)

print(cpu.registers["X1"])
